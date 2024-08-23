from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import (
    TrainerForm,
    StudentForm,
    Edit_Trainer,
    Edit_Trainer_Passport,
    Course_Reg_form as CRF,
    Course_creation as CC,
)
from .models import Trainer, Student, Course
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Permission
from django.contrib import messages


# login user
def login_user(req):
    if req.method == "POST":

        # form = AF(request=req, data=req.POST)
        username = req.POST["username"]
        password = req.POST["password"]

        if "@" in username:
            emailname = User.objects.filter(email=username).first()
            print(emailname)
            # emailname.get(email=emailname).username

            user = authenticate(username=emailname, password=password)
        else:
            user = authenticate(username=username, password=password)

        # authenticate the user
        # if they are authenticated
        # print
        if user is not None:
            # log them in
            login(req, user=user)
            messages.success(req, "You have logged in successfully")
            return redirect("DashBoard")
        else:
            messages.error(req, "Invalid User name or password")
            print(username, user)
            return render(
                req, "accounts/login.html", {"username": username, "password": password}
            )

    if req.user.is_authenticated:
        # if it's a trainer
        return redirect("DashBoard")
    else:
        return render(req, "accounts/login.html")


# register trainer
def register_trainer(req):
    if req.method == "POST":
        # if the user is signing up

        form = TrainerForm(req.POST, req.FILES)

        # check

        # if form is valid
        if form.is_valid():

            # get the username and password
            username = req.POST.get("UserName")
            password = req.POST.get("password1")
            email = req.POST["Email"]
            fname = req.POST["FirstName"]
            lname = req.POST["LastName"]
            bio = req.POST["bio"]
            passport = form.cleaned_data.get("passport_photo")

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
                    "accounts/signup_trainer.html",
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
                    "accounts/signup_trainer.html",
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
                userform = form.save()

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
                    "course": ["view", "add", "change", "delete"],
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
                return render(req, "accounts/trainer_profile.html")

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
                "accounts/signup_trainer.html",
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
        # form = TrainerForm()
        return render(req, "accounts/signup_trainer.html")


# register student
def register_student(req):
    if req.method == "POST":
        # if the user is signing up
        form = StudentForm(req.POST)
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
                    "accounts/signup_stu.html",
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
                    "accounts/signup_stu.html",
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

                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=fname,
                    last_name=lname,
                    password=userform.password,
                )
                Student.objects.create(user=user)

            # authenticate and  log the user in
            user = authenticate(username=username, password=password)
            print(f"the user {user}.")

            if user is not None:
                login(req, user)

                # drop a success message
                messages.success(req, "You have successfully registered!")
                # render back the page
                return render(req, "accounts/student_profile.html")
            else:
                messages.error(req, "Something went wrong")
                # render back the page
                return redirect("Home")

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
                "accounts/signup_stu.html",
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
        return render(req, "accounts/signup_stu.html")


# logout the user
def logout_user(req):
    # log the user out
    logout(req)
    return redirect("Home")


# the user dashboard
def dash(req, user_id=None):

    if req.method == "POST":

        trainers = get_object_or_404(Trainer, user=req.user)

        form = Edit_Trainer_Passport(req.POST, req.FILES)

        if form.is_valid():
            passport = form.cleaned_data["passport_photo"]
            # save the photo
            trainers.passport_photo = passport
            trainers.save()
            messages.success(req, "You have changed your profile photo")

        else:
            messages.error(req, "something went wrong")
            redirect("DashBoard")

    # if the user is logged in move on
    if req.user.is_authenticated and req.method == "GET":

        # Get the list of all courses and their corresponding trainer data
        courses = Course.objects.select_related("trainer")

        # if the user is an Admin
        if req.user.is_superuser:

            messages.info(
                req,
                "You are a super user, Your profile page is not ready, contact the developer",
            )
            return redirect("Home")

        # if the user is a trainer
        if req.user.is_staff and not req.user.is_superuser:

            # Get the trainer info
            trainer_profile_pic = Trainer.objects.get(user=req.user)

            return render(
                req,
                "accounts/trainer_profile.html",
                {
                    "profile_pic": trainer_profile_pic.passport_photo.url,
                    "courses": courses,
                },
            )

        # else if the user is a student
        elif not req.user.is_staff:

            student = Student.objects.get(user=req.user)
            courses = student.courses.all()

            return render(req, "accounts/student_profile.html", {"courses": courses})

    # else sent him/her to the login page
    else:
        return redirect("Login")


# course creation page for trainers
def course_create(req):
    trainer = get_object_or_404(Trainer, user=req.user)
    form = CC()
    if req.method == "POST":
        form = CC(req.POST, req.FILES)

        if form.is_valid():
            print(form)
            form = form.save(commit=False)
            form.trainer = trainer
            form.save()
            messages.success(req, "You have successfully added a course")
            return redirect("DashBoard")
        else:
            messages.error(req, "Unable to create course")

    return render(req, "accounts/course_creation.html", {"form": form})


# Course editing page
def course_edit(req, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.trainer.user == req.user:
        return render(req, "accounts/course_creation.html", {"course": course})

    elif req.user.is_superuser:
        messages.info(req, "Go edit in the Admin!")
        return redirect("Home")
    else:
        messages.error(
            req,
            "You are not allowed to delete a course, and you're not suppose to even see this",
        )
        return redirect("DashBoard")


# Deleting Course
def course_delete(req, course_id):
    course = get_object_or_404(Course, id=course_id)
    if req.user != course.trainer.user:
        messages.error(req, "You can't delete this course")
        return redirect("DashBoard")
    else:
        course.delete()
        messages.info(req, "You have successfully deleted this course")
        return redirect("DashBoard")


# student course registration page
def course_reg(req, course_id):

    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, user=req.user)

    # Register for the course
    student.courses.add(course)
    messages.success(req, "You have successfully registered this course")

    return redirect("DashBoard")


# the page new users go to for signing up as either a student or teacher
def redirect_page(req):
    return render(req, "accounts/redirect.html")


# Page for editing profile
def edit_trainer_profile(req):

    current_user = get_object_or_404(User, id=req.user.id)
    trainers = get_object_or_404(Trainer, user=current_user)

    if req.method == "POST":

        form = Edit_Trainer(req.POST, req.FILES)
        print(form)
        if form.is_valid():

            username = req.POST.get("UserName")
            email = req.POST["Email"]
            fname = req.POST["FirstName"]
            lname = req.POST["LastName"]
            bio = req.POST["bio"]

            # save the info
            current_user.username = username
            current_user.email = email
            current_user.first_name = fname
            current_user.last_name = lname
            trainers.bio = bio

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

        else:
            messages.error(req, "There has been an error in your form")
            return render(req, "accounts/edit_profile.html", {"trainer": trainers})

    return render(req, "accounts/edit_profile.html", {"trainer": trainers})


def edit_student_profile(req):
    current_user = User.objects.get(id=req.user.id)
    # student = Student.objects.get(user=current_user)

    if req.method == "POST":

        username = req.POST.get("UserName")
        email = req.POST["Email"]
        fname = req.POST["FirstName"]
        lname = req.POST["LastName"]

        # save the info
        current_user.username = username
        current_user.email = email
        current_user.first_name = fname
        current_user.last_name = lname

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

        # drop a success message
        messages.success(req, "You have successfully updated your profile!")
        # redirect to the dashboard
        return redirect("DashBoard")

    return render(req, "accounts/edit_profile.html")


# About trainer
def about_trainer(req, trainer_id):
    trainer = get_object_or_404(Trainer, user=trainer_id)
    return render(req, "accounts/trainer_about.html", {"trainer": trainer})
