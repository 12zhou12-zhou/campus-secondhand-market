# -*- coding: utf-8 -*-
"""账号模块测试：注册校验、角色限制、登录状态。"""
from django.test import TestCase
from django.urls import reverse

from .models import User


class RegisterTests(TestCase):
    def test_buyer_register_ok(self):
        resp = self.client.post(reverse("accounts:register"), {
            "username": "buyer1", "role": User.ROLE_BUYER, "phone": "13800000001",
            "email": "buyer1@example.com", "nickname": "买家一", "college": "计算机2401",
            "contact": "13800000001", "password": "pass12345", "confirm": "pass12345",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="buyer1").exists())

    def test_admin_cannot_register(self):
        resp = self.client.post(reverse("accounts:register"), {
            "username": "adminx", "role": User.ROLE_ADMIN, "phone": "13800000002",
            "email": "adminx@example.com", "password": "pass12345", "confirm": "pass12345",
        })
        form = resp.context["form"]
        self.assertFormError(form, "role", "管理员不开放注册")

    def test_duplicate_phone_rejected(self):
        User.objects.create_user(username="u1", phone="13800000003", email="u1@example.com", password="x")
        resp = self.client.post(reverse("accounts:register"), {
            "username": "u2", "role": User.ROLE_BUYER, "phone": "13800000003",
            "email": "u2@example.com", "password": "pass12345", "confirm": "pass12345",
        })
        form = resp.context["form"]
        self.assertFormError(form, "phone", "该手机号已注册")


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="seller1", role=User.ROLE_SELLER, phone="13800000004",
            email="s1@example.com", password="pass12345",
        )

    def test_pending_user_cannot_enter_business(self):
        resp = self.client.post(reverse("accounts:login"), {
            "username": "seller1", "password": "pass12345",
        })
        self.assertFalse(resp.wsgi_request.user.is_authenticated)
