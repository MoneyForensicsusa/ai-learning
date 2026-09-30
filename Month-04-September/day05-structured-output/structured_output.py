import os

from openai import OpenAI

from pydantic import BaseModel, Field


class DocumentSummary(BaseModel):
    summary: str
    key_points: list[str]
    entities: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    notes: str

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)


response = client.responses.parse(
    model="gpt-5-mini",
    input="""
Analyze the following policy text.

Policy:
All employees accessing company systems remotely must use
multi-factor authentication. Remote access must be approved
by the employee's manager. The IT Security team reviews
remote-access permissions every six months.

Return a summary, key points, relevant entities, a confidence
value between 0 and 1, and notes.
""",
    text_format=DocumentSummary,
)


result = response.output_parsed

print(result)
print("\nObject type:")
print(type(result))

print("\nSummary only:")
print(result.summary)

print("\nConfidence only:")
print(result.confidence)


