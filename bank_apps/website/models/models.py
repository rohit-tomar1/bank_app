from django.db import models


class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=10, blank=True, default='')
    account_number = models.CharField(max_length=10, blank=True, default='')
    title = models.CharField(max_length=10, blank=True, default='')
    first_name = models.CharField(max_length=100, blank=False, default='')
    middle_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=50, blank=False, default='')
    phone_number = models.CharField(max_length=255, blank=True, default='')
    dob = models.CharField(max_length=15, blank=True, default='')
    address = models.CharField(max_length=150, blank=True, default='')
    city = models.CharField(max_length=150, blank=True, default='')
    country = models.CharField(max_length=15, blank=True, default='')
    postal_code = models.CharField(max_length=15, blank=True, default='')
    password = models.CharField(max_length=255, blank=True, default='')
    status = models.CharField(max_length=10, blank=True, default='A')
    ct = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = "customers"




class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=20, blank=True, default='')
    transType = models.CharField(max_length=15, blank=True, default='')
    amount = models.CharField(max_length=15, blank=True, default='')
    summary = models.CharField(max_length=250, blank=True, default='')
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    class Meta:  
        db_table = "transaction"  
        
        
class Cards(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=20, blank=True, default='')
    card_number = models.CharField(max_length=255, blank=True, default='')
    valid_till = models.CharField(max_length=255, blank=True, default='')
    pin_number = models.CharField(max_length=255, blank=True, default='')
    security_code = models.CharField(max_length=255, blank=True, default='')
    status = models.CharField(max_length=10, blank=True, default='A')
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    class Meta:  
        db_table = "cards"

class RecurringPayment(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=20, blank=True, default='')
    amount = models.CharField(max_length=15, blank=True, default='')
    ct = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    account_number = models.CharField(max_length=10, blank=True, default='')
    frequency = models.CharField(max_length=10, blank=True, default='')
    status = models.CharField(max_length=10, blank=True, default='A')
    class Meta:  
        db_table = "recurringPayment"  
  
  
class UserRequest(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=20, blank=True, default='')
    requestType = models.CharField(max_length=15, blank=True, default='')
    summary = models.CharField(max_length=250, blank=True, default='')
    status = models.CharField(max_length=10, blank=True, default='O')
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    class Meta:  
        db_table = "user_requests"  
        
  