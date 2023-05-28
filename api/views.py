from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, QueryDict
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from . import models, serializers, bookings
from datetime import datetime
import json

# Views that respond to the HTTP requests defined in the Spec of CW1 and match the Urls set in urls.py
# All methods check if the appropriate HTTP verb has been used and if not, return a 403 Forbidden response.

# Responds to POST request and provides a list of available flights.
@csrf_exempt
def search_all_flights(request):
    if request.method == 'GET':
        flights_list = models.Flight.objects.all()
        out = serializers.FlightSerializer(flights_list, many = True)
        data = {'flights': out.data}
        return JsonResponse(data)
    else:
        return HttpResponseForbidden()

# Responds to POST request and provides a list of available flights that match the specified URL parameters.
@csrf_exempt
def search_flight(request, origin, destination, date):
    if request.method == 'GET':
        date_obj = datetime.strptime(date, '%d-%m-%Y').date()
        flights_list = models.Flight.objects.filter(origin=origin, destination=destination, scheduled__date=date_obj)

        out = serializers.FlightSerializer(flights_list, many = True)
        data = {'flights': out.data}
        return JsonResponse(data)
    else:
        return HttpResponseForbidden()

# Responds to POST request to create a booking, details are provided as JSON payload.
@csrf_exempt
def book_seat(request):
    if request.method == 'POST' and request.body != None:
        # Tries to retrieve the relevant data from the POST request.
        try: 
            name = request.POST['passengerName']
            payment = request.POST['payment']
            address = request.POST['address']
            flight_code = request.POST['flightNumber']
            scheduled_at = request.POST['scheduledAt']
            # Booking is created if all fields required are present.
            booking = bookings.create_booking(name,payment, address, flight_code, scheduled_at)
            # If the booking is succesfully created, returns a JSON response in accordance to the Spec.
            if(booking):
                print("Succesful Booking!")
                data = {
                    "status": "Created",
                    "reservation": {
                        "seatNumber" : booking.seat_num,
                        "bookingReference": booking.id
                    }
                }
                return JsonResponse(data = data, status = 201)
            # If the booking is unsuccessufl, returns a JSON response in accordance to the Spec.
            else:
                print("Payment failed, please try again.")
                data = {
                    "status": "Error",
                    "reservation": {
                    }
                }
                return JsonResponse(data = data, status=500)
        # If the request does not match the required format a code 400 Response is sent.
        except:
            data = "Failed Request! Check you have submitted the required request fields correctly."
            return JsonResponse(data = data, status=400, safe=False)
    else:
        return HttpResponseForbidden()

# Method used to cancel a booking.
@csrf_exempt
def cancel_booking(request):
    if request.method == 'DELETE' and request.body != None:
        # We try and load the JSON payload.
        try: 
            body = json.loads(request.body)
            booking_ref = body['bookingReference']
            # The booking reference is retrieved if it exists, and used to cancel the booking.
            cancellation = bookings.cancel_booking(booking_ref)
            # If the cancellation was successful, the JSON response according to the Spec is sent.
            if cancellation == 1:
                print("Cancellation was succesful!")
                data = {
                        "status": "Deleted",
                    }
                return JsonResponse(data= data, status = 202)
            # If the cancellation was unsuccessful, the JSON response according to the Spec is sent.
            else:
                print("Cancellation was unsuccessful!")
                data = {
                        "status": "Error",
                    }
                return JsonResponse(data= data, status = 500)
        # If any of the request data is invalid, the appropriate response is sent.
        except:
            data = "Failed request, check that booking exists and has not already been cancelled."
            return JsonResponse(data= data, status = 400, safe=False)
    else: 
        return HttpResponseForbidden()