from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from orders.models import Order

from .forms import LoginForm, ProfileForm, RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("users:profile")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)
            messages.success(request, "You are signed in.")
            return redirect(request.GET.get("next") or "products:home")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("products:home")


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=profile)
    orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]
    return render(request, "users/profile.html", {"form": form, "orders": orders})
