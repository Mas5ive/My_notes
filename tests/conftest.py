import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from application.user import UserData


@pytest.fixture(autouse=True, scope="function")
def mock_input():
    with create_pipe_input() as pipe_input:
        with create_app_session(input=pipe_input, output=DummyOutput()):
            yield pipe_input


@pytest.fixture(autouse=True, scope="function")
def user_data() -> 'UserData':
    ud = UserData('non-existent-path')
    ud.history = [
        'note #1',
        'note #2',
        'note #3',
    ]
    ud.notes = {
        'note #1': 'text',
        'note #2': 'text,\n text',
        'note #3': 'text,\n text,\n text',
    }
    return ud
