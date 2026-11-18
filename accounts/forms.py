# -*- coding: utf-8 -*-
"""账号相关表单：注册、资料、审核。"""
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


PHONE_RE = re.compile(r"^1[3-9]\d{9}$")


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput, min_length=6)
    confirm = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "role", "phone", "email", "nickname", "college", "contact"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("请填写 11 位有效手机号")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("该手机号已注册")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已注册")
        return email

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if role == User.ROLE_ADMIN:
            raise forms.ValidationError("管理员不开放注册")
        return role

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm"):
            self.add_error("confirm", "两次密码不一致")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.audit_status = User.STATUS_PENDING
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname", "phone", "email", "college", "contact"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("请填写 11 位有效手机号")
        qs = User.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("该手机号已被使用")
        return phone


class LoginForm(AuthenticationForm):
    """登录表单：不提交角色，角色由服务端从数据库读取。"""

    username = forms.CharField(label="账号")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)


class AuditForm(forms.Form):
    result = forms.ChoiceField(
        label="审核结果",
        choices=[
            (User.STATUS_ACTIVE, "通过"),
            (User.STATUS_SUPPLEMENT, "待补充"),
            (User.STATUS_REJECTED, "未通过"),
        ],
    )
    note = forms.CharField(label="原因说明", widget=forms.Textarea, required=False)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("result") != User.STATUS_ACTIVE and not cleaned.get("note"):
            self.add_error("note", "待补充或未通过必须填写原因")
        return cleaned
