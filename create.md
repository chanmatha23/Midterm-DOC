🎫 Creating a model
Within the app's models.py file, an example of a simple model can be added with the following:
from django.db import models

class Person(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
Note that you don't need to create a primary key, Django automatically adds an IntegerField.

To perform changes in your models, use the following commands in your shell:
$ python manage.py makemigrations <app_name>
$ python manage.py migrate
Note: including <app_name> is optional.

A one-to-many relationship can be made with a ForeignKey:
class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
In this example, to query for the set of albums of a musician:
>>> m = Musician.objects.get(pk=1)
>>> a = m.album_set.get()
A many-to-many relationship can be made with a ManyToManyField:
class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
Note that the ManyToManyField is only defined in one model. It doesn't matter which model has the field, but if in doubt, it should be in the model that will be interacted with in a form.

Although Django provides a OneToOneField relation, a one-to-one relationship can also be defined by adding the kwarg of unique = True to a model's ForeignKey:
ForeignKey(SomeModel, unique=True)
For more detail, the official documentation for database models provides a lot of useful information and examples.
📮 Creating model objects and queries
Example models.py file:
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline
To create an object within the shell:
$ python manage.py shell
>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()
To save a change in an object:
>>> b.name = 'The Best Beatles Blog'
>>> b.save()
To retrieve objects:
>>> all_entries = Entry.objects.all()
>>> indexed_entry = Entry.objects.get(pk=1)
>>> find_entry = Entry.objects.filter(name='Beatles Blog')
