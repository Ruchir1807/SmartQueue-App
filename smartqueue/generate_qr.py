import os
import django
import qrcode

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartqueue.settings")
django.setup()

from queuesystem.models import Service

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

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Sanitize filename
        safe_name = service_name.replace(" ", "_")
        filename = os.path.join(output_folder, f"{safe_name}_qr.png")
        img.save(filename)
        print(f"QR code saved for '{service_name}' -> {filename}")

print("All QR codes generated successfully!")

