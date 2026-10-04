# Day 11 — Baseline Evaluation Scorecard

## Evaluation Run

Model: GPT-5-mini  
Evaluation cases: 15  
Dataset: evaluation_dataset.json

## Results

| Dimension | Passed | Total | Pass Rate |
|---|---:|---:|---:|
| Schema / Format Compliance | 15 | 15 | 100% |
| Relevance | 15 | 15 | 100% |
| Completeness | 15 | 15 | 100% |
| Groundedness | 15 | 15 | 100% |
| Latency ≤ 10 seconds | 15 | 15 | 100% |
| Overall Case Pass | 15 | 15 | 100% |

## Latency

- Minimum latency: 1.81 seconds
- Maximum latency: 4.82 seconds
- Average latency: approximately 3.01 seconds

## Observations

The assistant correctly answered supported questions using the supplied policy.

For unsupported questions, the assistant consistently used the required fallback:

"The supplied document does not provide this information."

The assistant did not use outside knowledge when asked which VPN or MFA product the organization used.

All responses identified the Remote Access Policy as the source.

The summary test included the required policy elements:
- multi-factor authentication
- manager approval
- company-approved secure connection
- six-month permission review
- reporting suspected unauthorized remote access

All observed responses completed within the current 10-second learning threshold.

## Interpretation

This evaluation establishes a baseline for the current model, prompt, document,
and test dataset.

A 100% result on this dataset does not prove that the application is 100%
accurate or production-ready. It only means that the current system passed
all cases in evaluation dataset v1.

Future changes to the model, prompt, retrieval logic, schema, or application
behavior should be tested against the same dataset to detect regressions.

The evaluation dataset should also be expanded over time with harder,
ambiguous, adversarial, and real-world cases.



## Regression Test

The prompt was intentionally weakened by removing strict grounding,
unknown-response, speculation, and source-citation rules.

The same model, document, and 15-case evaluation dataset were reused.

### Regression Results

| Dimension | Baseline | Weakened Prompt |
|---|---:|---:|
| Required Format / Source Behavior | 15/15 | 0/15 |
| Relevance | 15/15 | 15/15 |
| Completeness | 15/15 | 15/15 |
| Groundedness | 15/15 | 8/15 |
| Latency ≤ 10 seconds | 15/15 | 15/15 |

Regression latency:
- Minimum: 1.41 seconds
- Maximum: 4.14 seconds
- Average: approximately 2.67 seconds

### Groundedness Regressions Observed

Cases 5, 6, 7, 8, 9, 10, and 14 introduced unsupported
recommendations, assumptions, or outside knowledge.

Examples included:
- incident-response steps not stated in the policy
- general password guidance
- assumptions about contractor access controls
- specific MFA products
- escalation procedures not defined in the policy
- assumptions about log-retention ownership
- specific VPN products

### Interpretation

The weakened prompt produced faster responses on average, but it reduced
groundedness and compliance with required answer behavior.

This demonstrates why AI application changes should be evaluated against a
fixed dataset rather than judged from one or two responses.

A response may sound more helpful while still being a regression against the
application's actual requirements.