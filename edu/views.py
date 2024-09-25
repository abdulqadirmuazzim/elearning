from django.shortcuts import (
    render,
    redirect,
    get_object_or_404 as goo4,
    HttpResponseRedirect,
    HttpResponse,
)
from .forms import comment, subscription, CourseComment_form, ReplyForm
from accounts.models import Course, Trainer
from django.contrib import messages
from accounts.models import Course_Comment, Student, Reply
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

# Create your views here.


# home
def home(req):
    if req.method == "POST":
        form = subscription(req.POST)
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
    courses = Course.objects.select_related("trainer")
    return render(req, "courses.html", {"courses": courses})


# course details
def course_detail(req, course_id):
    course = goo4(Course, id=course_id)
    comments = Course_Comment.objects.filter(course=course)
    context = {"course": course, "comments": comments}

    if req.user.is_authenticated and not req.user.is_staff:
        student = goo4(Student, user=req.user)

        if req.method == "POST" and "comment" in req.POST:
            form = CourseComment_form(req.POST)
            form.save(student=student, course=course)
            return HttpResponseRedirect(
                reverse("Course_detail", kwargs={"course_id": course_id})
            )

        elif req.method == "POST" and "reply" in req.POST:
            form = ReplyForm(req.POST)
            comment_id = req.POST["the_comment"]
            print(form)
            if form.is_valid():
                form.save(user=req.user, comment=comment_id)
                return HttpResponseRedirect(
                    reverse("Course_detail", kwargs={"course_id": course_id})
                )
            else:
                messages.error(req, "There was an error with the reply")
                return HttpResponseRedirect(
                    reverse("Course_detail", kwargs={"course_id": course_id})
                )

        return render(req, "course-details.html", context)
    else:
        if req.method == "POST":
            form = ReplyForm(req.POST)
            comment_id = req.POST["the_comment"]
            print(form)
            if form.is_valid():
                form.save(user=req.user, comment=comment_id)
                return HttpResponseRedirect(
                    reverse("Course_detail", kwargs={"course_id": course_id})
                )
            else:
                messages.error(req, "Something went wrong")
        return render(req, "course-details.html", context)


def make_comment(req):
    if req.method == "POST":
        req.POST["comment"]


def like_comments_toggle(req, comment_id):
    comment = goo4(Course_Comment, id=comment_id)
    user = goo4(User, id=req.user.id)
    if req.method == "POST":
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
        return HttpResponseRedirect(
            reverse("Like_comment", kwargs={"comment_id": comment_id})
        )
    else:
        return HttpResponse("<h1> bad request </h1>")


def edit_comment(req, comment_id):
    if req.method == "POST":
        new_comment = req.POST["comment"]
        old_comment = goo4(Course_Comment, id=comment_id)
        old_comment.comment = new_comment
        old_comment.save()
        messages.success(req, "Comment Changed")
        return redirect(
            reverse("Course_detail", kwargs={"course_id": old_comment.course.id})
        )
    return redirect(
        reverse("Course_detail", kwargs={"course_id": old_comment.course.id})
    )


def delete_comment(req, comment_id):
    comment = goo4(Course_Comment, id=comment_id)
    # our replies aren't going to be deleted automatically so let's delete them
    # get the replies
    replies = comment.replies.all()
    [reply.delete() for reply in replies]

    comment.delete()
    return redirect(reverse("Course_detail", kwargs={"course_id": comment.course.id}))


# events
def events(req):
    return render(req, "events.html")


# pricing
def pricing(req):
    return render(req, "pricing.html")


# trainers
def trainers(req):
    trainers = Trainer.objects.all()
    return render(req, "trainers.html", {"trainers": trainers})


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
