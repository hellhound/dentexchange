# -*- coding:utf-8 -*-
from django.views.generic.list import ListView
from .. import constants


class DentexchangeListView(ListView):
    paginate_by = constants.PAGINATE_BY
