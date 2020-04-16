from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import EventModel, CategoryModel, TicketModel, CartModel
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required	

def index(request):

    events = EventModel.objects.all()
    categories = CategoryModel.objects.all()
    current_user = request.user
    if str(current_user) != 'AnonymousUser' :
        return render(request, 'app/index.html', {'events': events, 'categories': categories, 'isLoggedIn': True})

    return render(request, 'app/index.html', {'events': events, 'categories': categories})

@login_required(login_url='/login')
def category(request, pk):

    category = CategoryModel.objects.get(pk = pk)
    categories = CategoryModel.objects.all()
    events = EventModel.objects.filter(category = category)

    return render(request, 'app/category.html', {'events': events, 'category': category,'categories': categories, 'isLoggedIn': True})

@login_required(login_url='/login')
def event(request, pk):

    event = EventModel.objects.get(pk = pk)
    categories = CategoryModel.objects.all()
    if request.method == 'POST':
        current_user = request.user
        if CartModel.objects.filter(user = current_user, event = event) or TicketModel.objects.filter(user = current_user, event = event):
            return render(request, 'app/event.html', {'event': event, 'categories': categories, 'isLoggedIn': True, 'success': False, 'post': True})
        else:
            cart = CartModel.objects.create(user = current_user, event = event)
            return render(request, 'app/event.html', {'event': event, 'categories': categories, 'isLoggedIn': True, 'success': True, 'post': True})
    else:
        return render(request, 'app/event.html', {'event': event, 'categories': categories, 'isLoggedIn': True, 'success': True, 'post': False})

@login_required(login_url='/login')
def events(request):

    events = EventModel.objects.all()
    categories = CategoryModel.objects.all()

    return render(request, 'app/events.html', {'events': events, 'categories': categories, 'isLoggedIn': True})

def login(request):

    events = EventModel.objects.all()
    categories = CategoryModel.objects.all()

    if request.method == 'POST':
        
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username = username,password=password)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'app/login.html', {'events': events, 'categories': categories, 'err': True, 'isLoggedIn': False})
    else:
        return render(request, 'app/login.html', {'events': events, 'categories': categories, 'err': False, 'isLoggedIn': False})

def signup(request):

    events = EventModel.objects.all()       

    categories = CategoryModel.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password_repeat = request.POST.get('password-repeat','')
        if password != password_repeat:
            return render(request, 'app/signup.html', {'events': events, 'categories': categories, 'err': True, 'errMsg': 'The passwords do not match!'})
        try:
            user = User.objects.create_user(username, email = None, password = password)
            user.save()
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/')
        except:
            return render(request, 'app/signup.html', {'events': events, 'categories': categories, 'err': True, 'errMsg': 'Username ' + username + ' already exists!'})
        
    else:
        return render(request, 'app/signup.html', {'events': events, 'categories': categories, 'err': False})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def cart(request):

    categories = CategoryModel.objects.all()
    user = request.user

    if request.method == 'POST':
        events = CartModel.objects.filter(user= user)
        event_name = []
        for i in events:
            event_name.append(i.event.name)
            TicketModel.objects.create(user = user, event = i.event)
            i.delete()
        totalcost = 0
        return render(request, 'app/cart.html', {'events': event_name, 'categories': categories, 'empty': True ,'isLoggedIn': True, 'payment': True})
    else:
        events = CartModel.objects.filter(user= user)
        totalcost = 0
        for i in events:
            totalcost += i.event.fee
        empty = False
        if totalcost == 0:
            empty = True

    return render(request, 'app/cart.html', {'events': events, 'categories': categories, 'empty': empty, 'totalcost': totalcost, 'isLoggedIn': True})

@login_required(login_url='/login')
def orders(request):

    categories = CategoryModel.objects.all()
    user = request.user

    events = TicketModel.objects.filter(user= user)
    totalcost = 0
    for i in events:
        totalcost += i.event.fee
    empty = False
    if totalcost == 0:
        empty = True

    return render(request, 'app/orders.html', {'events': events, 'categories': categories, 'empty': empty, 'isLoggedIn': True})

def about(request):

    events = EventModel.objects.all()
    categories = CategoryModel.objects.all()

    return render(request, 'app/about.html', {'events': events, 'categories': categories, 'isLoggedIn': True})

def delete(request, pk):

    event = EventModel.objects.get(pk = pk)
    user = request.user
    cartItem = CartModel.objects.filter(user = user, event = event)
    cartItem.delete()
    return HttpResponseRedirect('/cart')