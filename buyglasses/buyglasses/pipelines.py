# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BuyglassesPipeline:
    def process_item(self, item, spider):
        item['price_final'] = self.remove_rupiah_format(item['price_final'])
        return item
    
    def remove_rupiah_format(self, amount):
        # Remove "Rp" prefix
        amount = amount.replace("Rp", "")
        
        # Remove dot (".") separator
        amount = amount.replace(".", "")
        
        return amount
