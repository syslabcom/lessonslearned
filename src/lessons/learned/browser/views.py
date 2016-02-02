from Products.CMFPlone.browser.search import Search
from Products.CMFCore.utils import getToolByName
from Products.ZCTextIndex.ParseTree import ParseError
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFPlone.PloneBatch import Batch
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class LLFulltextSearchView(Search):
    def results(self, query=None, batch=True, b_size=10, b_start=0,
            use_content_listing=True):
        """ Get properly wrapped search results from the catalog.
        Everything in Plone that performs searches should go through this view.
        'query' should be a dictionary of catalog parameters.
        """
            
        if query is None:
            query = {}
        query['portal_type'] = 'llentry'
        results = super(LLFulltextSearchView, self).results(
            query, batch, b_size, b_start, use_content_listing)

        return results


class LLSearchView(LLFulltextSearchView):

    def subjects_list(self):
        site = getSite()
        self.catalog = getToolByName(site, "portal_catalog", None)
        if self.catalog is None:
            return []
        index = self.catalog._catalog.getIndex('Subject')
        return [subject for subject in index._index]

    def customers_list(self):
        factory = getUtility(IVocabularyFactory, 'lessons.learned.vocabularies.Customer')
        vocabulary = factory(self.context)
        return [term.value for term in vocabulary]


