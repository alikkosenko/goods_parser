from dataclasses import dataclass

HEADLESS = False
delay = 5
scroll_delay = 0.2

@dataclass
class Product:
    product_type: str
    name: str
    price: float
    old_price: float
    profit: int
    lnk: str


@dataclass
class ProductCategory:
    cat_id: int
    cat_lnk: str


shops = {
    "Silpo": {"url": "https://silpo.ua/", 'table_name': "Silpo_table"},
    "ATB": {"url": "https://www.atbmarket.com/", 'table_name': "ATB_table"},
    "Tavria": {"url": "https://www.tavriav.ua/", 'table_name': "Tavria_table"}
}

html_classes = {
    "Silpo": {'card_c': 'product-card', 'name_c': 'product-card__title', 
              'price_c': 'product-card-price__displayPrice', 
              'oprice_c': 'product-card-price__displayOldPrice',
              'href_c': None,
              'num_c': 'pagination-item ng-star-inserted'},
    "ATB": {'card_c': 'product-card', 'name_c': 'product-card__title', 
              'price_c': 'product-card-price__displayPrice', 
              'oprice_c': 'product-card-price__displayOldPrice', 
              'href_c': 'href', 'num_c': 'pagination-item ng-star-inserted'},

}

categories = {
    "beer": {shops["Silpo"]['url']: "category/pyvo-4503",
             shops["ATB"]['url']: "catalog/310-pivo",
             shops["Tavria"]['url']: "search?name=%D0%BF%D0%B8%D0%B2%D0%BE"},
    "nuts": {shops["Silpo"]['url']: "search?find=%D0%B3%D0%BE%D1%80%D1%96%D1%85%D0%B8&",
             shops["ATB"]['url']: "sch?lang=uk&location=1154&query=%D0%B3%D0%BE%D1%80%D1%96%D1%85%D0%B8",
             shops["Tavria"]['url']: "search?name=%D0%B3%D0%BE%D1%80%D1%96%D1%85"},
    "cottage_cheese": {shops["Silpo"]['url']: "search?find=%D1%81%D0%B8%D1%80+%D0%BA%D0%B8%D1%81%D0%BB%D0%BE%D0%BC%D0%BE%D0"
                                       "%BB%D0%BE%D1%87%D0%BD%D0%B8%D0%B9&",
                       shops["ATB"]['url']: "catalog/379-sir-kislomolochniy",
                       shops["Tavria"]['url']: "ca/%D0%BC%D0%BE%D0%BB%D0%BE%D1%87%D0%BD%D1%96-%D0%B2"
                                        "%D0%B8%D1%80%D0%BE%D0%B1%D0%B8-%D1%81%D0%B8%D1%80%D0%B8-%D1%8F%D0%B8%D1%86"
                                        "%D1%8F/%D0%BA%D0%B5%D1%84%D1%96%D1%80-%D0%BA%D0%B8%D1%81%D0%BB%D0%BE%D0%BC"
                                        "%D0%BE%D0%BB%D0%BE%D1%87%D0%BD%D1%96-%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1"
                                        "%82%D0%B8/%D0%BA%D0%B8%D1%81%D0%BB%D0%BE%D0%BC%D0%BE%D0%BB%D0%BE%D1%87%D0%BD"
                                        "%D0%B8%D0%B8-%D1%81%D0%B8%D1%80/9691/9696/11448"}
    }

