from django import forms  
from .models.models import Customers  
from .models.models import Transaction 
from .models.models import RecurringPayment  
class CustomersForm(forms.ModelForm):  
    class Meta:  
        model = Customers  
        widgets = {
        'password': forms.PasswordInput(),
    }
        fields = "__all__"  


class TransactionForm(forms.ModelForm):  
    class Meta:  
        model = Transaction     
        fields = "__all__"  

class RecurringPaymentForm(forms.ModelForm):  
    class Meta:  
        model = RecurringPayment     
        fields = "__all__"  