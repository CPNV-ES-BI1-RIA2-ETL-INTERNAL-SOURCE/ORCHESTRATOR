import pytest
from unittest.mock import MagicMock, patch
from app.Orchestrator import Orchestrator
from app.WorkflowManager import WorkflowManager
from app.Caller import Caller
from app.ConfigLoader import ConfigLoader
from app.AuthManager import AuthManager
from app.models.RequestModel import RequestModel, Process, Params, DataItem, URLParams, QueryParams
import os
import requests

@pytest.fixture
def config_loader():
    config_loader = ConfigLoader()
    config_path = os.path.join(os.path.dirname(__file__), 'config/config.yaml')
    return config_loader.load_config(config_path)


@pytest.fixture
def workflow_manager(config_loader):
    return WorkflowManager(config_loader)


@pytest.fixture
def caller():
    mock_caller = MagicMock(spec=Caller)

    def mock_call_microservice(header, method, url, data):
        return {"status": "ok", "result": f"Processed {data}"}

    mock_caller.call_microservice.side_effect = mock_call_microservice
    return mock_caller


@pytest.fixture
def orchestrator(workflow_manager, caller, config_loader):
    return Orchestrator(
        workflow_manager=workflow_manager,
        caller=caller,
        config_loader=config_loader
    )

@pytest.fixture
def auth_manager():
    return AuthManager()

#def test_full_process(orchestrator):
#    request_data = RequestModel(
#        processes=[
#            Process(
#                name="stationboard-process",
#                params=Params(
#                    url=URLParams(country="country", resource="resource", stop="stop"),
#                    query=QueryParams(date="12/01/2025"),
#                    data=[
#                        DataItem(country="CH", resource="stationboard", stop="Yverdon-les-Bains"),
#                        DataItem(country="CH", resource="stationboard", stop="Lausanne")
#                    ]
#                )
#            )
#        ]
#    )
#
#    result = orchestrator.start_process(request_data)
#
#    assert len(result) == 2
#    assert result[0]["status"] == "success"
#    assert result[1]["status"] == "success"

def test_workflow_manager_flow(workflow_manager):
    steps = workflow_manager.steps

    assert len(steps) == 4
    assert steps[0]["name"] == "data_generator"
    assert steps[1]["name"] == "extract"
    assert steps[2]["name"] == "transform"
    assert steps[3]["name"] == "load"

def test_login_success(auth_manager):
    mock_response = {
        "access_token": "fake-token",
        "token_type": "Bearer",
        "expires_in": 300
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        credentials = {
            "username": "test_user",
            "password": "test_password"
        }

        result = auth_manager.login(credentials)

        assert result == mock_response
        mock_post.assert_called_once()

def test_login_failure(auth_manager):
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        credentials = {
            "username": "test_user",
            "password": "test_password"
        }

        result = auth_manager.login(credentials)

        assert "error" in result
        assert "Connection error" in result["error"]

def test_login_invalid_credentials(auth_manager):
    with patch('requests.post') as mock_post:
        mock_post.return_value.ok = False
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")

        credentials = {
            "username": "wrong_user",
            "password": "wrong_password"
        }

        result = auth_manager.login(credentials)

        assert "error" in result
        assert "401 Client Error" in result["error"]
