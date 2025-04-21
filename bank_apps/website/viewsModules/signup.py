from django.views import View
from django.shortcuts import render, redirect

from ..utils.otp import OTPHandler
from ..repositories.customer import CustomerRepository


class SignUpView(View):

    def get(self, request):
        route = request.path
        if 'signup1' in route:
            return render(request, 'signup1.html')
        elif 'signup2' in route:
            return render(request, 'signup2.html')
        elif 'signup3' in route:
            return render(request, 'signup3.html')
        elif 'signup4' in route:
            return render(request, 'signup4.html')
        else:
            return render(request, 'signup1.html')

    def post(self, request):
        formId = request.POST['form_id']
        context = SignUpView.getContext({**request.POST})
        if formId == 'signup1':
            request.session['tempData1'] = request.POST
            if request.POST['actionBtn'] == 'Proceed':
                return redirect('signup2')

        elif formId == 'signup2':
            request.session['tempData2'] = request.POST
            if request.POST['actionBtn'] == 'Proceed':
                isExist = CustomerRepository.findByEmail(request.POST['email'])
                if isExist:
                    context['error_message'] = 'Email Id Already Registered. Please try other one.'
                    return render(request, 'signup2.html', context)
                else:
                    return redirect('signup3')
            else:
                oldFormContext = SignUpView.getContext(
                    {**request.session['tempData1']}, oldData=True)
                return render(request, 'signup1.html', oldFormContext)

        elif formId == 'signup3':
            request.session['tempData3'] = request.POST
            if request.POST['actionBtn'] == 'Proceed':
                return redirect('signup4')
            else:
                oldFormContext = SignUpView.getContext(
                    {**request.session['tempData2']}, oldData=True)
                return render(request, 'signup2.html', oldFormContext)

        elif formId == 'signup4':
            request.session['tempData4'] = request.POST
            request.session['email'] = dict(
                request.session['tempData2'].items()).get('email')
            request.session['otpAction'] = 'signup'
            if request.POST['actionBtn'] == 'Proceed':
                otpObj = OTPHandler(request, request.session['email'])
                otpObj.sentOTP()
                return redirect('otp')
            else:
                oldFormContext = SignUpView.getContext(
                    {**request.session['tempData3']}, oldData=True)
                return render(request, 'signup3.html', oldFormContext)
        else:
            oldFormContext = SignUpView.getContext(
                {**request.session['tempData1']}, oldData=True)
            return render(request, 'signup1.html', oldFormContext)

    @staticmethod
    def getContext(context, oldData=False):
        newContext = {}
        for key, value in context.items():
            if oldData:
                newContext[key] = value
            else:
                newContext[key] = value[0]

        return newContext