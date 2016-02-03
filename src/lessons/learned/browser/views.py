from Products.CMFPlone.browser.search import Search
from Products.CMFCore.utils import getToolByName
from Products.ZCTextIndex.ParseTree import ParseError
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFPlone.PloneBatch import Batch
from zope.site.hooks import getSite
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.AdvancedQuery import Eq, Or, And


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
        if self.request.form.get('customer', '') == 'All':
            del self.request.form['customer']
        results = super(LLFulltextSearchView, self).results(
            query, batch, b_size, b_start, use_content_listing)

        return results


class LLSearchView(Search):

    def subjects_list(self):
        site = getSite()
        self.catalog = getToolByName(site, "portal_catalog", None)
        if self.catalog is None:
            return []
        index = self.catalog._catalog.getIndex('Subject')
        return [subject for subject in index._index]

    def customers_list(self):
        factory = getUtility(IVocabularyFactory,
                             'lessons.learned.vocabularies.Customer')
        vocabulary = factory(self.context)
        return (
            ['No matches by customer'] +
            [term.value for term in vocabulary] +
            ['All']
        )

    def results(self, query=None, batch=True, b_size=10, b_start=0,
                use_content_listing=True):
        """ Get properly wrapped search results from the catalog.
        Everything in Plone that performs searches should go through this view.
        'query' should be a dictionary of catalog parameters.
        """
        if query is None:
            query = {}
        query['portal_type'] = 'llentry'
        # if self.request.form.get('customer','') == 'All':
        #     del self.request.form['customer']
        if batch:
            query['b_start'] = b_start = int(b_start)
            query['b_size'] = b_size
        query = self.filter_query(query)

        advanced_query = self.transform_query(query)
        if query is None:
            results = []
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            try:
                results = catalog.evalAdvancedQuery(advanced_query)
            except ParseError:
                return []

        if use_content_listing:
            results = IContentListing(results)
        if batch:
            results = Batch(results, b_size, b_start)
        return results

    def transform_query(self, query):
        search_indexes = []
        other_indexes = []
        search_keys = ('customer', 'Subject', 'No matches by customer')
        for key in query.keys():
            if key in ('b_start', 'b_size', 'batch', 'show_inactive'):
                continue
            if key in search_keys:
                if key == 'customer' and query['customer'] == 'All':
                    for customer in self.customers_list():
                        if customer in ('All', 'No matches by customer'):
                            continue
                        search_indexes.append(Eq('customer', customer))
                elif (key == 'customer' and
                      query['customer'] == 'No matches by customer'):
                    pass
                else:
                    self.add_to_index_list(search_indexes, query, key)
            else:
                self.add_to_index_list(other_indexes, query, key)
        other_indexes = And(*other_indexes)
        search_indexes = Or(*search_indexes)
        return And(other_indexes, search_indexes)

    def add_to_index_list(self, index_list, dic, key):
        if isinstance(dic[key], list):
            for val in dic[key]:
                index_list.append(Eq(key, val))
        else:
            index_list.append(Eq(key, dic[key]))
