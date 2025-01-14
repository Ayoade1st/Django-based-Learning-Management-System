from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Count, F
from django.core.exceptions import ValidationError
from .models import Course, Student, Enrollment
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer

class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Course Views
class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['start_date', 'end_date']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'title', 'enrolled_students']

    def get_queryset(self):
        return Course.objects.annotate(
            total_enrollments=Count('enrollment')
        ).select_related()

class CourseCreate(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.annotate(
            total_enrollments=Count('enrollment')
        ).prefetch_related(
            Prefetch('enrollment_set', 
                    queryset=Enrollment.objects.select_related('student'))
        )

class CourseUpdate(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            new_capacity = request.data.get('capacity')
            
            if new_capacity and new_capacity < instance.enrolled_students:
                raise ValidationError("New capacity cannot be less than current enrollment")
            
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class CourseDelete(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.enrolled_students > 0:
            return Response(
                {'error': 'Cannot delete course with enrolled students'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

class CourseEnrollmentStatus(APIView):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        data = {
            'total_capacity': course.capacity,
            'current_enrollment': course.enrolled_students,
            'available_seats': course.capacity - course.enrolled_students,
            'is_full': course.enrolled_students >= course.capacity,
            'enrollment_percentage': (course.enrolled_students / course.capacity) * 100
        }
        return Response(data)

# Student Views
class StudentList(generics.ListAPIView):
    serializer_class = StudentSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

    def get_queryset(self):
        return Student.objects.annotate(
            courses_enrolled=Count('enrollment')
        ).prefetch_related('enrollment_set')

class StudentCreate(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class StudentDetail(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.prefetch_related(
            Prefetch('enrollment_set',
                    queryset=Enrollment.objects.select_related('course'))
        )

class StudentUpdate(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDelete(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.enrollment_set.exists():
            return Response(
                {'error': 'Cannot delete student with active enrollments'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

# Enrollment Views
class EnrollmentList(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'student']

    def get_queryset(self):
        queryset = Enrollment.objects.select_related('course', 'student')
        course_id = self.request.query_params.get('course_id', None)
        student_id = self.request.query_params.get('student_id', None)

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset

class EnrollmentCreate(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        try:
            course = get_object_or_404(Course, pk=request.data.get('course'))
            
            # Check if student is already enrolled
            if Enrollment.objects.filter(
                course=course,
                student_id=request.data.get('student')
            ).exists():
                raise ValidationError("Student already enrolled in this course")

            # Check course capacity
            if course.enrolled_students >= course.capacity:
                raise ValidationError("Course is at full capacity")

            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class EnrollmentDetail(generics.RetrieveAPIView):
    queryset = Enrollment.objects.select_related('course', 'student')
    serializer_class = EnrollmentSerializer

class EnrollmentDelete(generics.DestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            enrollment = self.get_object()
            course = enrollment.course
            
            # Update course enrolled_students count
            course.enrolled_students = F('enrolled_students') - 1
            course.save()
            
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
