from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .viewsModules.login import LoginView
from .viewsModules.signup import SignUpView
from .viewsModules.otp import OTPView
from .viewsModules.dashboard import DashboardView
from .viewsModules.transaction import TransactionView
from .viewsModules.recurringPayment import RecurringPaymentView
from .viewsModules.setting import SettingView
from .viewsModules.logout import LogoutView
from .viewsModules.passbook import PassbookView
from .viewsModules.loan import LoanView
from .viewsModules.privacyPolicy import PrivacyPolicy


from .middleware.auth import login_required, check_If_Already_LogIn


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacyPolicy/', PrivacyPolicy.as_view(), name='privacyPolicy'),
    path('login/', check_If_Already_LogIn(LoginView.as_view()), name='login'),
    path('signup1/', check_If_Already_LogIn(SignUpView.as_view()), name='signup1'),
    path('signup2/', check_If_Already_LogIn(SignUpView.as_view()), name='signup2'),
    path('signup3/', check_If_Already_LogIn(SignUpView.as_view()), name='signup3'),
    path('signup4/', check_If_Already_LogIn(SignUpView.as_view()), name='signup4'),
    path('otp/', check_If_Already_LogIn(OTPView.as_view()), name='otp'),
    path('main/', login_required(DashboardView.as_view()), name='main'),
    path('card/', login_required(views.card), name='card'),
    path('chequebook/', login_required(PassbookView.as_view()), name='chequebook'),
    path('settings/', login_required(SettingView.as_view()), name='settings'),
    path('loan/', login_required(LoanView.as_view()), name='loan'),
    path('help/', login_required(views.help), name='help'),
    path('investment/', login_required(RecurringPaymentView.as_view()), name='investment'),
    path('transaction/', login_required(TransactionView.as_view()), name='transaction'),
    path('logout/', login_required(LogoutView.as_view()), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
