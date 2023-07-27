import os
import datetime
import json
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
User = get_user_model()


def format_phone_number(phone_number):
    # Remove all non-digit characters from the input phone number
    digits_only = ''.join(filter(str.isdigit, phone_number))

    # Extract the last 10 digits from the phone number
    last_10_digits = digits_only[-10:]

    # Add '234' to the beginning of the last 10 digits
    formatted_number = '234' + last_10_digits

    return formatted_number


def send_otp(formatted_number, otp):
    url = "https://api.sendchamp.com/api/v1/verification/create"

    payload = {
        "channel": "sms",
        "sender": "Sendchamp",
        "token_type": "numeric",
        "token_length": 4,
        "expiration_time": 5,
        "customer_email_address": "",
        "customer_mobile_number": formatted_number,
        "meta_data": {},
        "token": otp
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.getenv('SENDCHAMP_KEY')}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
