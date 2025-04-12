import os
import sys

from openai import OpenAI
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from term_assist.constants import GPT4O, GPT4O_MINI, OPENAI_API_KEY


class LLMWithFallback(BaseModel):
    model_name: str
    model_context: int
    fallback_model_name: str
    fallback_model_context_length: int


GPT4 = LLMWithFallback(
    model_name=GPT4O_MINI,
    model_context=128000,
    fallback_model_name=GPT4O,
    fallback_model_context_length=1280000,
)


def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.openai.com/v1")


def get_llm_response(model: str, prompt: str, client: OpenAI):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        temperature=0.2,
        top_p=0.7,
        stream=True,
    )
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content

    return response


def get_response_from_llm_with_fallback(
    llm: LLMWithFallback, prompt: str, client: OpenAI
):
    try:
        response = get_llm_response(llm.model_name, prompt, client)
        return response
    except Exception as e:
        try:
            response = get_llm_response(llm.fallback_model_name, prompt, client)
            return response
        except Exception as e:
            return "LLM failed!"
