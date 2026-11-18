# -*- coding: utf-8 -*-
"""账号视图：注册、登录退出、资料、身份审核。"""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import AuditForm, LoginForm, ProfileForm, RegisterForm
from .models import AuditRecord, User


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("items:home")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "注册成功，请等待管理员审核后登录。")
        return redirect("accounts:login")
    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        return redirect("items:home")
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        if not user.is_active:
            messages.error(request, "账号已停用，请联系管理员。")
            return render(request, "accounts/login.html", {"form": form})
        if not user.can_business:
            messages.warning(request, f"账号当前状态：{user.get_audit_status_display()}，暂不能进入业务系统。")
            return render(request, "accounts/login.html", {"form": form})
        login(request, user)
        return redirect("items:home")
    return render(request, "accounts/login.html", {"form": form})


@require_http_methods(["POST"])
@login_required
def user_logout(request):
    logout(request)
    return redirect("items:home")


@login_required
def profile(request):
    user = request.user
    form = ProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, "资料已保存。")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def audit_list(request):
    if not request.user.is_admin:
        messages.error(request, "无权限访问。")
        return redirect("items:home")
    users = User.objects.exclude(role=User.ROLE_ADMIN).order_by("-created_at")
    return render(request, "accounts/audit_list.html", {"users": users})


@login_required
@require_http_methods(["GET", "POST"])
def audit_detail(request, pk):
    if not request.user.is_admin:
        messages.error(request, "无权限访问。")
        return redirect("items:home")
    target = get_object_or_404(User, pk=pk)
    form = AuditForm(request.POST or None)
    if form.is_valid():
        result = form.cleaned_data["result"]
        note = form.cleaned_data["note"]
        target.audit_status = result
        target.audit_note = note
        target.save()
        AuditRecord.objects.create(
            user=target, auditor=request.user, result=result, note=note
        )
        messages.success(request, "审核结果已保存。")
        return redirect("accounts:audit_list")
    records = target.audit_records.all()
    return render(request, "accounts/audit_detail.html", {
        "target": target, "form": form, "records": records,
    })
