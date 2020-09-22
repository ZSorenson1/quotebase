from django.db import models
import bcrypt, re

class userManager(models.Manager):
    def regvalidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 4:
            errors["name"] = "Name should be at least 4 characters"
        if len(postData['password']) < 5:
            errors["password"] = "Password should be at least 5 characters"
        if postData['password'] != postData['confirmPW']:
            errors['confirmPW'] = "Passwords must match"
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        for users in User.objects.all():
            if users.email == postData['email']:
                errors['email'] = "Email in use!"
        return errors
    def loginvalidator(self, postData):
        errors = {}
        password = postData['password']
        userval = None
        for users in User.objects.all():
            if users.email == postData['email']:
                userval = users
        if userval == None:
            errors['user'] = "User does not exist!"
            return errors
        if bcrypt.checkpw(postData['password'].encode(), userval.password.encode()):
            print("password match")
        else:
            errors['password'] = "Password Incorrect!"
        return errors
    def quotevalidator(self, postData):
        errors = {}
        if len(postData['quotedBy']) < 2:
            errors['quotedBy'] = "Quoted By field should be at least 2 characters"
        if len(postData['message']) < 10:
            errors['message'] = "Message should be at least 10 characters"
        return errors

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.TextField()
    objects = userManager()

class Quote(models.Model):
    quotedBy = models.CharField(max_length=50)
    message = models.TextField()
    addedBy = models.ForeignKey(User, related_name="addedQuotes", on_delete = models.CASCADE)
    favoritedBy = models.ManyToManyField(User, related_name="favorites")
    objects = userManager()