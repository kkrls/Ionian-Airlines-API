import json, requests
from .models import *

# Payment Provider API links to complete and cancel transactions
url = 'https://sc19ws2.pythonanywhere.com/PayZen/pay'
delete_url = 'https://sc19ws2.pythonanywhere.com/PayZen/'

# Function that creates a booking in the API's database.
def create_booking(name, payment, address, flight_code, scheduled_at):
    # Searches for flight that matches the code and date given (should only be one flight on that date, hence we don't use time too)
    flight = Flight.objects.get(number = flight_code, scheduled__date=scheduled_at)
    # If the flight exists and there are available seats, we proceed with the payment and booking.
    if flight != None and flight.remaining_seats > 0:
        # Makes payment and if succesfull, proceeds with the booking.
        transaction = make_payment(payment, address)
        if transaction:
            # Add the passenger to the DB
            passenger = Passenger.objects.create(name = name)
            passenger.save()
            # Create aand add a new booking to the DB
            booking = Booking.objects.create(passenger_id = passenger, flight_id = flight, seat_num = flight.remaining_seats)
            booking.save()
            # Update the flight's available seats to reflect that a booking has been made
            flight.current_seats += 1
            flight.save()
            # Transaction is saved to the DB, along with the transaction_id provided by the payment API
            # which is used to cancel the transaction.
            payment_prov = PaymentProvider.objects.get(id = 1)
            transaction = Transaction(seat_booking_id = booking, payment_prov_id = payment_prov, transaction_id = transaction)
            transaction.save()
            return booking

# Function that completes the payment with the Payment API.
def make_payment(payment, address):
    # We parse the address and payments details which were passed to the Airline API.
    address_json = json.loads(address)
    payment_json = json.loads(payment)
    # Body of JSON object used to POST a payment is created.
    data = {
        "customer": {
            "email": payment_json['email'],
            "billing_address": {
                "city": address_json['city'],
                "country": address_json['country'],
                "address_1": address_json['address_1'],
                "postcode": address_json['postcode']
            },
            "credit_card": {
                "name_on_card": payment_json['name_on_card'],
                "card_number": payment_json['card_number'],
                "cvv": payment_json['cvv'],
                "exp_month": payment_json['exp_month'],
                "exp_year": payment_json['exp_year']
                }
            },
            "value": float(payment_json['amount']),
            "currency": payment_json['currency'],
            "company": "Ionian Airlines"
        }
    # We POST the request and return the transaction_id if successful.
    response = requests.post(url, json=data)
    response_vals = json.loads(response.content)
    return response_vals['transaction_id']

# Function used to cancel a booking.
def cancel_booking(booking_ref):
    # Booking first is retrieved and checked if it exists.
    booking = Booking.objects.get(id= booking_ref)
    if booking:
        # We retrieve all relevant fields.
        passenger = Passenger.objects.get(id = booking.passenger_id.id)
        flight = Flight.objects.get(id = booking.flight_id.id)
        transaction = Transaction.objects.get(seat_booking_id = booking_ref)
        # The transaction_id is added as a URL parameter for the DELETE request to the payment API.
        request_url = delete_url + transaction.transaction_id
        # DELETE request is made
        response = requests.delete(request_url)
        # Current seats are updated
        flight.current_seats -= 1
        # Changes to relevant fields are saved, and the booking, passenger and transactions cancelled are deleted.
        flight.save()
        passenger.delete()
        transaction.delete()
        booking.delete()
        # If the DELETE request was successful we return 1, otherwise 0.
        if response.status_code == 202:
            return 1
        else:
            return 0