from django.db import models
from django.contrib.auth.models import AbstractUser

from ckeditor.fields import RichTextField

# Create your models here.

class User(AbstractUser):
    pass

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=50, unique= True)

    def __str__(self):
        return self.name

class Course(BaseModel):
    subject = models.CharField(max_length=255)
    des = models.TextField()
    image = models.ImageField(upload_to='courses/%Y/%m')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject

class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='courses/%Y/%m')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject' , 'course')

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique= True)

    def __str__(self):
        return self.name