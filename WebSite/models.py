from django.db import models
from django.db.models import UniqueConstraint

#Model for the Meal Order to store into DB
class Meal(models.Model):
    UniqueConstraint(name = 'name', fields = ['locker'])
    lockerChoices = [('1',1),('2',2),
                     ('3',3),('4',4)]
    food = models.CharField(max_length = 50)
    price  = models.DecimalField(max_digits = 4,decimal_places = 2)
    name   = models.CharField(max_length=50, blank = False)
    locker = models.CharField(max_length = 1,choices = lockerChoices,
                            default = 1,unique = True,blank = False)
    code = models.CharField(max_length=6)
#Model to insert items into the DB
class Item(models.Model):
    food = models.CharField(max_length = 15, blank = False, editable = True)
    total = models.DecimalField(max_digits = 4, decimal_places = 2, editable = True)
                            


    
