import datetime

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404


# Create your views here.
from .models import Book, Customer, CustomerBook
from .serializers import BookSerializer, CustomerSerializer, CustomerBookSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_fields = ('id')

class CustomerBookList(generics.ListCreateAPIView):
    queryset = CustomerBook.objects.all()
    serializer_class = CustomerBookSerializer


class CustomerBookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerBook.objects.all()
    serializer_class = CustomerBookSerializer
    lookup_fields = ('id')



@api_view(http_method_names=['POST'])
def calculate_rent(request):
    user_id = request.data['user']

    if not user_id:
        return Response({
            'error': "please input a user id"
        })
    user_rent = CustomerBook.objects.user_rent(user_id)
    return Response({
        'customer':  user_id,
        'total_rent_owed': 'Rs' + ' ' + str(user_rent)
    })


@api_view(http_method_names=['POST'])
def checkout(request):
    user = request.data['user']
    books = request.data['books']
    user_obj = get_object_or_404(Customer, id=user)
    cost_per_book = []
    for book in books:
        book_obj = get_object_or_404(Book, id=book['book'])
        new_item = CustomerBook(
            customer=user_obj,
            book=book_obj
        )
        new_item.save()
        cost_per_book.append(int(str(new_item.rental_charges).split()[0]))
    return Response({"Customer rental charges": sum(cost_per_book)})