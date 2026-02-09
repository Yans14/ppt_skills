import os
import base64
from io import BytesIO
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from PIL import Image


def get_client() -> AzureOpenAI:
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )
    return AzureOpenAI(
        azure_ad_token_provider=token_provider,
        api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


def image_to_base64(img: Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def validate_text_legibility(img: Image.Image, description: str = "") -> bool:
    client = get_client()
    b64 = image_to_base64(img)

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Is the text in this image legible and readable? Answer only YES or NO."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}"}
                    }
                ]
            }
        ],
        max_tokens=10
    )

    answer = response.choices[0].message.content.strip().upper()
    return "YES" in answer
