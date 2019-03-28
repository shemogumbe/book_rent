import datetime

from django.test import TestCase
from ..models import Book, Customer, CustomerBook

class BookTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Book.objects.create(
            title="Becoming", genre="fiction")
        Book.objects.create(
            title='audacity of hope',  genre="novel")
        Book.objects.create(
            title='dreams from africa',  genre="regular")

    def test_book_title(self):
        book = Book.objects.get(title="Becoming")
        self.assertEqual(book.__str__(), "Becoming")
    
    def test_cost_perday_novel(self):
        book = Book.objects.get(title="audacity of hope")
        self.assertEqual(book.cost_perday, 1.5)
    
    def test_cost_perday_fiction(self):
        book = Book.objects.get(title="Becoming")
        self.assertEqual(book.cost_perday, 3)
    
    def test_cost_perday_regular(self):
        book = Book.objects.get(title="dreams from africa")
        self.assertEqual(book.cost_perday, 1.5)

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
        self.book1 = Book.objects.create(
            title="Becoming", genre="novel")
        self.book2 = Book.objects.create(
            title="Becoming two", genre="regular")
        # model default for genre is fiction
        self.book3 = Book.objects.create(
            title="Becoming three")
        self.customer_book1 = CustomerBook.objects.create(
            customer=self.customer,
            book=self.book1
            )
        self.customer_book2 = CustomerBook.objects.create(
            customer=self.customer,
            book=self.book2
            )
        self.customer_book3 = CustomerBook.objects.create(
            customer=self.customer,
            book=self.book3
            )

    def test_customer_rent_book(self):

        self.assertTrue(isinstance(self.customer_book1, CustomerBook))
    
    def test_rental_charges_regular(self):
        # default rent duration is 30 days
        regular_charges_30_days = 2 + (28 * 1.5)
        self.assertEqual(self.customer_book2.rental_charges, regular_charges_30_days)
    
    def test_rental_charges_novel_base_charge(self):
        # default charges within first 3 days
        customer_book = CustomerBook.objects.create(
            customer=self.customer,
            book=self.book1,
            borrowed_date=datetime.date.today(),
            due_date=datetime.date.today() + datetime.timedelta(days=2)
            )
        self.assertEqual(customer_book.rental_charges, 4.5)
    
    def test_rental_charges_regular_base_charge(self):
        # default charges within first 2 days
        customer_book = CustomerBook.objects.create(
            customer=self.customer,
            book=self.book2,
            borrowed_date=datetime.date.today(),
            due_date=datetime.date.today() + datetime.timedelta(days=2)
            )
        self.assertEqual(customer_book.rental_charges, 2)
    
    def test_rental_charges_novel(self):
        # default rent duration is 30 days
        novel_charges_30_days = self.book1.cost_perday * 30
        self.assertEqual(self.customer_book1.rental_charges, novel_charges_30_days)
    

    def test_rental_charges_fiction(self):
        # default rent duration is 30 days
        novel_charges_30_days = self.book3.cost_perday * 30
        self.assertEqual(self.customer_book3.rental_charges, novel_charges_30_days)
    
    

    



