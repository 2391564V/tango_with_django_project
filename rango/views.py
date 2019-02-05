from django.shortcuts import render
from django.http import HttpResponse

# import models
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Define different views to send a reponse to
def index(request):
    # Retrieve top 5 Categories and '-' means descending order
    category_list = Category.objects.order_by('-likes')[:5]
    # Retrieve top 5 viewed pages
    page_list = Page.objects.order_by("-views")[:5]

    context_dict = {'categories': category_list, 'pages': page_list}
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

def add_category(request):
    form = CategoryForm()

    # A http post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Check validity
        if form.is_valid():
            form.save(commit=True) # Save to database
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    category = Category.objects.get(slug=category_name_slug)
    form = PageForm()

    # A http post?
    if request.method == 'POST':
        print("Post recieved.")
        form = PageForm(request.POST)

        # Check validity
        if form.is_valid():
            print("Valid form.")
            page = form.save(commit=False) # Save to database
            page.category = category
            page.views = 0
            page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    pages = Page.objects.filter(category=category)
    context_dict = {'form':form, 'category':category, 'pages':pages}
    return render(request, 'rango/add_page.html', context_dict)

# User registration
def register(request):
    registered = False

    # If request is a http POST, process form
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Hash user password, save.
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            # Profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Save
            profile.save()
            registered = True
        else:
            # Invalid forms, print problems to terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a http POST, so render registration form
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'rango/register.html', context_dict)
