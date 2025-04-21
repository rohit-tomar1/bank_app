# from django.db import models  
# class Customers(models.Model):   
#     title = models.CharField(max_length=10, blank=True, default='')
#     first_name = models.CharField(max_length=100, blank=True, default='')  
#     middle_name = models.CharField(max_length=100, blank=True, default='') 
#     last_name = models.CharField(max_length=100, blank=True, default='') 
#     email = models.CharField(max_length=150, blank=True, default='') 
#     phone_number= models.CharField(max_length=10, blank=True, default='')
#     dob =models.CharField(max_length=15, blank=True, default='') 
#     address = models.CharField(max_length=150, blank=True, default='')
#     city= models.CharField(max_length=150, blank=True, default='')
#     country=  models.CharField(max_length=15, blank=True, default='')
#     postal_code = models.CharField(max_length=15, blank=True, default='')
#     password = models.CharField(max_length=15, blank=True, default='')
#     status = models.CharField(max_length=15, blank=True, default='')
#     confirm_password = models.CharField(max_length=15,blank=True, default='')
#     actionBtn = models.CharField(max_length=15, blank=True, default='')
#     card_number = models.CharField(max_length=30, blank=True, default='')
#     pin_number = models.CharField(max_length=4, blank=True, default='')
#     security_code = models.CharField(max_length=3, blank=True, default='')


#     class Meta:  
#         db_table = "customers"  



# class Transaction(models.Model): 
#     account_number_and_name = models.CharField(max_length=150, blank=True, default='')
#     transType = models.CharField(max_length=15, blank=True, default='')
#     amount = models.CharField(max_length=15, blank=True, default='')
#     balance_after = models.CharField(max_length=15, blank=True, default='')
#     balance_before = models.CharField(max_length=15, blank=True, default='')
#     summary = models.CharField(max_length=250, blank=True, default='')
#     date = models.CharField(max_length=15, blank=True, default='')
#     email = models.CharField(max_length=150, blank=True, default='')
#     class Meta:  
#         db_table = "transaction"  
  
