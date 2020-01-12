# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
# from tools.zhima_ip import GetIP
import time, random, logging


class DmticketsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DmticketsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 随机更换user-agent
class RandomUserAgentMiddlware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            # print(request.headers)
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())


# 设置随机延时
class RandomDelayMiddleware(object):
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        delay = crawler.spider.settings.get("RANDOM_DELAY", 10)
        if not isinstance(delay, int):
            raise ValueError("RANDOM_DELAY need a int")
        return cls(delay)

    def process_request(self, request, spider):
        # delay = random.randint(0, self.delay)
        delay = random.uniform(0, self.delay)
        delay = float("%.1f" % delay)
        logging.debug("### random delay: %s s ###" % delay)
        time.sleep(delay)


# 使用PYPPETEER
from scrapy.http import HtmlResponse
import asyncio
import pyppeteer
import random
import logging
pyppeteer_level = logging.WARNING
logging.getLogger('pyppeteer').setLevel(pyppeteer_level)
logging.getLogger('websockets.protocol').setLevel(pyppeteer_level)
pyppeteer_logger = logging.getLogger('pyppeteer')
pyppeteer_logger.setLevel(logging.WARNING)
from lxml import etree


class FundscrapyDownloaderMiddleware(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.getbrowser())
        self.loop.run_until_complete(task)
        self.user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
        ]
        # 填入目标网址
        self.target_url = "https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_6.591b23e14gTCgT&id=610094000342"

    async def getbrowser(self):
        width, height = 1366, 768
        # get_ip = GetIP()
        # proxy_ip = get_ip.get_random_ip()
        # proxy_ip = proxy_ip.split("://")[1]
        # print("当前使用的代理IP是" + proxy_ip)
        self.browser = await pyppeteer.launch(
            headless=False,
            # headless=True,
            timeout=1500,
            # 开发者工具
            devtools=False,
            dumpio=True,
            options={'args':
                        [
                         '--no-sandbox',
                          # 关闭提示条
                          '--disable-infobars',
                          f'--window-size={width},{height}',
                          '--disable-extensions',
                          '--hide-scrollbars',
                          '--disable-bundled-ppapi-flash',
                          '--mute-audio',
                          '--disable-setuid-sandbox',
                          '--disable-gpu',
                          # '--headless',
                          # f'--proxy-server=111.29.3.186:8080',
                          # '--proxy-server={}'.format(proxy_ip),
                        ],
                    }
        )
        # 无痕模式浏览器
        context = await self.browser.createIncogniteBrowserContext()
        self.page = await context.browser.newPage()

    async def getnewpage(self):
        return await self.browser.newPage()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        usePypp = request.meta.get('usePypp', False)
        loop = asyncio.get_event_loop()
        if usePypp:
            task = asyncio.ensure_future(self.usePyppeteer(request))
            loop.run_until_complete(task)
            return HtmlResponse(url=request.url, body=task.result(), encoding="utf-8", request=request)
        else:
            pass

    async def usePyppeteer(self, request):
        num = random.randint(3, 6)
        await asyncio.sleep(num)
        # UA
        await self.page.setUserAgent(random.choice(self.user_agent))
        await self.page.setViewport({'width': 1366, 'height': 768})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)
        try:
            await self.page.goto(request.url, options={'timeout': 30000, "waitUntil": "networkidle2"})
        except Exception as e:
            print(e)
            print("error" * 100)
        await self.page.evaluate("""() =>{Object.defineProperties(navigator, {webdriver:{get: () => false}})}""")
        # await self.page.evaluate(
        #     '''() => {window.navigator.chrome = {runtime: {}, }; }''')
        await self.page.evaluate(
            '''() =>{Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});}''')
        await self.page.evaluate(
            '''() =>{Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
        # num = random.randint(3, 6)
        await asyncio.sleep(10)
        content = await self.page.content()
        content = etree.HTML(content)
        nick_name = content.xpath("//div[@class='span-box-header name-user show']/text()")[0]
        print(nick_name)
        if nick_name == "城市猫哥":
            # cookies = await self.get_cookie(self.page)
            # 不断循环，检测是否可以购买
            while True:
                page = await self.choose_tickets()
                if page:
                    while True:
                        page = await self.submit_order()
                        if page:
                            time.sleep(3000)
                        else:
                            continue
                else:
                    continue

    # 选票
    async def choose_tickets(self):
        await self.page.goto(self.target_url, options={'timeout': 30000, "waitUntil": "networkidle2"})
        # 添加选座功能
        # await self.page.click(".perform__order__select perform__order__select__performs > div.select_right > div.select_right_list > div.select_right_list_item")
        # await self.page.click(".perform__order__select > div.select_right > div.select_right_list > div.select_right_list_item sku_item")
        # buybtn = await self.page.xpath("//div[@class='buybtn']//text()")
        content = await self.page.content()
        content = etree.HTML(content)
        buybtn = content.xpath("//div[@class='buybtn']//text()")
        print(buybtn[0])
        if buybtn:
            if buybtn[0] == "立即预订" or buybtn[0] == "立即购买":
                await self.page.click(".buybtn")
                await asyncio.sleep(1)
                return True
            else:
                return None
        else:
            return None

    # 提交订单
    async def submit_order(self):
        content = await self.page.content()
        content = etree.HTML(content)
        order = content.xpath("//div[@class='submit-wrapper']/button/text()")
        if order:
            print("exit order!")
            content = await self.page.content()
            print(content)
            try:
                await self.page.click(".next-checkbox-label")
                await self.page.click(".submit-wrapper > button")
                return True
            except Exception as e:
                print(e)
                return await self.choose_tickets()
        else:
            return None


        # else:
        #     continue


    # 获取登录后cookie
    async def get_cookie(self, page):
        # res = await self.page.content()
        cookies_list = await page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        return cookies

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def close_spider(self, spider):
        self.page.close()
