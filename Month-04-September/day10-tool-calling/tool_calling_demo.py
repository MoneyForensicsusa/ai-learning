import json
import os

from openai import OpenAI


client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)



CONTRACTS = {
    "SPE123": {
        "status": "In Production",
        "vendor": "ABC Corp"
    },
    "SPE456": {
        "status": "Awaiting Materials",
        "vendor": "XYZ Industries"
    }
}


USER_ACCESS = {
    "user_001": ["SPE123"],
    "user_002": ["SPE456"],
}

def can_access_contract(user_id: str, contract_number: str) -> bool:
    allowed_contracts = USER_ACCESS.get(user_id, [])
    return contract_number in allowed_contracts


def get_contract_status(contract_number: str) -> dict:
    contract = CONTRACTS.get(contract_number)

    if contract is None:
        return {
            "found": False,
            "contract_number": contract_number
        }

    return {
        "found": True,
        "contract_number": contract_number,
        "status": contract["status"],
        "vendor": contract["vendor"]
    }

TOOLS = [
    {
        "type": "function",
        "name": "get_contract_status",
        "description": "Get the current status and vendor for a contract number.",
        "parameters": {
            "type": "object",
            "properties": {
                "contract_number": {
                    "type": "string",
                    "description": "The contract number, for example SPE123."
                }
            },
            "required": ["contract_number"],
        },
    }
]


response = client.responses.create(
    model="gpt-5-mini",
    input="What is the current status of contract SPE123?",
    tools=TOOLS,
)

current_user = "user_001"

tool_outputs = []
for item in response.output:
    if item.type != "function_call":
        continue

    arguments = json.loads(item.arguments)
    contract_number = arguments["contract_number"]

    # Check authorization first
    if not can_access_contract(current_user, contract_number):
        print("Access denied.")
        print("You are not authorized to access this contract.")

    else:
        # Only authorized requests can execute the real tool
        result = get_contract_status(contract_number)

        print("Tool result:")
        print(result)

        # Only send a tool result back to the model
        # if the tool was actually allowed to run
        final_response = client.responses.create(
            model="gpt-5-mini",
            previous_response_id=response.id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result),
                }
            ],
        )

        print("\nFinal answer:")
        print(final_response.output_text)