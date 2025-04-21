from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


from ..repositories.userRequest import UserRequestRepository


@method_decorator(never_cache, name='dispatch')
class PassbookView(View):

    def get(self, request):
        return render(request, 'passbook.html')

    def post(self, request):
        msg = "Something went wrong!!"
        try:
            customerId = request.session['customerId']
            requestType = UserRequestRepository.requestType.get('checkbook')
            summary = request.POST['summary']
            _, msg = UserRequestRepository.createNewRequest(
                customerId, requestType, summary)
            request.session['errorMessage'] = msg
            return redirect('main')
        except Exception as e:
            print(e)
            request.session['errorMessage'] = msg
            return redirect('main')
