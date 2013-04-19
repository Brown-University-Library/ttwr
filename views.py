# -*- coding: utf-8 -*-

from django.http import HttpResponse


def stub( request ):
    return HttpResponse( u'still under construction' )
