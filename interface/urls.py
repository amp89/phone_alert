from django.urls import path

from interface import views

app_name = 'interface'

urlpatterns = [
        path('login/', views.LoginView.as_view(), name="login", ),
        path('accounts/login/', views.LoginView.as_view(), name="login", ),

        path('sign_up/<str:code>/', views.SignupView.as_view(), name="sign_up"),
        
        path('logout/', views.LogoutView.as_view(), name="logout", ),

        path('settings/', views.SettingsView.as_view(), name="settings"),
        
        path('password/', views.PasswordView.as_view(), name="password"),

        path('', views.HomeView.as_view(), name="home"),

        
    ]
