from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date, time
from .models import *
import bcrypt
# Create your views here.
def index(request):
	return render(request, 'main/index.html')

def create_user(request):
	if User.objects.validate(request,request.POST) == True:
		user = User.objects.create(
			name = request.POST.get('name'),
			alias = request.POST.get('alias'),
			email = request.POST.get('email'),
			password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
		)
		request.session['user_id'] = user.id
		return redirect('/success')
	return redirect('/')

def login_user(request):
	login = User.objects.login_user(request,request.POST)
	if login[0]:
		request.session['user_id'] = login[1].id
		return redirect('/home')
	return redirect('/')

def success(request):
	context = {
		'users': User.objects.all(),
		"curr_user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'main/success.html', context)

def home(request):
	user = User.objects.filter(id=request.session['user_id'])

	quotes = Quote.objects.all()

	favorites_show = Favorite.objects.filter(user_id=user)

	favorited = []
	for favorite in favorites_show:
		favorited.append(favorite.quote)

	quotes_show = Quote.objects.all()

	not_favorited = []
	for quote in quotes_show:
		if quote not in favorited:
			not_favorited.append(quote)

	context = {
		"curr_user": User.objects.get(id=request.session['user_id']),
		"quotes": not_favorited,
		"favorites": favorites_show
	}
	return render(request, 'main/home.html', context)

def user(request,user_id):
	user = User.objects.get(id=user_id)
	my_quotes = Quote.objects.filter(user_id=user_id)
	number_quotes = len(my_quotes)
	context = {
		"number_quotes": number_quotes,
		"user": user,
		"my_quotes": my_quotes
	}
	return render(request, "main/user.html", context)

def quote(request,user_id):
	if Quote.objects.validation(request,request.POST) == True:
		user = User.objects.get(id=user_id)
		Quote.objects.create(
			quote = request.POST['quote'],
			quote_by = request.POST['quote_by'],
			user=user,
		)
		return redirect('/home')
	return redirect('/home')

def add(request, quote_id):
	user = User.objects.get(id=request.session['user_id'])
	quote = Quote.objects.get(id=quote_id)
	Favorite.objects.create(
		quote=quote,
		user=user
	)
	return redirect('/home')

def remove(request, favorite_id):
	Favorite.objects.get(id=favorite_id).delete()
	return redirect('/home')
