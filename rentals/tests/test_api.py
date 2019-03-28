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
            genre="novel")
        self.book2 = Book.objects.create(
            title='laugh it out', 
            genre="fiction")
        self.book3 = Book.objects.create(
            title='build an empire', 
            genre="regular")
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
        duration = int(str(customer_book.due_date - customer_book.borrowed_date).split()[0])
        rent_owed = customer_book.book.cost_perday * duration

        response = client.post("/api/calculate_rent",
        data={"user": json.dumps(self.customer.id)},
        content_type='application/json'
        )
        self.assertEqual(response.data, 
        {
             "customer": str(self.customer.id),
            "total_rent_owed": "Rs " + str(rent_owed)
        })
    
    def test_checkout(self):
        payload = {
            "user": json.dumps(self.customer.id),
            "books": [{"book": self.book1.id}, {"book":self.book2.id}, {"book":self.book3.id}]
        }
        output  = (self.book1.cost_perday * 30) + (self.book2.cost_perday * 30) + (self.book3.cost_perday * 30)


        response = client.post("/api/checkout",
        data=json.dumps(payload),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

