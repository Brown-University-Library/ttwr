# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json


BIO_BOOKS = json.dumps(
{
    'items': {
        'numFound': 0,
        'docs': [],
    }
}
)

BIO_PRINTS = json.dumps(
{
    'items': {
        'numFound': 0,
        'docs': [],
    }
}
)

ANNOTATIONS = json.dumps(
{
    'response': {
        'numFound': 1,
        'docs': [{'rel_is_annotation_of_ssim': ['test:1234']}],
    }
}
)

PAGES = json.dumps(
{
    'response': {
        'numFound': 1,
        'docs': [{'pid': 'test:5678'}],
    }
}
)
