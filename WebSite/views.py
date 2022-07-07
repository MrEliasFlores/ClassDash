from django.shortcuts import render
from .forms import MealForm
from .models import Meal
from django.utils.crypto import get_random_string

def code():
    randomNumber = get_random_string(length = 6, allowed_chars = '0123456789')
    while Meal.objects.filter(code=str(randomNumber)):
        randomNumber = get_random_string(length = 6, allowed_chars = '0123456789')
    return randomNumber
    
def landingPage(request, *args, **kwargs):
    qs = list(Meal.objects.values('locker'))
    dic = {'one':'1','two':'2','three':'3','four':'4'}
    if Meal.objects.filter(locker=1).exists():
        del dic['one']
    if Meal.objects.filter(locker=2).exists():
        del dic['two']
    if Meal.objects.filter(locker=3).exists():
        del dic['three']
    if Meal.objects.filter(locker=4).exists():
        del dic['four']
    return render(request, 'landingPage.html', dic)

def orderFood(request, *args, **kwargs):
    return render(request, 'orderFood.html',{})

def orderChoice(request, *args, **kwargs):
    return render(request, 'orderChoice.html',{})

def Meal1(request):
    secret = code();
    form = MealForm(initial = {'code': secret,'food':'Meal 1','price':'9.99'})
    context = {'form':form}
    if request.method == 'POST':
        form = MealForm(request.POST or None)
        if form.is_valid():
            form.save()
            return render(request, 'orderSuccess.html',{})
        else:
            form = MealForm()
            context = {'form':MealForm}
            return render(request, 'orderFail.html',context)
    return render(request, 'choice1.html',context)
        
def Meal2(request):
    secret = code();
    form = MealForm(initial = {'code': secret,'food':'Meal 2','price':'12.99'})
    context = {'form':form}
    if request.method == 'POST':
        form = MealForm(request.POST or None)
        if form.is_valid():
            form.save()
            return render(request, 'orderSuccess.html',cl)
        else:
            form = MealForm()
            context = {'form':MealForm}
            return render(request, 'orderFail.html',context)
    return render(request, 'choice2.html',context)
