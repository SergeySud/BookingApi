# BookingApi
Application setup:
1. Download dependencies: Django, djangorestframework, psycopg2
2. Create a new user and a new database or edit DATABASES parametrs in settings.py
3. Apply migrations:
```python manage.py makemigrations```
```python manage.py migrate```
4. Create a superuser:
```python manage.py createsuperuser```
5. Run server:
```python manage.py runserver```
6. The app uses BasicAuth.

API documentation:
API has the following endpoints: 

```/admin/``` - you can access the admin panel here by loging in a superuser account.

```/accounts/register``` - the endpoint is avaliable without authentifaction. The endpoint accepts only POST requests. The endpoint accepts the demands the following parametrs in request body:
```
{
    "username": "user2",
    "password": "1",
    "password2": "1"
}
```

```/booking/rooms/``` - the endpoint is avaliable without authentifaction. The endpoint accepts only GET requests.

You can send the following parametrs to filter and sort avaliable rooms.
```
    "guests_number": 1,
    "sort_by": "price_per_day",
    "reservation_start_date": "2023-12-02", 
    "reservation_end_date": "2023-12-03",
```
You can use "name", "price_per_day", "guests_number" parametrs for sorting.


```/booking/reservations/``` - the endpoint is avaliable only for autahrized users.

Sending a GET request will result in a response with a list of reservation for the user.

Sending a POST request will add a reservation for the user. The endpoint demands the following parametrs:
```
{
    "reservation_start_date": "2023-11-01",
    "reservation_end_date": "2023-11-10",
    "room": 3
}
```

Sending a DELETE request will delete a reservation for the user or by a superuser. The endpoint demands id of the reservation:
```
{
    "id": 3
}
```
