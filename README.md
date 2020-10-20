# Cigabuy Scrapy

In `setting.py`
FEED_EXPORT_ENCODING = 'utf-8'

```py
# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['cigabuy.com']
    start_urls = [
        'https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    def parse(self, response):
        for product in response.xpath("//div[@class='r_b_c']/div[@class='p_box_wrapper']"):
            yield {
                'title': product.xpath(".//div/a[2]/text()").get(),
                'url': product.xpath(".//div/a[2]/@href").get(),
                'discounted_price': product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get(),
                'original_price': product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get()
            }
```

Now that we have the information for the first page, we now need to inspect the `Next Page` button on the webpage and find the class to have it absolutly. Then we need to make a variable that will find it and then include some logic to continue the scrape if the url exists.

```python
# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['cigabuy.com']
    start_urls = [
        'https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    def parse(self, response):
        for product in response.xpath("//div[@class='r_b_c']/div[@class='p_box_wrapper']"):
            yield {
                'title': product.xpath(".//div/a[2]/text()").get(),
                'url': product.xpath(".//div/a[2]/@href").get(),
                'discounted_price': product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get(),
                'original_price': product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get()
            }
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

```

## Change User Agent

```python
# -*- coding: utf-8 -*-
import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        for glasses in response.xpath("//div[@id='product-lists']/div"):

            if glasses.xpath(".//span[@class='im img-tag tag-off-per product-icon-text'][ contains(text(), 'Sale')]").get():
                sale = True
            else:
                sale = False

            yield {
                'product_url': glasses.xpath(".//div[1]/a/@href").get(),
                'product_image': glasses.xpath(".//div[1]/a[1]/img[1]/@src").get(),
                'product_name': str(glasses.xpath(".//div[2]/div[@class = 'mt-3']/div/div[1]/div/a/text()").get()).strip(),
                'product_price': glasses.xpath(".//div[2]/div[@class = 'mt-3']/div/div[2]/div/div/span/text()").get(),
                'sale': sale
            }

        next_page = response.xpath("//a[contains(text(), 'Next')]/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

```

# Debuggging
