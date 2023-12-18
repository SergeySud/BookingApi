# BookingApi
Application setup:
1. Download dependencies from requirements.txt
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

```/admin/``` - you can access the admin panel here by logging in a superuser account.

```/accounts/register``` - the endpoint is available without authentication. The endpoint accepts only POST requests. The endpoint accepts the demands the following parameters in request body:
```
{
    "username": "user2",
    "password": "1",
    "password2": "1"
}
```

```/booking/rooms/``` - the endpoint is available without authentication. The endpoint accepts only GET requests.

You can use  the following parameters in URL to filter and sort available rooms.
```
/booking/rooms/?price_per_day=10&guests_number=1&reservation_start_date=2023-12-02&reservation_end_date=2023-12-03
```


```/booking/reservations/``` - the endpoint is available only for authorized users.

Sending a GET request will result in a response with a list of reservation for the user. The endpoint demands to send any data in 'user' parameter:
```/booking/reservations/?user=Anydata```

Sending a POST request will add a reservation for the user. The endpoint demands the following parameters:
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
