# -*- coding: utf-8 -*-
from plone.supermodel import model
from zope import schema
from plone.autoform import directives
from plone.app.z3cform.widget import AjaxSelectFieldWidget


class ILLEntry(model.Schema):
    """ Dexterity Schema for entries to the LL database
    """

    customer = schema.Tuple(
        title=(u'Customer'),
        value_type=schema.TextLine(),
        missing_value=(),
        required=False
    )

    directives.widget(
        'customer',
        AjaxSelectFieldWidget,
        vocabulary="lessons.learned.vocabularies.Customer"
    )
