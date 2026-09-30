from pydantic import BaseModel, Field, ValidationError


class DocumentSummary(BaseModel):
    summary: str
    key_points: list[str]
    entities: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    notes: str


print("TEST 1 — Invalid structure/constraint")

try:
    invalid_confidence = DocumentSummary(
        summary="Remote access requires MFA.",
        key_points=["MFA is required"],
        entities=["IT Security"],
        confidence=1.7,
        notes="Example."
    )

except ValidationError as error:
    print("Pydantic rejected the data:")
    print(error)


print("\nTEST 2 — Structurally valid but factually wrong")

wrong_but_valid = DocumentSummary(
    summary="Remote-access permissions are reviewed every three months.",
    key_points=[
        "MFA is required",
        "Manager approval is required",
        "Permissions are reviewed every three months"
    ],
    entities=["IT Security team"],
    confidence=0.99,
    notes="Policy summary."
)

print(wrong_but_valid)