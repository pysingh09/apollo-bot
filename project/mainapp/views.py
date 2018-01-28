from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
import facebook

from mainapp.forms import UserForm
from mainapp.models import UserPage, BusinessAccountDetails
from mainapp import utils
from datetime import date


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

def store_details(user, data):
    # {'follows_count': 12, 'total_like_count': 1, 'total_comment_count': 0, 'followers_count': 0}
    create_new = False
    try:
        obj = BusinessAccountDetails.objects.filter(user=user).latest('date')
        if obj.date != date.today():
            if obj.follows_count != data['follows_count'] or obj.followers_count != data['followers_count'] or obj.total_like_count != data['total_like_count'] or obj.total_comment_count != data['total_comment_count']:
                # create new record here
                create_new = True

        print("obj", obj);
        # update current date record here
    except Exception as e:
        create_new = True
    
    BusinessAccountDetails.objects.create(
        user=user,
        follows_count=data['follows_count'],
        followers_count=data['followers_count'],
        total_like_count=data['total_like_count'],
        total_comment_count=data['total_comment_count'])


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
        user_pages = UserPage.objects.filter(user=user).first()
        if user_pages.business_account_id == None:
            res = utils.businessAccount(user_pages.page_id, token)
            business_account_id = res['instagram_business_account']['id']
            user_pages.business_account_id = business_account_id
            user_pages.save()
        response = utils.getFollowers(user_pages.business_account_id, token)
        
        card_row = {'total_like_count': 0, 'total_comment_count': 0, 'follows_count': 0, 'followers_count': 0}
        
        media_response = utils.mediaCounts(user_pages.business_account_id, token)
        for item in media_response['media']['data']:
            card_row['total_comment_count'] += item['comments_count']
            card_row['total_like_count'] += item['like_count']

        print("response", response)
        card_row['follows_count'] = response['follows_count']
        card_row['followers_count'] = response['followers_count']
        card_row['profile_url'] = media_response['profile_picture_url']
        card_row['user_name'] = media_response['username']
        # storing details in database
        store_details(user, card_row)

        context = {'pages': [user_pages], 'data': card_row}
        template = loader.get_template('dashboard.html')
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