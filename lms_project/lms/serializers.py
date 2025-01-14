from rest_framework import serializers
from .models import Course, Student, Enrollment
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'capacity', 'enrolled_students']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'age', 'gender']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'student', 'enrollment_date']

    def validate(self, data):
       if data['course'].enrolled_students >= data['course'].capacity:
          raise serializers.ValidationError("Course is at full capacity")
       return data