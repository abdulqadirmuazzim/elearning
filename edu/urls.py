from django.urls import path
from . import views as v


urlpatterns = [
    path("", v.home, name="Home"),
    path("about", v.about, name="About"),
    path("courses", v.courses, name="Courses"),
    path("course-detail", v.course_detail, name="Course_detail"),
    path("events", v.events, name="Events"),
    path("pricing", v.pricing, name="Pricing"),
    path("trainers", v.trainers, name="Train"),
    path("starter", v.starter_page, name="Starter"),
    path("contact", v.contact, name="Contact"),
    path("login", v.login_user, name="Login"),
    path("register", v.register_user, name="Reg"),
    path("logout", v.logout_user, name="Logout"),
    path("dashboard", v.dash, name="DashBoard"),
]
