from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
import os
import datetime
import json
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
User = get_user_model()


def compress_image(image, size):
    img = Image.open(image)
    img.thumbnail(size, Image.ANTIALIAS)

    # Convert the image to BytesIO and save it
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)  # Adjust the quality as needed
    img_content = ContentFile(img_io.getvalue())

    # Create a new SimpleUploadedFile with the compressed image
    return SimpleUploadedFile(image.name, img_content.read(), content_type='image/jpeg')


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
