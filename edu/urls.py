from django.urls import path
from . import views as v


urlpatterns = [
    path("", v.home, name="Home"),
    path("about", v.about, name="About"),
    path("courses", v.courses, name="Courses"),
    path("course-detail/<int:course_id>", v.course_detail, name="Course_detail"),
    path("comment/<int:comment_id>", v.like_comments_toggle, name="Like_comment"),
    path("change_comment/<int:comment_id>", v.edit_comment, name="Edit_comment"),
    path("delete_comment/<int:comment_id>", v.delete_comment, name="Delete_comment"),
    path("events", v.events, name="Events"),
    path("pricing", v.pricing, name="Pricing"),
    path("trainers", v.trainers, name="Train"),
    path("starter", v.starter_page, name="Starter"),
    path("contact", v.contact, name="Contact"),
]
