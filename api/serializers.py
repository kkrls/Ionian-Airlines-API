from rest_framework import serializers
from . import models

# Serializer to provide the JSON representation of the response to a GET request for flights.
# Fields are given different names to match the required JSON payload argument names set in the Spec.
class FlightSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source = 'number')
    departingAt = serializers.DateTimeField(source = 'scheduled')
    # using CharField serializer even though it is an Integer field in our Model, since the specification requires
    # a String representation of the capacity to be returned as part of the Json response.
    seatCapacity = serializers.CharField(source = 'max_seats')
    # returns calculated field method from model and returns as string, for the same reason as above.
    remainingSeats = serializers.CharField(source = 'remaining_seats')
    class Meta:
        model = models.Flight
        fields = ['code', 'origin', 'destination', 'departingAt', 'seatCapacity', 'remainingSeats']