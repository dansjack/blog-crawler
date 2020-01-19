# -*- coding: utf-8 -*-
import scrapy
"""
    Spiders to crawl Github.blog
    NOTE: MAKE SURE A DOWNLOAD DELAY OF 10 IS ENABLED 
          AND ITEM PIPELINE IS SET APPROPRIATELY
"""


class BlogSpiderAll(scrapy.Spider):
    """
    Crawls all pages of Github.blog
    """
    name = "all-blogs"
    start_urls = [
        "https://github.blog/",
        "https://github.blog/page/2/"
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

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class BlogSpiderFront(scrapy.Spider):
    """
    Crawls only the front page of Github.blog
    """
    name = "blog-front"
    start_urls = [
        "https://github.blog/",
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


class BlogSpiderFrontFive(scrapy.Spider):
    """
    Crawls first five pages of Github.blog
    """
    name = "blog-front-five"
    start_urls = [
        "https://github.blog/",
        "https://github.blog/page/2/",
        "https://github.blog/page/3/",
        "https://github.blog/page/4/",
        "https://github.blog/page/5/"
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
