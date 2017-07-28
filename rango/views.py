# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from models import Category, Page, User, UserProfile
from forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    context = RequestContext(request)

    category_list = Category.objects.order_by('-likes')
    page_list = Page.objects.all()

    context_dict = {'categories': category_list, 'pages': page_list}

    print "&&&dfgrter&&&&&", context_dict, "&&&&&&rertert&&"

    for category in category_list:
        category.url = category.name.replace(" ", "_")

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    print last_visit

    return render(request,'rango/index.html', context_dict)


def about(request):
    context = RequestContext(request)
    context_dict = {
        'boldmessage': "I am a working professional looking for new opportunities in Web development."}
    return render(request,'rango/about.html', context_dict)


def blog(request):
    return render(request, 'rango/blog.html')


def category(request, category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['pages'] = pages
        context_dict['category'] = category

    except category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    context = RequestContext(request)
    print "********************************",request.method
    if request.method == 'POST':

        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request,'rango/add_category.html', {'form': form})

@login_required
def add_page(request,category_name_url):
    context = RequestContext(request)
    print "***********category_name_url***************",category_name_url
    category_name = category_name_url.replace('_',' ')
    print "****************categoryname*****************", category_name
    print "********************POST************",request.method

    try:
        cat = Category.objects.get(name = category_name)
    except category.doesNotExist:
        pass

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=True)
            page.category = cat
            page.views = 0
            page.save()
            return category(request,category_name_url)
        else:

            print(form.errors)
    else:
        form = PageForm()
    return render(request,'rango/add_page.html',{'category_name_url':category_name_url,'category_name':category_name, 'form':form})

def register(request):

    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()

    registered = False
    context = RequestContext(request)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = userprofile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
            #return render(request,'rango/index.html')
        else:
            print user_form.errors, userprofile_form.errors
    else:
        user_form = UserForm()
        userprofile_form = UserProfileForm()

    return render(request,'rango/register.html', {'user_form':user_form, 'userprofile_form':userprofile_form,'registered': registered })

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        print username,password
        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request,user)
                print "****23423*****--------*****",request.user.username

                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return HttpResponse('welcome to Rango',request.user.username)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

def track_url(request):
    url='/rango/'
    if request.method == "GET":
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

        try:
            page = Page.objects.get(id=page_id)
            page.views = page.views +1
            print page.views,"000000000000000000000000000000"
            page.save()
            url = page.url
        except page.doesNotExist:
            pass

    return redirect(url)


@login_required
def like_category(request):

    cat_id = None
    if request.method =="GET":
            cat_id = request.GET['category_id']
    likes = 0

    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

def more(request):
    return render(request, 'rango/more.html', {})