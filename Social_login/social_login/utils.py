import random
from datetime import datetime

import requests
from pyotp import TOTP

from Social_login import settings
from social_login import mapper
from social_login.exceptions import NoneServiceError
from social_login.models import User


# class Otp_Services:
#
#     def __int__(self, service=settings.SERVICE):
#         self.service = service
#         self.url = mapper.fast2sms_url
#
#     def fast2sms_service(self, message, phone_number):
#         import pdb;
#         pdb.set_trace()
#         payload = f"sender_id=FSTSMS&message={message}&language=english&route=p&numbers={phone_number}"
#
#         headers = {
#             'authorization': settings.FAST2SMS_API_KEY,
#             'Content-Type': "application/x-www-form-urlencoded",
#             'Cache-Control': "no-cache",
#         }
#         response = requests.request("POST", self.url, data=payload, headers=headers)
#         if response.status_code == 200:
#             return "OTP sent Successfully"
#
#         return "Phone number does not exist !!!"
#
#     def msg91_service(self, message, phone_number):
#         pass
#

class Otp_Verification:
    def __init__(self, interval=120):
        self.interval = interval
        self.current = None
        self.time_otp = TOTP('base32secret3232', interval=self.interval)
        self.otp = None

    def generate_otp(self):
        self.current = datetime.now()
        self.otp = self.time_otp.now()

    def send_otp(self,phone_number):
        self.generate_otp()
        # self.service.fast2sms_service(self.otp, phone_number)
        payload = f"sender_id=FSTSMS&message={self.otp}&language=english&route=p&numbers={phone_number}"

        headers = {
            'authorization': settings.FAST2SMS_API_KEY,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", self.url, data=payload, headers=headers)
        if response.status_code == 200:
            return "OTP sent Successfully"

        return "Phone number does not exist !!!"

    def verify_otp(self, otp_received):
        if self.otp == str(otp_received):
            return True
        return False

    def expired(self):
        if not self.otp == self.time_otp.now():
            return True
        return False


def generate_username(cleaned_data):
    username = cleaned_data.get('first_name').replace(' ', '_').lower()\
                       + cleaned_data.get('last_name').lower() + str(random.randint(1, 100))
    while User.objects.filter(username=username).exists():
        username = cleaned_data.get('first_name').replace(' ', '_').lower() \
                   + cleaned_data.get('last_name').lower() + str(random.randint(1, 100))
    return username


