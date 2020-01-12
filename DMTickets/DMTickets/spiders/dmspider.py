# -*- coding: utf-8 -*-
import scrapy


class DmspiderSpider(scrapy.Spider):
    name = 'dmspider'
    allowed_domains = ['damai.cn']
    # start_urls = ['http://damai.cn/']
    # 爬虫的设置
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'DMTickets.middlewares.FundscrapyDownloaderMiddleware': 260,
        }
    }

    def start_requests(self):
        # url = "https://www.damai.cn/"
        url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
        yield scrapy.FormRequest(
            url=url,
            callback=self.parse,
            meta={"usePypp": True},
            dont_filter=True,
        )

    def parse(self, response):
        print(response.text)
