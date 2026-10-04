import json
import os
import time

from openai import OpenAI


client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)


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


INSTRUCTIONS = """
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
"""


with open("evaluation_dataset.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)


results = []


for test in test_cases:
    print(f"\nRunning test {test['id']}...")

    start = time.perf_counter()

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=INSTRUCTIONS,
        input=f"""
SUPPLIED DOCUMENT:

{DOCUMENT}

USER QUESTION:

{test["question"]}
""",
    )

    latency = time.perf_counter() - start

    result = {
        "id": test["id"],
        "question": test["question"],
        "expected_behavior": test["expected_behavior"],
        "expected_answer": test["expected_answer"],
        "actual_answer": response.output_text,
        "latency_seconds": round(latency, 2),
    }

    results.append(result)

    print(f"Answer: {response.output_text}")
    print(f"Latency: {latency:.2f} seconds")


with open("evaluation_results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)


print("\nEvaluation run complete.")
print("Results saved to evaluation_results.json")