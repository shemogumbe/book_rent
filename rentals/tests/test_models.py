from django.test import TestCase
from ..models import Book, Customer, CustomerBook

class BookTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Book.objects.create(
            title="Becoming", genre="fiction")
        Book.objects.create(
            title='audacity of hope',  genre="novel")

    def test_book_title(self):
        book = Book.objects.get(title="Becoming")
        self.assertEqual(book.__str__(), "Becoming")
    
    def test_cost_perday(self):
        book = Book.objects.get(title="Becoming")
        self.assertEqual(book.cost_perday, 1)

class CustomerTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Customer.objects.create(
            first_name="Shem", last_name="Ogumbe")

    def test_customer_name(self):
        customer = Customer.objects.get(first_name="Shem")
        self.assertEqual(customer.__str__(), "Shem Ogumbe")
    

class CustomerBookTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Shem", last_name="Ogumbe")
        self.book = Book.objects.create(
            title="Becoming", genre="fiction")
        self.customer_book = CustomerBook.objects.create(
            customer=self.customer,
            book=self.book
            )

    def test_customer_rent_book(self):

        self.assertTrue(isinstance(self.customer_book, CustomerBook))
    
    def test_rental_charges_with_date_defaults(self):
        duration = self.customer_book.due_date - self.customer_book.borrowed_date
        self.assertEqual(self.customer_book.rental_charges, duration * 1)

    


