# Day 8 — Prompt Evaluation Findings

## Test Setup

- Same model: GPT-5-mini
- Same document
- Same 10 questions
- Questions 1–5 were answerable from the document
- Questions 6–10 were intentionally unsupported

## Baseline Prompt

The baseline generally answered supported questions correctly, but behavior
was inconsistent when information was missing.

Observed issues included:
- adding suggestions not present in the supplied document
- making reasonable-sounding inferences
- inconsistent answer length
- inconsistent source citation
- treating absence of evidence as a definite "No" in one case

## Revised Prompt

The revised prompt added:
- explicit grounding rules
- no outside knowledge
- no speculation
- defined unknown behavior
- two-sentence limit
- required source identification

This produced more predictable behavior across all 10 tests.

## Few-Shot Examples

Two examples were added:
1. a supported-answer example
2. an unsupported-answer example

The examples did not substantially change factual performance, but they
improved consistency of the response pattern and source formatting.

## Conclusion

Prompt quality should be evaluated across representative examples rather than
judged from a single response.

Rules and constraints produced the largest behavioral improvement in this test.
Few-shot examples provided additional consistency but also increase prompt
tokens, so they should be used only when they add measurable value.