
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

You could run application without variable set, using default one defined in `src/error_generator.py`

### Run from the system shell

Set the required environment variables before running:

```bash
export MIN_EXIT_CODE=1
export MAX_EXIT_CODE=255
export INTERVAL_SECONDS=5
export SPECIAL_EXIT_CODE=42
export SPECIAL_CODE_CHANCE=0.1

python src/error_generator.py
```

### Run from the container

To manual container and override default variables run
``` bash
docker run --rm \
    -e MIN_EXIT_CODE=1 \
    -e MAX_EXIT_CODE=100 \
    -e INTERVAL_SECONDS=2 \
    -e SPECIAL_EXIT_CODE=150 \
    -e SPECIAL_CODE_CHANCE=0.15 \
    -e DRY_RUN=true \
    trouble-generator:0.1.0
```

## CI

### Code linting with flake8

To run it locally the same way as in GitHub Action Workflow
``` bash
source venv/bin/activate
pip install flake8
pip install -r requirements.txt
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
deactivate
```

### Python tests

To run it locally the same way as in GitHub Action Workflow
``` bash
source venv/bin/activate
pip install -r requirements-dev.txt
pytest -vv --tb=short --junit-xml=pytest-report.xml
deactivate
```

### Container build

To manual container build run
``` bash
export DOCKER_BUILDKIT=1
docker build -t trouble-generator:0.1.0 .
```
