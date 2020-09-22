from django.shortcuts import render, redirect
from .models import User, Quote
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.regvalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['password']
    pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        name = request.POST["name"],
        email = request.POST["email"],
        password = pwhash
    )
    messages.success(request, "Account Successfully Created!")
    return redirect("/")

def login(request):
    errors = User.objects.loginvalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    request.session['user'] = {"name": User.objects.get(email=request.POST['email']).name, "email": User.objects.get(email=request.POST['email']).email}
    return redirect("/login/success")

def loginsuccess(request):
    if request.session['user'] != None:
        return render(request, "loginsuccess.html")
    else:
        messages.error(request, "User not logged in")
        return redirect('/')

def logout(request):
    request.session['user'] = None
    return redirect("/")

def quotes(request):
    if request.session['user'] == None:
        messages.error(request, "User not logged in")
        return redirect('/')
    context = {"users": User.objects.all(), "quotes": Quote.objects.exclude(favoritedBy=User.objects.get(email=request.session['user']['email'])), "currentuser": User.objects.get(email=request.session['user']['email'])}
    return render(request, "quotes.html", context)

def createQuote(request):
    errors = Quote.objects.quotevalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    Quote.objects.create(
        quotedBy = request.POST['quotedBy'],
        message = request.POST['message'],
        addedBy = User.objects.get(email=request.session['user']['email'])
    )
    return redirect("/quotes")

def deleteQuote(request, itemID):
    Quote.objects.get(id=itemID).delete()
    return redirect('/quotes')

def editQuote(request, itemID):
    if Quote.objects.get(id=itemID).addedBy.email != request.session['user']['email']:
        messages.error(request, "Quote does not belong to current user")
        return redirect("/quotes")
    context = {"quote": Quote.objects.get(id=itemID)}
    return render(request, "editquote.html", context)

def submitEdit(request, itemID):
    errors = Quote.objects.quotevalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    c = Quote.objects.get(id=itemID)
    c.quotedBy = request.POST['quotedBy']
    c.message = request.POST['message']
    c.save()
    messages.success(request, "Quote successfully updated!")
    return redirect("/quotes")

def users(request, itemID):
    if request.session['user'] == None:
        messages.error(request, "User not logged in")
        return redirect('/')
    if User.objects.get(id=itemID) == None:
        messages.error(request, "User does not exist!")
        return redirect("/quotes")
    context = {'user': User.objects.get(id=itemID), 'currentuser': User.objects.get(email=request.session['user']['email']), 'count': len(User.objects.get(id=itemID).addedQuotes.all()) }
    return render(request, "user.html", context)

def addFavorite(request, itemID):
    User.objects.get(email=request.session['user']['email']).favorites.add(Quote.objects.get(id=itemID))
    return redirect('/quotes')

def removeFavorite(request, itemID):
    User.objects.get(email=request.session['user']['email']).favorites.remove(Quote.objects.get(id=itemID))
    return redirect('/quotes')
