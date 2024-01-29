from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page

# each view must return a HttpRespinse object - it takes a string representing the content of
# the page we wish to send to the client requesting the view


def about(request):
    about_context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, "rango/about.html", context=about_context_dict)


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = {
        "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!",
        "categories": category_list,
        "pages": page_list,
    }
    # Render the response and send it back!
    return render(request, "rango/index.html", context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict["pages"] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict["category"] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict["category"] = None
        context_dict["pages"] = None

    # Go render the response and return it to the client.
    return render(request, "rango/category.html", context=context_dict)
