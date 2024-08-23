from django.urls import path
from . import views as v


urlpatterns = [
    path("login", v.login_user, name="Login"),
    path("student_or_teacher", v.redirect_page, name="RedirectMe"),
    path("register_trainer", v.register_trainer, name="Reg_trainer"),
    path("register_stu", v.register_student, name="Reg_student"),
    path("logout", v.logout_user, name="Logout"),
    path("dashboard", v.dash, name="DashBoard"),
    path("edit_tra_profile", v.edit_trainer_profile, name="edit_trainer_profile"),
    path("edit_stu_profile", v.edit_student_profile, name="edit_student_profile"),
    path(
        "student_course_registration/<int:course_id>", v.course_reg, name="course_reg"
    ),
    path("course_creation", v.course_create, name="course_creation"),
    path("trainer/<int:trainer_id>", v.about_trainer, name="about_trainer"),
    path("edit/<int:course_id>", v.course_edit, name="edit_course"),
    path("delete/<int:course_id>", v.course_delete, name="delete_course"),
]
