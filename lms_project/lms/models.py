# models.py
from django.db import models
from django.core.exceptions import ValidationError

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
    enrolled_students = models.IntegerField(default=0)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")
        if self.capacity < 0:
            raise ValidationError("Capacity must be positive")

    def __str__(self):
        return self.title

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.email})"

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new enrollments
            if self.course.enrolled_students >= self.course.capacity:
                raise ValidationError("Course is at full capacity")
            self.course.enrolled_students += 1
            self.course.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.course.enrolled_students -= 1
        self.course.save()
        super().delete(*args, **kwargs)