"""Response contracts. ``extra="forbid"`` makes any undocumented field a failure."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ApiMessage(StrictModel):
    """Envelope for every non-data response, including errors reported via the body."""

    response_code: int = Field(alias="responseCode")
    message: str = Field(min_length=1)


class HttpErrorDetail(StrictModel):
    """Framework-level error returned with a real HTTP 4xx status."""

    detail: str = Field(min_length=1)


class UserType(StrictModel):
    usertype: str = Field(min_length=1)


class Category(StrictModel):
    usertype: UserType
    category: str = Field(min_length=1)


class Product(StrictModel):
    id: PositiveInt
    name: str = Field(min_length=1)
    price: str = Field(pattern=r"^Rs\. \d+$")
    brand: str = Field(min_length=1)
    category: Category


class ProductsResponse(StrictModel):
    response_code: Literal[200] = Field(alias="responseCode")
    products: list[Product]


class Brand(StrictModel):
    id: PositiveInt
    brand: str = Field(min_length=1)


class BrandsResponse(StrictModel):
    response_code: Literal[200] = Field(alias="responseCode")
    brands: list[Brand]


class UserDetail(StrictModel):
    id: PositiveInt
    name: str
    email: str
    title: str
    birth_day: str
    birth_month: str
    birth_year: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    country: str
    state: str
    city: str
    zipcode: str


class UserDetailResponse(StrictModel):
    response_code: Literal[200] = Field(alias="responseCode")
    user: UserDetail
