from .utils import *
from .models import (
    County, Constituency, Ward, Account, Group, Guarantor, Bank, Member, System_User, Allocation, Application, 
    Disbursement, Loan, Message, Loanee, Defaulter, PasswordResetToken, Contact
)

from .forms import (
   GroupForm, BankForm, MemberForm, AdminSignUpForm, BankSignUpForm, GroupSignUpForm, MemberSignUpForm, LoginForm,
   DefaulterForm, PaymentForm, ApplicationForm, DisbursementForm, AllocationForm, PasswordResetForm , ResetForm, 
   ContactForm 
)
from django import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, DeleteView, ListView, TemplateView, FormView

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.views import View
from .models import PasswordResetToken, System_User
from .forms import PasswordResetForm

from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta


from django.db import models
from django.db.models import DecimalField
from django.core.exceptions import ValidationError
from django.db.models import Sum
from decimal import Decimal
from django import forms
import string
import random
from datetime import datetime
import time
import hashlib
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

class ResetPasswordView(View):
    template_name = 'reset_password.html'
    form_class = PasswordResetForm
    success_redirect_url = 'home'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = System_User.objects.filter(username=username).first()
            if user:
                try:
                    # Generate a unique token
                    token = get_random_string(length=32)
                    # Save the token to the database
                    PasswordResetToken.objects.create(username=user, token=token)
                    # Generate the correct reset link
                    
                    email = System_User.objects.filter(username=user).first()
                    reset_link = request.build_absolute_uri(f'/Linker/reset-password/{token}/')
                    # Send password reset email
                    send_mail(
                        'Reset Your Password',
                        f'Click the link to reset your password: {reset_link}',
                        settings.EMAIL_HOST_USER,
                        [email.email_address],
                        fail_silently=False,
                    )
                    return redirect(self.success_redirect_url)
                except Exception as e:
                    error_message = f"An error occurred: {str(e)} or Email Address does not exist in our records"
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            else:
                error_message = "Email Address does not exist in our records."
                return render(request, self.template_name, {'form': form, 'error_message': error_message})

        return render(request, self.template_name, {'form': form})


class ResetPasswordConfirmView(View):
    template_name = 'reset_password_confirm.html'
    invalid_token_template = 'reset_password_token_invalid.html'
    form_class = ResetForm

    def get(self, request, token):
        # Check if the token exists in the database
        password_reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not password_reset_token or password_reset_token.is_expired():
            # Token is invalid or expired, handle appropriately
            return render(request, self.invalid_token_template)

        # Initialize the form for GET requests
        form = self.form_class()

        # Render the form in the template
        return render(request, self.template_name, {'form': form, 'token': token})

    def post(self, request, token):
        # Check if the token exists in the database
        password_reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not password_reset_token or password_reset_token.is_expired():
            # Token is invalid or expired, handle appropriately
            return render(request, self.invalid_token_template)

        # Update the user's password
        form = self.form_class(request.POST)
        if form.is_valid():
            password_hash = form.cleaned_data['password_hash']
            #borrower_id = borrower.national_id
            #member_account = get_object_or_404(GroupMember, national_id=borrower_id)
            #borrower_account = get_object_or_404(Account, account_no=member_account.account)

            reset = get_object_or_404(PasswordResetToken, token=password_reset_token)
            user = get_object_or_404(System_User, username=reset.username)
            password = user.password_hash
            password.delete()
            user = form.save(commit=False)
            user.set_password(password_hash)
            user.save()
            # Delete the used token
            password_reset_token.delete()

            return redirect('password-reset-success')

        # If form is invalid, render the form again with errors
        return render(request, self.template_name, {'form': form, 'token': token})


class PasswordResetSuccessView(View):
    template_name = 'password_reset_success.html'

    def get(self, request):
        return render(request, self.template_name)

class HomePage_View(View):
    template_name = 'index.html'
    
    def get(self,request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email_address = form.cleaned_data['email_address']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Create the account if all checks pass
            user_message = form.save(commit=False)
            user_message.full_name = full_name
            user_message.email_address = email_address
            user_message.subject = subject
            user_message.message = message
            user_message.save()
            return redirect('home')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
    
class RegistrationSuccessView(TemplateView):
    template_name = 'register_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username', 'default_value')  # Safely access username
        return context
    
class LogoutView(View):

    def get(self, request, *args, **kwargs):
        django_logout(request)
        return redirect('home')    
class AdminSignUpView(View):
    template_name = 'admin_signup.html'

    def get(self, request):
        form = AdminSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AdminSignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']
            
            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.role_name = "Admin"
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('admin-login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        
        
class GroupSignUpView(View):
    template_name = 'group_signup.html'

    def get(self, request):
        form = GroupSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GroupSignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']
            
            # Check if username exists in the Bank model
            if not Group.objects.filter(username=username).exists():
                # Add error message to the form
                form.add_error('username', "The username does not exist. Please register as a group first.")
                return render(request, self.template_name, {'form': form})
            
            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.role_name = "Group"
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('group-login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        
class BankSignUpView(View):
    template_name = 'bank_signup.html'

    def get(self, request):
        form = BankSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BankSignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']

            # Check if username exists in the Bank model
            if not Bank.objects.filter(username=username).exists():
                # Add error message to the form
                form.add_error('username', "The username does not exist. Please register as a bank first.")
                return render(request, self.template_name, {'form': form})

            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.role_name = "Bank"
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('bank-login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})

        
class MemberSignUpView(View):
    template_name = 'member_signup.html'

    def get(self, request):
        form = MemberSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MemberSignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password_hash = form.cleaned_data['password_hash']
           
            # Check if username exists in the Bank model
            if not Member.objects.filter(username=username).exists():
                # Add error message to the form
                form.add_error('username', "The username does not exist. Please register as a member first.")
                return render(request, self.template_name, {'form': form})
            
            # Check if username already exists in System_User model
            if System_User.objects.filter(username=username).exists():
                form.add_error('username', "This username has already been used in the system!")
                return render(request, self.template_name, {'form': form})

            # Create the account if all checks pass
            new_account = form.save(commit=False)
            new_account.role_name = "Member"
            new_account.set_password(password_hash)
            new_account.save()
            return redirect('member-login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        
class AdminLoginView(View):
    template_name = 'admin.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    
            user = System_User.objects.filter(username=username).first()
            if user and user.check_password(password):
                # Authentication successful
                request.session['username'] = user.username  # Store username in session
                return redirect(reverse('dashboard'))
            else:
                # Authentication failed
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})
        
class GroupLoginView(View):
    template_name = 'group_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if the username exists in the Lender model with lender_type 'group'
            group = Group.objects.filter(username=username).first()
            if group:
                user = System_User.objects.filter(username=username).first()
                if user and user.check_password(password):
                    # Authentication successful
                    request.session['username'] = user.username  # Store username in session
                    return redirect(reverse('group-dashboard'))
                else:
                    # Authentication failed
                    error_message = 'Wrong Username or Password'
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            else:
                # Username does not exist in the Lender model with lender_type 'group'
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})

class BankLoginView(View):
    template_name = 'bank_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if the username exists in the bank model
            bank = Bank.objects.filter(username=username).first()
            if bank:
                user = System_User.objects.filter(username=username).first()
                if user and user.check_password(password):
                    # Authentication successful
                    request.session['username'] = user.username  # Store username in session
                    return redirect(reverse('bank-dashboard'))
                else:
                    # Authentication failed
                    error_message = 'Wrong Username or Password'
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            else:
                # Username does not exist in the Lender model with lender_type 'group'
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})

class MemberLoginView(View):
    template_name = 'member_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if the username exists in the member model
            member = Member.objects.filter(username=username).first()
            if member:
                user = System_User.objects.filter(username=username).first()
                if user and user.check_password(password):
                    # Authentication successful
                    request.session['username'] = user.username  # Store username in session
                    return redirect(reverse('member-dashboard'))
                else:
                    # Authentication failed
                    error_message = 'Wrong Username or Password'
                    return render(request, self.template_name, {'form': form, 'error_message': error_message})
            else:
                # Username does not exist in the Lender model with lender_type 'group'
                error_message = 'Wrong Username or Password'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        else:
            error_message = 'Wrong Username or Password'
            return render(request, self.template_name, {'form': form, 'error_message': error_message})

                
        
class DashboardView(View):
    def get(self, request):
        banks = Bank.objects.all()
        groups = Group.objects.all()
        defaulters = Defaulter.objects.all()
        constituencies = Constituency.objects.all()
        wards = Ward.objects.all()
        guarantors = Guarantor.objects.all()
            
        context = {
            'banks': banks,
            'groups': groups,
            'defaulters': defaulters,
            'constituencies': constituencies,
            'wards': wards,
            'guarantors': guarantors,
        }
        
        username = request.session.get('username')
        if not username:
            return redirect('admin-login')  # Redirect to login if username is not in session
            
        try:
            user = System_User.objects.get(username=username)
        except System_User.DoesNotExist:
            return redirect('admin-login')
        
        # Add the 'user' object to the context
        context['user'] = user

        # Pass the full context to the template
        return render(request, 'dashboard.html', context)

    
class Group_DashboardView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('group-login')  # Redirect to login if username is not in session

        try:
            user = System_User.objects.get(username=username)
            banks = Bank.objects.all()
            groups = Group.objects.all()
            defaulters = Defaulter.objects.all()
            constituencies = Constituency.objects.all()
            wards = Ward.objects.all()
            guarantors = Guarantor.objects.all()
            
            context = {
                'banks': banks,
                'groups': groups,
                'defaulters': defaulters,
                'constituencies': constituencies,
                'wards': wards,
                'guarantors': guarantors,
            }
            
        except System_User.DoesNotExist:
            return redirect('group-login')
        
        context['user'] = user

        return render(request, 'group_dashboard.html', context)
    
class Bank_DashboardView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')  # Redirect to login if username is not in session

        try:
            user = System_User.objects.get(username=username)
            banks = Bank.objects.all()
            groups = Group.objects.all()
            defaulters = Defaulter.objects.all()
            constituencies = Constituency.objects.all()
            wards = Ward.objects.all()
            guarantors = Guarantor.objects.all()
            
            context = {
                'banks': banks,
                'groups': groups,
                'defaulters': defaulters,
                'constituencies': constituencies,
                'wards': wards,
                'guarantors': guarantors,
            }
            
        except System_User.DoesNotExist:
            return redirect('bank-login')
        
        context['user'] = user

        return render(request, 'bank_dashboard.html', context)
    
class Member_DashboardView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('member-login')  # Redirect to login if username is not in session

        try:
            user = System_User.objects.get(username=username)
            banks = Bank.objects.all()
            groups = Group.objects.all()
            defaulters = Defaulter.objects.all()
            constituencies = Constituency.objects.all()
            wards = Ward.objects.all()
            guarantors = Guarantor.objects.all()
            
            context = {
                'banks': banks,
                'groups': groups,
                'defaulters': defaulters,
                'constituencies': constituencies,
                'wards': wards,
                'guarantors': guarantors,
            }
            
        except System_User.DoesNotExist:
            return redirect('member-login')
        
        context['user'] = user

        return render(request, 'member_dashboard.html', context)
 
class Register_GroupView(View):
    template_name = 'register_group.html'

    def get(self, request):
        form = GroupForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = GroupForm(request.POST)
        if form.is_valid():
            group_no = form.cleaned_data['group_no']
            group_name = form.cleaned_data['group_name']
            email_address = form.cleaned_data['email_address']
            phone_number = form.cleaned_data['phone_number']
            ward = form.cleaned_data['ward']
            guarantor = form.cleaned_data['guarantor']
            account = form.cleaned_data['account']            
            
            if Group.objects.filter(email_address=email_address).exists():
                form.add_error(None, "This Group already exist !")
                return render(request, self.template_name, {'form': form})

            # Proceed with registration
            group = form.save(commit=False)
            group.username = email_address
            username = group.username
            group.save()
            
            # Create and save the account
            account = Account(
                account_no=account,
                account_name=f'{group_name}',
                account_bal=0.00,
            )
            account.save()

            return redirect('success', kwargs={'username': username})
        else:
            return render(request, self.template_name, {'form': form})
        
        
class Register_BankView(View):
    template_name = 'register_bank.html'

    def get(self, request):
        form = BankForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = BankForm(request.POST)
        if form.is_valid():
            bank_no = form.cleaned_data['bank_no']
            bank_name = form.cleaned_data['bank_name']
            email_address = form.cleaned_data['email_address']
            phone_number = form.cleaned_data['phone_number']
            constituency = form.cleaned_data['constituency']
            account = form.cleaned_data['account']            
            
            if Bank.objects.filter(email_address=email_address).exists():
                form.add_error(None, "This Bank already exist !")
                return render(request, self.template_name, {'form': form})

            # Proceed with registration
            bank = form.save(commit=False)
            bank.username = email_address
            username = bank.username
            bank.save()

            # Create and save the account
            account = Account(
                account_no=account,
                account_name=f'{bank_name}',
                account_bal=0.00,
            )
            account.save()
            
            return redirect('success', kwargs={'username': username})
        else:
            return render(request, self.template_name, {'form': form})
        
class GroupFAQsView(View):
    template_name = 'group_faqs.html'

    def get(self, request):
        faqs = [
            {
                "question": "What is KIA Parcels?",
                "answer": "KIA Parcels is a parcel management platform developed in July 2024 for Kisumu International Airport by Kasuku Tech Junction."
            },
            {
                "question": "How can I send a parcel?",
                "answer": "To send a parcel, simply navigate to the 'Send Parcel' section on our platform, fill in the necessary details, and follow the instructions."
            },
            {
                "question": "How can I track my sent parcels?",
                "answer": "You can track your sent parcels by visiting the 'Sent Parcels' section and entering your tracking number."
            },
            {
                "question": "How can I receive a parcel?",
                "answer": "You will be notified when a parcel addressed to you arrives. You can then visit the 'Received Parcels' section to check its status."
            },
            {
                "question": "How do I contact support?",
                "answer": "For any assistance, please visit our 'Contact Us' page where you can find our contact details and a form to send us a message."
            },
        ]
        return render(request, self.template_name, {'faqs': faqs}) 
    
class BankFAQsView(View):
    template_name = 'bank_faqs.html'

    def get(self, request):
        faqs = [
            {
                "question": "What is KIA Parcels?",
                "answer": "KIA Parcels is a parcel management platform developed in July 2024 for Kisumu International Airport by Kasuku Tech Junction."
            },
            {
                "question": "How can I send a parcel?",
                "answer": "To send a parcel, simply navigate to the 'Send Parcel' section on our platform, fill in the necessary details, and follow the instructions."
            },
            {
                "question": "How can I track my sent parcels?",
                "answer": "You can track your sent parcels by visiting the 'Sent Parcels' section and entering your tracking number."
            },
            {
                "question": "How can I receive a parcel?",
                "answer": "You will be notified when a parcel addressed to you arrives. You can then visit the 'Received Parcels' section to check its status."
            },
            {
                "question": "How do I contact support?",
                "answer": "For any assistance, please visit our 'Contact Us' page where you can find our contact details and a form to send us a message."
            },
        ]
        return render(request, self.template_name, {'faqs': faqs})
    
class MemberFAQsView(View):
    template_name = 'member_faqs.html'

    def get(self, request):
        faqs = [
            {
                "question": "What is KIA Parcels?",
                "answer": "KIA Parcels is a parcel management platform developed in July 2024 for Kisumu International Airport by Kasuku Tech Junction."
            },
            {
                "question": "How can I send a parcel?",
                "answer": "To send a parcel, simply navigate to the 'Send Parcel' section on our platform, fill in the necessary details, and follow the instructions."
            },
            {
                "question": "How can I track my sent parcels?",
                "answer": "You can track your sent parcels by visiting the 'Sent Parcels' section and entering your tracking number."
            },
            {
                "question": "How can I receive a parcel?",
                "answer": "You will be notified when a parcel addressed to you arrives. You can then visit the 'Received Parcels' section to check its status."
            },
            {
                "question": "How do I contact support?",
                "answer": "For any assistance, please visit our 'Contact Us' page where you can find our contact details and a form to send us a message."
            },
        ]
        return render(request, self.template_name, {'faqs': faqs})         
        
class AddMemberView(View):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('group_login')  # Redirect to login if username is not in session

        try:
            user = System_User.objects.get(username=username)
            group = Group.objects.get(username=user)
        except (System_User.DoesNotExist, Group.DoesNotExist):
            return redirect('home')

        form = MemberForm()
        context = {
            'user': user,
            'group': group,
            'form': form,
        }
        return render(request, 'add_member.html', context)

    def post(self, request):
        form = MemberForm(request.POST)
        username = request.session.get('username')
        if not username:
            return redirect('home')

        try:
            user = System_User.objects.get(username=username)
            group = Group.objects.get(username=user)
        except (System_User.DoesNotExist, Group.DoesNotExist):
            return redirect('home')

        if form.is_valid():
            national_id_no = form.cleaned_data.get('national_id_no')
            email_address = form.cleaned_data.get('email_address')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = form.cleaned_data.get('phone_number')
            dob = form.cleaned_data.get('dob')
            gender = form.cleaned_data.get('gender')
            grp_worth = form.cleaned_data.get('grp_worth')
            account_no = form.cleaned_data.get('account_no')
            approved = form.cleaned_data.get('approved')
            
            if Defaulter.objects.filter(national_id_no=national_id_no).exists():
                return render(request, 'add_member.html', {
                    'form': form,
                    'error_message': 'This member is listed as a defaulter and cannot be added to the group.'
                })

            try:
                member = form.save(commit=False)
                member.username = email_address
                member.group_no = group 
                member.loan_status = 'OPEN'
                member.loan_bal = 0.00
                member.save()
                
                # Create and save the account
                account = Account(
                    account_no=account_no,
                    account_name=f'{first_name}  {last_name}',
                    account_bal=0.00,
                )
                account.save()

                return render(request, 'add_member.html', {
                    'form': MemberForm(),
                    'first_name': member.first_name,
                    'success_message': f'{member.first_name} added successfully.'
                })
            except Exception as e:
                return render(request, 'add_member.html', {
                    'form': form,
                    'error_message': 'An error occurred while adding the member. Please try again.'
                })
        else:
            # Added detailed form errors for debugging
            print(form.errors)  # Print form errors to console or log them for debugging

        return render(request, 'add_member.html', {
            'form': form,
            'error_message': 'Form Invalid. Errors: {}'.format(form.errors)
        })

class MemberListView(ListView):
    template_name = 'member_list.html'
    context_object_name = 'members'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('group-login')  # Redirect to login if username is not in session
        try:
            # Query the user from the database using the username
            user = System_User.objects.get(username=username)
            group = Group.objects.get(username=user)
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('home')
        except Group.DoesNotExist:
            # Handle the case where the group does not exist
            return redirect('home')
        group_no = group.group_no

        # Retrieve group members
        members = Member.objects.filter(group_no=group_no)

        return render(request, self.template_name, {'members': members})


class MemberUpdateView(UpdateView):
    model = Member
    fields = ['national_id_no', 'email_address', 'username', 'first_name', 'last_name', 'phone_number', 'dob', 'gender', 'group_no', 'grp_worth', 'account_no', 'approved', 'loan_status', 'loan_bal']
    widgets = {
            'gender': forms.RadioSelect(choices=Member.GENDER_CHOICES),
        }
    template_name = 'member_update.html'
    success_url = reverse_lazy('member-list')


class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'member_delete.html'
    success_url = reverse_lazy('member-list')



class DefaultersView(View):
    template_name = 'defaulter.html'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')  # Redirect to the bank dashboard if lender_no is not in session
        
        bank = Bank.objects.filter(username=username)
        bank_no = bank.bank_no 
        form = DefaulterForm(initial={'bank_no': bank_no})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')  # Redirect to the bank dashboard if lender_no is not in session

        form = DefaulterForm(request.POST)

        if form.is_valid():
            national_id_no = form.cleaned_data['national_id_no']
            amount_owed = form.cleaned_data['amount_owed']

            if Defaulter.objects.filter(national_id_no=national_id_no, bank_no=bank_no).exists():
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': 'Defaulter already exists. Please try again.'
                })

            defaulter = form.save(commit=False)
            defaulter.submission_date = datetime.now() 
            defaulter.bank_no = bank_no  
            defaulter.save()

            return redirect('bank-dashboard') 

        return render(request, self.template_name, {'form': form})


class DefaulterListView(View):
    template_name = 'defaulters_list.html'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')
        bank = get_object_or_404(Bank, username=username)
        bank_no = bank.bank_no 
        defaulters = Defaulter.objects.filter(bank_no=bank_no)
        return render(request, self.template_name, {'defaulters': defaulters})



class DefaulterUpdateView(View):
    template_name = 'defaulter_update.html'

    def get(self, request, pk):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')  # Redirect to the bank dashboard if lender_no is not in session
        
        bank = get_object_or_404(Bank, username=username)
        bank_no = bank.bank_no
        defaulter = get_object_or_404(Defaulter, pk=pk)
        if defaulter.bank_no != bank_no:
            messages.error(request, 'You have no privilege to update the details of this defaulter.')
            return redirect('defaulter-list')  # Redirect to the defaulter list if lender_no does not match

        form = DefaulterUpdateForm(instance=defaulter)
        return render(request, self.template_name, {'form': form, 'defaulter': defaulter})

    def post(self, request, pk):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')  # Redirect to the bank dashboard if lender_no is not in session
        
        bank = get_object_or_404(Bank, username=username)
        bank_no = bank.bank_no
        defaulter = get_object_or_404(Defaulter, pk=pk)
        if defaulter.bank_no != bank_no:
            messages.error(request, 'You have no privilege to update the details of this defaulter.')
            return redirect('defaulter_list')  # Redirect to the defaulter list if lender_no does not match

        form = DefaulterUpdateForm(request.POST, instance=defaulter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Defaulter details successfully updated.')
            return redirect('defaulter-list')  # Redirect to the defaulter list after updating

        return render(request, self.template_name, {'form': form, 'defaulter': defaulter})



class DefaulterDeleteView(View):

    def post(self, request, pk):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')  # Redirect to the bank dashboard if lender_no is not in session
        
        bank = get_object_or_404(Bank, username=username)
        bank_no = bank.bank_no
        defaulter = get_object_or_404(Defaulter, pk=pk)
        if defaulter.bank_no != bank_no:
            messages.error(request, 'You have no privilege to delete this defaulter.')
            return redirect('defaulters-list')  # Redirect to the defaulter list if bank_no does not match

        defaulter.delete()
        messages.success(request, 'Defaulter successfully deleted.')
        return redirect('defaulters-list')  # Redirect to the defaulter list after deleting


class AllocationView(View):
    template_name = 'allocation.html'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank-login') 

        bank = get_object_or_404(Bank, username=username)
        bank_no = bank.bank_no
        form = AllocationForm(initial={'bank_no': bank_no})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank_login') 

        bank = get_object_or_404(Bank, username=username)
        bank_no = bank.bank_no
        form = AllocationForm(request.POST)

        if form.is_valid():
            allocation_no = unique_allocation_number()
            amount = form.cleaned_data['amount']
            allocation_date = datetime.now()  # Get current date and time

            # Fetch the lender and their account balance
            try:
                bank = Bank.objects.get(bank_no=bank_no)
                account = Account.objects.get(account_no=bank.account.account_no)
                account_balance = account.account_bal
            except Bank.DoesNotExist:
                return redirect('bank-dashboard')
            except Bank.DoesNotExist:
                return redirect('bank-dashboard')

            # Ensure the amount is 2000 less than the account balance
            if amount > (account_balance - 2000):
                return render(request, self.template_name, {
                    'form': form,
                    'allocation_no': allocation_no,
                    'error_message': f'The allocated amount must be less than {account_balance - 2000}.'
                })

            # Create and save the allocation
            allocation = form.save(commit=False)
            allocation.allocation_no = allocation_no  # Assign the generated allocation number
            allocation.allocation_date = allocation_date  # Assign current date and time
            allocation.bank_no = bank_no  # Assign lender_no from session
            allocation.save()
            
            return redirect('allocation-success', {'allocation_no': allocation_no})
        

        else:
            print(form.errors)  # Print form errors to console or log them for debugging

            # If the form is not valid, return the template with the form
            return render(request, self.template_name,  {
                'form': AllocationForm(),
                'allocation_no': allocation_no,
                'error_message': 'Form Invalid. Errors: {}'.format(form.errors)
            })
            
            
class AllocationSuccessView(TemplateView):
    template_name = 'allocation_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocation_no'] = self.kwargs.get('allocation_no', 'default_value')  # Safely access username
        return context
    
    
class AllocationsView(ListView):
    model = Allocation
    template_name = 'allocations_list.html'
    context_object_name = 'allocations'
    
class ApplicationView(FormView):
    form_class = ApplicationForm
    template_name = 'application.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        allocation_no = self.kwargs['allocation_no']
        
        # Retrieve national_id_no from session
        username = self.request.session.get('username', None)
        member = get_object_or_404(Member, username=username)
        national_id_no = member.national_id_no
        
        kwargs['initial'] = {
            'allocation_no': allocation_no,
            'application_no': unique_application_number(),
            'application_date': timezone.now().date(),
            'national_id_no': national_id_no  # Add borrower_no to initial data
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allocation_no'] = self.kwargs['allocation_no']
        
        # Add borrower_no to context
        username = self.request.session.get('username', None)
        member = get_object_or_404(Member, username=username)
        context['national_id_no'] = member.national_id_no
        
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        allocation_no = self.kwargs['allocation_no']
        application_no = unique_application_number()
        username = self.request.session.get('username', None)
        member = get_object_or_404(Member, username=username)
        national_id_no = member.national_id_no

        
        group_no = member.group_no.group_no if hasattr(member.group_no, 'group_no') else member.group_no  # Ensure this is fetching the correct attribute
        member_count = Member.objects.filter(group_no=member.group_no).count()

        


        # Fetch Group object related to group_no
        group = get_object_or_404(Group, group_no=group_no)

        # Fetch Account object related to group's account
        account = get_object_or_404(Account, account_no=group.account.account_no)
        total_allocations = 10
        grp_worth = account.account_bal
        account_n = member.account_no
        member_acc = get_object_or_404(Account, account_no=account_n)
        member_bal = member_acc.account_bal
        # Additional logic you have in your form_valid method
        age = member.calculate_age()
        gender = member.gender
        membgrp_worth = member.grp_worth
        
        # Check if the member is approved
        if member.approved != Member.YES:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': 'This group member is not approved for a loan.'
            })
        
        # Assign account balance to member_balance
        member_balance = account.account_bal
        
        allocation = get_object_or_404(Allocation, allocation_no=allocation_no)
        
        # Fetch Lender object based on lender_no from Allocation
        bank = get_object_or_404(Bank, bank_no=allocation.bank_no)

        # Calculate the total applied amount for the allocation_no
        total_applied_amount = Application.objects.filter(allocation_no=allocation.allocation_no).aggregate(total=models.Sum('loan_amount'))['total'] or 0
        remaining_amount = allocation.amount - total_applied_amount

        # Check if the loan amount to be applied is less than or equal to the remaining amount
        loan_amount = form.cleaned_data['loan_amount']
        if loan_amount > remaining_amount:
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_message': f'The loan amount exceeds the remaining allocation amount of {remaining_amount}.'
            })
            
        # Test MachineLearningModel class
        ml_model = MachineLearningModel()
        mse, r2 = ml_model.accuracy()
        loan_proposal = LoanProposal()
        #loan_proposal.data_retrieval('Mary', age, 'Male', member_bal, member_count, 300000, 3500, 7, loan_amount)
        loan_proposal.data_retrieval('Mary', age, gender, member_bal, member_count, grp_worth, membgrp_worth, total_allocations, loan_amount)
        prediction_result = loan_proposal.data_preparation()
        result = float(f"{float(prediction_result):.2f}")
        # Assign form data to the application instance
        application = form.save(commit=False)
        application.allocation_no = allocation_no
        application.application_no = application_no
        application.application_date = timezone.now().date()
        application.proposed_amount = result  # Assign the loan amount
        application.national_id_no = national_id_no  # Correctly assign the borrower object
        
        
        # Check if the member has any unsettled loans with a balance above 0   
        loanee = get_object_or_404(Loanee, national_id_no=national_id_no)    
        if loanee.approved == 'no':
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_application_no': application_no,
                'error_message': 'You already have unsettled loan(s). Please settle your loan(s) first!'
            })
            
        if loanee.applied == 'yes':
            return render(self.request, self.template_name, {
                'form': form,
                'allocation_no': allocation_no,
                'error_application_no': application_no,
                'error_message': 'You already have an hanging application. Please be patient, Your Loan will be Disbursed soon!'
            })
        
        # Save the form instance
        application.save()
        
        # Create and save the message
        message_no = self.generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=member.username,  # Borrower's username
            recipient_username=bank.username,  # Lender's username
            message_name='Loan Application Submitted',
            message_description=f'Loan Application of Application Number {application_no} has been submitted.',
            message_date=timezone.now().date()
        )
        message.save()
        
        return redirect('application-success', {'application_no': application_no})

    def form_invalid(self, form):
        allocation_no = self.kwargs['allocation_no']
        print(form.errors)  # Print form errors to console or log them for debugging
        return render(self.request, self.template_name, {
            'form': form,
            'allocation_no': allocation_no,
            'error_message': f'Form Invalid. Errors: {form.errors}',
        })

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no
            
class ApplicationSuccessView(TemplateView):
    template_name = 'application_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application_no'] = self.kwargs.get('application_no', 'default_value')  # Safely access username
        return context
            
class RequestsView(ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        # Get the lender_no from the session
        username = self.request.session.get('username')
        bank = get_object_or_404(Bank, username=username)
        bank_no = bank.bank_no

        if bank_no:
            # Get allocations related to the lender_no
            allocations = Allocation.objects.filter(bank_no=bank_no)
            
            # Extract allocation numbers
            allocation_numbers = allocations.values_list('allocation_no', flat=True)

            # Get applications related to these allocations and exclude those with disbursements
            applications_without_disbursement = Application.objects.filter(
                allocation_no__in=allocation_numbers
            ).exclude(
                application_no__in=Disbursement.objects.values_list('application_no', flat=True)
            )
            
            return applications_without_disbursement
        else:
            # If lender_no is not in the session, handle appropriately
            return Application.objects.none()  # No applications listed if lender_no is not in session
        
class DisbursementView(FormView):
    form_class = DisbursementForm
    template_name = 'disbursement.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        application_no = self.kwargs['application_no']
        kwargs['initial'] = {
            'application_no': application_no,
            'transaction_no': unique_transaction_number(),
            'disbursement_date': datetime.now().date()
        }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application_no'] = self.kwargs['application_no']
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        application_no = self.kwargs['application_no']
        transaction_no = unique_transaction_number()

        application = get_object_or_404(Application, application_no=application_no)
        allocation = get_object_or_404(Allocation, allocation_no=application.allocation_no)
        bank_no = allocation.bank_no
        national_id_no = application.national_id_no
        bank = Bank.objects.get(bank_no=bank_no)

        member = get_object_or_404(Member, national_id_no=national_id_no)

        # Get the proposed amount from the Application table
        proposed_amount = application.proposed_amount

        # Check if the entered amount is valid
        entered_amount = form.cleaned_data.get('disbursed_amount')
        if entered_amount > proposed_amount:
            entered_amount = proposed_amount
            
        if entered_amount < 100.00:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': form.cleaned_data.get('transaction_no', None),
                'error_message': 'You can not Disburse Amount less than Kshs 100'
            })
        
        member_account = Account.objects.get(account_no=member.account_no)

        # Fetch the bank's account
        bank_account = get_object_or_404(Account, account_no=bank.account.account_no)

        # Check if the bank's account has sufficient balance
        if bank_account.account_bal < entered_amount:
            return render(self.request, self.template_name, {
                'form': form,
                'application_no': application_no,
                'error_transaction_no': form.cleaned_data.get('transaction_no', None),
                'error_message': f'Insufficient account balance. Current balance is {bank_account.account_bal}.'
            })

        # Update lender's account balance
        bank_account.account_bal -= entered_amount
        bank_account.save()

        # Update borrower's account balance
        member_account.account_bal += entered_amount
        member_account.save()

        disbursed_amount = entered_amount
        # Save the disbursement if everything is valid
        form.instance.disbursed_amount = disbursed_amount
        form.instance.application_no = application_no
        form.instance.transaction_no = transaction_no
        form.instance.national_id_no = national_id_no
        form.instance.loan_duration_months = 12
        form.instance.disbursement_date = datetime.now().date()

        form.save()
        
        loanee = get_object_or_404(Loanee, national_id_no=national_id_no)
        loanee.approved = 'no'
        loanee.applied = 'no'
        loanee.save()

        # Create and save the message
        message_no = self.generate_unique_message_number()
        message = Message(
            message_no=message_no,
            sender_username=bank.username,
            recipient_username=member.username,
            message_name='Disbursement Successfully Submitted',
            message_description=f'Transaction Number {transaction_no} for amount {entered_amount} has been submitted.',
            message_date=timezone.now().date()
        )
        message.save()

        # Create and save the loan
        payment_no = unique_payment_number()
        loan = Loan(
            transaction_no=transaction_no,
            payment_no=payment_no,
            national_id_no=national_id_no,
            bank_no=bank_no,
            principal=disbursed_amount,
            loan_interest=allocation.interest_rate,
            principal_interest=disbursed_amount,
            amount_paid=0,
            balance=disbursed_amount,
            loan_date=timezone.now().date()
        )
        loan.save()
        
        return redirect('disbursement-success', {'transaction_no': transaction_no})
        
    def form_invalid(self, form):
        application_no = self.kwargs['application_no']
        return render(self.request, self.template_name, {
            'form': form,
            'application_no': application_no,
            'error_transaction_no': form.cleaned_data.get('transaction_no', None),
            'error_message': 'There was an error with your disbursement. Please correct the errors.'
        })

    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no

class DisbursementSuccessView(TemplateView):
    template_name = 'disbursement_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_no'] = self.kwargs.get('transaction_no', 'default_value')  # Safely access username
        return context            
            
class BankLoansView(ListView):
    template_name = 'bank_loans.html'
    context_object_name = 'loans_to_be_paid'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('bank_login')  # Redirect to login if username is not in session
        try:
            bank = get_object_or_404(Bank, username=username)
            bank_no = bank.bank_no
            
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('bank_login')
        # Retrieve loans
        loans_to_be_paid = Loan.objects.filter(bank_no = bank_no)

        return render(request, self.template_name, {'loans_to_be_paid': loans_to_be_paid})
    
class MemberLoansView(ListView):
    template_name = 'member_loans.html'
    
    context_object_name = 'loans_to_pay'

    def get(self, request):
        username = request.session.get('username')
        if not username:
            return redirect('borrower_login')  # Redirect to login if username is not in session
        try:
            # Query the user from the database using the username
            member = get_object_or_404(Member, username=username)
            national_id_no = member.national_id_no
            
        except System_User.DoesNotExist:
            # Handle the case where the user does not exist
            return redirect('borrower_login')

        # Retrieve Loans
        loans_to_pay = Loan.objects.filter(national_id_no = national_id_no)
        
        return render(request, self.template_name, {'loans_to_pay': loans_to_pay})
    
class LoanPaymentView(View):
    template_name = 'payment.html'

    def get(self, request, transaction_no):
        loan = get_object_or_404(Loan, transaction_no=transaction_no)
        form = PaymentForm()

        context = {
            'loan': loan,
            'form': form,
            'transaction_no': transaction_no,
            'success_message': request.GET.get('success_message', ''),
            'error_message': request.GET.get('error_message', ''),
        }

        return render(request, self.template_name, context)

    def post(self, request, transaction_no):
        loan = get_object_or_404(Loan, transaction_no=transaction_no)
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment_amount = form.cleaned_data['payment_amount']

            disbursement = get_object_or_404(Disbursement, transaction_no=transaction_no)
            disbursement_date = disbursement.disbursement_date

            national_id_no = loan.national_id_no
            bank_no = loan.bank_no
            member = get_object_or_404(Member, national_id_no=national_id_no)
            bank = get_object_or_404(Bank, bank_no=bank_no)
            
            member_account = get_object_or_404(Account, account_no=member.account_no)

            bank_account = get_object_or_404(Account, account_no=bank.account.account_no)

            if member_account.account_bal < payment_amount:
                error_message = 'You have Insufficient Account Balance to Complete this Transaction.'
                return render(request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': error_message,
                })

            interest_rate = loan.loan_interest
            loan_duration = disbursement.loan_duration_months

            elapsed_months = calculate_time_elapsed_in_months(disbursement_date)
            new_loan_interest = calculate_compound_interest(loan.balance, interest_rate, elapsed_months)
            loan.loan_interest = interest_rate
            loan.principal_interest = new_loan_interest

            # Ensure payment amount does not exceed the loan balance
            if payment_amount > loan.balance:
                error_message = 'Payment amount exceeds the current loan balance. Please enter a valid amount.'
                return render(request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': error_message,
                })
                
            if payment_amount < 1.00:
                error_message = 'Payment amount should be Kshs 1 and above.'
                return render(self.request, self.template_name, {
                    'loan': loan,
                    'form': form,
                    'transaction_no': transaction_no,
                    'error_message': error_message,
                })


            loan.amount_paid += payment_amount
            loan.balance = loan.principal_interest - loan.amount_paid
            if loan.balance < 0:
                loan.balance = 0  # Ensure balance does not go below 0
            loan.loan_date = datetime.now().date()
            loan.save()
            if loan.balance == 0:
                loanee = get_object_or_404(Loanee, national_id_no=national_id_no)
                loanee.approved = 'YES'
                loanee.save()

            
            member_account.account_bal -= payment_amount
            member_account.save()

            # Update lender's and borrower's account balances
            bank_account.account_bal += payment_amount
            bank_account.save()

            
            message_no = self.generate_unique_message_number()
            message = Message(
                message_no=message_no,
                sender_username=bank.username,
                recipient_username=member.username,
                message_name='Payment Successfully Completed',
                message_description=(
                    f'Loan Payment for Disbursement Transaction Number {transaction_no} '
                    f'amount {payment_amount} has been submitted. '
                    f'Balance: {loan.balance}'
                ),
                message_date=timezone.now().date()
            )
            message.save()
            
            return redirect('payment-success', {'transaction_no': transaction_no})

        error_message = 'Payment failed. Please correct the errors below.'
        return render(request, self.template_name, {
            'loan': loan,
            'form': form,
            'transaction_no': transaction_no,
            'error_message': error_message,
        })
        
    def generate_unique_message_number(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            digits = ''.join(random.choices(string.digits, k=3))
            message_no = letters + digits
            if not Message.objects.filter(message_no=message_no).exists():
                return message_no
        
class PaymentSuccessView(TemplateView):
    template_name = 'payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_no'] = self.kwargs.get('transaction_no', 'default_value')  # Safely access username
        return context 


 
class BankSentMessagesView(ListView):
    template_name = 'bank_sent_messages.html'
    context_object_name = 'messages'

    def get(self, request):
        # Check if user is logged in and retrieve their information
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')
        
        # Initialize message lists as empty
        mssgs = []
        
        if username:
            mssgs = Message.objects.filter(sender_username=username)

        # Pass the loans to the template
        return render(request, self.template_name, {
            'mssgs': mssgs,
        }) 
        
class BankRcvdMessagesView(ListView):
    template_name = 'bank_received_messages.html'
    context_object_name = 'messages'

    def get(self, request):
        # Check if user is logged in and retrieve their information
        username = request.session.get('username')
        if not username:
            return redirect('bank-login')
        
        # Initialize message lists as empty
        mssgs = []
        
        if username:
            mssgs = Message.objects.filter(recipient_username=username)

        # Pass mssgs to the template
        return render(request, self.template_name, {
            'mssgs': mssgs,
        })   

class MemberSentMessagesView(ListView):
    template_name = 'member_sent_messages.html'
    context_object_name = 'messages'

    def get(self, request):
        # Check if user is logged in and retrieve their information
        username = request.session.get('username')
        if not username:
            return redirect('member-login')
        
        # Initialize message lists as empty
        mssgs = []
        
        if username:
            mssgs = Message.objects.filter(sender_username=username)

        # Pass the loans to the template
        return render(request, self.template_name, {
            'mssgs': mssgs,
        }) 
        
class MemberRcvdMessagesView(ListView):
    template_name = 'member_received_messages.html'
    context_object_name = 'messages'

    def get(self, request):
        # Check if user is logged in and retrieve their information
        username = request.session.get('username')
        if not username:
            return redirect('member-login')
        
        # Initialize message lists as empty
        mssgs = []
        
        if username:
            mssgs = Message.objects.filter(recipient_username=username)

        # Pass mssgs to the template
        return render(request, self.template_name, {
            'mssgs': mssgs,
        })   
