
from django.contrib import admin
from django.urls import path
from .views import (
    BookList, BookDetail, CustomerList,
    CustomerDetail, CustomerBookList,
    CustomerBookDetail, calculate_rent,
    checkout
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books', BookList.as_view()),
    path('books/<pk>', BookDetail.as_view()),
    path('customers', CustomerList.as_view()),
    path('customers/<pk>', CustomerDetail.as_view()),
    path('customer_book', CustomerBookList.as_view()),
    path('customer_book/<pk>', CustomerBookDetail.as_view()),
    path('calculate_rent', calculate_rent),
    path('checkout', checkout)
]
