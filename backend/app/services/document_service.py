"""
Document service — handles OCR, verification logic, and document-task linkage.
"""

import os
import uuid
from typing import Optional
from datetime import datetime
from PIL import Image
import pytesseract

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.models.task import UserTask, TaskStatus
from app.services.ollama_service import ollama_service

# Tesseract path configuration for Windows
# You may need to update this path based on where Tesseract is installed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


async def process_uploaded_document(
    session: AsyncSession, document_id: uuid.UUID
) -> Document:
    """
    Process a newly uploaded document:
    1. Extract text using OCR
    2. Analyze with Ollama to verify if it matches the expected task type
    3. Update document status and linked task status
    """
    statement = select(Document).where(Document.id == document_id)
    result = await session.execute(statement)
    document = result.scalar_one_or_none()

    if not document:
        return None

    # Mark as processing
    document.status = DocumentStatus.PROCESSING
    session.add(document)
    await session.commit()
    await session.refresh(document)

    try:
        # Step 1: Perform OCR if it's an image
        ocr_text = ""
        if document.file_type.startswith("image/"):
            try:
                # Need to run blocking OCR in a thread pool ideally, but doing sync here for simplicity
                image = Image.open(document.file_path)
                ocr_text = pytesseract.image_to_string(image)
                document.ocr_text = ocr_text
                document.ocr_confidence = 0.8  # Dummy confidence for now
            except Exception as e:
                print(f"OCR failed: {e}")
                ocr_text = ""

        # Step 2: Use Ollama to verify the document
        is_verified = False
        rejection_reason = None

        if ocr_text.strip():
            # If we extracted text, ask LLM to verify
            task_context = ""
            if document.task_id:
                stmt = select(UserTask).where(UserTask.id == document.task_id)
                res = await session.execute(stmt)
                user_task = res.scalar_one_or_none()
                if user_task and user_task.task:
                    task_context = f"The user uploaded this document for the task: '{user_task.task.title}' - '{user_task.task.description}'."

            prompt = f"""You are a document verification assistant.
{task_context}
Here is the text extracted from the document via OCR:
---
{ocr_text[:2000]}
---

Does this document appear to be valid for the task? 
Respond with EXACTLY ONE WORD: "YES" or "NO". If NO, briefly explain why on the next line.
"""
            llm_response = await ollama_service.generate(
                prompt=prompt,
                temperature=0.1,
                max_tokens=100
            )
            
            lines = llm_response.strip().split('\\n')
            if lines and "yes" in lines[0].lower():
                is_verified = True
            else:
                is_verified = False
                rejection_reason = " ".join(lines[1:]) if len(lines) > 1 else "Document contents do not match requirements."
        else:
            # For PDFs or unreadable images, we might just mark for manual review
            # but let's auto-verify for demonstration purposes or leave for manual
            # For Phase 4, let's mark it as requiring manual verification if no text
            is_verified = False
            rejection_reason = "Could not extract text. Manual verification required."

        # Step 3: Update Document
        if is_verified:
            document.status = DocumentStatus.VERIFIED
            document.verified_at = datetime.utcnow()
        else:
            document.status = DocumentStatus.REJECTED
            document.rejection_reason = rejection_reason

        session.add(document)

        # Step 4: Update linked UserTask if verified
        if is_verified and document.task_id:
            stmt = select(UserTask).where(UserTask.id == document.task_id)
            res = await session.execute(stmt)
            user_task = res.scalar_one_or_none()
            if user_task and user_task.status != TaskStatus.COMPLETED:
                user_task.status = TaskStatus.COMPLETED
                user_task.completed_at = datetime.utcnow()
                session.add(user_task)

        await session.commit()
        await session.refresh(document)

    except Exception as e:
        print(f"Error processing document: {e}")
        document.status = DocumentStatus.UPLOADED  # Revert so it can be retried or manually processed
        session.add(document)
        await session.commit()

    return document

