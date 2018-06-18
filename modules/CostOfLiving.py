import requests
from lxml import html


class CostOfLivingClient:

    def __init__(self):
        self.session = requests.session()
        self.countries = self._get_countries()

    def get_cities(self, country):
        if country not in self.countries:
            raise Exception('country {country} not supported'.format(country=country))
        response = self.session.get(
            'https://www.numbeo.com/cost-of-living/country_result.jsp?country={country}'.format(
                country=country.replace(' ', '+')
            )
        )
        html_tree = html.fromstring(response.content)
        return list(map(lambda x: x.text, html_tree.cssselect('.cityOrCountryInIndicesTable a')))

    def _get_countries(self):
        response = self.session.get('https://www.numbeo.com/cost-of-living/')
        html_tree = html.fromstring(response.content)
        return list(map(lambda x: x.text, html_tree.cssselect('table.related_links a')))

    def get_costs_for_city_for_currency(self, city, currency='USD'):
        response = self.session.get(
            'https://www.numbeo.com/cost-of-living/in/{city}?displayCurrency={currency}'.format(
                city=city.replace(' ', '-'),
                currency=currency
            )
        )
        html_tree = html.fromstring(response.content)
        rows = list(filter(lambda x: len(x.cssselect('td.priceValue')) > 0,
                           html_tree.cssselect('.data_wide_table tr')))
        return dict(
            map(
                lambda x: (
                    x.cssselect('td')[0].text,
                    float(x.cssselect('td')[1].text.replace('\xa0$', '').replace(',', ''))
                ),
                rows
            )
        )
