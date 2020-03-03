# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BlogCrawlerSpider(CrawlSpider):
    name = 'blog_crawler'
    allowed_domains = ['github.blog']
    start_urls = ["https://github.blog/page/{}/".format(i) for i in
                  range(2, 30)]
    start_urls.insert(0, "https://github.blog/")

    rules = (Rule(
        LinkExtractor(allow=r'github.blog\/(2019|2020)-((0[1-9])|(1[0-2]))-([0-3][0-9])'),
        callback='parse_blog',  follow=True),)

    def parse_blog(self, response):  # parse individual blogs
        item = {}
        item['title'] = response.xpath('//article[contains(concat(" ",'
                                       'normalize-space(@class)," ")," post '
                                       '")]//h1//text()').get().strip() or ''
        blog_content = response.xpath('//div[contains(concat(" ",'
                                         'normalize-space(@class)," "),'
                                         '" post__content ")]//text('
                                         ')').extract() or ''
        blog_text = "".join(blog_content)
        for i in ['\tLinkedIn\t', '\tShare on LinkedIn', '\tShare on '
                    'Twitter\t', '\tTwitter\t', '\tFacebook\t',
                    '\tShare on Facebook\t', '\tShare']:
            blog_text = blog_text.replace(i, '')
        # item['text'] = blog_text
        word_count = re.split(r'\s+', blog_text)
        item['url'] = response.url
        item['date'] = response.xpath('//time/@datetime').get()
        item['author'] = response.xpath('//p[contains(concat(" ",'
                                        'normalize-space(@class)," "),'
                                        '" hero-post__author-name ")]//text('
                                        ')').get().strip() or ''
        item['author_url'] = response.xpath('//a[contains(concat(" ",'
                                            'normalize-space(@class)," ")," author-block ")]/@href').get() or ''
        item['word_count'] = len(list(filter(None, word_count)))
        return item
