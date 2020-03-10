# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


"""
    Spiders to crawl Github.blog -- DEPRECATED -- SEE blog_crawler.py
"""


class BlogCrawlerSpider(CrawlSpider):
    name = 'blog_crawler'
    allowed_domains = ['github.blog']
    start_urls = ["https://github.blog/page/{}/".format(i) for i in range(10)]

    rules = (Rule(
        LinkExtractor(allow=r'github.blog\/20(17|18|19|20)-((0[1-9])|(1['
                            r'0-2]))-([0-3][0-9])',
                      restrict_xpaths='//section[contains(concat(" ",'
                                      'normalize-space(@class)," "),'
                                      '" all-posts ")]'),
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
        item['authorUrl'] = response.xpath('//a[contains(concat(" ",'
                                            'normalize-space(@class)," ")," author-block ")]/@href').get() or ''
        item['wordCount'] = len(list(filter(None, word_count)))
        item['categories'] = response.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," post__categories ")]//li//text()').extract()
        item['imgCount'] = len(response.xpath('//div[contains(concat(" ",'
                                        'normalize-space(@class)," "),'
                                        '" post__content ")]//img').extract())
        return item


class BlogChangelogCrawlerSpider(CrawlSpider):
    name = 'changelog_crawler'
    allowed_domains = ['github.blog']
    start_urls = ["https://github.blog/changelog/page/{}/".format(i) for i in
                  range(4)]

    rules = (Rule(
        LinkExtractor(allow=r'github.blog\/changelog\/20(17|18|19|20)-((0['
                            r'1-9])|(1['
                            r'0-2]))-([0-3][0-9])'),
        callback='parse_blog',  follow=True),)

    def parse_blog(self, response):  # parse individual blogs
        item = {}
        item['title'] = response.xpath('//h1[contains(concat(" ",normalize-space(@class)," ")," post__title ")]//text()').get().strip() or ''
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
        item['word_count'] = len(list(filter(None, word_count)))
        item['imgCount'] = len(response.xpath('//div[contains(concat(" ",'
                                              'normalize-space(@class)," "),'
                                              '" post__content ")]//img').extract())
        return item
