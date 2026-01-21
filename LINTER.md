# Linter Commands

## Check code for issues
```bash
ruff check src/
```

## Auto-fix issues (import sorting, etc.)
```bash
ruff check --fix src/
```

## Format code (Black-style)
```bash
ruff format src/
```

## Check types with mypy
```bash
mypy src/
```

## All checks at once
```bash
ruff check src/ && mypy src/
```

## Watch mode (auto-check on file changes) - if needed later
```bash
ruff check --watch src/
```

