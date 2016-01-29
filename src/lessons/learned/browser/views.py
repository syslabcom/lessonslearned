from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

class QueryDbView(BrowserView):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.keywords = ['ldap','postgres','solr']
        self.customers = ['unspecific','star','denso','osha','unibw']
        self.entries = [
            {'title': 'AaAaAa',
             'text': 'Don\'t for get to bring a towel!',
             'keywords': ['ldap','solr'],
             'customer': 'unspecific'},
            {'title': 'BbBbBb',
             'text': 'Beware of ... ',
             'keywords': ['ldap','postgres'],
             'customer': 'denso'},
            {'title': 'CcCcCc',
             'text': 'Rememeber that ...',
             'keywords': ['solr','postgres'],
             'customer': 'unspecific'},
            {'title': 'DdDdDd',
             'text': 'It is absolutely crucial ...',
             'keywords': ['ldap'],
             'customer': 'osha'},
            {'title': 'EeEeEe',
             'text': 'In some cases ...',
             'keywords': ['solr'],
             'customer': 'unibw'},
            {'title': 'FfFfFf',
             'text': 'Keep in mind that ...',
             'keywords': ['postgres'],
             'customer': 'star'},
        ]
        return super(QueryDbView, self).__call__()

    def customers(self):
        return self.customers

    def keywords(self):
        return self.keywords

    def results(self):
        results = []
        for e in self.entries:
            keywords_match = False
            customer_matches = False
            if 'keywords' not in self.request.form:
                keywords_match = True
            else:
                if not isinstance(self.request.form['keywords'], list):
                    self.request.form['keywords'] = [self.request.form['keywords']]
                matches = set.intersection(set(self.request.form['keywords']),set(e['keywords']))
                if matches:
                    keywords_match = True
            if self.request.form['customer'] == e['customer'] or self.request.form['customer'] == 'unspecific' or e['customer'] == 'unspecific':
                customer_matches = True
            if keywords_match and customer_matches:
                results.append(e)
               
        return results

# keywords:
# - schnittmenge ist nicht leere menge -> uebereinstimmung
# - keyword in request = [] -> uebereinstimmung

# kunde:
# - kunde in request == unspecific -> uebereinstimmung
# - kunde in entry == unspecific -> uebereinstimmung
# - kunde gleich -> uebereinstimmung


    def is_post(self):
        return self.request.method == 'POST'

    def keywords_as_string(self, entry):
        res = ''
        for k in entry['keywords']:
            res += k + ' '
        return res


class UpdateDbView(BrowserView):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.keywords = ['ldap','postgres','solr']
        self.customers = ['unspecific','star','denso','osha','unibw']
        self.messages = IStatusMessage(self.request)
        if self.is_post():
            self.process_data()
        return super(UpdateDbView, self).__call__()

    def customers(self):
        return self.customers

    def keywords(self):
        return self.keywords

    def is_post(self):
        return self.request.method == 'POST'

    def process_data(self):
        self.messages.add(u'The entry has been added to the database', type=u'info')
        return

    def keywords_as_string(self, entry):
        res = ''
        for k in entry['keywords']:
            res += k + ' '
        return res

## achtung: evtl. kann es probleme geben, weil ein einzelnes keyword nicht als liste, sondern einfach als string uebergeben wird

## dran denken, dass entries ohne kundenbezug auch angezeigt werden sollten, wenn entries fuer einen bestimmten kunden angefragt werden
## umgekehrt sollen alle passenden entries angezeigt werden, wenn man bbei einer anfrage keinen kunden angibt

## dran denken, dass man bei neuen eintraegen mindestens ein keyword angeben muss
#keywords UND kunde muessen uebereinstimmen

