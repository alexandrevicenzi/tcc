# -*- coding: utf-8 -*-

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AccessToken(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Ativo'), default=True)
    access_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=_(u'Usuário'))

    class Meta:
        verbose_name = _(u'Token de Acesso')
        verbose_name_plural = _(u'Tokens de Acesso')
