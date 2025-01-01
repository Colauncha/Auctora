from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from server.utils.helpers import (
    category_id_generator, sub_category_id_generator
)

class GetItemCategorySchema(BaseModel):
    id: UUID = Field(
        description="ID of the Item Category",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )
    item_id: UUID = Field(
        description="ID of the Item",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )
    category_id: UUID = Field(
        description="ID of the Category",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )

    model_config = {"from_attributes": True}


class ImageLinkObj(BaseModel):
    link: str = Field(
        description="Image link of the Item",
        examples=["https://www.example.com/image1.jpg"]
    )
    public_id: str = Field(
        description="Asset ID",
        examples=["rfe45g"]
    )
    model_config = {"from_attributes": True}


class CreateItemSchema(BaseModel):
    id: Optional[UUID] = Field(
        description="ID of the Item",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )
    sellers_id: UUID = Field(
        description="ID of the Seller",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )
    name: str = Field(
        description="Name of the Item",
        examples=["Example Item"]
    )
    description: str = Field(
        description="Description of the Item",
        examples=["This is a test item."]
    )
    starting_price: float = Field(
        description="Starting price of the Item",
        examples=[10.0]
    )
    current_price: Optional[float] = Field(
        description="Current price of the Item",
        examples=[10.0]
    )
    image_link: ImageLinkObj # Watch for errors
    image_link_2: Optional[ImageLinkObj] = Field(
        description="Second image link of the Item",
        examples=["https://www.example.com/image2.jpg"]
    )
    image_link_3: Optional[ImageLinkObj] = Field(
        description="Third image link of the Item",
        examples=["https://www.example.com/image3.jpg"]
    )
    image_link_4: Optional[ImageLinkObj] = Field(
        description="Fourth image link of the Item",
        examples=["https://www.example.com/image4.jpg"]
    )
    image_link_5: Optional[ImageLinkObj] = Field(
        description="Fifth image link of the Item",
        examples=["https://www.example.com/image5.jpg"]
    )

    @model_validator(mode='after')
    def set_current_price(self):
        if self.current_price is None:
            self.current_price = self.starting_price
        return self

    model_config = {"from_attributes": True}


class GetItemSchema(CreateItemSchema):
    id: UUID


class CreateCategorySchema(BaseModel):
    name: str = Field(
        description="Name of the Category",
        examples=["Electronics"]
    )
    description: Optional[str] = Field(
        description="Description of the Category",
        examples=["Devices and gadgets."]
    )

    model_config = {"from_attributes": True}


class CreateSubCategorySchema(BaseModel):
    parent_id: str = Field(
        description="ID of the Parent Category",
        examples=['CAT001']
    )
    name: str = Field(
        description="Name of the Subcategory",
        examples=["Smartphones"]
    )
    model_config = {"from_attributes": True}


class GetCategorySchema(CreateCategorySchema):
    id: str = Field(
        description="ID of the Parent Category",
        examples=['CAT001']
    )
    subcategories: Optional[list] = Field(
        description="List of Subcategories",
        examples=[[{"id": "SUBCAT001", "name": "Smartphones"}]], default=None
    )

    def set_subcategories(self, subcategories: list):
        self.subcategories = subcategories
        return self


# class GetAllCategoriesSchema(BaseModel):
#     categories: Dict[str, str] = Field(
#         description="List of all Categories",
#         examples=[{"id": "CAT001", "name": "Electronics"}]
#     )


class GetSubCategorySchema(CreateSubCategorySchema):
    id: str = Field(
        description="ID of the Parent Category",
        examples=['SUBCAT0001']
    )
    parent_name: Optional[str] = Field(
        description="Name of the Parent Category",
        examples=["Electronics"], default=None
    )
    parent_description: Optional[str] = Field(
        description="Description of the Parent Category",
        examples=["Devices and gadgets."], default=None
    )
    def set_parent_details(self, parent_name: str, parent_description: str):
        self.parent_name = parent_name
        self.parent_description = parent_description
        return self