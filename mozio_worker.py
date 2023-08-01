import sys
import time
from mozio_service import MozioService

mozio_reservation = MozioService()
search_params = {
            "start_address": "44 Tehama Street, San Francisco, CA, USA",
            "end_address": "SFO",
            "mode": "one_way",
            "pickup_datetime": "2023-12-01 15:30",
            "num_passengers": 2,
            "currency": "USD",
            "campaign": "Brayan Smith Garcia"
}
result = mozio_reservation.search_create(search_params)
search_id = result['search_id']

number_of_req = 0
accumulated_results = {}

# New search results are concatenated to meet API consideration
while number_of_req < 10:
    search_results = mozio_reservation.polling_search_results(search_id)
    more_coming = search_results.get('more_coming')
    if more_coming:
        if 'result' in accumulated_results:
            accumulated_results['results'].extend(search_results
                                                  .get('results'))
        else:
            accumulated_results = search_results
        number_of_req += 1
        time.sleep(2)
    else:
        if not accumulated_results:
            accumulated_results = search_results
        break

providers = accumulated_results['results']
provider_lowest_price = mozio_reservation.find_lowest_price(
    providers, 'Dummy External Provider')

# If the provider with the given name is not found, a message
# is printed and the execution of the code is stopped
if not provider_lowest_price:
    print("Provider with given name not found")
    sys.exit()

result_id = provider_lowest_price['result_id']
reservation_data = {
    "search_id": search_id,
    "result_id": result_id,
    "email": "smithgaspri@gmail.com",
    "country_code_name": "US",
    "phone_number": "8776665544",
    "first_name": "Brayan",
    "last_name": "Garcia",
    "airline": "AA",
    "flight_number": "123",
    "customer_special_instructions": "Just trying"
}
reservation = mozio_reservation.post_reservation(reservation_data)
time.sleep(3)

poll_reservation = mozio_reservation.poll_reservation(search_id)
print(f"The reservation has been made: {poll_reservation}")

reservation_id = poll_reservation['reservations'][0]['id']
reservation_cancellation = mozio_reservation.reservation_cancellation(
    reservation_id)
print(f"The reservation has been canceled : {reservation_cancellation}")
