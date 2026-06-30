# USD Asset Validator

A publish-time validation gate for USD asset libraries. Extends Pixar's `usdchecker`
with batch scanning and studio-specific pipeline conventions. The idea is Ruff for `.usda` files.

## Why

Informed by recent CI/CD contributions to an open-source project and bounded by an application deadline, 
I created USD Asset Validator to learn OpenUSD's composition model hands-on rather than from documentation alone.

USD emits warnings for things like broken references or missing `defaultPrim` metadata,
but it doesn't always raise exceptions. Execution continues silently, and the failure can
surface later, far from the actual root cause. This tool converts those warnings
into enforceable checks to be used before an asset gets published to a shared library.

## Architecture

```
validator/
├── validator.py          # entry point, CLI parsing
├── runner.py             # orchestrates: discover files → run checks → collect results
├── checks/
│   ├── default_prim.py
│   ├── references.py
│   └── naming.py
├── config.py             # loads pipeline_config.json
├── reporter.py           # formats results → terminal, JSON
└── pipeline_config.json
```

## What it checks

- **`defaultPrim` validation** — every file intended to be referenced by another needs
  a valid default prim declared.
- **Broken reference chains** — walks the full dependency tree of a file and reports
  any reference that can't be resolved.
- **Naming conventions** — validates file names and prim names against configurable
  regex patterns, defined separately in `pipeline_config.json`.

Severity (ERROR vs WARNING) for each check is configurable per path pattern. For
example, a missing `defaultPrim` might be a hard error in `assets/` but only a warning
in `shots/`.

## Demo

[Terminal output on test assets.](demo/terminal_ouput.png)

## Usage

```bash
# Terminal output (colorized, human-readable)
python validator.py /prod/assets/SQ040/

# Export results to JSON
python validator.py /prod/assets/SQ040/ --out report.json

# Strict mode — exit code 1 on any failure, for CI integration
python validator.py /prod/assets/SQ040/ --strict
```

## Status

Core validation engine (defaultPrim, reference, and naming checks; batch directory
scanning; config-driven severity; terminal and JSON reporting) is complete and tested
against a set of generated `.usda` fixtures covering pass/fail cases for each check.

An AI summary layer (`--summarize`, piping results through an LLM API for
plain-English triage) is in progress.

## Stack

Python, `pxr` (OpenUSD Python bindings), Rich for terminal output. LLM API to be determined.

## Constraints

This tool doesn't auto-fix broken paths, doesn't do renderer-specific checks, and
doesn't assume any particular internal directory structure or naming
conventions. Those live entirely in `pipeline_config.json`, and if deployed in a real pipeline, are meant to be
adapted per production and studio standards.