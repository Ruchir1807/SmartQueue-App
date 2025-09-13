from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Service, Token
from .forms import JoinQueueForm, CheckStatusForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
import qrcode
import io
import base64



def home(request):
    return render(request,'queuesystem/home.html')


@login_required(login_url="login")
def join_queue(request):
    if request.method == 'POST':
        form = JoinQueueForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            student = request.user if request.user.is_authenticated else None
            count = Token.objects.filter(service=service, status="waiting").count() + 1
            token_number = f"{service.name[:2].upper()}-{count}"

            token = Token.objects.create(
                service=service,
                student=student,
                token_number=token_number,
                status="waiting"
            )

            # calculate queue position
            ahead = Token.objects.filter(service=service, status="waiting", id__lt=token.id).count()
            position = ahead + 1

            return render(request, 'queuesystem/token.html', {
                'token': token,
                'position': position
            })
    else:
        form = JoinQueueForm()

    return render(request, 'queuesystem/join_queue.html', {'form': form})


@login_required(login_url="login")
def check_status(request):
    # If superuser/staff → show all tokens
    if request.user.is_staff or request.user.is_superuser:
        tokens = Token.objects.all().order_by('-created_at')
    else:
        # If normal student → show only their tokens
        tokens = Token.objects.filter(student=request.user).order_by('-created_at')

    # Calculate positions for "waiting" tokens
    token_statuses = []
    for token in tokens:
        ahead = Token.objects.filter(
            service=token.service,
            status="waiting",
            id__lt=token.id
        ).count()
        position = ahead + 1 if token.status == "waiting" else 0

        token_statuses.append({
            "token": token,
            "position": position
        })

    return render(
        request,
        'queuesystem/check_status.html',
        {"token_statuses": token_statuses}
    )





@staff_member_required(login_url="login")
def counter_view(request):
    tokens = Token.objects.filter(status="waiting").order_by("created_at")

    if request.method == "POST":
        token_id = request.POST.get("token_id")
        action = request.POST.get("action")
        token = get_object_or_404(Token, id=token_id)
        if action == "serve":
            token.status = "served"
        elif action == "cancel":
            token.status = "cancelled"
        token.save()
        tokens = Token.objects.filter(status="waiting").order_by("created_at")

    return render(request, "queuesystem/counter.html", {"tokens": tokens})








def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "queuesystem/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def join_queue_qr(request):
    """
    Auto-join queue after scanning a QR code.
    QR code should contain ?service=<service_name>
    """
    service_name = request.GET.get("service")
    if not service_name:
        messages.error(request, "Invalid QR code!")
        return redirect("home")

    try:
        service = Service.objects.get(name=service_name)
    except Service.DoesNotExist:
        messages.error(request, "Service not found!")
        return redirect("home")

    student = request.user
    count = Token.objects.filter(service=service, status="waiting").count() + 1
    token_number = f"{service.name[:2].upper()}-{count}"

    token = Token.objects.create(
        service=service,
        student=student,
        token_number=token_number,
        status="waiting"
    )

    # Calculate queue position
    ahead = Token.objects.filter(service=service, status="waiting", id__lt=token.id).count()
    position = ahead + 1

    return render(request, 'queuesystem/token.html', {
        'token': token,
        'position': position
    })


