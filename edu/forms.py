from django import forms
from .models import Contact as con, Subscription as subs
from accounts.models import Course_Comment, Reply


# contact form
class comment(forms.ModelForm):
    class Meta:
        model = con
        fields = ["Name", "Email", "Subject", "Message"]


# subscription form
class subscription(forms.ModelForm):
    class Meta:
        model = subs
        fields = ["Email"]


# Course Comment from
class CourseComment_form(forms.ModelForm):
    class Meta:
        model = Course_Comment
        fields = ["comment"]

    def save(self, student, course):
        if self.is_valid():
            course_comment = Course_Comment.objects.create(
                user=student, course=course, comment=self.cleaned_data["comment"]
            )
            course_comment.save()
        else:
            raise forms.ValidationError("could not save comment")
        return self.data


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["reply"]

    def save(self, user, comment):
        if self.is_valid():
            comment_reply = Reply.objects.create(
                user=user, reply=self.cleaned_data["reply"]
            )
            comment_reply.save()
            comment_ = Course_Comment.objects.get(id=comment)
            comment_.replies.add(comment_reply)
        else:
            raise forms.ValidationError("Couldn't reply to this message")
        return self.data["reply"]
