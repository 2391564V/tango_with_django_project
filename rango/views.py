from django.shortcuts import render
from django.http import HttpResponse

# import models
from rango.models import Category, Page

# Define different views to send a reponse to
def index(request):
    # Retrieve top 5 Categories and '-' means descending order
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    # Contect dictionary to be passed to template rendering engine
    context_dict = {}

    # Try to find category with given slug name,
    # Then add it's associated pages to the contect dictionary
    # Otherwise, add None to dictionary
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)
