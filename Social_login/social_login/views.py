import random

import requests
from pyotp import TOTP
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView

from Social_login import settings
from Social_login.settings import EMAIL_HOST
from social_login.forms import UserSignUp, UserUpdateForm, PhoneNumber
from social_login.models import User
from social_login.tokens import account_activation_token
from social_login.utils import Otp_Verification, generate_username


def index(request):
    return render(request, "social_login/base.html")


def mail_send(to_mail, username, html_content, from_mail=EMAIL_HOST):
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(f'You need to activate and use username as : {username}', text_content,
                                 from_mail, [to_mail])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def phone_verification(request):
    counter = 0
    form = PhoneNumber()

    otp_verification = Otp_Verification(interval=60)

    if counter == 0:
        msg = otp_verification.send_otp(request.session.get("phone_number"))
        messages.info(request, msg)

    counter += 1

    if request.method == "POST":
        form = PhoneNumber(request.POST)
        if form.is_valid():
            counter = 0
            if otp_verification.expired():
                messages.error(request, "The session timed out and new otp send !!")
                return redirect('phone_verify')

            if otp_verification.verify_otp(form.cleaned_data.get("otp")):
                messages.success(request, "The phone number is verified and now you can login with that")
                return redirect('login')
            else:
                messages.error(request, "The otp entered is wrong")
                return redirect('phone_verify')
    return render(request, "social_login/phone_verify.html", {'form': form,
                                                              'phone_number': request.session.get("phone_number")})


def user_register(request):
    form = UserSignUp()
    if request.method == "POST":
        form = UserSignUp(request.POST, request.FILES)
        if form.is_valid():
            username = generate_username(form.cleaned_data)
            form.instance.username = username
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email = form.cleaned_data['email']

            html_content = render_to_string('social_login/email_confirmation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            mail_send(email, username, html_content)
            request.session['phone_number'] = user.phone_number

            return redirect("phone_verify")

    return render(request, "social_login/signup.html", {'form': form})


def authentication(username, password):
    user = authenticate(username=username, password=password)
    if not user:
            try:
                user = User.objects.get(phone_number=username)
                user = authenticate(username=user.username, password=password)
            except (ValueError, User.DoesNotExist):
                return None
    return user


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('update')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authentication(username, password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('update')
            else:
                messages.error(request, "Your account is not active yet")
        else:
            messages.error(request, "Invalid login details given")
        return redirect('login')
    else:
        return render(request, 'social_login/login.html', {})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('update')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('login')


@login_required
def user_update(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Profile Updated Successfully!!!!")
            form.save()
    return render(request, "social_login/update_profile.html", {"form": form})
