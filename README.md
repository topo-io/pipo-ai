# pipo_ai

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m pipo_ai
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

## Project structure

```bash
$ tree "pipo_ai"
pipo_ai
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "PIPO*AI*" prefix.

For example if you see in your "pipo_ai/settings.py" a variable named like
`random_parameter`, you should provide the "PIPO_AI_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `pipo_ai.settings.Settings.Config`.

An example of .env file:

```bash
PIPO_AI_RELOAD=True
PIPO_AI_DB_HOST=localhost
PIPO_AI_DB_PORT=5432
PIPO_AI_DB_BASE=pipo_ai
PIPO_AI_DB_USER=postgres
PIPO_AI_DB_PASS=postgres
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Migrations

If you want to migrate your database, you should run following commands:

```bash
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:

```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:

```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.

1. you need to start a database.

I prefer doing it with docker:

```
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=pipo_ai" -e "POSTGRES_USER=pipo_ai" -e "POSTGRES_DB=pipo_ai" postgres:13.8-bullseye
```

2. Run the pytest.

```bash
pytest -vv .
```
