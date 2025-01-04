import scrapy
import json
from urllib.parse import urlencode

class HijupGraphQLSpider(scrapy.Spider):
    name = "hijup_all"
    allowed_domains = ["hijup.com"]
    base_url = "https://www.hijup.com/proxy/graphql"


    # Initialize the first page
    def start_requests(self):
        # GraphQL query parameters for the first page
        params = {
            "operationName": "Search",
            "variables": json.dumps({
                "basic_colors": [],
                "category_names": [],
                "price": [],
                "keywords": None,
                "permalink": None,
                "price_ranges": [],
                "only_new": True,
                "max_price": None,
                "page": 1,  # Start from the first page
                "per_page": 70,
                "vendor_names": [],
                "discounts": None,
                "ids": [],
                "tags": [],
                "locale": "en",
                "min_price": None,
                "sort": "Newest",
                "only_shown": True,
                "show_all": False,
                "category_slug": None,
                "slug_name": "",
                "slug_type": "all_products",
                "currency": "IDR"
            }),
            "extensions": json.dumps({
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "1f224057a14687d1d211587c77bfde59e37a128888ea8ffb0e5c568f6aa14010"
                }
            })
        }
        
        # Send the initial request with the first page
        url = f"{self.base_url}?{urlencode(params)}"
        yield scrapy.Request(url, callback=self.parse, meta={"page": 1})

    def parse(self, response):
        # Parse the JSON response
        try:
            data = json.loads(response.text)
            products = data.get("data", {}).get("search", {}).get("products", [])

            # Extract product details (name, url, price)
            for product in products:
                yield {
                    "name": product.get("name"),
                    "url": f'https://www.hijup.com{product.get("url")}',
                    "price_final": product.get("prices", {}).get("final")
                }

            # Pagination handling
            current_page = response.meta["page"]
            total_products = data.get("data", {}).get("search", {}).get("total_products", 0)
            per_page = 70

            # If there are more pages, continue scraping
            if current_page * per_page < total_products:
                next_page = current_page + 1
                params = {
                    "operationName": "Search",
                    "variables": json.dumps({
                        "basic_colors": [],
                        "category_names": [],
                        "price": [],
                        "keywords": None,
                        "permalink": None,
                        "price_ranges": [],
                        "only_new": True,
                        "max_price": None,
                        "page": next_page,
                        "per_page": per_page,
                        "vendor_names": [],
                        "discounts": None,
                        "ids": [],
                        "tags": [],
                        "locale": "en",
                        "min_price": None,
                        "sort": "Newest",
                        "only_shown": True,
                        "show_all": False,
                        "category_slug": None,
                        "slug_name": "",
                        "slug_type": "all_products",
                        "currency": "IDR"
                    }),
                    "extensions": json.dumps({
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "1f224057a14687d1d211587c77bfde59e37a128888ea8ffb0e5c568f6aa14010"
                        }
                    })
                }

                # Generate the next page URL
                next_url = f"{self.base_url}?{urlencode(params)}"
                yield scrapy.Request(next_url, callback=self.parse, meta={"page": next_page})

        except json.JSONDecodeError:
            self.log("Error decoding JSON response")

