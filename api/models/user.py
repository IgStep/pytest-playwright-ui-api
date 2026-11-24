from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Title(StrEnum):
    MR = "Mr"
    MRS = "Mrs"


class UserData(BaseModel):
    """Request payload for createAccount / updateAccount (form-encoded)."""

    model_config = ConfigDict(frozen=True)

    name: str
    email: str
    password: str
    title: Title
    birth_date: str
    birth_month: str
    birth_year: str
    firstname: str
    lastname: str
    company: str
    address1: str
    address2: str
    country: str
    zipcode: str
    state: str
    city: str
    mobile_number: str

    def to_form(self) -> dict[str, str]:
        return self.model_dump(mode="json")

    def expected_user_detail(self) -> dict[str, str]:
        """Fields as getUserDetailByEmail returns them.

        The API renames some fields on the way out and never returns
        ``password`` or ``mobile_number``.
        """
        return {
            "name": self.name,
            "email": self.email,
            "title": self.title.value,
            "birth_day": self.birth_date,
            "birth_month": self.birth_month,
            "birth_year": self.birth_year,
            "first_name": self.firstname,
            "last_name": self.lastname,
            "company": self.company,
            "address1": self.address1,
            "address2": self.address2,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "zipcode": self.zipcode,
        }
