from django.contrib import admin
from .models import Flight, Passenger, Booking, PaymentProvider, Transaction

# Modifies and registers the views of the tables for the admin panel.

class FlightAdmin(admin.ModelAdmin):
    list_display = ('number', 'origin', 'destination', 'scheduled')
    ordering = ('number',)
    search_fields = ('number',)

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id', )
    search_fields = ('id',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_passenger_id', 'flight_id')
    ordering = ('id', )
    search_fields = ('id',)

class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id', )
    search_fields = ('id',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'seat_booking_id', 'payment_prov_id')
    ordering = ('id', )
    search_fields = ('id',)

admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Transaction, TransactionAdmin)

