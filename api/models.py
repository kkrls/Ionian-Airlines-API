from django.db import models
import datetime

# All models created according to the spec of CW1, including relationships and exact column names.

# Database model for Flights.
class Flight(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Flight ID')
    number = models.CharField('Flight Code', max_length=7, unique=True, default="ION1234")
    origin = models.CharField('Departing Airport', max_length=3, default= 'CFU')
    destination = models.CharField('Arrival Airport', max_length=3, default= 'ATH')
    scheduled = models.DateTimeField('Departure Time', default= datetime.datetime(2023, 12, 31, 12, 00))
    max_seats = models.PositiveIntegerField('Maximum Seat Capacity', default= 120)
    current_seats = models.PositiveIntegerField('Current Booked Seats', default= 0)

    # Returns the string representation of the Flight Id, used in the Admin panel.
    def __str__(self):
        return self.number
    
    # Calculates available remaining seats.
    @property
    def remaining_seats(self):
        return self.max_seats - self.current_seats
    
# Database model for Passengers.
class Passenger(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Passenger ID')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Database model for Bookings.
class Booking(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Booking ID')
    passenger_id = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_num = models.IntegerField(default=0)

    # Returns a string representation of Passenger ID, to be presented in the Admin panel.
    @property
    def get_passenger_id(self):
        return self.passenger_id.id

# Database model for Payment Providers.
class PaymentProvider(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Payment Provider ID')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Database model for Transactions. 
class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Transaction ID')
    seat_booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_prov_id = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length= 50)
