from api.client.base_client import ApiResponse, BaseApiClient
from api.models.user import UserData


class AccountsClient(BaseApiClient):
    CREATE_ACCOUNT = "createAccount"
    UPDATE_ACCOUNT = "updateAccount"
    DELETE_ACCOUNT = "deleteAccount"
    VERIFY_LOGIN = "verifyLogin"
    USER_DETAIL_BY_EMAIL = "getUserDetailByEmail"

    def create_account(self, user: UserData) -> ApiResponse:
        return self.request("POST", self.CREATE_ACCOUNT, form=user.to_form())

    def update_account(self, user: UserData) -> ApiResponse:
        return self.request("PUT", self.UPDATE_ACCOUNT, form=user.to_form())

    def delete_account(self, email: str, password: str) -> ApiResponse:
        return self.request(
            "DELETE",
            self.DELETE_ACCOUNT,
            form={"email": email, "password": password},
        )

    def verify_login(self, email: str, password: str) -> ApiResponse:
        return self.request(
            "POST",
            self.VERIFY_LOGIN,
            form={"email": email, "password": password},
        )

    def get_user_detail_by_email(self, email: str) -> ApiResponse:
        return self.request("GET", self.USER_DETAIL_BY_EMAIL, params={"email": email})
