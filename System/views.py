from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from django.core.mail import EmailMessage
# library of encode and decode pip install pyjwt
import jwt
from .models import Jobs, extended
import random
from faker import Faker

fake = Faker()


def fake_data(request):
    obj = Jobs()

    job_list = []

    for _ in range(50):
        job = {
            "title": fake.job(),
            "description": fake.text(max_nb_chars=100),
            "amount": round(random.uniform(20.0, 500.0), 2),
            "status": random.choice(["Open", "In Progress", "Completed"]),
            "date": fake.date_between(start_date="-30d", end_date="today").strftime("%Y-%m-%d")
        }

        job_list.append(job)

    for data in job_list:
        Jobs.objects.create(
            title=data['title'],
            description=data['description'],
            amount=data['amount'],
            status=data['status'],
            date=data['date']
        )

    return HttpResponse("Fake Data inserted in Jobs Model")


@login_required(login_url='my_login')
def home(request):
    # if request.user.is_authenticated:

    return render(request, 'home.html',
                  {'username': request.user.username, 'ob': obj, 'user_image': request.user.extended.img})


obj = Jobs.objects.all()


# username = request.user.username
# user = User.objects.get(username=username)
# in context 'user' : user
# in template user.username , user.extended.img.url


# else:
#     return render(request, 'login.html')

# obj = Jobs.objects.all()
# return render(request, 'home.html', {'ob': obj})


def delete(request, id):
    obj = Jobs.objects.get(pk=id)
    try:
        obj.delete()
        return redirect(reverse("home"), {'ob': obj, 'user_image': request.user.extended.img})
    except:
        return HttpResponse("Job not existed")


from datetime import datetime


# def edit(request, id):
def edit(request, slug):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        amount = request.POST['amount']
        status = request.POST['status']
        date = request.POST['date']
        # obj = Jobs.objects.get(pk=id)
        obj = Jobs.objects.get(slug=slug)
        obj.title = title
        obj.description = description
        obj.amount = amount
        obj.status = status
        # date_ob = datetime.strptime(date, "%b. %d, %Y")
        # for_date = date_ob.strftime("%Y-%m-%d")
        # obj.date = for_date
        obj.save()
        try:

            obj = Jobs.objects.all()

            return render(request, 'home.html', {'ob': obj, 'user_image': request.user.extended.img})
        except:
            return HttpResponse("Network issue...")
    # obj = Jobs.objects.get(pk=id)
    obj = Jobs.objects.get(slug=slug)
    return render(request, 'edit.html', {'ob': obj})


# import pdb;pdb.set_trace():

def my_login(request):
    if request.method == 'POST':
        usern = request.POST['username']
        passw = request.POST['password']
        user = authenticate(username=usern, password=passw)
        if user is not None:
            login(request, user)
            user = User.objects.all()
            return render(request, 'home.html', {'username': usern, 'ob': obj, 'user_image': request.user.extended.img})
        else:
            return render(request, 'login.html', {'msg': "Wrong Credentials."})
    return render(request, 'login.html')


def my_logout(request):
    logout(request)
    return render(request, 'login.html')


def my_signup(request):
    if request.method == "POST":
        new_username = request.POST['nam']
        new_email = request.POST['emai']
        new_password = request.POST['passwor']
        im = request.FILES['imageFile']
        # for email authentication => is_active=False
        user = User.objects.create_user(username=new_username, email=new_email, password=new_password, is_active=True)
        try:
            user.save()
            ex = extended()
            ex.id = user
            ex.img = im
            ex.save()
            encode = jwt.encode({'myid': str(user.pk)}, key="secret", algorithm='HS256')
            # link = 'http://127.0.0.1:8000/activation/'+str(user.pk)+'/' never use hardcore url address
            link = request.scheme + '://' + request.META['HTTP_HOST'] + '/activation/' + str(encode) + '/'
            em = EmailMessage("Account Activation", "Thanks for Registeration....!\n" + link, "garrison18552gmail.com",
                              [new_email])
            em.send()
            return render(request, 'login.html', {'msg': 'user created successfully!'})
        except:
            return render(request, 'signup.html', {'msg': 'Network Error!!'})
    return render(request, 'signup.html')


def activation(request, id):
    decode = jwt.decode(id, key='secret', algorithms=['HS256'])
    us = User.objects.get(pk=int(decode['myid']))
    us.is_active = True
    us.save()
    return render(request, 'login.html', {'msg': 'Account Activated Successfully....!'})


from .forms import BookForm


def book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("data saved ...!")
    form = BookForm()
    return render(request, 'bookform.html', {'bform': form})


from .models import Contact_form


def base(request):
    if request.method == 'POST':
        contact_name = request.POST['name']
        contact_email = request.POST['email']
        contact_message = request.POST['message']
        form = Contact_form()
        form.name = contact_name
        form.email = contact_email
        form.message = contact_message
        form.save()
        return render(request, 'base.html', {'msg': 'Your data has been successfully sent.'})

    return render(request, "base.html")


from .serializers import JobSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET', 'PUT', 'DELETE'])
def jobdata_api(request, id):
    try:
        obj = Jobs.objects.get(pk=id)
    except:
        return Response({'msg', 'You have written invalid id which not exist.'}, status=status.HTTP_404_NOT_FOUND)
        # d = Jobs.objects.all()
        # sr = JobSerializer(d, many=True)
        # return Response(sr.data)

    if request.method == 'GET':
        # d = Jobs.objects.get(pk=id)
        sr = JobSerializer(obj)
        # return JsonResponse(sr.data, safe=False)
        return Response(sr.data)

    if request.method == 'PUT':
        sr = JobSerializer(data=request.data)
        if sr.is_valid():
            sr.save()
            return Response(sr.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # d = Jobs.objects.all()
        # sr = JobSerializer(d, many=True)
        # return Response(sr.data)


from .models import Book
from .serializers import BookSerializer


@api_view(['GET', 'POST'])
def bookdata_api(request):
    if request.method == 'GET':
        b = Book.objects.all()
        sr = BookSerializer(b, many=True)
        return Response(sr.data)

    if request.method == 'POST':
        sr = BookSerializer(data=request.data)
        if sr.is_valid():
            sr.save()
            b = Book.objects.all()
            sr = BookSerializer(b, many=True)
            return Response(sr.data)


def picpage(request):
    return render(request, 'picpage.html')


from django.conf import settings
# from django.core.files.storage import FileSystemStorage
#
# def upload_blog(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         my_file = request.FILES['myfile']
#         f__e = FileSystemStorage()
#         filename = f__e.save(my_file.name, my_file)
#         uploaded_file_url = f__e.url(filename)
#         return render(request, 'upload_blog.html',{'uploaded_file_url':uploaded_file_url})
#     return render(request,'upload_blog.html')

# from .forms import DocumentForm
from .models import Document


blogs = Document.objects.all()
def upload_blog(request):
    if request.method == 'POST':
        title_e = request.POST.get('title','')
        description = request.POST.get('description','')
        file = request.FILES['file']
        date = request.POST.get('date')
        docs = Document()
        docs.title = title_e
        docs.description = description
        docs.document = file
        docs.uploaded_at = date
        try:
            docs.save()
            return render(request, 'upload_blog.html', {'msg': 'One more blog added in the BLOGS '})
        except:
            return render(request, 'upload_blog.html', {'msg': 'Network error, your blog not uploaded.'})
    return render(request,'upload_blog.html',{'blogs':blogs})

    #     form = Document(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    # else:
    #     form = DocumentForm()
