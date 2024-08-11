from django.urls import path
from . import views as v


urlpatterns = [
    path("", v.home, name="Home"),
    path("about", v.about, name="About"),
    path("courses", v.courses, name="Courses"),
    path("course-detail/<int:course_id>", v.course_detail, name="Course_detail"),
    path("events", v.events, name="Events"),
    path("pricing", v.pricing, name="Pricing"),
    path("trainers", v.trainers, name="Train"),
    path("starter", v.starter_page, name="Starter"),
    path("contact", v.contact, name="Contact"),
]
