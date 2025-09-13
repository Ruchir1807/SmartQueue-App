import os
import django
import qrcode

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartqueue.settings")
django.setup()

from queuesystem.models import Service  # Import your Service model

# Folder to save QR codes
output_folder = "qrcodes"
os.makedirs(output_folder, exist_ok=True)

# Base URL for QR codes
BASE_URL = "http://127.0.0.1:8000/join_queue_qr/?service="

# Get all services from the database
services = Service.objects.all()

if not services:
    print("No services found in the database!")
else:
    for service in services:
        service_name = service.name
        url = f"{BASE_URL}{service_name}"
        qr = qrcode.make(url)
        filename = os.path.join(output_folder, f"{service_name}_qr.png")
        qr.save(filename)
        print(f"QR code saved for '{service_name}' -> {filename}")

print("All QR codes generated successfully!")

