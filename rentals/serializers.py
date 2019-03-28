import datetime

from rest_framework import serializers

from .models import Book, Customer, CustomerBook

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id','first_name', 'last_name', 'email']


class CustomerBookSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(required=False)

    class Meta:
        model = CustomerBook
        fields = ['id', 'customer', 'book', "borrowed_date", 'due_date']