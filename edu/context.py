from accounts.models import Course
from accounts.models import Student


def course_links(req):
    courses = Course.objects.all()
    return {"Courses": courses}


def student_registered_courses(req):
    if req.user.is_authenticated and not req.user.is_staff:
        student = Student.objects.get(user=req.user)
        all_courses = student.courses.all()
        return {"RegisteredCourses": all_courses}
    else:
        return {"RegisteredCourses": None}
