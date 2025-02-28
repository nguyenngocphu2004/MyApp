from django.contrib import admin
from django.db.models import Count
from django.template.backends.django import Template
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.urls import path
from courses.models import Category, Course, Lesson, Tag

from django import forms
from ckeditor_uploader.widgets \
import CKEditorUploadingWidget
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'


class MyLesson(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'create_date']
    search_fields = ['subject']
    list_filter = ['id', 'create_date']
    list_editable = ['subject']
    readonly_fields = ['image_view']
    form = LessonForm

    def image_view(self, lesson):
        return mark_safe(f"<img src='/static/{lesson.image.name}' width='200' />")

    class Media:
        css = {
            'all' : ('/static/css/style.css',)
        }

class MyAdminSite(admin.AdminSite):
    site_header = 'OU eCourse Online'
    def get_urls(self):
        return [path('course-stats/',self.course_stats),] + super().get_urls()
    def course_stats(self, request):
        stats = Category.objects.annotate(course_count=Count('course__id')).values('id', 'name', 'course_count')
        return TemplateResponse(request,'admin/stats.html',{
            'stats' : stats
        })

admin_site = MyAdminSite(name='eCourse')

admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Lesson, MyLesson)
admin_site.register(Tag)