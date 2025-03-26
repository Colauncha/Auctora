from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field, model_validator


class ImageLinkObj(BaseModel):
    link: Optional[str] = Field(
        description="Image link of the Item",
        examples=["https://www.example.com/image1.jpg"]
    )
    public_id: Optional[str] = Field(
        description="Asset ID",
        examples=["rfe45g"]
    )
    model_config = {"from_attributes": True}


class CreateItemSchema(BaseModel):
    name: str = Field(
        description="Name of the Item",
        examples=["Example Item"]
    )
    description: str = Field(
        description="Description of the Item",
        examples=["This is a test item."]
    )
    category_id: str = Field(
        description="ID of the Category",
        examples=["CAT001"]
    )
    sub_category_id: str = Field(
        description="ID of the Subcategory",
        examples=["SUBCAT001"]
    )

    model_config = {"from_attributes": True}


class UpdateItemSchema(CreateItemSchema):
    image_link: Optional[ImageLinkObj] # Watch for errors
    image_link_2: Optional[ImageLinkObj]
    image_link_3: Optional[ImageLinkObj]
    image_link_4: Optional[ImageLinkObj]
    image_link_5: Optional[ImageLinkObj]
    weight: Optional[float] = Field(
        description="Weight of the Item",
        examples=[1.0]
    )
    height: Optional[float] = Field(
        description="Height of the Item",
        examples=[1.0]
    )
    width: Optional[float] = Field(
        description="Width of the Item",
        examples=[1.0]
    )
    length: Optional[float] = Field(
        description="Length of the Item",
        examples=[1.0]
    )

class GetItemSchema(UpdateItemSchema):
    id: UUID
    users_id: UUID


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


class UpdateCategorySchema(CreateCategorySchema):
    pass


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


class UpdateSubCategorySchema(CreateSubCategorySchema):
    pass


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