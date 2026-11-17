"""The TOTP step staff pass after signing in when ADMIN_REQUIRE_2FA is on."""

from django import forms
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django_otp import login as otp_login
from django_otp import match_token


class TokenForm(forms.Form):
    token = forms.CharField(
        label="6-digit code from your authenticator app",
        max_length=8,
        widget=forms.TextInput(attrs={"autocomplete": "one-time-code", "inputmode": "numeric", "autofocus": True}),
    )


@login_required(login_url="admin:login")
def verify_otp(request):
    target = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(target, {request.get_host()}, require_https=request.is_secure()):
        target = "admin:index"

    form = TokenForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        device = match_token(request.user, form.cleaned_data["token"])
        if device is not None:
            otp_login(request, device)
            return redirect(target)
        form.add_error("token", "That code is not valid. Check your device’s clock and try again.")

    context = {**admin.site.each_context(request), "form": form, "title": "Two-step verification"}
    return render(request, "admin/otp_verify.html", context)
