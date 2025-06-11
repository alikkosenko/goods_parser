from dataclasses import dataclass

HEADLESS = False

@dataclass
class Shop:
    shop_id: int
    name: str
    link: str

@dataclass
class Product:
    product_type: str
    name: str
    price: float
    old_price: float
    profit: int
    weight: str
    lnk: str
    picture_lnk: str

@dataclass
class ProductCategory:
    cat_id: int
    cat_lnk: str

