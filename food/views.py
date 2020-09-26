from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Food, Meal
from django.urls import reverse_lazy
from .forms import MealForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    template = 'list.html'
    meals = Meal.objects.all()
    context = {
		'meals': meals,
    }
    # get_total_calories = meals.values('serving_size')

    return render(request, template, context)

@login_required(login_url='/accounts/login/')
def add_meal(request):
	template = "add_meal.html"

	if request.method == "POST":
		form = MealForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse_lazy('food:index'))
	else:
		context = {
			'meal_form': MealForm(),
		}
	return render(request, template, context)

@login_required(login_url='/accounts/login/')
def delete_meal(request, meal_id):
	meal = Meal.objects.get(id=int(meal_id))
	meal.delete()
	return HttpResponseRedirect(reverse_lazy('food:index'))

@login_required(login_url='/accounts/login/')
def update_meal(request, meal_id):
	template = "update_meal.html"
	meal = Meal.objects.get(id=int(meal_id))

	if request.method == "POST":
		form = MealForm(request.POST, instance=meal)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse_lazy('food:index'))
	else:
		context = {
			'meal_form': MealForm(instance=meal),
		}
	return render(request, template, context)

@login_required(login_url='/accounts/login/')
def view_food(request, food_id):
	template = "view_food.html"
	food = Food.objects.get(id=int(food_id))
	context = {
		'food':food
    }

	return render(request, template, context)

def login(request):
	if request.user.is_authenticated:
	    return HttpResponseRedirect(reverse_lazy('food:index'))
	else:
	    return HttpResponseRedirect(reverse_lazy('auth_login'))