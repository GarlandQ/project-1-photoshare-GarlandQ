from unittest import mock

from django.conf import settings
from photoshare.utils import anonymous_required


def test_anonymous_required(monkeypatch):
    @anonymous_required
    def sample_view_function(request):
        return 'Success'

    mock_http_response_redirect = mock.MagicMock()
    monkeypatch.setattr('photoshare.utils.HttpResponseRedirect', mock_http_response_redirect)

    mock_request = mock.MagicMock()

    mock_request.user.is_authenticated = True
    response = sample_view_function(mock_request)
    mock_http_response_redirect.assert_called_with(settings.LOGIN_REDIRECT_URL)
    assert response == mock_http_response_redirect(settings.LOGIN_REDIRECT_URL)

    mock_request.user.is_authenticated = False
    mock_http_response_redirect.reset_mock()
    response = sample_view_function(mock_request)
    mock_http_response_redirect.assert_not_called()
    assert response == 'Success'
