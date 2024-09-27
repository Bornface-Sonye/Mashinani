from django.db import models
from datetime import date
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .validators import validate_kenyan_id, validate_kenyan_phone_number


class County(models.Model):
    county_id = models.AutoField(primary_key=True, unique=True)
    county_name = models.CharField(max_length=100, help_text="Enter County Name")

    def __str__(self):
        return self.county_name

class Constituency(models.Model):
    constituency_id = models.AutoField(primary_key=True, unique=True)
    constituency_name = models.CharField(max_length=100, help_text="Enter Constituency Name")
    county_id = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.constituency_name


class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True, unique=True)
    ward_name = models.CharField(max_length=100, help_text="Enter Ward Name")
    constituency_id = models.ForeignKey(Constituency, on_delete=models.CASCADE)

    def __str__(self):
        return self.ward_name

class Account(models.Model):
    account_no = models.DecimalField(max_digits=50, decimal_places=0, primary_key=True, help_text="Enter Account Number")
    account_name = models.CharField(max_length=100, help_text="Enter Account Name")
    account_bal = models.DecimalField(max_digits=20, decimal_places=2, help_text="Enter Account Balance")

    def __str__(self):
        return self.account_name

class Role(models.Model):
    role_id = models.AutoField(primary_key=True, unique=True)
    role_name = models.CharField(max_length=100, help_text="Enter Role Name")

    def __str__(self):
        return self.role_name    
    
class Guarantor(models.Model):
    guarantor_id = models.AutoField(primary_key=True, unique=True)
    national_id_no = models.DecimalField(max_digits=8, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    first_name = models.CharField(max_length=30, help_text="Enter First Name")
    last_name = models.CharField(max_length=30, help_text="Enter Last Name")
    username = models.CharField(max_length=50, help_text="Enter Username", blank=True)
    phone_number = models.CharField(max_length=13, validators=[validate_kenyan_phone_number], help_text="Enter phone number in the format 0798073204 or +254798073404")
    dob = models.DateField(help_text="Enter Date of Birth")
    occupation = models.CharField(max_length=100, help_text="Enter Occupation")
    account_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    
    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    def __str__(self):
        return f"{self.first_name}"
    
class Group(models.Model):
    group_no = models.CharField(max_length=50, primary_key=True, unique=True, help_text="Enter Group Number")
    group_name = models.CharField(max_length=100, help_text="Enter Group Name")
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    phone_number = models.CharField(max_length=13, validators=[validate_kenyan_phone_number], help_text="Enter phone number in the format 0798073204 or +254798073404")
    username = models.CharField(max_length=50, help_text="Enter Username", blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    guarantor = models.ForeignKey(Guarantor, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name

class Bank(models.Model):
    bank_no = models.CharField(max_length=50, primary_key=True, unique=True, help_text="Enter Bank Number")
    bank_name = models.CharField(max_length=50, unique=True, help_text="Enter Bank Name")
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    phone_number = models.CharField(max_length=13,  validators=[validate_kenyan_phone_number], help_text="Enter phone number in the format 0798073204 or +254798073404")
    username = models.CharField(max_length=50, help_text="Enter Username", blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
   
    def __str__(self):
        return f"{self.bank_name}"    
    
class Member(models.Model):
    member_id = models.AutoField(primary_key=True, unique=True)
    national_id_no = models.DecimalField(max_digits=20, decimal_places=0, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    email_address = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    username = models.EmailField(unique=True, max_length=50, help_text="Enter Email Address")
    first_name = models.CharField(max_length=50, help_text="Enter First Name")
    last_name = models.CharField(max_length=50, help_text="Enter Last Name")
    phone_number = models.CharField(max_length=13,  validators=[validate_kenyan_phone_number], help_text="Enter phone number in the format 0798073204 or +254798073404")
    dob = models.DateField(help_text="Enter Date of Birth")
    
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Enter Member Gender")
    grp_worth = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, help_text="Enter Group Worth in Kshs.")
    account_no = models.CharField(max_length=50, default='00000000', help_text="Account Number")

    YES = 'yes'
    NO = 'no'
    APPROVAL_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No'),
    ]
    approved = models.CharField(max_length=3, choices=APPROVAL_CHOICES, default=NO, help_text="Is the member approved")
   
    OPEN = 'open'
    CLOSED = 'closed'
    LOAN_STATUS = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]
    loan_status = models.CharField(max_length=6, choices=LOAN_STATUS, default=OPEN, help_text="Member Loan Status")
    loan_bal =models.DecimalField(max_digits=20, decimal_places=2, default=0.00, help_text="Loan Balance")
    group_no = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name}"

    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age


class System_User(models.Model):
    username = models.EmailField(primary_key=True, unique=True, max_length=50, help_text="Enter a valid Username")
    password_hash = models.CharField(max_length=128, help_text="Enter a valid password")  # Store hashed password
    role_name = models.CharField(max_length=8, help_text="Enter a valid role")

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def clean(self):
        # Custom validation for password field
        if len(self.password_hash) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def __str__(self):
        return self.username


class Allocation(models.Model):
    allocation_id = models.AutoField(primary_key=True, unique=True)
    allocation_no = models.CharField(unique=True, max_length=50, help_text="Enter the Allocation Number", blank=True)
    bank_no = models.CharField(max_length=100, help_text="Enter Bank Number:")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Allocate")
    interest_rate = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Interest Rate")
    allocation_date = models.DateField(help_text="Enter Date of Allocation", blank=True)

    def __str__(self):
        return f"{self.allocation_no}"

class Application(models.Model):
    application_id = models.AutoField(primary_key=True, unique=True)
    application_no = models.CharField(unique=True, max_length=50, help_text="Enter the Application Number", blank=True)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Request")
    proposed_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount Proposed")
    application_date = models.DateField(help_text="Enter Date of Application", blank=True)
    national_id_no =  models.CharField(max_length=100, help_text="Enter National Identification Number:")
    allocation_no = models.CharField(max_length=50, help_text="Enter the Allocation Number", blank=True)

    def __str__(self):
        return f"Application - {self.application_no}"


class Disbursement(models.Model):
    disbursement_id = models.AutoField(primary_key=True, unique=True)
    transaction_no = models.CharField(unique=True, max_length=30, help_text="Enter the Transaction Number", blank=True)
    disbursed_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Disburse")
    disbursement_date = models.DateField(help_text="Enter Date of Disbursement")
    loan_duration_months = models.IntegerField(help_text="Loan Duration in Months")
    national_id_no =  models.CharField(max_length=100, help_text="Enter National Identification Number:")
    application_no = models.CharField(max_length=50, help_text="Enter the Application Number", blank=True)

    def __str__(self):
        return f"{self.transaction_no}"
    
    
class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True, unique=True)
    payment_no = models.CharField(max_length=30, help_text="Enter the Payment Number", blank=True)
    principal = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount to Pay")
    loan_interest = models.DecimalField(max_digits=15, decimal_places=2, help_text="Interest Rate")
    principal_interest = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total Amount")
    amount_paid =  models.DecimalField(max_digits=15, decimal_places=2, help_text="Total Paid")
    balance =  models.DecimalField(max_digits=15, decimal_places=2, help_text="Balance")
    loan_date = models.DateField(help_text="Enter Date of last Payment",default='2024-01-01')
    bank_no =  models.CharField(max_length=100, help_text="Enter Bank Number:")
    national_id_no =  models.CharField(max_length=100, help_text="Enter National Identification Number:")
    transaction_no =  models.CharField(max_length=30, help_text="Enter the Transaction Number", blank=True)

    def __str__(self):
        return f"{self.transaction_no}"
    
class Message(models.Model):
    message_id = models.AutoField(primary_key=True, unique=True)
    message_no = models.CharField(max_length=50, help_text="Enter Message Number")
    sender_username = models.CharField(max_length=50, help_text="Enter Sender Username")
    recipient_username = models.CharField(max_length=50, help_text="Enter Recipient Username")
    message_name = models.CharField(max_length=50, help_text="Enter Message Name")
    message_description = models.CharField(max_length=50, help_text="Enter Message Description")
    message_date = models.DateField(help_text="Enter Date Sent")

    def __str__(self):
        return f"{self.message_no}"
    
class Loanee(models.Model):
    loanee_id = models.AutoField(primary_key=True, unique=True)
    YES = 'yes'
    NO = 'no'
    APPROVAL_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No'),
    ]
    approved = models.CharField(max_length=3, choices=APPROVAL_CHOICES, default=YES, help_text="Is member approved")
    applied = models.CharField(max_length=3, choices=APPROVAL_CHOICES, default=NO, help_text="Does member has an hanging application")
    national_id_no =  models.CharField(max_length=100, help_text="Enter National Identification Number:")
    
    def __str__(self):
        return f"{self.national_id_no} - Approved - {self.approved}"  

class Defaulter(models.Model):
    national_id_no = models.DecimalField(max_digits=8, decimal_places=0, primary_key=True, unique=True, validators=[validate_kenyan_id], help_text="Enter National Identification Number:")
    amount_owed = models.DecimalField(max_digits=15, decimal_places=2, help_text="Enter Amount Owed")
    submission_date = models.DateField(help_text="Enter Date of Submission", blank=True)
    bank_no =  models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.national_id_no)


class PasswordResetToken(models.Model):
    username = models.ForeignKey(System_User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.username}"

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=5)
        return timezone.now() > expiration_time
    
class Contact(models.Model):
    message_id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=50, help_text="Enter Full Name")
    email_address = models.EmailField(max_length=50, help_text="Enter Email Address")
    subject = models.CharField(max_length=100, help_text="Enter Subject", blank=True)
    message = models.TextField(help_text="Enter Message", blank=True)
   
    def __str__(self):
        return f"{self.full_name}" 

