"""
Ollama service — wrapper for interacting with the Ollama API
for text generation and embeddings.
"""

import httpx
from typing import List, Optional, AsyncGenerator
from app.config import get_settings

settings = get_settings()


class OllamaService:
    """Handles all communication with the local Ollama instance."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.vision_model = settings.OLLAMA_VISION_MODEL

    async def check_health(self) -> dict:
        """Check if Ollama is running and the required model is available."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check Ollama is running
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

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generate a text response from Ollama.
        Returns the complete response text.
        """
        target_model = model or self.model

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": target_model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a text response from Ollama token by token.
        Yields individual content chunks for SSE streaming.
        """
        target_model = model or self.model

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": target_model,
                    "messages": messages,
                    "stream": True,
                    "options": {"temperature": temperature},
                },
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        import json
                        try:
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue

    async def generate_embeddings(
        self, texts: List[str], model: str = "nomic-embed-text"
    ) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Ollama.
        Uses nomic-embed-text by default (768 dimensions, fast).
        """
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
