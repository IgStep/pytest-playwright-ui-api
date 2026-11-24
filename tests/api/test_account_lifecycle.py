import pytest

from api.assertions import assert_api_response
from api.client import AccountsClient
from api.data.factories import unique_email
from api.models.responses import UserDetailResponse

REQUIRED_FIELDS = [
    "name",
    "email",
    "password",
    "firstname",
    "lastname",
    "address1",
    "country",
    "zipcode",
    "state",
    "city",
    "mobile_number",
]
OPTIONAL_FIELDS = [
    "title",
    "birth_date",
    "birth_month",
    "birth_year",
    "company",
    "address2",
]
ACCOUNT_NOT_FOUND = "Account not found!"


def _get_user_detail(accounts_client: AccountsClient, email: str):
    return assert_api_response(
        accounts_client.get_user_detail_by_email(email), model=UserDetailResponse
    ).user


@pytest.mark.smoke
def test_create_account(accounts_client, new_user, cleanup_user):
    cleanup_user(new_user)

    response = accounts_client.create_account(new_user)

    assert_api_response(response, code=201, message="User created!")
    detail = _get_user_detail(accounts_client, new_user.email)
    expected = new_user.expected_user_detail()
    assert detail.model_dump(include=set(expected)) == expected


def test_update_account(accounts_client, registered_user, faker):
    updated_user = registered_user.model_copy(
        update={
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "city": faker.city(),
            "company": faker.company(),
        }
    )

    response = accounts_client.update_account(updated_user)

    assert_api_response(response, code=200, message="User updated!")
    detail = _get_user_detail(accounts_client, registered_user.email)
    expected = updated_user.expected_user_detail()
    assert detail.model_dump(include=set(expected)) == expected


def test_delete_account(accounts_client, registered_user):
    response = accounts_client.delete_account(
        registered_user.email, registered_user.password
    )

    assert_api_response(response, code=200, message="Account deleted!")
    assert_api_response(
        accounts_client.verify_login(registered_user.email, registered_user.password),
        code=404,
    )
    assert_api_response(
        accounts_client.get_user_detail_by_email(registered_user.email),
        code=404,
        message="Account not found with this email, try another email!",
    )


@pytest.mark.parametrize("field", OPTIONAL_FIELDS)
def test_create_account_without_optional_field(
    accounts_client, new_user, cleanup_user, field
):
    cleanup_user(new_user)
    form = new_user.to_form()
    del form[field]

    response = accounts_client.request("POST", AccountsClient.CREATE_ACCOUNT, form=form)

    assert_api_response(response, code=201)


@pytest.mark.negative
@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_create_account_without_required_field(
    accounts_client, new_user, cleanup_user, field
):
    cleanup_user(new_user)  # in case the API wrongly accepts the request
    form = new_user.to_form()
    del form[field]

    response = accounts_client.request("POST", AccountsClient.CREATE_ACCOUNT, form=form)

    assert_api_response(
        response,
        code=400,
        message=f"Bad request, {field} parameter is missing in POST request.",
    )


@pytest.mark.negative
def test_create_account_with_existing_email(accounts_client, registered_user, faker):
    duplicate = registered_user.model_copy(update={"name": faker.name()})

    response = accounts_client.create_account(duplicate)

    assert_api_response(response, code=400, message="Email already exists!")


@pytest.mark.negative
def test_update_account_with_wrong_password(accounts_client, registered_user, faker):
    original_city = registered_user.city
    tampered = registered_user.model_copy(
        update={"password": "wrong-password", "city": faker.city()}
    )

    response = accounts_client.update_account(tampered)

    assert_api_response(response, code=404, message=ACCOUNT_NOT_FOUND)
    detail = _get_user_detail(accounts_client, registered_user.email)
    assert detail.city == original_city, "Account was modified without valid password"


@pytest.mark.negative
def test_delete_account_with_wrong_password(accounts_client, registered_user):
    response = accounts_client.delete_account(registered_user.email, "wrong-password")

    assert_api_response(response, code=404, message=ACCOUNT_NOT_FOUND)
    assert_api_response(
        accounts_client.verify_login(registered_user.email, registered_user.password),
        code=200,
        message="User exists!",
    )


@pytest.mark.negative
def test_delete_account_without_password(accounts_client, registered_user):
    response = accounts_client.request(
        "DELETE", AccountsClient.DELETE_ACCOUNT, form={"email": registered_user.email}
    )

    assert_api_response(
        response,
        code=400,
        message="Bad request, password parameter is missing in DELETE request.",
    )


@pytest.mark.negative
def test_get_user_detail_for_unknown_email(accounts_client):
    response = accounts_client.get_user_detail_by_email(unique_email())

    assert_api_response(
        response,
        code=404,
        message="Account not found with this email, try another email!",
    )


@pytest.mark.negative
def test_get_user_detail_without_email(accounts_client):
    response = accounts_client.request("GET", AccountsClient.USER_DETAIL_BY_EMAIL)

    assert_api_response(
        response,
        code=400,
        message="Bad request, email parameter is missing in GET request.",
    )
