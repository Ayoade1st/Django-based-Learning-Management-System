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

# serializers.py
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        if data['course'].enrolled_students >= data['course'].capacity:
            raise serializers.ValidationError("Course is at full capacity")
        return data

# views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['start_date', 'end_date']
    ordering_fields = ['start_date', 'title']

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'student']

# Frontend views
def dashboard(request):
    context = {
        'courses_count': Course.objects.count(),
        'students_count': Student.objects.count(),
        'enrollments_count': Enrollment.objects.count(),
    }
    return render(request, 'lms/dashboard.html', context)

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'lms/course_list.html', {'courses': courses})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'lms/student_list.html', {'students': students})

def enrollment_list(request):
    enrollments = Enrollment.objects.all()
    courses = Course.objects.all()
    students = Student.objects.all()
    context = {
        'enrollments': enrollments,
        'courses': courses,
        'students': students,
    }
    return render(request, 'lms/enrollment_list.html', context)

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', dashboard, name='dashboard'),
    path('courses/', course_list, name='course_list'),
    path('students/', student_list, name='student_list'),
    path('enrollments/', enrollment_list, name='enrollment_list'),
]