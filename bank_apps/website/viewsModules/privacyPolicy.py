from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


from ..repositories.userRequest import UserRequestRepository


@method_decorator(never_cache, name='dispatch')
class PrivacyPolicy(View):
    def get(self, request):
        return render(request, 'privacyPolicy.html')