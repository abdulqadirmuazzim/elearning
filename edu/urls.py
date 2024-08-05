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
    path("student_or_teacher", v.redirect_page, name="RedirectMe"),
    path("register_trainer", v.register_trainer, name="Reg_trainer"),
    path("register_stu", v.register_student, name="Reg_student"),
    path("logout", v.logout_user, name="Logout"),
    path("dashboard", v.dash, name="DashBoard"),
    path("edit_tra_profile", v.edit_trainer_profile, name="edit_trainer_profile"),
    path("edit_stu_profile", v.edit_student_profile, name="edit_student_profile"),
    path("student_course_registration", v.course_reg, name="course_reg"),
]
