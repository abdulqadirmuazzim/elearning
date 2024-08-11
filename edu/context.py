from accounts.models import Course


def course_links(req):
    courses = Course.objects.all()
    return {"Courses": courses}
