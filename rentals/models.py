import datetime


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
        return 1


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
        if self.borrowed_date:
            self.due_date = self.borrowed_date + datetime.timedelta(days=30)
        else:
            self.borrowed_date = datetime.datetime.today().strftime('%Y-%m-%d')
            self.due_date = datetime.date.today() + datetime.timedelta(30)
        super(CustomerBook, self).save(*args, **kwargs)



    @property
    def rental_charges(self):
        "Calculate the cost of renting any book for the given period"
        rent_duration = self.due_date - self.borrowed_date
        return self.book.cost_perday * rent_duration
    