from django.views import View
from django.shortcuts import render, redirect
import time
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ..repositories.customer import CustomerRepository

@method_decorator(never_cache, name='dispatch')
class SettingView(View):

    def get(self, request):
        customerId = request.session['customerId']
        customerDetails = CustomerRepository.getCustomerDetails(customerId)
        if customerDetails == None:
            return redirect('login')

        context = {
            "passwordmessage": "",
            "editmessage": "",
            "closemessage": "",
            "first_name": customerDetails['first_name'],
            "last_name": customerDetails['last_name'],
            "email": customerDetails['email'],
            "phone_number": customerDetails['phone_number'],
            "account_type": customerDetails['account_type']
        }
        return render(request, 'settings.html', context=context)

    def post(self, request):
        editmessage = ""
        passwordmessage = ""
        closemessage = ""
        try:
            customerId = request.session['customerId']
            customerDetails = CustomerRepository.getCustomerDetails(customerId)
            if customerDetails == None:
                return redirect('login')

            context = {
                "passwordmessage": "",
                "editmessage": "",
                "closemessage": "",
                "first_name": customerDetails['first_name'],
                "last_name": customerDetails['last_name'],
                "email": customerDetails['email'],
                "phone_number": customerDetails['phone_number'],
                "account_type": customerDetails['account_type'],
                
                
            }
            if request.POST['actionBtn'] == 'Submit':
                data = {
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'phone_number': request.POST['phone_number'],
                    "account_type": request.POST['account_type']
                }
                status = CustomerRepository.updateProfile(request, data)
                if status:
                    context['editmessage'] = "Saved Successfully"
                else:
                    context['editmessage'] = "Something went wrong!"

            if request.POST['actionBtn'] == 'Change Password':
                data = {
                    'password': request.POST['password']
                }
                status = CustomerRepository.updateProfile(request, data)
                if status:
                    context['passwordmessage'] = "Update Successfully"
                else:
                    context['passwordmessage'] = "Something went wrong!"
            if request.POST['actionBtn'] == 'Close Account':
                data = {
                    'status': CustomerRepository.inActiveStatus
                }
                status = CustomerRepository.updateProfile(request, data)
                if status:
                    context['closemessage'] = "Closed Successfully"
                else:
                    context['closemessage'] = "Something went wrong!"
                time.sleep(5)
                return redirect('login')

            return render(request, 'settings.html', context)

        except Exception as e:
            print(e)
            return render(request, 'settings.html', {"passwordmessage": passwordmessage, "editmessage": editmessage, "closemessage": closemessage})
