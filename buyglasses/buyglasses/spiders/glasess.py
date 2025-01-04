import scrapy
import json


class GlasessSpider(scrapy.Spider):
    name = "glasess"
    allowed_domains = ["smartbuyglasses.co.id"]
    #https://www.smartbuyglasses.co.id/designer-eyeglasses/Arise-Collective/new-arrivals?brand=Arise-Collective&popular=new-arrivals
    start_urls = ["https://zvix9dzogt-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(5.8.1)%3B%20Lite%20(5.8.1)%3B%20Browser%3B%20instantsearch.js%20(4.75.1)%3B%20react%20(18.3.1)%3B%20react-instantsearch%20(7.13.4)%3B%20react-instantsearch-core%20(7.13.4)%3B%20next.js%20(14.2.15)%3B%20JS%20Helper%20(3.22.5)&x-algolia-api-key=7581b7923f0ca0576427c37941aba161&x-algolia-application-id=ZVIX9DZOGT"]

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Parse JSON response
        try:
            data = json.loads(response.body)
            # Algolia responses often have data nested in `results` and `hits`
            products = data.get('results', [{}])[0].get('hits', [])

            # Loop through all products and extract data
            for product in products:
                yield {
                    'product_name': product.get('name', 'N/A'),
                
                }
        except Exception as e:
            self.log(f"Error parsing JSON: {e}")
        