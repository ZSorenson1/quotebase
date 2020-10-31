from django.shortcuts import render, redirect
from .models import User, Quote
from .forms import QuoteForm
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
    return redirect("/quotes")

def logout(request):
    request.session['user'] = None
    return redirect("/")

def quotes(request):
    if request.session['user'] == None:
        messages.error(request, "User not logged in")
        return redirect('/')
    context = {
        "users": User.objects.all(), 
        "quotes": Quote.objects.exclude(favoritedBy=User.objects.get(email=request.session['user']['email'])), 
        "currentuser": User.objects.get(email=request.session['user']['email']),
        'AddQuote' : QuoteForm()
    }
    return render(request, "quotes.html", context)

def createQuote(request):
    if request.method == 'POST':
        bound_form = QuoteForm(request.POST)

        if bound_form.is_valid():
            Quote.objects.create(
                quotedBy = request.POST['quotedBy'],
                message = request.POST['message'],
                addedBy = User.objects.get(email=request.session['user']['email'])
            )
        context = {
                'quotes': Quote.objects.all()
        }
        return render(request, 'quotespartial.html', context)

def deleteQuote(request, itemID):
    Quote.objects.get(id=itemID).delete()
    context = {
        'quotes': Quote.objects.exclude(favoritedBy=User.objects.get(email=request.session['user']['email'])),
        "currentuser": User.objects.get(email=request.session['user']['email'])
    }
    return render(request, 'allquotespartial.html', context)

def editQuote(request, itemID):
    context = {"quote": Quote.objects.get(id=itemID)}
    return render(request, "editquote.html", context)

def submitEdit(request, itemID):
    if request.method == "POST":
        c = Quote.objects.get(id=itemID)
        c.quotedBy = request.POST['quotedBy']
        c.message = request.POST['message']
        c.save()
        context = {
            'quotes': Quote.objects.exclude(favoritedBy=User.objects.get(email=request.session['user']['email'])),
            "currentuser": User.objects.get(email=request.session['user']['email'])
        }
        return render(request, 'allquotespartial.html', context)

def users(request, itemID):
    if request.session['user'] == None:
        messages.error(request, "User not logged in")
        return redirect('/')
    context = {'user': User.objects.get(id=itemID), 'currentuser': User.objects.get(email=request.session['user']['email']), 'count': len(User.objects.get(id=itemID).addedQuotes.all()) }
    return render(request, "user.html", context)

def addFavorite(request, itemID):
    User.objects.get(email=request.session['user']['email']).favorites.add(Quote.objects.get(id=itemID))
    context = {
        'quotes': Quote.objects.exclude(favoritedBy=User.objects.get(email=request.session['user']['email'])),
        "currentuser": User.objects.get(email=request.session['user']['email'])
    }
    return render(request, "allquotespartial.html", context)

def removeFavorite(request, itemID):
    if request.method == "POST":
        User.objects.get(email=request.session['user']['email']).favorites.remove(Quote.objects.get(id=itemID))
        context = {
            'quotes': Quote.objects.exclude(favoritedBy=User.objects.get(email=request.session['user']['email'])),
            "currentuser": User.objects.get(email=request.session['user']['email'])
        }
        return render(request, "allquotespartial.html", context)

def backToQuotes(request):
    context = {
            'quotes': Quote.objects.exclude(favoritedBy=User.objects.get(email=request.session['user']['email'])),
            "currentuser": User.objects.get(email=request.session['user']['email']),
            'AddQuote' : QuoteForm()
        }
    return render(request, 'quotesbody.html', context)
