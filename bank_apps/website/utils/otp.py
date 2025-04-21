import time
import random
from django.conf import settings
from django.core.mail import send_mail


class OTPHandler:
    def __init__(self, request, emailId):
        self.request = request
        self.TTL = 180  # 2 minutes
        self.emailId = emailId
        self.OTP_KEY = 'OTP_' + emailId
        self.OTP_TTL_KEY = 'OTP_TTL_' + emailId

        self.invalidOTPMsg = 'Invalid OTP. Please Enter valid OTP.'
        self.expiredOTPMsg = 'OTP Expired! Please retry.'
        self.successMsg = 'Success.'
        self.SWW = 'Something went wrong! Please retry.'

    def _generateOTP(self):
        return random.randint(100000, 999999)

    def _isExpired(self):
        current_time = time.time()
        otpTTL = self.request.session[self.OTP_TTL_KEY]
        return current_time - otpTTL <= self.TTL

    def _resetOTPKeys(self):
        try:
            del self.request.session[self.OTP_KEY]
            del self.request.session[self.OTP_TTL_KEY]
        except:
            pass

    def _sendMail(self, otp):
        subject = 'OTP Mail'
        message = f'Hi this is your OTP {otp}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.emailId]
        send_mail(subject, message, email_from, recipient_list)

    def sentOTP(self):
        otp = self._generateOTP()
        self.request.session[self.OTP_KEY] = otp
        self.request.session[self.OTP_TTL_KEY] = time.time()

        # send OTP on mail
        # self._sendMail(otp);
        print(f"YOUR OTP IS {otp}")

    def validateOTP(self, enteredOTP):
        try:
            otp = self.request.session[self.OTP_KEY]
            if self._isExpired() == False:
                self._resetOTPKeys()
                return False, self.expiredOTPMsg

            if str(otp) != str(enteredOTP):
                return False, self.invalidOTPMsg

            self._resetOTPKeys()
            return True, self.successMsg
        except:
            return False, self.SWW
