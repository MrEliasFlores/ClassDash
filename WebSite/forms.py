from django import forms
from django.db.models import UniqueConstraint
from .models import Meal
    
class MealForm(forms.ModelForm):
    UniqueConstraint(fields = ['locker',], name = 'name')
    code = forms.CharField(max_length = 6)
    food = forms.CharField(max_length = 50)
    price = forms.DecimalField(max_digits = 4,decimal_places = 2)
    class Meta:
        model = Meal
        fields = [
            'food',
            'price',
            'name',
            'locker',
            'code',
            ]


