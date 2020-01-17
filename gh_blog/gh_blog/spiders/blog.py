# -*- coding: utf-8 -*-
import scrapy


class BlogSpider(scrapy.Spider):
    name = "all-blogs"
    start_urls = [
        "file:///Users/danjack/gh-blog.html",
        "file:///Users/danjack/gh-blog2.html",
    ]

    def parse(self, response):
        articles = response.xpath('////main//section[contains(concat(" ",normalize-space(@class)," ")," all-posts ")]//article[contains(concat(" ",normalize-space(@class)," ")," post-item ")]')
        for blog in articles:
            yield {
                'title': blog.xpath(
                    'div/h4/a/text()').get().strip('\n').strip('\t').replace(
                    "\u2019", "'"),
                'link': blog.xpath('div/h4/a/@href').get(),
                'date': blog.xpath('div/a/time/@datetime').get(),
                'author': blog.xpath(
                    'div/a/p/text()').get().strip('\n').strip('\t'),
                'authorProfile': blog.xpath(
                    'div/a[contains(concat(" ",normalize-space(@class)," "),'
                    '" author-block ")]/@href').get()
            }

        next_page = response.xpath('//*[contains(concat(" ",'
                                   'normalize-space(@class)," "),'
                                   '" next_page ")]/@href').get()
        if next_page is None:
            next_page = response.xpath('//*[contains(concat(" ",'
                                       'normalize-space(@class)," "),'
                                       '" all-posts__view-more ")]/@href').get()
        # print(next_page)
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)