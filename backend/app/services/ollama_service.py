"""
Ollama service — stripped to only health check and embeddings.
No conversational/generate methods. RAG pipeline handles all responses.
"""

import httpx
from typing import List, Optional
from app.config import get_settings

settings = get_settings()


class OllamaService:
    """Handles Ollama communication for health checks and embeddings only."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.vision_model = settings.OLLAMA_VISION_MODEL

    async def check_health(self) -> dict:
        """Check if Ollama is running and the required model is available."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code != 200:
                    return {"status": "error", "message": "Ollama not reachable"}
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                return {
                    "status": "connected",
                    "available_models": model_names,
                    "text_model": self.model,
                    "text_model_available": any(
                        self.model in name for name in model_names
                    ),
                    "vision_model": self.vision_model,
                    "vision_model_available": any(
                        self.vision_model in name for name in model_names
                    ),
                }
        except httpx.ConnectError:
            return {
                "status": "disconnected",
                "message": "Cannot connect to Ollama. Is it running?",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def generate_embeddings(
        self, texts: List[str], model: str = "nomic-embed-text"
    ) -> List[List[float]]:
        """Generate embeddings for a list of texts using Ollama."""
        embeddings = []
        async with httpx.AsyncClient(timeout=60.0) as client:
            for text in texts:
                response = await client.post(
                    f"{self.base_url}/api/embed",
                    json={"model": model, "input": text},
                )
                response.raise_for_status()
                data = response.json()
                embedding = data.get("embeddings", [[]])[0]
                embeddings.append(embedding)
        return embeddings

    async def generate_single_embedding(
        self, text: str, model: str = "nomic-embed-text"
    ) -> List[float]:
        """Generate embedding for a single text."""
        result = await self.generate_embeddings([text], model=model)
        return result[0] if result else []


# Singleton instance
ollama_service = OllamaService()
