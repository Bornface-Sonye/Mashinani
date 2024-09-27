from django.contrib import admin
from .models import (
    County, Constituency, Ward, Account, Group, Guarantor, Bank, Member, System_User, Allocation, Application, 
    Disbursement, Loan, Message, Loanee, Defaulter, PasswordResetToken, Role, Contact
)

models_to_register = [
    County, Constituency, Ward, Account, Group, Guarantor, Bank, Member, System_User, Allocation, Application, 
    Disbursement, Loan, Message, Loanee, Defaulter, PasswordResetToken, Role, Contact
    
]

i = 0
while True:
    admin.site.register(models_to_register[i])
    i += 1
    if i >= len(models_to_register):
        break
