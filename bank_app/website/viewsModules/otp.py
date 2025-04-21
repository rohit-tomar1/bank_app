from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ..utils.otp import OTPHandler
from ..repositories.customer import CustomerRepository

@method_decorator(never_cache, name='dispatch')
class OTPView(View):

    def get(self, request):
        context = {
            "error_message": '',
            "emailID": request.session['email'],
            "otpAction": request.session['otpAction']
        }
        print(context)
        return render(request, 'otp.html', context)

    def getEnteredOTP(self, request):
        otp1 = request.POST['otp1']
        otp2 = request.POST['otp2']
        otp3 = request.POST['otp3']
        otp4 = request.POST['otp4']
        otp5 = request.POST['otp5']
        otp6 = request.POST['otp6']
        otp = otp1+otp2+otp3+otp4+otp5+otp6
        return otp

    def post(self, request):
        try:
            errorMsg = None
            action = request.session['otpAction']
            if request.POST['actionBtn'] == 'Cancel':
                if action == 'signup':
                    return redirect('signup1')
                else:
                    return redirect('')

            otp = self.getEnteredOTP(request)
            emailId = request.session['email']

            otpObject = OTPHandler(request, emailId)
            isValid, errorMsg = otpObject.validateOTP(otp)
            print(isValid, errorMsg)
            context = {
                "error_message": '',
                "emailID": request.session['email'],
                "otpAction": request.session['otpAction']
            }
            if otp == "":
                context['error_message'] = 'Please Enter OTP.'
                return render(request, 'otp.html', context)
            elif isValid == False:
                context['error_message'] = errorMsg
                return render(request, 'otp.html', context)

            print("User action", action)
            if action == 'signup':
                status, errorMsg = CustomerRepository.createNewCustomer(
                    request)
                print("User Status", status, errorMsg)
                if status == False:
                    context['error_message'] = errorMsg
                    return render(request, 'otp.html', context)
                else:
                    return redirect('main')
            else:
                CustomerRepository.setUserSession(request)
                return redirect('main')

        except Exception as e:
            print(e)
            return render(request, 'login.html', {"error_message": 'Something went wrong!!'})
