from django.shortcuts import render, redirect, HttpResponse
from .forms import comment, TrainerForm, subscription, StudentForm, Edit_Trainer
from .models import Trainer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Permission
from django.contrib import messages

# Create your views here.


# home
def home(req):
    if req.method == "POST":
        form = subscription(req.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(req, "You have successfully subscibed")
            return redirect("Home")
        else:
            messages.error(req, "Could not Subscribe")
            errors = form.errors.values()
            return render(req, "index.html", dict(err=errors))
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


# login user
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


# register trainer
def register_trainer(req):
    if req.method == "POST":
        # if the user is signing up

        form = TrainerForm(req.POST, req.FILES)

        # check
        # get the username and password
        username = req.POST.get("UserName")
        password = req.POST.get("password1")
        email = req.POST["Email"]
        fname = req.POST["FirstName"]
        lname = req.POST["LastName"]
        bio = req.POST["bio"]
        passport = form.cleaned_data.get("passport_photo")

        # if form is valid
        if form.is_valid():
            # save
            # check to see if username exists
            is_user = User.objects.filter(username=username).exists()

            # check to see if email exists
            is_email = User.objects.filter(email=email).exists()

            if is_user:
                # if username exists
                form.add_error("UserName", "This username is taken")
                return render(
                    req,
                    "signup_trainer.html",
                    {
                        "err": form.errors.values(),
                        "f_name": fname,
                        "l_name": lname,
                        "email": email,
                        "user_name": username,
                    },
                )

            elif is_email:
                # if username exists
                form.add_error("Email", "This email is taken")
                return render(
                    req,
                    "signup_trainer.html",
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
                userform = form.save(commit=False)

                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=fname,
                    last_name=lname,
                    password=userform.password,
                )
                # we want our trainer to have some permissions
                # so let's list the model objects and actions
                model_objects = {
                    "student": ["view"],
                    "course": ["view", "add", "delete"],
                    "trainer": ["view"],
                }
                # iterate over the dictionary of objects
                for people in model_objects:
                    actions = model_objects[people]

                    # now we iterate over the list of actions for each object
                    for action in actions:
                        # get the permissions by code names
                        permission = Permission.objects.get(
                            codename=f"{action}_{people}"
                        )
                        # Add the permissions to the user
                        user.user_permissions.add(permission)
                # let's make sure the user is a staff
                user.is_staff = True
                user.save()

                trainer = Trainer.objects.create(
                    user=user, bio=bio, passport_photo=passport
                )
                print(f"passport  {passport}")

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
                "signup_trainer.html",
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
        form = TrainerForm
        return render(req, "signup_trainer.html", {"form": form.as_p})


# register student
def register_student(req):
    if req.method == "POST":
        # if the user is signing up

        form = req.POST
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
                    "signup_stu.html",
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
                    "signup_stu.html",
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
                "signup_stu.html",
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
        return render(req, "redirect.html")


# logout the user
def logout_user(req):
    # log the user out
    logout(req)
    return redirect("Home")


# the user dashboard
def dash(req, user_id=None):
    if req.user.is_authenticated and req.method == "GET":
        return render(req, "dashboard.html")

    else:
        return redirect("Login")


# the page new users go to for signing up as either a student or teacher
def redirect_page(req):
    return render(req, "redirect.html")


# Page for editing profile
def edit_profile(req):
    current_user = User.objects.get(id=req.user.id)
    trainers = Trainer.objects.get(user=current_user)
    if req.method == "POST":

        form = Edit_Trainer(req.POST, req.FILES)

        # print(form)
        if form.is_valid():

            username = req.POST.get("UserName")
            email = req.POST["Email"]
            fname = req.POST["FirstName"]
            lname = req.POST["LastName"]
            bio = req.POST["bio"]
            passport = form.cleaned_data["passport_photo"]

        # save the info
        current_user.username = username
        current_user.email = email
        current_user.first_name = fname
        current_user.last_name = lname
        trainers.bio = bio
        trainers.passport_photo = passport

        # Let's make sure the username and email dont exist
        # check to see if username exists
        is_user = User.objects.filter(username=username).exists()

        # check to see if email exists
        is_email = User.objects.filter(email=email).exists()

        if is_user and req.user.username != username:
            # if username exists and it's not the current username
            messages.error(req, "This username is taken")
            return redirect("edit_profile")

        elif is_email and req.user.email != email:
            # if email exists and not the current email
            messages.error(req, "This email is in use")
            return redirect("edit_profile")
        else:
            # save
            # form.save()
            current_user.save()
            trainers.save()

        # drop a success message
        messages.success(req, "You have successfully updated your profile!")
        # redirect to the dashboard
        return redirect("DashBoard")

        # else:
        #     messages.error(req, "There has been an error in your form")
        #     return redirect("edit_profile")

    return render(req, "edit_profile.html", {"trainer": trainers})
