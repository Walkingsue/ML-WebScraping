import scrapy
from Products.items import ProductsItem


class LaptopsSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["listado.mercadolibre.com.ve"]
    start_urls = ["https://listado.mercadolibre.com.ve/laptops#D[A:laptops]"]

    def parse(self, response):
        for laptop in response.xpath("//div[@class='ui-search-result__wrapper']"):
            item = ProductsItem()
            item["url"] = laptop.xpath("//div[contains(@class, 'ui-search-result__wrapper')]//h3/a").get()
            item["title"] = laptop.xpath(".//h3/a/text()").get()
            item["price"] = laptop.xpath("//div[@class='poly-price__current']/span/span[2]").get()
            item["currency"] = laptop.xpath("(//span[@class='andes-money-amount__currency-symbol']"
            "[normalize-space()='US$'])[1]").get()
            yield item

        current_offset = self.get_offset_from_url(response.url)
        next_offset = current_offset + 48  # ajusta según cuántos productos por página
        if next_offset < 5000:
            next_page_url = f"https://listado.mercadolibre.com.ve/laptops-accesorios/laptop_Desde_{next_offset}_NoIndex_True"
            yield scrapy.Request(next_page_url, callback=self.parse)

    def get_offset_from_url(self, url):
        # Extraer el número después de "_Desde_" si existe
        import re
        match = re.search(r'_Desde_(\d+)', url)
        if match:
            return int(match.group(1))
        return 1  # página inicial
