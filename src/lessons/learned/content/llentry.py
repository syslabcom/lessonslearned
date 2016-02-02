# -*- coding: utf-8 -*-
from plone.supermodel import model
from zope import schema
from plone.autoform import directives
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.content.browser.vocabulary import _permissions

class ILLEntry(model.Schema):
    """ Dexterity Schema for entries to the LL database
    """

    customer = schema.TextLine(
        title=(u'Customer'),
        required=True
    )
    _permissions['lessons.learned.vocabularies.Customer'] = 'View'
    directives.widget(
        'customer',
        AjaxSelectFieldWidget,
        vocabulary="lessons.learned.vocabularies.Customer"
    )
