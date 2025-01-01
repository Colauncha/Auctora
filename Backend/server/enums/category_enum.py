from enum import Enum


class Electronics(Enum):
    APPLIANCES = None
    TVS_AND_ACCESSORIES = None
    CONSOLES = None
    BUILT_IN_APPLIANCES = None


class Gadgets(Enum):
    PHONES = None
    PHONES_ACCESSORIES = None
    LAPTOPS = None
    LAPTOPS_ACCESSORIES = None


class CategoryList(Enum):
    ELECTRONICS = Electronics
    GADGETS = Gadgets
    FASHION = None
    HOME_AND_GARDEN = None
    SUPERMARKET = None
    BEAUTY = None
    CULTURE = None
    SPORTS = None
    AUTOMOTIVE = None
    PROPERTIES = None