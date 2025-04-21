from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'isLogin' in request.session and 'customerId' in request.session:
            isLogin = request.session['isLogin']
            if isLogin == True:
                return view_func( request, *args, **kwargs)
        
        request.session.flush()
        return redirect(reverse('login'))

    return wrapped_view

def check_If_Already_LogIn(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'isLogin' in request.session and 'customerId' in request.session:
            isLogin = request.session['isLogin']
            if isLogin == True:
                return redirect(reverse('main'))
                
        return view_func( request, *args, **kwargs)

    return wrapped_view