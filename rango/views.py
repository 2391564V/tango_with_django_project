from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from datetime import datetime

# import models
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Define different views to send a reponse to
def index(request):
    request.session.set_test_cookie()

    # Retrieve top 5 Categories and Pages, '-' means descending order.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    # Create cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # Return response to user
    return render(request, 'rango/index.html', context_dict)

def visitor_cookie_handler(request):
    # Get number of visitors to the site
    # If cookie exists, use 'visits' value otherwise default to 1
    visits = int(get_server_side_cookie(request, 'visits', 1))

    # Get time from last visit
    last_visit_cookie = get_server_side_cookie(
        request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                        '%Y-%m-%d %H:%M:%S')

    # If its been more than a day
    if(datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        # Update the last visit cookie to now
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    # Update the visits cookie
    request.session['visits'] = visits

# Helper function to check if requested cookie is in session data,
# If not, returns default value
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def about(request):
    if request.session.test_cookie_worked():
        print("Test cookie worked.")
        request.session.delete_test_cookie()

    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!",
        'visits': request.session['visits']}
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
    context_dict = {'user_form': user_form, 'profile_form': profile_form,
                    'registered': registered}
    return render(request, 'rango/register.html', context_dict)

# Log in
def user_login(request):
    # A http post?
    if request.method == 'POST':
        # Get input from user
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use django machinery to validate
        user = authenticate(username=username, password=password)

        # If correct, user object is created
        if user:
            # Check if user has been disabled
            if user.is_active:
                # If user is valid and active, log in
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details provided
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # If not a http post, display log in form.
    else:
        return render(request, 'rango/user_login.html', {})
