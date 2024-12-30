from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field, model_validator


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

    @model_validator
    def set_current_price(cls, values):
        if values.get("current_price") is None:
            values["current_price"] = values["starting_price"]
        return values

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


class CreateSubCategorySchema(CreateCategorySchema):
    parent_category_id: UUID = Field(
        description="ID of the Parent Category",
        examples=["84hgdf-dmeu-fvtre-wectb-yyrrv4254"]
    )
    sub_name: str = Field(
        description="Name of the Subcategory",
        examples=["Smartphones"]
    )


class GetCategorySchema(CreateCategorySchema):
    id: UUID


class GetSubCategorySchema(CreateSubCategorySchema):
    id: UUID
