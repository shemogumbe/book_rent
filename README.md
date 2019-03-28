
## Product overview
 The project is used to calculate book rental charges for customers at a bookstore

## Development set up

#### Set up with docker
- 
    
- Create Application environment variables and save them in .env file
    ```
    
    ```
- Run application.
    
    ```
- Running migrations

   
 	```
     python manage.py makemigrations
 	```

    
 	```
     python manage.py migrate
 	```



    
- Run application.
    ```
    python manage.py runserver
    ```

- Running Tests
 ```
 python manage.py test -v 2
 ```
 
## Built with
- Python version  3
- Django
- Djangorestframework
- Postgres

## Endpoints
Add books or list books(post/get)
```
/api/books
```

Edit/delete/retrieve books
```
/api/books/<pk>
```
Add customers or list customers(post/get)
```
/api/customers
```

Edit/delete/retrieve customers
```
/api/customers/<pk>
```

Add customers or list customers book rentals(post/get)
```
/api/customer_book
```

Edit/delete/retrieve customer book rentals
```
/api/customer_book/<pk>
```

Calculate customer rental charges for all his/her books in db
```
/api/calculate_rent
```

date format
```
{"user": <id>}
```

Checkout a customer 
```
/api/checkout
```
data format
```
 {
"user": 2,
"books": [
 {"book": 2},
 {"book":3}
]
}
```
