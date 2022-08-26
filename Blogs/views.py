from distutils.command.config import config
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from django.views.generic.base import View
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets
from .serializers import *
from .models import *
from Blogs.tasks import send_mail_func
from decouple import config
import requests
from django.utils import timezone

def send_mail(request, message):
    current_user = request.user.email
    send_mail_func.delay(current_user,message)
    return HttpResponse("Sent")

@method_decorator(login_required, name='dispatch')
class Home(View):
    def get(self, request):
        apikey = config('apikey')
        res = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={apikey}")
        res = res.json()
        articles = res.get('articles')
        result = []
        i = 0
        while i < len(articles):
            result.append(articles[i:i+6])
            i += 6

        final_articles = []
        j = 0
        while j < len(result):
            final_articles.append(
                {'first': result[j][:2], 'second': result[j][2:]})
            j += 1
        return render(request, "index.html", {'final_articles': final_articles, 'active_home': 'active'})


@method_decorator(login_required, name='dispatch')
class Contact(View):
    def get(self, request):
        return render(request, "contact.html", {'active_contact': 'active'})


class Register(View):
    def get(self, request):
        inp_res = Registration_Form()
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, "register.html", {'register': inp_res, 'active_signin': 'active'})

    def post(self, request):
        register = Registration_Form(request.POST)
        if register.is_valid():
            register.last_login = timezone.now() 
            register.save()
            messages.success(request, "Registered Successfully!!")
            return HttpResponseRedirect('/accounts/login/')
        else:
            return render(request, "register.html", {'register': register})


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filterset_fields = ['id', 'title', 'user']
    search_fields = ['^id', '^title', '^user']
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]


@method_decorator(login_required, name='dispatch')
class Blogs(View):
    def get(self, request):
        result = Blog.objects.all()
        blogs = []
        i = 0
        while i < len(result):
            blogs.append({'row': result[i:i+2]})
            i += 2
        return render(request, "blogs.html", {'blogs': blogs, 'active_blogs': 'active'})


@method_decorator(login_required, name='dispatch')
class BlogDetails(View):
    def get(self, request, id):
        blog = Blog.objects.get(pk=id)
        user = User.objects.get(pk=request.user.id)
        user_id = User.objects.get(username=blog.user)
        related = [related_blog for related_blog in user.blog_set.all() if related_blog.id != blog.id]
        return render(request, "blogdetails.html", {'blog': blog, 'related': related, 'user' : user_id})


@method_decorator(login_required, name='dispatch')
class AddBlog(View):
    def get(self, request):
        emp_blog_form = BlogForm()
        if not request.user.is_authenticated:
            messages.info(
                request, "The Page You Are Trying To Visit is Login Protected. ")
            return HttpResponseRedirect('/login/')
        return render(request, 'addblog.html', {'blog_form': emp_blog_form})

    def post(self, request):
        post = request.POST.copy()
        post['user'] = f'{request.user.id}'
        request.POST = post
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            blog_form.save()
        else:
            return render(request, 'addblog.html', {'blog_form': blog_form})
        messages.success(request, "Blog Added Successfully!!")
        send_mail(request, "Blog Added Successfully!!")
        return HttpResponseRedirect('/blogs/')


@method_decorator(login_required, name='dispatch')
class UpdateBlog(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            messages.info(
                request, "The Page You Are Trying To Visit is Login Protected. ")
            return HttpResponseRedirect('/login/')
        blog = Blog.objects.get(pk=id)
        blog_form = BlogForm(instance=blog)
        return render(request, 'updateblog.html', {'blog_form': blog_form})

    def post(self, request, id):
        post = request.POST.copy()
        post['user'] = f'{request.user.id}'
        request.POST = post
        blog = Blog.objects.get(pk=id)
        blog_form = BlogForm(request.POST, instance=blog)
        if blog_form.is_valid():
            blog_form.save()
            send_mail(request,"Blog Updated Successfully!!")
            messages.success(request, "Blog Updated Successfully!!")
            return HttpResponseRedirect(f'/blogs/{id}/')
        else:
            blog_form = BlogForm(request.POST)
            return render(request, 'updateblog.html', {'blog_form': blog_form})


@method_decorator(login_required, name='dispatch')
class DeleteBlog(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            messages.info(
                request, "The Page You Are Trying To Visit is Login Protected. ")
            return HttpResponseRedirect('/login/')
        blog = Blog.objects.get(pk=id)
        blog.delete()
        send_mail(request,"Blog Deleted Successfully!!")
        messages.success(request, "Blog Deleted Successfully!!")

        return HttpResponseRedirect('/blogs/')
    
