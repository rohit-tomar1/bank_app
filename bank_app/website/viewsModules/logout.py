from django.views import View
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ..repositories.customer import CustomerRepository


@method_decorator(never_cache, name='dispatch')
class LogoutView(View):

    def get(self, request):
        CustomerRepository.deleteUserSession(request)
        return redirect('login')
