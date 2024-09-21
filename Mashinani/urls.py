from django.urls import path
from .views import (
    HomePage_View, Register_GroupView, Register_BankView, AddMemberView, MemberListView, MemberUpdateView, 
    MemberDeleteView, DashboardView, success, AdminSignUpView, AdminLoginView, GroupSignUpView, BankSignUpView,
    MemberSignUpView, GroupLoginView, BankLoginView, MemberLoginView, Group_DashboardView, Bank_DashboardView,
    Member_DashboardView
)

urlpatterns = [
    path('', HomePage_View.as_view(), name='home'),
    path('register/group/', Register_GroupView.as_view(), name='register-group'),
    path('register/bank/', Register_BankView.as_view(), name='register-bank'),
    path('add/member', AddMemberView.as_view(), name='add-member'),
    path('members/', MemberListView.as_view(), name='member-list'),
    path('update/member/',  MemberUpdateView.as_view(), name='member-update'),
    path('delete/member/', MemberDeleteView.as_view(), name='member-delete'),
    path('register/',AdminSignUpView.as_view(), name='admin-signup'),
    path('login/',AdminLoginView.as_view(), name='admin-login'),
    path('group/register/',GroupSignUpView.as_view(), name='group-signup'),
    path('group/login/',GroupLoginView.as_view(), name='group-login'),
    path('bank/register/',BankSignUpView.as_view(), name='bank-signup'),
    path('bank/login/',BankLoginView.as_view(), name='bank-login'),
    path('member/register/',MemberSignUpView.as_view(), name='member-signup'),
    path('member/login/',MemberLoginView.as_view(), name='member-login'),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('group/dashboard/',Group_DashboardView.as_view(), name='group-dashboard'),
    path('bank/dashboard/',Bank_DashboardView.as_view(), name='bank-dashboard'),
    path('member/dashboard/',Member_DashboardView.as_view(), name='member-dashboard'),
    path('success/', success, name='success'),   
]
