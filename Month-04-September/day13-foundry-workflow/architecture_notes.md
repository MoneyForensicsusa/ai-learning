# Day 13 — Microsoft Foundry / Azure OpenAI Workflow

## Core Azure AI Setup

- Project name:
- Resource name:
- Endpoint:
- Deployment name:
- Model name:

## What each one means

- Project name: The logical workspace in Microsoft Foundry where related AI assets, deployments, evaluations, and development work are organized.

- Resource name: The unique name of the underlying Azure AI resource that provides the service capabilities, endpoint, identity, quota, and access controls used by the project.

- Endpoint: The network address of the Azure AI resource that the application sends API requests to.

- Deployment name: The application-facing name of a specific model deployment. The deployment connects a model/version to configuration such as deployment type and allocated quota, and this is the name the application references when making inference calls.

- Model name: The actual model family behind the deployment that performs the inference.



## Identity and Access Path

### Current Local Development Path

Python application on local machine
    ↓
API key stored in environment variable
    ↓
Azure AI endpoint
    ↓
Model deployment
    ↓
Model inference

The API key authenticates the local application to the Azure AI resource.

### Preferred Azure-Hosted Production Path

Azure-hosted application
    ↓
Managed Identity
    ↓
Microsoft Entra ID authentication
    ↓
Azure RBAC authorization
    ↓
Azure AI / Foundry resource
    ↓
Model deployment
    ↓
Model inference

The application should receive only the permissions required to call the
AI service.



## Inference Request Path

Application code
    ↓
Authentication credential
(API key in local development or Managed Identity in Azure)
    ↓
Azure AI endpoint
    ↓
Authorization check
    ↓
Requested deployment
    ↓
Quota / rate-limit enforcement
    ↓
Model inference
    ↓
Response returned to application
    ↓
Application logging / monitoring

## What Each Layer Controls

- Endpoint: Determines which Azure AI resource receives the request.
- Identity / Credential: Proves who or what is making the request.
- Authorization: Determines whether the caller may use the AI resource.
- Deployment: Determines which configured model deployment receives the request.
- Quota: Limits available request/token throughput.
- Model: Performs the inference.
- Monitoring: Provides evidence about latency, failures, usage, and operational health.




## Local Development vs Azure-Hosted Deployment

### Local Development

Developer machine
    ↓
Python application
    ↓
API key stored in PowerShell environment variable
    ↓
Public Azure AI endpoint
    ↓
Model deployment
    ↓
Model inference

Current configuration:

- Credential: API key
- Application location: developer machine
- Endpoint: Azure AI endpoint
- Deployment: GPT-5-mini deployment
- Configuration source: local environment variables


### Azure-Hosted Production

Azure App Service / Function / Container App
    ↓
System-assigned or user-assigned Managed Identity
    ↓
Microsoft Entra ID
    ↓
Azure RBAC
    ↓
Azure AI endpoint
    ↓
Model deployment
    ↓
Model inference
    ↓
Application monitoring / logging

Production changes:

- Remove the API key from application configuration where Managed Identity is supported.
- Enable Managed Identity on the hosting resource.
- Assign that identity the required Azure AI RBAC permissions.
- Keep endpoint and deployment names in application configuration.
- Add production monitoring, logging, alerts, and retry behavior.
- Apply network restrictions or private connectivity if required by the solution.


## End-to-End Azure AI Architecture Sketch

```text
                     USER / CLIENT
                           ↓
                  Web App / API Client
                           ↓
                    Azure App Service
                 or Function / Container
                           ↓
                  Managed Identity
                           ↓
                     Microsoft Entra ID
                           ↓
                       Azure RBAC
                           ↓
                Azure AI / Foundry Resource
                           ↓
                      AI Endpoint
                           ↓
                   Model Deployment
                     GPT-5-mini
                           ↓
                    Model Inference
                           ↓
                  Response to Application
                           ↓
                     User Response