# -*- coding: utf-8 -*-
"""账号与身份审核领域模型。"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """平台用户：卖家、买家、管理员共用一张表，以 role 区分。"""

    ROLE_SELLER = "seller"
    ROLE_BUYER = "buyer"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_SELLER, "卖家"),
        (ROLE_BUYER, "买家"),
        (ROLE_ADMIN, "管理员"),
    ]

    STATUS_PENDING = "pending"
    STATUS_ACTIVE = "active"
    STATUS_SUPPLEMENT = "supplement"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "待审核"),
        (STATUS_ACTIVE, "已通过"),
        (STATUS_SUPPLEMENT, "待补充"),
        (STATUS_REJECTED, "未通过"),
    ]

    role = models.CharField("角色", max_length=10, choices=ROLE_CHOICES, default=ROLE_BUYER)
    phone = models.CharField("手机号", max_length=11, unique=True)
    email = models.EmailField("找回邮箱", unique=True)
    nickname = models.CharField("昵称", max_length=30, blank=True)
    college = models.CharField("学院或年级", max_length=50, blank=True)
    contact = models.CharField("联系方式", max_length=50, blank=True)
    audit_status = models.CharField(
        "审核状态", max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    audit_note = models.TextField("审核说明", blank=True)
    created_at = models.DateTimeField("注册时间", auto_now_add=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return f"{self.username}({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_seller(self):
        return self.role == self.ROLE_SELLER

    @property
    def can_business(self):
        """是否可进入业务系统：管理员预置可登录；卖家/买家需审核通过。"""
        if self.is_admin:
            return True
        return self.audit_status == self.STATUS_ACTIVE


class AuditRecord(models.Model):
    """身份审核记录：保存审核人、时间、结果和说明，不可覆盖。"""

    RESULT_APPROVED = "approved"
    RESULT_SUPPLEMENT = "supplement"
    RESULT_REJECTED = "rejected"
    RESULT_CHOICES = [
        (RESULT_APPROVED, "通过"),
        (RESULT_SUPPLEMENT, "待补充"),
        (RESULT_REJECTED, "未通过"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audit_records", verbose_name="被审核用户")
    auditor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="audits", verbose_name="审核人"
    )
    result = models.CharField("审核结果", max_length=12, choices=RESULT_CHOICES)
    note = models.TextField("原因说明", blank=True)
    created_at = models.DateTimeField("审核时间", auto_now_add=True)

    class Meta:
        verbose_name = "审核记录"
        verbose_name_plural = "审核记录"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} {self.get_result_display()}"
