from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
import facebook

from mainapp.forms import UserForm


# Create your views here.
class HomePage(View):
    def get(self, request):
        # token = "EAAdQNiOzTR8BADZBus9Gg1oCvF1QjLcb5QXUJHpgDBIldbQzgVBsghmsCBz1zHqLCXYBrdJQLbY912MQMNM5mm0yyPM3f2uiuo437YYA7Ex6aIncCXXFJQLZAQhI5BSHelhwUqkFz4b8WVfxvMPoRg73EeZAm8s9nN1NHtORtvycZCN0NlctT5tavWzOkfrKaZAAe3C6EKQZDZD"
        # graph = facebook.GraphAPI(access_token=token, version="2.1")
        return render(request, 'mainapp/landing.html')


class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('index')


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
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(username=username, password=password)
        # if user is not None:
        #     if user.is_active:
        #         login(request, user)
        #         return redirect('index')
        #     else:
        #         return render(request, 'login.html', {'error_message': 'Invalid login'})
        return render(request, 'mainapp/login.html', {'error_message': 'Invalid login'})


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
        form = UserForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, 'mainapp/signup.html',context)

    def post(self, request):

        # form = UserForm(request.POST or None)
        # if form.is_valid():
        #     user = form.save(commit=False)
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        #     user.set_password(password)
        #     user.save()
        #     user = authenticate(username=username, password=password)
        #     if user is not None:
        #         if user.is_active:
        #             login(request, user)
        #             return redirect('index')
        context = {
            "form": form,
        }

        return render(request, 'mainapp/signup.html',context=context)

class Dashboard(LoginRequiredMixin, View):
        
    def get(self, request):
        context = {}
        template = loader.get_template('app/index.html')
        # return render(request,'mainapp/dashboard.html', {'msg_card':'','items':'','user':'user', 'status':'',
        #         'unfollow': 'unfollow_status'})
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