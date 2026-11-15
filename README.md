# ScenarioLab

An independent constraint auditor for proposed time-series changes.

An original standalone utility maintained by Divyansh Gupta. No upstream research implementation is bundled.

## Added functionality

Checks rectangular finite time-by-feature matrices, immutable feature columns, per-feature bounds and an L1 change budget. Reports each changed value and violation. Exit status 1 means a well-formed candidate violates constraints; 0 means it satisfies the supplied checks.

## Quick start

The new utility uses Python 3.10+ and the standard library. The examples are synthetic. GPU packages are not required for the new utility or its tests.

```bash
python3 scenariolab.py examples/scenario.json --output report.json
python3 -m unittest discover -s tests -v
```

## Scope and limitations

Contains no Glacier code and does not generate forecasts or counterfactuals. Export your original and candidate series as JSON. Feasibility is relative to the supplied constraints, not proof of causality. L1 budgets depend on feature units; normalize data deliberately before using a shared budget.

## Licensing

MIT licensed; see LICENSE. External models and data are not included and have their own terms.
