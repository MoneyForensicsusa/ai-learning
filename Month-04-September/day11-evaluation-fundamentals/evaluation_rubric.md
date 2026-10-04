# Day 11 — Evaluation Rubric

## Purpose

Evaluate the document assistant consistently across the same fixed test set.

The evaluator should not ask whether an answer merely "looks good."
Each response is checked against specific quality dimensions.

## Evaluation Dimensions

### 1. Schema / Format Compliance

Pass if:
- the response follows the application's required output format
- required fields or response elements are present
- no required element is missing

Fail if:
- required structure is missing
- required fields are malformed or absent

For the current document-assistant baseline, the expected response should contain:
- an answer
- the source when the answer is based on the supplied policy

---

### 2. Relevance

Pass if:
- the response directly answers the user's question
- it does not drift into unrelated information

Fail if:
- the response avoids the actual question
- it provides unrelated facts instead

Example:

Question:
How often are permissions reviewed?

Bad response:
Employees must use MFA.

The statement may be grounded in the document, but it is not relevant to the question.

---

### 3. Completeness

Pass if:
- the response includes all information required to answer the question adequately

Fail if:
- important required information is omitted

Example:

Question:
Does the policy require both MFA and a secure connection?

Incomplete:
Yes, MFA is required.

Complete:
Yes. The policy requires MFA and a company-approved secure connection.

---

### 4. Groundedness

Pass if:
- every factual claim is supported by the supplied document
- unsupported questions result in the defined unknown behavior

Fail if:
- the response invents information
- uses outside knowledge
- makes unsupported assumptions
- converts missing evidence into a definite claim

Example:

Policy:
Remote access requires MFA.

Question:
Which MFA application should employees use?

Bad response:
Microsoft Authenticator.

This is relevant but not grounded because the policy never names an MFA application.

---

### 5. Latency

Pass if:
- the response completes within the application's current latency target

Initial learning target:
10 seconds or less per model call

Fail if:
- latency exceeds 10 seconds

The threshold is a learning baseline and may change depending on real business requirements.

---

## Pass / Fail Scoring

Each test case receives:

| Dimension | Score |
|---|---|
| Schema / Format | Pass or Fail |
| Relevance | Pass or Fail |
| Completeness | Pass or Fail |
| Groundedness | Pass or Fail |
| Latency | Pass or Fail |

A case passes overall only if all required dimensions pass.

## Why Dimensions Are Scored Separately

A response can succeed in one area and fail in another.

Example:

"The company uses Microsoft Authenticator."

This may be:

- Schema compliant: Pass
- Relevant: Pass
- Complete: Pass
- Grounded: Fail

Therefore one overall "good/bad" judgment would hide the real failure.

## Evaluation Principle

The same dataset and rubric should be reused after changes to:

- model
- prompt
- retrieval logic
- chunking
- structured-output schema
- tool logic
- application rules

This allows regressions and improvements to be measured rather than guessed.