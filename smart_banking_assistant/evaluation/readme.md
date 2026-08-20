# Evaluation

The evaluation suite is intentionally independent of the production graph implementation.

## Run

```bash
uv run python -m evaluation.evaluator
```

For SQL/hybrid cases, set an account ID that exists in your test database:

```powershell
$env:EVAL_ACCOUNT_ID="your-test-account-id"
uv run python -m evaluation.evaluator
```

Results are written to `evaluation/results.json`.

## Metrics

- `routing_accuracy`: classifier selected the expected graph path.
- `citation_compliance`: RAG/hybrid cases returned citations when required.
- `mean_confidence`: average confidence returned by the response model.
- `pass_rate`: all checks passed for the case.

Do not use production customer identifiers in the evaluation dataset.

## Runtime LangGraph Evaluation

The workflow now contains an `evaluation` node after `output_guardrail` and
before `memory_save`.

Flow:

```text
response_generator
      |
      v
output_guardrail
      |
      v
evaluation
      |
      v
memory_save
      |
      v
END
```

The runtime evaluator is intentionally non-blocking. It stores:
- `evaluation`
- `evaluation_score`
- `evaluation_status`
in the graph state and never replaces the user-facing answer.
The existing offline evaluator in this directory remains available for
dataset-level evaluation.
