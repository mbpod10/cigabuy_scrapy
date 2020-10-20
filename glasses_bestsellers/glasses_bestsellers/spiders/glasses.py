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

# //div[@id= 'product-lists']/div/div[1]/a/@href
# //div[@id = 'product-lists']/div/div[1]/a[1]/img[1]/@src
# //div[@id = 'product-lists']/div/div[2]/div[@class = 'mt-3']/div/div[1]/div/a/text() # title
# //div[@id = 'product-lists']/div/div[2]/div[@class = 'mt-3']/div/div[2]/div/div/span/text() # price
