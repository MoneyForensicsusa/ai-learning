# Day 9 — Multi-Stage Contract Processing Workflow

## Goal

Process a contract document and produce:

- contract number
- vendor
- award amount
- delivery date
- risk summary
- final user-facing response

## Workflow

```text
Contract Document
    ↓
[1. Extraction]
    ↓
ExtractedContract
    ↓
[2. Schema Validation]
    ↓
Structurally Valid ExtractedContract
    ↓
[3. Content / Evidence Validation]
    ↓
Source-Verified ExtractedContract
    ↓
[4. Normalization]
    ↓
NormalizedContract
    ↓
[5. Normalized / Business Validation]
    ↓
Validated Contract Data
    ↓
[6. Risk Analysis]
    ↓
RiskAnalysis
    ↓
[7. Final Response]
    ↓
User-facing result
```

## Stage Responsibilities

| Stage | Job | Preferred Method |
|---|---|---|
| Extraction | Find contract number, vendor, amount, and delivery date | LLM for irregular documents; deterministic parser for consistently structured documents |
| Schema Validation | Confirm that extracted output contains the required fields and expected data types | Pydantic / Python |
| Content / Evidence Validation | Confirm that extracted values are actually supported by the source document | Python / deterministic source comparison where practical |
| Normalization | Convert verified dates, currency, and identifiers into consistent machine-friendly formats | Python |
| Normalized / Business Validation | Confirm normalized values are valid and satisfy required business rules | Python / Pydantic |
| Risk Analysis | Interpret validated contract data and relevant language to identify meaningful risks | LLM |
| Final Response | Present validated facts and analysis clearly to the user | LLM or deterministic formatting depending on need |

## Stage Input / Output Contracts

### 1. Extraction

Input:

- raw contract text or parsed document content

Output:

```json
{
  "contract_number": "SPE123",
  "vendor": "ABC Corp",
  "award_amount_raw": "$250,000",
  "delivery_date_raw": "October 15, 2026"
}
```

Purpose:

Extract required information from the source document while preserving the values as they were found.

For irregular or unstructured documents, an LLM may perform this extraction.

For consistently structured documents, a deterministic parser may be preferable.

---

### 2. Schema Validation

Input:

- ExtractedContract

Output:

```json
{
  "is_schema_valid": true,
  "errors": [],
  "extracted_contract": {
    "contract_number": "SPE123",
    "vendor": "ABC Corp",
    "award_amount_raw": "$250,000",
    "delivery_date_raw": "October 15, 2026"
  }
}
```

Purpose:

Confirm that the extraction stage returned the expected structure.

Examples of checks:

- contract number exists
- vendor exists
- award amount is represented as a string
- delivery date is represented as a string
- required fields are not missing

Schema validation confirms the shape of the extracted data, but it does not prove that the values are factually correct.

---

### 3. Content / Evidence Validation

Input:

- schema-valid ExtractedContract
- original source document or parsed source data

Output:

```json
{
  "is_evidence_valid": true,
  "errors": [],
  "verified_contract": {
    "contract_number": "SPE123",
    "vendor": "ABC Corp",
    "award_amount_raw": "$250,000",
    "delivery_date_raw": "October 15, 2026"
  }
}
```

Purpose:

Confirm that the extracted values are actually supported by the source document before transforming or using them downstream.

Example:

Source:

```text
Delivery Date: October 15, 2026
```

Extracted:

```text
Delivery Date: October 15, 2027
```

The extracted value may pass schema validation because it is still a valid string.

However, evidence validation should fail because the extracted value does not match the source.

For consistently structured documents, Python may compare extracted values against the corresponding table cells or fields.

For example:

```text
Extracted contract number
→ compare against source contract-number field

Extracted vendor
→ compare against source vendor field

Extracted amount
→ compare against source award-amount field

Extracted delivery date
→ compare against source delivery-date field
```

If the source and extracted values do not match, processing should stop and the mismatch should be logged or routed for correction or human review.

For less structured documents, an exact string comparison may not always work. The application may need to compare parsed or normalized source values while still verifying that the extracted information is supported by the original evidence.

---

### 4. Normalization

Input:

- source-verified ExtractedContract

Output:

```json
{
  "contract_number": "SPE123",
  "vendor": "ABC Corp",
  "award_amount": 250000.00,
  "delivery_date": "2026-10-15"
}
```

Purpose:

Convert verified source values into consistent machine-friendly formats.

Examples:

```text
"$250,000"
→ 250000.00
```

```text
"October 15, 2026"
→ "2026-10-15"
```

Normalization should happen after evidence validation so the application first confirms that the extracted raw value is faithful to the source before transforming it.

---

### 5. Normalized / Business Validation

Input:

- NormalizedContract

Output:

```json
{
  "is_valid": true,
  "errors": [],
  "contract": {
    "contract_number": "SPE123",
    "vendor": "ABC Corp",
    "award_amount": 250000.00,
    "delivery_date": "2026-10-15"
  }
}
```

Purpose:

Confirm that normalized data is valid and satisfies required business rules.

Examples:

- contract number must not be blank
- vendor must not be blank
- award amount must be numeric
- award amount must be greater than zero
- delivery date must be a valid date
- required fields must be present

This stage answers:

```text
"The value came from the source, but is the normalized result valid and acceptable for the application?"
```

---

### 6. Risk Analysis

Input:

- validated contract data
- relevant contract clauses or surrounding text

Output:

```json
{
  "risk_level": "medium",
  "risk_summary": "The delivery schedule appears tight relative to the stated requirements.",
  "risk_factors": [
    "Short delivery window"
  ]
}
```

Purpose:

Interpret validated contract data and relevant contract language to identify meaningful risks that deterministic rules alone may not capture.

Example contract language:

```text
All materials must be delivered within 10 calendar days of award,
and late delivery may result in termination for default.
```

Python can identify the delivery date, but an LLM may be useful for interpreting whether the language creates schedule, operational, or contractual risk.

If strict and auditable risk scoring is required, the LLM may identify the risk factors while deterministic business rules calculate the final risk level.

---

### 7. Final Response

Input:

- validated contract data
- validated risk analysis

Output:

- user-facing contract summary

Example:

```text
Contract SPE123 was awarded to ABC Corp for $250,000.
Delivery is due October 15, 2026.

Risk summary:
The delivery schedule may require close monitoring because of the short delivery window.
```

Purpose:

Present validated facts and analysis clearly to the user.

The final-response stage should consume validated outputs from earlier stages rather than returning to the raw contract and reinterpreting the entire document from scratch.

## Failure Handling

If any stage produces invalid, incomplete, or unsupported output, downstream stages should not blindly continue.

The pipeline should fail at the earliest trustworthy checkpoint.

Example:

```text
Extraction
    ↓
Schema Validation
    ↓
Schema valid?
    ├── No → stop and record schema errors
    ↓ Yes
Content / Evidence Validation
    ↓
Evidence matches source?
    ├── No → stop and record source mismatch
    ↓ Yes
Normalization
    ↓
Normalized / Business Validation
    ↓
Business-valid?
    ├── No → stop and record validation errors
    ↓ Yes
Risk Analysis
    ↓
Final Response
```

Possible failure actions include:

- stop processing
- record the error
- record the operation or document ID
- identify the failed field
- record the extracted value
- record the source value or source location when appropriate
- record the validation result
- retry an appropriate earlier stage
- route the document for correction
- route the document for human review

Invalid or unverified data should not be allowed to flow into later AI stages.

## Validation Layers

The workflow intentionally uses multiple types of validation.

### Schema Validation

Question:

```text
Did the extraction return the structure and data types we require?
```

Example:

```text
delivery_date_raw = "October 15, 2027"
```

This may pass schema validation because it is a valid string.

Schema validation checks structure, required fields, types, and defined constraints.

It does not prove that the extracted value is true.

### Content / Evidence Validation

Question:

```text
Did this extracted value actually come from or match the source evidence?
```

Example:

```text
Source:
October 15, 2026

Extracted:
October 15, 2027
```

Result:

```text
Evidence validation failed.
```

The pipeline should stop before normalization and downstream analysis.

For a structured table, this validation may be performed deterministically with Python by comparing the extracted output against the corresponding source field.

### Normalization

Question:

```text
How do we convert a verified source value into a consistent machine-friendly format?
```

Example:

```text
"$250,000"
→ 250000.00
```

```text
"October 15, 2026"
→ "2026-10-15"
```

Only source-verified values should be normalized.

### Normalized / Business Validation

Question:

```text
After transforming the verified source value, is the result valid and acceptable under our application rules?
```

Example:

```text
"$250,000"
→ 250000.00
```

Then validate:

```text
Is it numeric?        Yes
Is it greater than 0? Yes
Is it required?       Yes
```

## Final Mental Model

```text
Raw document
    ↓
Extraction
→ What information did we find?

    ↓
Schema Validation
→ Is the extracted result shaped correctly?

    ↓
Content / Evidence Validation
→ Is the extracted information actually supported by the source?

    ↓
Normalization
→ Convert verified values into standard machine-friendly formats.

    ↓
Normalized / Business Validation
→ Are those normalized values valid and acceptable to use?

    ↓
Risk Analysis
→ What do the validated facts and contract clauses mean?

    ↓
Final Response
→ How should the validated result be presented to the user?
```

The key engineering principle is:

> First confirm that extracted information is structurally valid and faithful to the source. Only then transform it, apply business rules, perform interpretation, and generate the final response.