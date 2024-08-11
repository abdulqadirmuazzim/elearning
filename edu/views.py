from django.shortcuts import render, redirect, get_object_or_404 as goo4
from .forms import comment, subscription
from accounts.models import Course, Trainer
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
    courses = Course.objects.all()
    return render(req, "index.html", {"courses": courses})


# about
def about(req):
    return render(req, "about.html")


# courses
def courses(req):
    courses = Course.objects.select_related("trainer")
    return render(req, "courses.html", {"courses": courses})


# course details
def course_detail(req, course_id):
    course = goo4(Course, id=course_id)
    return render(req, "course-details.html", {"course": course})


# events
def events(req):
    return render(req, "events.html")


# pricing
def pricing(req):
    return render(req, "pricing.html")


# trainers
def trainers(req):
    trainers = Trainer.objects.all()
    return render(req, "trainers.html", {'trainers': trainers})


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


# 404 Page
def not_found(req, exception):
    return render(req, "404.html", status=404)
