import datetime
from dateutil import parser


from django.db import models

# Create your models here.
book_types = (
    ('novel', 'novel'),
    ('fiction', 'fiction'),
    ('regular', 'regular')
)


class BookManager(models.Manager):
    def user_rent(self, customer_id):
        customer_books = self.filter(customer=customer_id)
        if not customer_books:
            return "customer has no books"
        cost_per_book = []
        for book in customer_books:
            duration = book.due_date - book.borrowed_date
            cost_perday = Book.objects.get(id=book.book.id).cost_perday
            charges = cost_perday * int(str(duration).split()[0])
            cost_per_book.append(charges)

        return sum(cost_per_book)


class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    genre = models.CharField(max_length=100, choices=book_types, default='fiction')

    def __str__(self):
        "sets the book object verbose identifier to title"
        return self.title
    
    @property
    def cost_perday(self):
        "sets the cost of each book per day to Rs 1"
        if self.genre == "fiction":
            return 3
        elif self.genre == "novel" or self.genre == "regular":
            return 1.5



class Customer(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(null=False, max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class CustomerBook(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(
        auto_now_add=False)

    objects = BookManager()


    def save(self, *args, **kwargs):
        if not self.due_date:
            if not self.borrowed_date:
                self.borrowed_date = datetime.date.today()
                self.due_date = self.borrowed_date + datetime.timedelta(days=30)
            self.due_date = self.borrowed_date + datetime.timedelta(days=30)
        else:
            self.due_date = parser.parse(str(self.due_date)).date()
        super(CustomerBook, self).save(*args, **kwargs)



    @property
    def rental_charges(self):
        "Calculate the cost of renting any book for the given period"
        rent_duration = int(str(self.due_date - self.borrowed_date).split()[0])
        print(rent_duration)
        if self.book.genre == "regular":
            if rent_duration <= 2:
                return 2
            elif rent_duration > 2:
                return 2 + ((rent_duration -2) * 1.5)
        if self.book.genre == "novel":
            if rent_duration <= 3:
                return 4.5
            else:
                return self.book.cost_perday * rent_duration
        return self.book.cost_perday * rent_duration
    