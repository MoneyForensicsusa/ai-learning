# Day 10 — Tool / Function Calling Notes

## Core Flow

User asks a question
    ↓
Model decides whether a tool is needed
    ↓
Model requests a tool and provides arguments
    ↓
Application parses the arguments
    ↓
Application checks authorization
    ↓
If authorized:
    execute the tool
    ↓
    send the trusted tool result back to the model
    ↓
    model produces the final user-facing answer

If unauthorized:
    do not execute the tool
    do not send protected data to the model
    do not make a second model call
    return a deterministic access-denied response

## Key Principle

The model can request a capability, but it does not own execution.

The application owns:

- authentication
- authorization
- argument validation
- tool execution
- access to protected data
- whether the result is returned to the model

## Tool Definition vs Tool Execution

Tool definition:

Describes the capability to the model.

Example:

get_contract_status(contract_number)

Actual tool:

The Python function or external service that performs the real operation.

The model selecting the tool does not execute the real function.

## Authorization Boundary

Correct order:

Model requests tool
    ↓
Application parses requested resource
    ↓
Authorization check
    ↓
Authorized?
    ├── No → stop
    └── Yes → execute tool

Authorization must happen before protected data is retrieved.

## Current User

In the learning lab, the user identity is hardcoded:

current_user = "user_001"

In production, the current user should come from a trusted authentication
system such as Microsoft Entra ID, not from user prompt text or model output.

## Tool Result

For authorized requests, the application sends the tool result back to the
model using the function call ID so the model can continue the same request
and generate a natural-language response.

For denied requests, the application should normally return a deterministic
authorization response without giving the denial result back to the model.

## Final Mental Model

Model:
"What capability do I need?"

Application:
"Is this request valid and authorized?"

Tool:
"Perform the approved operation."

Model:
"Present the trusted result to the user."