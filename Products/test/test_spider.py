#from requests..api import head
from asyncio import timeout
import os  
import requests
import pytest
from scrapy.http import HtmlResponse, Request
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Products.spiders.laptops import LaptopsSpider

def test_laptops_spider():

    path = os.path.join(os.path.dirname(__file__), 'Laptop_MercadoLibre.html')
    assert os.path.exists(path), f"No se encontró el archivo en: {path}"
    with open(path, encoding="utf-8") as f:
        html = f.read()

        request = Request(
            url="https://listado.mercadolibre.com.ve/laptops#D[A:laptops]",
        )
        response = HtmlResponse(
            url=request.url,
            body=html,
            encoding='utf-8',
            request= request
        )

        spider = LaptopsSpider()
        items = list(spider.parse(response))

    product_items = [item for item in items if isinstance(item, dict)]

    assert len(items) == 49, "Expected 49 items, got {}".format(len(items))

    for i, item in enumerate(product_items):
        assert 'url' in item, "Item missing 'url' field"
        assert 'title' in item, "Item missing 'title' field"
        assert 'price' in item, "Item missing 'price' field"
        assert 'currency' in item, "Item missing 'currency' field"
        assert item['url'] is not None, "Item 'url' should not be None"
        assert item['title'] is not None, "Item 'title' should not be None"
        assert item['price'] is not None, "Item 'price' should not be None"
        assert item['currency'] is not None, "Item 'currency' should not be None"

def test_access_laptops_spider():
    url = "https://listado.mercadolibre.com.ve/laptops#D[A:laptops]"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-VE,es;q=0.9",
    }
    response = requests.get(url,headers=headers)

    assert response.status_code == 200, f"Failed to access {url}, status code: {response.status_code}"
    assert "<html" in response.text.lower(), "Response does not contain HTML content"