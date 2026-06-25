# USD-Validator

## Architecture

```
validator/
├── validator.py          # entry point, CLI parsing
├── runner.py             # orchestrates: discover files → run checks → collect results
├── checks/
│   ├── default_prim.py
│   ├── references.py
│   └── naming.py
├── config.py             # loads and validates pipeline_config.json
├── reporter.py           # formats results → terminal, JSON
└── pipeline_config.json
```