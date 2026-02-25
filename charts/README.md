# error-generator Helm chart

Helm chart for deploying the `error_generator` app.

## Install

```bash
helm install error-generator ./charts
```

## Upgrade

```bash
helm upgrade error-generator ./charts
```

## Configuration

- All application environment variables are defined in `values.yaml` under `env`.
- They are rendered into a `ConfigMap` and injected into the container via `envFrom`.
- Deployment includes `checksum/config` annotation, so changing only `ConfigMap` values triggers a rolling restart.

## Tests

Run chart tests locally:

```bash
bash ./charts/tests/run.sh
```

This script checks:

- default rendering,
- override values rendering,
- checksum update when `ConfigMap` values change.
