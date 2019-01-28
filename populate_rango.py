import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

# Random number generation for page views
import random
max_random = 5000

# Data to populate with
def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
        "url":"http://docs.python.org/2/tutorial/",
        "views": random.randint(1, max_random)},
        {"title":"How to Think like a Computer Scientist",
        "url":"http://www.greenteapress.com/thinkpython/",
        "views": random.randint(1, max_random)},
        {"title":"Learn Python in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/",
        "views": random.randint(1, max_random)} ]

    django_pages = [
        {"title":"Official Django Tutorial",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
        "views": random.randint(1, max_random)},
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/",
        "views": random.randint(1, max_random)},
        {"title":"How to Tango with Django",
        "url":"http://www.tangowithdjango.com/",
        "views": random.randint(1, max_random)} ]

    other_pages = [
        {"title":"Bottle",
        "url":"http://bottlepy.org/docs/dev/",
        "views": random.randint(1, max_random)},
        {"title":"Flask",
        "url":"http://flask.pocoo.org",
        "views": random.randint(1, max_random)} ]

    cats = {"Python": {"views": 128, "likes": 64, "pages": python_pages},
        "Django": {"views": 64, "likes": 32, "pages": django_pages},
        "Other Frameworks": {"views": 32, "likes": 16, "pages": other_pages} }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

# Functions to add instances of pages and categories
def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Main execution
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
