from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('login/success', views.loginsuccess),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('quotes/create', views.createQuote),
    path('quotes/addfavorite/<itemID>', views.addFavorite),
    path('quotes/removefavorite/<itemID>', views.removeFavorite),
    path('quotes/edit/<itemID>', views.editQuote),
    path('quotes/edit/<itemID>/submit', views.submitEdit),
    path('users/<itemID>', views.users),
    path('quotes/delete/<itemID>', views.deleteQuote)
]