pythonanywhere URL: http://sc19kk.pythonanywhere.com/search/

Requests can be made to 4 endpoints:

To see all available flights :

GET request to http://sc19kk.pythonanywhere.com/search/

To see flight with specified parameters, e.g.: 

http://sc19kk.pythonanywhere.com/search/CFU/SKG/31-12-2023/


To make a booking you do a POST request to http://sc19kk.pythonanywhere.com/seat/book/,
using a JSON form-data payload, e.g.:

passengerName:Kostis
payment:{"email":"none@gmail.com","name_on_card":"Kostis","card_number":"2407199919992407","exp_month":"7","exp_year":"24","cvv":"123","amount":"100","currency":"GBP"}
address:{"address_1":"1 Clarendon Place","city":"Leeds","postcode":"LS29JY","country":"United Kingdom"}
flightNumber:ION1235
scheduledAt:2023-12-31

To cancel a booking, a DELETE request is made to http://sc19kk.pythonanywhere.com/seat/cancel/,
with a simple JSON payload, which includes the bookingReference to be deleted, e.g.:

{"bookingReference": "39"}

