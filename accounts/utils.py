import datetime
import json
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
User = get_user_model()

url = "https://api.sendchamp.com/api/v1/verification/create"


def send_otp(phone_number, otp):
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
        'Authorization': "Bearer sendchamp_live_$2a$10$SPoBf4VaLDbsxwk2JzKqj.Fvy1ALyPECJokxL1WLoMUhY.llUH7FS"
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        response_data = response.json()
        # Extract relevant information from the response_data if needed
        print(response_data)
        # Return your own success response here
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
        print("Response:", response.text)


def verify_otp(phone_number, otp):
    try:
        user = User.objects.get(phone_number=phone_number)

        # Check if the OTP is expired
        current_time = datetime.datetime.now()
        if user.otp_expiry and current_time > user.otp_expiry:
            return False

        # Check if the provided OTP matches the stored OTP
        if user.otp == otp:
            return True
    except User.DoesNotExist:
        pass

    return False
