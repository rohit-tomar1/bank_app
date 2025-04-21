from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ..utils.cryptography import Cryptography
from ..utils.otp import OTPHandler
from ..repositories.customer import CustomerRepository

@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    
    def get(self, request):
        return render(request, 'login.html')
        

    def post(self, request):
        error_message = None
        try:
            CustomerRepository.deleteUserSession(request)
            emailID = request.POST['email']
            password = request.POST['password']
            customerDetails = CustomerRepository.findByEmail(emailID)
            if customerDetails == None:
                error_message = 'Invalid email ID. Please enter valid Email ID'
                return render(request, 'login.html', {"error_message": error_message})

            # decrypt password
            decryptedPass = Cryptography.decryption(customerDetails.password)
            if password != decryptedPass:
                error_message = 'Invalid password. Please enter correct password.'
                return render(request, 'login.html', {"error_message": error_message})

            request.session['email'] = emailID
            request.session['customerId'] = customerDetails.id
            request.session['otpAction'] = 'login'
            
            otpObj = OTPHandler(request, emailID)
            otpObj.sentOTP()
            return redirect('otp')
        except Exception as e:
            print(e)
            return render(request, 'login.html', {"error_message": 'Something went wrong!!'})
