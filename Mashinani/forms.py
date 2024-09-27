from django import forms
import re
from django.contrib.auth.models import User
from .models import (
    County, Constituency, Ward, Account, Group, Guarantor, Bank, Member, System_User, Allocation, Application, 
    Disbursement, Loan, Message, Loanee, Defaulter, PasswordResetToken, Contact
)

class GroupForm(forms.ModelForm):
        
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.all(),
        required=True,
        label='Ward',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    guarantor = forms.ModelChoiceField(
        queryset=Guarantor.objects.all(),
        required=True,
        label='Guarantor Number',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    class Meta:
        model = Group
        fields = ['group_no', 'group_name', 'email_address', 'phone_number', 'ward', 'guarantor', 'account']
        labels = {
            'group_no': 'Group Number',
            'group_name': 'Group Name',
            'email_address': 'Email Address',
            'phone_number': 'Phone Number',
            'account': 'Account',
        }
        
        widgets = {
            'group_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Group Number'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Group Name'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'account': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Account'}),
        }
        
        
class BankForm(forms.ModelForm):
        
    constituency = forms.ModelChoiceField(
        queryset=Constituency.objects.all(),
        required=True,
        label='Constituency',
        widget=forms.Select(attrs={'class': 'black-input-box'}),
    )
    
    
    class Meta:
        model = Bank
        fields = ['bank_no', 'bank_name', 'email_address', 'phone_number', 'constituency', 'account']
        labels = {
            'bank_no': 'Bank Number',
            'bank_name': 'Bank Name',
            'email_address': 'Email Address',
            'phone_number': 'Phone Number',
            'account': 'Account',
        }
        
        widgets = {
            'bank_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Number'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Name'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'account': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Account'}),
        }
        
        
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['username', 'group_no', 'loan_status', 'loan_bal']  # Exclude fields you handle manually
        labels = {
            'national_id_no': 'National Identification Number:',
            'email_address': 'Email Address:',
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'phone_number': 'Phone Number:',
            'dob': 'Date Of Birth:',
            'gender': 'Gender:',
            'grp_worth': 'Worth in Kshs:',
            'account_no': 'Account Number',
            'approved': 'Member approved for Loan ?',
        }
        widgets = {
            'national_id_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter National Identification Number'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Date Of Birth'}),
            'gender': forms.RadioSelect(choices=Member.GENDER_CHOICES),
            'grp_worth': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Worth in Kshs'}),
            'account_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account Number'}),
            'approved': forms.Select(attrs={'class': 'form-control'}),
        }
        
        
class AdminSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        exclude = ['role_name']
        fields = ['username', 'password_hash']
        labels = {
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg kcbgroup@lender.co.ke'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance
    
class GroupSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        exclude = ['role_name']
        fields = ['username', 'password_hash']
        labels = {
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg kcbgroup@lender.co.ke'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance
    
class BankSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        exclude = ['role_name']
        fields = ['username', 'password_hash']
        labels = {
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg kcbgroup@lender.co.ke'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance
    
class MemberSignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    class Meta:
        model = System_User
        exclude = ['role_name']
        fields = ['username', 'password_hash']
        labels = {
            'username': 'Username',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username eg kcbgroup@lender.co.ke'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance
    
class LoginForm(forms.Form):
    username = forms.EmailField(
        label="Username",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username:'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password:'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        return cleaned_data


class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        exclude = ['allocation_no', 'bank_no']
        fields = ['allocation_no', 'bank_no', 'amount', 'interest_rate', 'allocation_date']
        labels = {
            'amount': 'Amount to Allocate',
            'interest_rate': 'Interest Rate'
        }
        widgets = {
            'bank_no': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount to Allocate'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Interest Rate/per Month'}),
        }

class DisbursementForm(forms.ModelForm):
     class Meta:
        model = Disbursement
        exclude = ['transaction_no', 'application_no']
        fields = ['disbursed_amount']
        labels = {
            'disbursed_amount': 'Amount to Disburse',
        }
        widgets = {
            'disbursed_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount to Disburse'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['national_id_no']
        fields = ['national_id_no', 'loan_amount']
        labels = {
            'loan_amount': 'Loan Amount',
        }
        widgets = {
            'national_id_no': forms.HiddenInput(),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Loan Amount'}),
        }

class PaymentForm(forms.Form):
    payment_amount = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label='Payment Amount',
        min_value=0.01,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter payment amount'})
    )
      

class DefaulterForm(forms.ModelForm):
    class Meta:
        model = Defaulter
        exclude = ['bank_no']
        fields = ['national_id_no', 'bank_no', 'amount_owed']
        widgets = {
            'submission_date': forms.HiddenInput(),
        }


class PasswordResetForm(forms.Form):
    username = forms.EmailField(
        label='Username',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not System_User.objects.filter(username=username).exists():
            raise forms.ValidationError("This Username is not associated with any account.")
        return username
    
 
class ResetForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    
    class Meta:
        model = System_User
        fields = ['password_hash']
        labels = {
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email_address', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Message'}),
        }