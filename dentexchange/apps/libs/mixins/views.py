# -*- coding:utf-8 -*-
import urlparse

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http.response import HttpResponseBadRequest

from .base import Mixin
from .. import strings


class SuccessURLAliasViewMixin(Mixin):
    def get_success_url(self):
        return reverse(self.success_url_alias)


class HttpRefererViewMixin(Mixin):
    def get(self, request, referers=None, *args, **kwargs):
        from_referer = urlparse.urlsplit(
            request.META.get('HTTP_REFERER', '')).path
        if referers is not None \
                and all(map(lambda r: unicode(r) != from_referer, referers)):
            return HttpResponseBadRequest(
                strings.HTTP_REFERER_VIEW_MIXIN_FORM_VIEW_BAD_REQUEST \
                % from_referer)
        return self.base_impl(
            HttpRefererViewMixin, self).get(request, args, kwargs)


class KwargsUserFormViewMixin(Mixin):
    def get_form_kwargs(self):
        kwargs = self.base_impl(KwargsUserFormViewMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
