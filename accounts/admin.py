# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import AuditRecord, User

admin.site.register(User)
admin.site.register(AuditRecord)
