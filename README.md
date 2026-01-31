# pylicit - Explicit Python

## Development Environment

### Dependencies

- `uv`: Install from here:
  [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### Environment Setup

On every session start, call:

```bash
source env
```

* Adds relative directory `scripts/` to `PATH`
* Calls `scripts/setup` and checks for system dependecies
* Creates `.venv` and syncs dependencies

On the first startup, this should setup the dev environment completely.
Otherwise you can call `scripts/setup` manually.

### Development Tools

- Linting: `ruff`
- Type-checking: `ty`

### Internal Dev Commands

Some Commands that might be useful:

* `style-check`: Runs linter and type checker
* `style-format`: Runs formatter
