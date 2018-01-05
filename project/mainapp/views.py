from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
import facebook

from mainapp.forms import UserForm
from mainapp.models import UserPage
from mainapp import utils


# Create your views here.
class HomePage(View):
    def get(self, request):
        return render(request, 'mainapp/landing.html')


class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('login')


class Home(View):
    def get(self, request):
        return render(request, 'mainapp/landing.html')

class PrivacyPolicy(View):

    def get(self, request):
        return render(request, 'mainapp/privacy_policy.html')
        
class Login(View):
    def get(self, request):
        return render(request, 'app/login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username.lower(), password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return redirect('login')


class SignUp(View):
    def validate_data(self, request):
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if fname or lname or username or password or email is "":
            return ""

    def get(self, request):
        context = {
            'username': ''
        }
        template = loader.get_template('app/signup.html')
        return HttpResponse(template.render(context, request))

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not request.user.is_anonymous:
            print("in if")
            user = request.user
            user.username = username
            user.email = email
            user.set_password(password)
        else:
            print("in else")
            user = User()
            user.email = email
            user.username = username
            user.set_password(password)
        user.save()
        return redirect('dashboard')

class Dashboard(LoginRequiredMixin, View):
        
    def get(self, request):
        user = request.user
        if not user.has_usable_password():
            context = {
                'username': user.username
            }
            template = loader.get_template('app/signup.html')
            return HttpResponse(template.render(context, request))
        social = request.user.social_auth.get(provider='facebook')
        token = social.extra_data['access_token']
        res = utils.listUsersPage(token)
        pages = res['data']
        page_data = []
        for page in res['data']:
            page_data.append({'name': page['name'], 'id': page['id']})

            # storing page details in db
            obj = UserPage.objects.filter(user=user, page_id=page['id'])
            if not obj:
                new_page = UserPage()
                new_page.user = user
                new_page.page_name = page['name']
                new_page.page_id = page['id']
                new_page.save()

        user_pages = UserPage.objects.filter(user=user)
        context = {'pages': user_pages}
        template = loader.get_template('app/index.html')
        return HttpResponse(template.render(context, request))
        

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))