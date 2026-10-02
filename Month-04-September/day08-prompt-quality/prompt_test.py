import os
from openai import OpenAI

BASELINE_INSTRUCTIONS = """
Answer the user's question using the supplied document.
"""


REVISED_INSTRUCTIONS = """
You are a document assistant.

Task:
Answer the user's question using only the supplied document.

Rules:
1. Do not use outside knowledge.
2. If the document does not contain enough information to answer,
   say exactly:
   "The supplied document does not provide this information."
3. Do not speculate.
4. Answer in no more than two sentences.
5. Identify the source used.

Examples:

Example 1
Document:
SOURCE: Example Policy
Remote access requires multi-factor authentication.

Question:
Is multi-factor authentication required?

Answer:
Yes. Remote access requires multi-factor authentication.
Source: Example Policy

Example 2
Document:
SOURCE: Example Policy
Remote access requires multi-factor authentication.

Question:
How often must passwords be changed?

Answer:
The supplied document does not provide this information.
Source: Example Policy
"""

DOCUMENT = """
SOURCE: Remote Access Policy

All employees accessing company systems remotely must use
multi-factor authentication.

Remote access must be approved by the employee's manager.

The IT Security team reviews remote-access permissions every six months.

Remote access must use a company-approved secure connection.

Employees must report suspected unauthorized remote access
to the IT Security team.
"""
TEST_CASES = [
    {
        "id": 1,
        "question": "Is multi-factor authentication required for remote access?"
    },
    {
        "id": 2,
        "question": "Who must approve remote access?"
    },
    {
        "id": 3,
        "question": "How often are remote-access permissions reviewed?"
    },
    {
        "id": 4,
        "question": "What kind of connection must be used for remote access?"
    },
    {
        "id": 5,
        "question": "What should an employee do if they suspect unauthorized remote access?"
    },
    {
        "id": 6,
        "question": "How often must employees change their passwords?"
    },
    {
        "id": 7,
        "question": "Can contractors use remote access?"
    },
    {
        "id": 8,
        "question": "What MFA application does the company require?"
    },
    {
        "id": 9,
        "question": "What happens if a manager refuses a remote-access request?"
    },
    {
        "id": 10,
        "question": "Does the policy require remote-access logs to be retained for seven years?"
    },
]

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

def run_test(instructions: str, label: str):
    print(f"\n{'=' * 60}")
    print(label)
    print(f"{'=' * 60}")

    for test in TEST_CASES:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=f"""
SUPPLIED DOCUMENT:

{DOCUMENT}

USER QUESTION:

{test["question"]}
""",
        )

        print(f"\nTest {test['id']}")
        print(f"Question: {test['question']}")
        print(f"Answer: {response.output_text}")


run_test(
    BASELINE_INSTRUCTIONS,
    "BASELINE PROMPT"
)

run_test(
    REVISED_INSTRUCTIONS,
    "REVISED PROMPT"
)