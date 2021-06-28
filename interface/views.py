from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from api.models import ActivationCode
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    def get(self, request):
        return render(request, 'interface/login.html')

    def post(self, request):
        
        username = request.POST['username'].lower()
        pwd = request.POST['p1']
        
        user = authenticate(request, username=username, password=pwd)

        if user is not None:
            login(request, user)
            return redirect("interface:home")
        else:
            return render(request, 'interface/login.html', {'message':'Login Failed - Incorrect credentials'})

class SignupView(View):
    def get(self, request, code):
        try:
            code = ActivationCode.objects.get(code=code)
        except:
            return HttpResponseBadRequest("INVALID CODE")

        if code and code.check_validity() == False:
            return HttpResponseBadRequest("INVALID CODE")
        else:                
            return render(request, 'interface/signup.html', {'code':code})
        


    def post(self, request, code):
        
        code = request.POST['code']
        username = request.POST['username'].lower()
        pwd = request.POST['p1']
        pwd_conf = request.POST['p2']
        
        
        try:
            code_obj = ActivationCode.objects.get(code=code)
        except:
            return HttpResponseBadRequest("INVALID CODE")

        if code_obj and code_obj.check_validity() == False:
            return HttpResponseBadRequest("INVALID CODE")
        

        try:
            validators.validate_password(password=pwd, user=User)
        except Exception as e:
            return render(request, 'interface/signup.html', {'code':code, 'message': "Errors: " + str(e) + ".  Please try again."})

        if not pwd or not pwd_conf or pwd != pwd_conf:
            return render(request, 'interface/signup.html', {'code':code, 'message': 'Passwords must match! Please Try again'})

        try:
            u = User.objects.get(username=username)
            if u:
                return redirect("interface:login")
        except User.DoesNotExist:
            pass

        u = User(username=username)
        u.set_password(pwd)
        u.save()
        

        new_user = authenticate(request, username=username, password=pwd)
        if new_user is not None:
            login(request, new_user)
            return redirect("interface:home")
        else:
            return redirect("interface:login")

class PasswordView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'interface/password.html')

    def post(self, request):

        pwd = request.POST['p1']
        pwd_conf = request.POST['p2']

        try:
            validators.validate_password(password=pwd, user=User)
        except Exception as e:
            return render(request, 'interface/password.html', {'message': "Errors: " + str(e) + ".  Please try again."})

        if not pwd or not pwd_conf or pwd != pwd_conf:
            return render(request, 'interface/password.html', {'message': 'Passwords must match! Please Try again'})




        request.user.set_password(pwd)
        request.user.save()
        
        logout(request)
        new_user = authenticate(request, username=request.user.username.lower(), password=pwd)
        if new_user is not None:
            login(request, new_user)
            return redirect("interface:login")
        else:
            return redirect("interface:login")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("interface:login")



class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "interface/index.html")

class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        # if request.user.is_superuser():
        codes = ActivationCode.objects.all().order_by("-expiration_timestamp")
        return render(request, "interface/settings.html", {"codes":codes})

        



    
