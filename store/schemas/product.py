from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, Field
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from store.schemas.base import BaseSchemaMixin, OutSchema


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

class ProductIn(ProductBase, BaseSchemaMixin):
    ...

class ProductOut(ProductIn, OutSchema):
    ...

def convert_decimal_128(v):
    return Decimal128(str(v))

Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]

class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    updated_at: Optional[datetime] = None


class ProductUpdateOut(ProductOut):
    ...


def create_unique_index(collection, field_name: str):
    collection.create_index([(field_name, ASCENDING)], unique=True)


client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
collection = db["products"]


create_unique_index(collection, "name")


def convert_product_dict(product_dict):
    product_dict['price'] = Decimal128(str(product_dict['price']))
    return product_dict


product = ProductIn(name="Example Product", quantity=10, price=Decimal("99.99"), status=True)

try:
    collection.insert_one(convert_product_dict(product.dict()))
    print("Product inserted successfully.")
except DuplicateKeyError:
    print("Product with this name already exists.")
except Exception as e:
    print(f"An error occurred: {e}")
