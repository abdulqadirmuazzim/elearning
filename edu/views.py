from django.shortcuts import render, redirect, HttpResponse
from .forms import comment, register, subsrciption
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


# home
def home(req):
    if req.method == "POST":
        print("Post was made")
    return render(req, "index.html")


# about
def about(req):
    return render(req, "about.html")


# courses
def courses(req):
    return render(req, "courses.html")


# course details
def course_detail(req):
    return render(req, "course-details.html")


# events
def events(req):
    return render(req, "events.html")


# pricing
def pricing(req):
    return render(req, "pricing.html")


# trainers
def trainers(req):
    return render(req, "trainers.html")


# starter-page
def starter_page(req):
    return render(req, "starter-page.html")


# contact
def contact(req):
    if req.method == "POST":

        form = comment(req.POST)

        # if the form is valid
        if form.is_valid():
            # save
            form.save()
            # drop a success message
            messages.success(req, "Thanks for getting in touch")
            # render back the page
            return render(req, "contact.html")

        else:
            name = req.POST["Name"]
            email = req.POST["Email"]
            sub = req.POST["Subject"]
            mess = req.POST["Message"]
            # get the errors
            errors = form.errors.as_data()

            err_list = []

            for err in errors:
                err_list.append(f"{err}: {errors[err][0].message}")

            print(err_list)
            # pass it to the page
            return render(
                req,
                "contact.html",
                {
                    "err": err_list,
                    "name": name,
                    "email": email,
                    "sub": sub,
                    "message": mess,
                },
            )
    else:
        return render(req, "contact.html")


def login_user(req):
    if req.method == "POST":

        # form = AF(request=req, data=req.POST)
        username = req.POST["username"]
        password = req.POST["password"]

        if "@" in username:
            username = User.objects.get(email=username).username

            user = authenticate(username=username, password=password)
        else:
            user = authenticate(username=username, password=password)

        # authenticate the user
        # if they are authenticated
        # print
        if user is not None:
            # log them in
            login(req, user=user)
            messages.success(req, "You have logged in successfully")
            return render(req, "dashboard.html", {"user": username})
        else:
            messages.error(req, "Invalid User name or password")
            print(username, user)
            return render(
                req, "login.html", {"username": username, "password": password}
            )

    if req.user.is_authenticated:
        return redirect("DashBoard")
    else:
        return render(req, "login.html")


def register_user(req):
    if req.method == "POST":
        # if the user is signing up

        form = register(req.POST)
        # check

        # if form is valid
        if form.is_valid():
            # save
            userform = form.save(commit=False)

            # get the username and password
            username = form.cleaned_data.get("UserName")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data["Email"]
            fname = form.cleaned_data["FirstName"]
            lname = form.cleaned_data["LastName"]

            # check to see if username exists
            is_user = User.objects.filter(username=username).exists()

            # check to see if email exists
            is_email = User.objects.filter(email=email).exists()

            if is_user:
                # if username exists
                form.add_error("UserName", "This username is taken")
                return render(
                    req,
                    "signup.html",
                    {
                        "err": form.errors.values(),
                        "f_name": fname,
                        "l_name": lname,
                        "email": email,
                        "user_name": username,
                    },
                )

            elif is_email:
                # if email exists
                form.add_error("Email", "This email is in use")
                return render(
                    req,
                    "signup.html",
                    {
                        "err": form.errors.values(),
                        "f_name": fname,
                        "l_name": lname,
                        "email": email,
                        "user_name": username,
                    },
                )

            else:
                # create a new user

                User.objects.create(
                    username=username,
                    email=email,
                    first_name=fname,
                    last_name=lname,
                    password=userform.password,
                )

            # authenticate and  log the user in
            user = authenticate(username=username, password=password)
            print(f"the user {user}.")

            if user is not None:
                login(req, user)

            # drop a success message
            messages.success(req, "You have successfully registered!")
            # render back the page
            return render(req, "dashboard.html")

        else:
            fname = req.POST["FirstName"]
            lname = req.POST["FirstName"]
            username = req.POST["UserName"]
            email = req.POST["Email"]
            # get the errors
            errors = form.errors.as_data()

            err_list = []

            for err in errors:
                err_list.append(f"{err}: {errors[err][0].message}")

            print(err_list)
            # pass it to the page
            return render(
                req,
                "signup.html",
                {
                    "err": err_list,
                    "f_name": fname,
                    "l_name": lname,
                    "email": email,
                    "user_name": username,
                },
            )
    if req.user.is_authenticated:
        return redirect("DashBoard")
    else:
        return render(req, "signup.html")


def logout_user(req):
    # log the user out
    logout(req)
    return redirect("Home")


def dash(req, user_id=None):
    if req.user.is_authenticated and req.method == "GET":
        return render(req, "dashboard.html")

    else:
        return redirect("Login")
