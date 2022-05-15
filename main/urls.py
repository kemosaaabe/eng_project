from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/register', views.UserRegisterView.as_view(), name='register_user'),
    path('accounts/profile/change', views.ChangeUserInfoView.as_view(), name='change_user_info'),
    path('accounts/register_done', views.register_done, name='register_done'),
    path('register/password_change_form', PasswordChangeView.as_view(
        template_name='main/password_change_form.html'
    ), name='password_change'),
    path('register/password_change_done', PasswordChangeDoneView.as_view(
        template_name='main/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/profile', views.profile, name='profile'),
    path('modules/', views.show_modules, name='modules'),
    path('module/<int:pk>', views.show_module, name='module'),
    path('module/add', views.add_module, name='add_module'),
    path('module/delete/<int:pk>/', views.delete_module, name='delete_module'),
    path('module/edit/<int:pk>/', views.edit_module, name='edit_module'),
    path('tests/', views.show_tests, name='tests'),
    path('test/<int:pk>', views.show_test, name='test'),
    path('test/result/<int:test_id>', views.result_test, name='result_test'),
    path('profile/<int:pk>', views.user_profile, name='user_profile'),
]

