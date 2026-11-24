import pytest

from api.assertions import assert_api_response
from api.client import AccountsClient
from api.data.factories import unique_email

USER_NOT_FOUND = "User not found!"
MISSING_CREDENTIALS = (
    "Bad request, email or password parameter is missing in POST request."
)


@pytest.mark.smoke
def test_verify_login_with_valid_credentials(accounts_client, registered_user):
    response = accounts_client.verify_login(
        registered_user.email, registered_user.password
    )

    assert_api_response(response, code=200, message="User exists!")


@pytest.mark.negative
def test_verify_login_with_wrong_password(accounts_client, registered_user):
    response = accounts_client.verify_login(registered_user.email, "wrong-password")

    assert_api_response(response, code=404, message=USER_NOT_FOUND)


@pytest.mark.negative
def test_verify_login_with_unknown_email(accounts_client):
    response = accounts_client.verify_login(unique_email(), "any-password")

    assert_api_response(response, code=404, message=USER_NOT_FOUND)


@pytest.mark.negative
def test_verify_login_email_is_case_sensitive(accounts_client, registered_user):
    response = accounts_client.verify_login(
        registered_user.email.upper(), registered_user.password
    )

    assert_api_response(response, code=404, message=USER_NOT_FOUND)


@pytest.mark.negative
@pytest.mark.parametrize(
    "form",
    [
        {"password": "any-password"},
        {"email": "user@example.com"},
        {},
    ],
    ids=["missing-email", "missing-password", "empty-body"],
)
def test_verify_login_without_required_parameters(accounts_client, form):
    response = accounts_client.request("POST", AccountsClient.VERIFY_LOGIN, form=form)

    assert_api_response(response, code=400, message=MISSING_CREDENTIALS)
