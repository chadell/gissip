from gissip.github_api import GitAPI


FAKE_URL = "https://yourgithubapi.com"


def test_get_headers_without_token():
    mock_github_api = GitAPI(FAKE_URL)
    assert mock_github_api.headers is None


def test_get_headers_token_unauthorized(requests_mock):
    requests_mock.register_uri('GET', FAKE_URL, json={'message': 'fake'},
                               status_code=401)
    mock_github_api = GitAPI(FAKE_URL, 'sometoken')
    assert mock_github_api.headers is None


def test_get_headers_token_authorized(requests_mock):
    requests_mock.register_uri('GET', FAKE_URL, json={'message': 'fake'},
                               status_code=200)
    mock_github_api = GitAPI(FAKE_URL, 'sometoken')
    assert mock_github_api.headers == {'Authorization': 'token sometoken'}
