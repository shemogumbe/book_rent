import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Book, Customer, CustomerBook
from ..serializers import BookSerializer


# initialize the APIClient app
client = Client()

class GetAllBooks(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        self.book1 = Book.objects.create(
            title='Becoming', 
            genre="fiction")
        self.book2 = Book.objects.create(
            title='laugh it out', 
            genre="fiction")
        self.book3 = Book.objects.create(
            title='build an empire', 
            genre="fiction")
        self.customer = Customer.objects.create(
            first_name="Shem", last_name="Ogumbe")
       
    def test_get_all_books(self):
        # get API response
        response = client.get("/api/books")
        # get data from db
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_calculate_rental_charges_per_user(self):
        customer_book = CustomerBook.objects.create(
            book = self.book1,
            customer=self.customer
        )

        response = client.post("/api/calculate_rent",
        data={"user": json.dumps(self.customer.id)},
        content_type='application/json'
        )
        self.assertEqual(response.data, 
        {
             "customer": str(self.customer.id),
            "total_rent_owed": "Rs 30"
        })
    
    def test_checkout(self):
        payload = {
            "user": json.dumps(self.customer.id),
            "books": [{"book": self.book1.id}, {"book":self.book2.id}, {"book":self.book3.id}]
        }

        response = client.post("/api/checkout",
        data=json.dumps(payload),
        content_type='application/json'
        )
        self.assertEqual(response.data, 
        {
             "Customer rental charges": 90
        })

