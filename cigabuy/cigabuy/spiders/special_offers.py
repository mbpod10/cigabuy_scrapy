# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['cigabuy.com']
    # start_urls = [
    #     'https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    def start_requests(self):
        yield scrapy.Request(url='https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html', callback=self.parse, headers={
            'User-Agent': ' Mozilla/5.0 (Linux Android 6.0 Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Mobile Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath("//div[@class='r_b_c']/div[@class='p_box_wrapper']"):
            yield {
                'title': product.xpath(".//div/a[2]/text()").get(),
                'url': product.xpath(".//div/a[2]/@href").get(),
                'discounted_price': product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get(),
                'original_price': product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get(),
                'User-Agent': response.request.headers['User-Agent']
            }
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': ' Mozilla/5.0 (Linux Android 6.0 Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Mobile Safari/537.36'
            })

# JOIN URL IF RELATIVE  # 'url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
