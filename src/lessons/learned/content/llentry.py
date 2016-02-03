# -*- coding: utf-8 -*-
from plone.supermodel import model
from zope import schema
from plone.autoform import directives
from plone.app.z3cform.widget import AjaxSelectFieldWidget


class ILLEntry(model.Schema):
    """ Dexterity Schema for entries to the LL database
    """

    customer = schema.TextLine(
        title=(u'Customer'),
        required=True
    )

    directives.widget(
        'customer',
        AjaxSelectFieldWidget,
        vocabulary="lessons.learned.vocabularies.Customer"
    )
