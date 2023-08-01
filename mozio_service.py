import requests


class MozioService:
    def __init__(self) -> None:
        self.api_url = 'https://api-testing.mozio.com/v2/'
        self.headers = {
            'API-KEY': '6bd1e15ab9e94bb190074b4209e6b6f9',
            'LANG': 'es-ES'
        }

    def search_create(self, search_params):
        url = self.api_url + 'search/'
        r = requests.post(url=url, headers=self.headers, data=search_params)
        general_search = r.json()
        return general_search

    def polling_search_results(self, search_id):
        url = self.api_url + 'search/%s/poll/' % search_id
        r = requests.get(url=url, headers=self.headers)
        search = r.json()
        return search

    def post_reservation(self, reservation_data):
        url = self.api_url + 'reservations/'
        r = requests.post(url=url, headers=self.headers, data=reservation_data)
        reservation = r.json()
        return reservation

    def poll_reservation(self, search_id):
        url = self.api_url + 'reservations/%s/poll/' % search_id
        r = requests.get(url=url, headers=self.headers)
        poll_reservation = r.json()
        return poll_reservation

    def reservation_cancellation(self, reservation_id):
        url = self.api_url + 'reservations/%s/' % reservation_id
        r = requests.delete(url=url, headers=self.headers)
        reservation_cancelation = r.json()
        return reservation_cancelation

    def find_lowest_price(self, list_providers, provider_name):
        provider_set = [prov for prov in list_providers if
                        prov.get("steps")[0].get("details").
                        get("provider_name") == provider_name]
        provider_set.sort(key=lambda x: float(x.get("total_price")
                                              .get("total_price")
                                              .get("value")))
        provider_lower_price = provider_set[0] if provider_set else None
        return provider_lower_price
