# blog-crawler

This is a short scraping exercise using the [scrapy](https://github.com/scrapy/scrapy) web crawling and web scraping framework. 

The crawler looks at [GitHub.blog](https://github.blog/)'s posts and scrapes post titles, post link, post date, post author, and author profile.

Here's an example of what's returned:
```
{
'_id': ObjectId('5e56ef6992f1749894560e27'), 
'title': 'GitHub Desktop 2.3 removes obstacles to help you be more productive', 
'link': 'https://github.blog/2020-01-29-github-desktop-2-3-removes-obstacles-to-help-you-be-more-productive/', 
'date': '2020-01-29', 
'author': 'Neha Batra', 
'authorProfile': 'https://github.blog/author/nerdneha/'
}
```

I used the MongoDB example from the [scrapy documentation](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) to pipe the results to a MongoDB collection.
