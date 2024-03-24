import json
from unittest import mock

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from pipo_ai.db.dao.pipeline import PipelineDAO
from pipo_ai.db.models.pipeline import Pipeline


@pytest.mark.anyio
async def test_run_pipeline(fastapi_app: FastAPI, client: AsyncClient) -> None:
    """
    Tests that pipeline route works.

    :param fastapi_app: current application.
    :param client: client for the app.
    """
    url = fastapi_app.url_path_for("run_pipeline", slug="test")

    # Lisez le fichier d'entrée
    with open("pipo_ai/tests/input.json") as f:
        input_data = json.load(f)

    with open("pipo_ai/tests/code.txt") as f:
        code = f.read()

    mock_pipeline = Pipeline(slug="test", code=code)

    # Créez un objet PipelineDAO mocké
    mock_dao = PipelineDAO(None)
    mock_dao.get_pipeline_model = mock.AsyncMock(return_value=mock_pipeline)

    # Injectez le DAO mocké dans la route
    fastapi_app.dependency_overrides[PipelineDAO] = lambda: mock_dao

    # Effectuez la requête POST
    response = await client.post(
        url,
        json=input_data,
        headers={"Content-Type": "application/json"},
    )

    # Vérifiez que le code de statut est 200
    assert response.status_code == status.HTTP_200_OK

    # Lisez le fichier de sortie attendu
    with open("pipo_ai/tests/output.json") as f:
        expected_output = json.load(f)

    # Vérifiez que la réponse correspond au fichier de sortie attendu
    assert response.json() == expected_output
