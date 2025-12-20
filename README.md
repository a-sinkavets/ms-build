
# Error Generator Application

This application (`src/error_generator.py`) is a Python utility designed to randomly generate exit codes within a specified range at regular intervals.

## Environment Variables

The following environment variables are required to build or run the application:

| Variable | Description | Example |
|----------|-------------|---------|
| `MIN_EXIT_CODE` | Minimum exit code value (inclusive) | `1` |
| `MAX_EXIT_CODE` | Maximum exit code value (inclusive) | `255` |
| `INTERVAL_SECONDS` | Time interval in seconds between executions | `5` |
| `SPECIAL_EXIT_CODE` | A specific exit code to occasionally return | `42` |
| `SPECIAL_CODE_CHANCE` | Probability (0.0-1.0) of returning the special exit code | `0.1` |

## Usage

Set the required environment variables before running:

```bash
export MIN_EXIT_CODE=1
export MAX_EXIT_CODE=255
export INTERVAL_SECONDS=5
export SPECIAL_EXIT_CODE=42
export SPECIAL_CODE_CHANCE=0.1

python src/error_generator.py
```

## CI