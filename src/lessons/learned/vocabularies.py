from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from binascii import b2a_qp
from Products.CMFPlone.utils import safe_unicode


@implementer(IVocabularyFactory)
class CustomerVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "Subject" index
    """

    def __call__(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, "portal_catalog", None)
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex('customer')

        def safe_encode(term):
            if isinstance(term, unicode):
                # no need to use portal encoding for transitional encoding from
                # unicode to ascii. utf-8 should be fine.
                term = term.encode('utf-8')
            return term

        # Vocabulary term tokens *must* be 7 bit values, titles *must* be
        # unicode
        items = [
            SimpleTerm(i, b2a_qp(safe_encode(i)), safe_unicode(i))
            for i in index._index
            if query is None or safe_encode(query) in safe_encode(i)
        ]

        return SimpleVocabulary(items)

CustomerVocabularyFactory = CustomerVocabulary()
