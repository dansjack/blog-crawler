# blog-crawler

This is a short scraping exercise using the [scrapy](https://github.com/scrapy/scrapy) web crawling and web scraping framework. 

The crawler looks at [GitHub.blog](https://github.blog/)'s posts and changelogs and scrapes information about each post.

Here's an example of what's returned:
```
{"_id":{"$oid":"5e5e153eddd940e39aa7f754"},
"title":"Bring your monorepo down to size with sparse-checkout",
"url":"https://github.blog/2020-01-17-bring-your-monorepo-down-to-size-with-sparse-checkout/",
"date":"2020-01-17",
"author":"Derrick Stolee",
"authorUrl":"https://github.blog/author/dstolee/",
"wordCount":{"$numberInt":"2503"},
"categories":["Community","Open source"],
"imgCount":{"$numberInt":"7"}}
```

I used the MongoDB example from the [scrapy documentation](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) to pipe the results to a MongoDB collection.
