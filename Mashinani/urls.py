from django.urls import path
from .views import (
    HomePage_View, Register_GroupView, Register_BankView, RegistrationSuccessView, AddMemberView, MemberListView,
    MemberUpdateView,  MemberDeleteView, DashboardView, AdminSignUpView, AdminLoginView, GroupSignUpView, BankSignUpView,
    MemberSignUpView, GroupLoginView, BankLoginView, MemberLoginView, Group_DashboardView, Bank_DashboardView,
    Member_DashboardView, DefaultersView, DefaulterListView, DefaulterUpdateView, DefaulterDeleteView, AllocationView, 
    AllocationSuccessView, AllocationsView, ApplicationView, ApplicationSuccessView, RequestsView, DisbursementView,
    DisbursementSuccessView, LoanPaymentView, PaymentSuccessView, MemberLoansView, BankLoansView, BankSentMessagesView,
    BankRcvdMessagesView, MemberSentMessagesView,   MemberRcvdMessagesView, GroupFAQsView, BankFAQsView, MemberFAQsView, 
    LogoutView, ResetPasswordView, ResetPasswordConfirmView, PasswordResetSuccessView
)

urlpatterns = [
    path('', HomePage_View.as_view(), name='home'),
    path('register/group/', Register_GroupView.as_view(), name='register-group'),
    path('register/bank/', Register_BankView.as_view(), name='register-bank'),
    path('success/<str:username>/', RegistrationSuccessView.as_view(), name='success'),
    path('defaulters/', DefaulterListView.as_view(), name='defaulter-list'),
    path('defaulters/add/', DefaultersView.as_view(), name='add-defaulter'),
    path('defaulters/update/<int:pk>/', DefaulterUpdateView.as_view(), name='defaulter-update'),
    path('defaulters/delete/<int:pk>/', DefaulterDeleteView.as_view(), name='defaulter-delete'),
    path('add/member', AddMemberView.as_view(), name='add-member'),
    path('members/', MemberListView.as_view(), name='member-list'),
    path('update/member/<int:pk>/',  MemberUpdateView.as_view(), name='member-update'),
    path('delete/member/<int:pk>/', MemberDeleteView.as_view(), name='member-delete'),
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
    path('bank/allocation/', AllocationView.as_view(), name='bank-allocation'),
    path('allocation/success/<str:allocation_no>/', AllocationSuccessView.as_view(), name='allocation-success'),
    path('allocations/', AllocationsView.as_view(), name='allocations-list'),
    path('application/<str:allocation_no>/', ApplicationView.as_view(), name='loan-application'),
    path('application/success/<str:application_no>/', ApplicationSuccessView.as_view(), name='application-success'), 
    path('requests/', RequestsView.as_view(), name='applications-list'),
    path('disbursement/<str:application_no>/', DisbursementView.as_view(), name='loan-disbursement'),
    path('disbursement/success/<str:transaction_no>/', DisbursementSuccessView.as_view(), name='disbursement-success'),
    path('member/loans/', MemberLoansView.as_view(), name='member-loans-list'),
    path('bank/loans/', BankLoansView.as_view(), name='bank-loans-list'),
    path('payment/<str:transaction_no>/', LoanPaymentView.as_view(), name='loan-payment'),
    path('payment/success/<str:transaction_no>/', PaymentSuccessView.as_view(), name='payment-success'),
    path('member/sent/messages/', MemberSentMessagesView.as_view(), name='member-sent-messages-list'),
    path('member/received/messages/', MemberRcvdMessagesView.as_view(), name='member-received-messages-list'),
    path('bank/sent/messages/', BankSentMessagesView.as_view(), name='bank-sent-messages-list'),
    path('bank/received/messages/', BankRcvdMessagesView.as_view(), name='bank-received-messages-list'),
    path('group/frequently/asked/questions/', GroupFAQsView.as_view(), name='group-faqs'),
    path('bank/frequently/asked/questions/', BankFAQsView.as_view(), name='bank-faqs'),
    path('member/frequently/asked/questions/', MemberFAQsView.as_view(), name='member-faqs'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('password-reset-success/', PasswordResetSuccessView.as_view(), name='password-reset-success'),
]
