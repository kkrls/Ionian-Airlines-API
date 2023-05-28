from django.urls import path
from . import views

# URLS for our endpoints, according to the Spec of CW1.
urlpatterns = [
    # Used for GET request to retrieve all available flights of Ionian Airlines.
    path('search/', views.search_all_flights),
    # Used for GET request to retrieve flights that match the URL parameters.
    path('search/<str:origin>/<str:destination>/<slug:date>/', views.search_flight),
    # Used for POST request to complete a booking.
    path('seat/book/', views.book_seat),
    # Used for DELETE request to cancel a booking.
    path('seat/cancel/', views.cancel_booking)
]