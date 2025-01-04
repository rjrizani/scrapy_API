import scrapy
import json
from urllib.parse import urlencode

class AdidasSpider(scrapy.Spider):
    name = "hijup"
    allowed_domains = ["hijup.com"]
    start_urls = [
        "https://www.hijup.com/proxy/graphql?operationName=Search&variables=%7B%22basic_colors%22%3A%5B%5D%2C%22category_names%22%3A%5B%5D%2C%22price%22%3A%5B%5D%2C%22keywords%22%3Anull%2C%22permalink%22%3Anull%2C%22price_ranges%22%3A%5B%5D%2C%22only_new%22%3Atrue%2C%22max_price%22%3Anull%2C%22page%22%3A1%2C%22per_page%22%3A70%2C%22vendor_names%22%3A%5B%5D%2C%22discounts%22%3Anull%2C%22ids%22%3A%5B%5D%2C%22tags%22%3A%5B%5D%2C%22locale%22%3A%22en%22%2C%22min_price%22%3Anull%2C%22sort%22%3A%22Newest%22%2C%22only_shown%22%3Atrue%2C%22show_all%22%3Afalse%2C%22category_slug%22%3Anull%2C%22slug_name%22%3A%22%22%2C%22slug_type%22%3A%22all_products%22%2C%22currency%22%3A%22IDR%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%221f224057a14687d1d211587c77bfde59e37a128888ea8ffb0e5c568f6aa14010%22%7D%7D"
    ]
    
    def parse(self, response):
        # Try parsing the JSON response directly
        try:
            data = json.loads(response.text)
            products = data.get("data", {}).get("search", {}).get("products", [])

            # Loop through all products and extract the required fields
            for product in products:
                yield {
                    "name": product.get("name"),
                    "url": product.get("url"),
                    "price_final": product.get("prices", {}).get("final")
                }

                   # Handling next page if available
           

        except Exception as e:
            self.log(f"Error parsing JSON: {e}")
