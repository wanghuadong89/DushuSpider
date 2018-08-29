# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# crawlspider 是scrapy提供的基于basic一种更高级模板的爬虫，这种爬虫，可以通过一定的规则为下载器提供大批量的link，下载器可以自动的调用这些连接
from DushuSpider.items import DushuspiderItem

class DushuSpider(CrawlSpider):
    name = 'dushu'
    allowed_domains = ['dushu.com']
    start_urls = ['http://www.dushu.com/book/1163.html']

    rules = (
        Rule(LinkExtractor(allow=r'/book/1163_\d+\.html'), callback='parse_item', follow=True),
    )
    # 通过rules来对爬虫进行量的扩充，rules是一个元组，里面包含多个Rule对象
    # Rule对象第一个参数LinkExtractor里面传递一个匹配url的一个规则（可以是正则、xpath、bs4等规则），第二个参数回调函数，Rule规则匹配到url以后，就会把这些url全部交给调度器，调度器调用下载器，下载结束以后，就会回调回调函数，【注意】回调函数这里写成字符串
    # 【注意】Rule规则会自动的把一些无效的url剔除

    # LinkExtractor规则：
    # allow代表 用正则来匹配（常用）
    # xpath代表用 xpath语法来匹配
    # css代表用 css选择器来匹配

    def parse_item(self, response):
        book_list = response.xpath("//div[@class='bookslist']/ul/li")
        for book in book_list:
            item = DushuspiderItem()
            item["name"] = book.xpath(".//h3/a/text()").extract_first()
            item["author"] = book.xpath(".//p/a/text()").extract_first()
            item["cover_img"] = book.xpath(".//img/@data-original").extract_first()
            # 跳转二级页面
            next = "http://www.dushu.com" + book.xpath(".//h3/a/@href").extract_first()
            yield scrapy.Request(url=next,callback=self.parse_next,meta={"book":item})

    def parse_next(self, response):
        item = response.meta["book"]
        item['cbs'] = response.xpath("//div[@class='book-details-left']/table//tr[2]").extract_first()
        item['content'] = response.xpath("//div[@class='text txtsummary']").extract()[0]
        item['author_info'] = response.xpath("//div[@class='text txtsummary']").extract()[1]
        item['price'] = response.xpath("//p[@class='price']/span/text()").extract_first()

        m = response.xpath("//div[starts-with(@class,'text txtsummary')]/text()")
        if len(m) == 3:
            # 说明这时候书有目录
            item["mulu"] = m.extract()[2]
        else:
            item["mulu"] = ''
        yield item




