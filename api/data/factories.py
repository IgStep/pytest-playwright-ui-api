from typing import Any
from uuid import uuid4

from faker import Faker

from api.models.user import Title, UserData

# Values accepted by the site's signup form.
COUNTRIES = (
    "India",
    "United States",
    "Canada",
    "Australia",
    "Israel",
    "New Zealand",
    "Singapore",
)


def unique_email() -> str:
    # A uuid suffix keeps emails unique across reruns and xdist workers,
    # even when faker is seeded with a fixed value.
    return f"aqa.{uuid4().hex[:12]}@example.com"


def build_user(faker: Faker, **overrides: Any) -> UserData:
    birth = faker.date_of_birth(minimum_age=18, maximum_age=80)
    data: dict[str, Any] = {
        "name": faker.name(),
        "email": unique_email(),
        "password": faker.password(length=12),
        "title": faker.random_element(list(Title)),
        "birth_date": str(birth.day),
        "birth_month": birth.strftime("%B"),
        "birth_year": str(birth.year),
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "company": faker.company(),
        "address1": faker.street_address(),
        "address2": faker.secondary_address(),
        "country": faker.random_element(COUNTRIES),
        "zipcode": faker.postcode(),
        "state": faker.state(),
        "city": faker.city(),
        "mobile_number": faker.numerify("##########"),
    }
    data.update(overrides)
    return UserData(**data)
