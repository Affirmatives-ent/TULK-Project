import os
import datetime
import json
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
User = get_user_model()


def send_otp(phone_number, otp):
    url = "https://api.sendchamp.com/api/v1/verification/create"

    payload = {
        "channel": "sms",
        "sender": "Sendchamp",
        "token_type": "numeric",
        "token_length": 4,
        "expiration_time": 5,
        "customer_email_address": "",
        "customer_mobile_number": phone_number,
        "meta_data": {},
        "token": otp
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.getenv('SENDCHAMP_KEY')}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)


# def verify_otp(phone_number, otp):
#     try:
#         user = User.objects.get(phone_number=phone_number)

#         # Check if the OTP is expired
#         current_time = datetime.datetime.now()
#         if user.otp_expiry and current_time > user.otp_expiry:
#             return False

#         # Check if the provided OTP matches the stored OTP
#         if user.otp == otp:
#             return True
#     except User.DoesNotExist:
#         pass

#     return False
