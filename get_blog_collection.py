from pymongo import MongoClient
from gh_blog.gh_blog.settings import MONGO_URI


client = MongoClient(MONGO_URI)
gh = client.get_database('gh')

for post in gh.blogs.find():
    print(post)