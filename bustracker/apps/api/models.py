# -*- coding: utf-8 -*-

import uuid

from django.contrib.auth.models import User
from django.db import models


class AccessToken(models.Model):
    is_active = models.BooleanField(default=True)
    access_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
