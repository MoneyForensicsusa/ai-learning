from openai import OpenAI

from settings import get_settings


settings = get_settings()

client = OpenAI(
    base_url=settings["endpoint"],
    api_key=settings["api_key"],
)

response = client.responses.create(
    model=settings["deployment"],
    input="Explain Azure Blob Storage in exactly two sentences.",
)

print(response.output_text)
print("\nResponse ID:", response.id)
print("Usage:", response.usage)