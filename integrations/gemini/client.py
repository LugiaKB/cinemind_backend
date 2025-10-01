import os
import json
from google import genai
from google.genai import types
from google.genai.errors import APIError


class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash "):

        try:

            self.client = genai.Client()
            self.model = model

        except Exception as e:

            print(f"Erro ao inicializar o Gemini Client: {e}")
            self.client = None
            raise

    def generate_json_response(
        self, prompt: str, system_instruction: str, json_schema: dict
    ) -> dict:
        if not self.client:
            return {"status": "error", "message": "Client não está inicializado."}

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=types.Type.from_dict(json_schema),
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt, config=config
            )

            if response.text:
                return json.loads(response.text)
            else:
                return {
                    "status": "error",
                    "message": "Resposta vazia da API do Gemini.",
                }

        except APIError as e:

            return {"status": "error", "message": f"Erro na API do Gemini: {e}"}

        except json.JSONDecodeError:

            return {
                "status": "error",
                "message": "Falha ao processar o JSON retornado pela LLM.",
            }

        except Exception as e:

            return {
                "status": "error",
                "message": f"Erro inesperado no cliente Gemini: {e}",
            }
