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


def num_of_students(req):
    students = Student.objects.all()
    courses = Course.objects.all()
    counts = {}
    for course in courses:
        num = 0
        for stu in students:
            if course in stu.courses.all():
                num += 1
        counts[course.course_name] = num

    return {"registered_students": counts}
