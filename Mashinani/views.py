from .models import (
    County, Constituency, Ward, Account, Group, Guarantor, Bank, Member, System_User, Allocation, Application, 
    Disbursement, Loan, Message, Loanee, Defaulter, PasswordResetToken
)

from .forms import (
   GroupForm, BankForm, MemberForm, AdminSignUpForm, BankSignUpForm, GroupSignUpForm, MemberSignUpForm, LoginForm
)
from django import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, DeleteView, ListView

class HomePage_View(View):
    def get(self,request):
        return render(request, 'index.html')
    
    
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
            return redirect('group_login')
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
            return redirect('bank_login')
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
            return redirect('member_login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        
class AdminLoginView(View):
    template_name = 'admin_login.html'

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
                    return redirect(reverse('group'))
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
                    return redirect(reverse('bank'))
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
                    return redirect(reverse('bank'))
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
        username = request.session.get('username')
        if not username:
            return redirect('admin-login')  # Redirect to login if username is not in session

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
            return redirect('admin-login')

        return render(request, 'dashboard.html', {'user': user})
    
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

        return render(request, 'group-dashboard.html', {'user': user})
    
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

        return render(request, 'bank-dashboard.html', {'user': user})
    
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

        return render(request, 'member-dashboard.html', {'user': user})
 
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
            group.save()

            
            return redirect('success')
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
            bank.save()

            
            return redirect('success')
        else:
            return render(request, self.template_name, {'form': form})
        
def success(request):
    return render(request, 'register_success.html')

class SendParcelView(View):
    template_name = 'send_parcels.html'

    def get(self, request):
        form = SendParcelForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = SendParcelForm(request.POST)
        if form.is_valid():
            reciept_number = uuid.uuid4().hex[:10].upper()  # Generate ticket number
            sender =  request.session['email_address']
            send_parcel_form = form.save(commit=False)
            send_parcel_form.sender = sender
            send_parcel_form.reciept_number = reciept_number
            send_parcel_form.save()
            # Store the ticket number in the session
            request.session['reciept_number'] = reciept_number
            
            return redirect('sending_success')  # Redirect to sending success page
        else:
            return render(request, 'send_parcels.html', {'form': form})

class AboutUsView(View):
    template_name = 'about_us.html'

    def get(self, request):
        return render(request, self.template_name)

class ContactUsView(View):
    template_name = 'contact_us.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the ContactMessage model
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            contact_message.save()

            # Optionally, send a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us_success')
        return render(request, self.template_name, {'form': form})

class ContactUsSuccessPageView(View):
    template_name = 'contact_us_success.html'
    
    def get(self, request):
        return render(request, self.template_name )

class FAQsView(View):
    template_name = 'faqs.html'

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

        form = GroupMemberForm()
        context = {
            'user': user,
            'group': group,
            'form': form,
        }
        return render(request, 'add_member.html', context)

    def post(self, request):
        form = GroupMemberForm(request.POST)
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
            loan_status = form.cleaned_data.get('loan_status')
            loan_bal = form.cleaned_data.get('loan_bal')
            
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
                    account_no=account,
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
            return redirect('home')  # Redirect to login if username is not in session
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
    fields = ['national_id_no', 'email_address', 'username', 'first_name', 'last_name', 'phone_number', 'dob', 'gender', 'group_no', 'grp_worth', 'account', 'approved', 'loan_status', 'loan_bal']
    widgets = {
            'gender': forms.RadioSelect(choices=Member.GENDER_CHOICES),
        }
    template_name = 'member_update.html'
    success_url = reverse_lazy('member-list')


class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'member_delete.html'
    success_url = reverse_lazy('member-list')

