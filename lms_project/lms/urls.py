from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='course-list'),
    path('courses/create/', views.CourseCreate.as_view(), name='course-create'),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    path('courses/<int:pk>/update/', views.CourseUpdate.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', views.CourseDelete.as_view(), name='course-delete'),
    path('courses/<int:pk>/status/', views.CourseEnrollmentStatus.as_view(), name='course-status'),
    path('students/', views.StudentList.as_view(), name='student-list'),
    path('students/create/', views.StudentCreate.as_view(), name='student-create'),
    path('students/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student-delete'),
    path('enrollments/', views.EnrollmentList.as_view(), name='enrollment-list'),
    path('enrollments/create/', views.EnrollmentCreate.as_view(), name='enrollment-create'),
    path('enrollments/<int:pk>/', views.EnrollmentDetail.as_view(), name='enrollment-detail'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDelete.as_view(), name='enrollment-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]





# from django.urls import path
# from . import views

# urlpatterns = [
    # # Course URLs
    # path('courses/', views.CourseList.as_view(), name='course-list'),
    # path('courses/create/', views.CourseCreate.as_view(), name='course-create'),
    # path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    # path('courses/<int:pk>/update/', views.CourseUpdate.as_view(), name='course-update'),
    # path('courses/<int:pk>/delete/', views.CourseDelete.as_view(), name='course-delete'),
    # path('courses/<int:pk>/status/', views.CourseEnrollmentStatus.as_view(), name='course-status'),

    # # Student URLs
    # path('students/', views.StudentList.as_view(), name='student-list'),
    # path('students/create/', views.StudentCreate.as_view(), name='student-create'),
    # path('students/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    # path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student-update'),
    # path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student-delete'),

    # # Enrollment URLs
    # path('enrollments/', views.EnrollmentList.as_view(), name='enrollment-list'),
    # path('enrollments/create/', views.EnrollmentCreate.as_view(), name='enrollment-create'),
    # path('enrollments/<int:pk>/', views.EnrollmentDetail.as_view(), name='enrollment-detail'),
    # path('enrollments/<int:pk>/delete/', views.EnrollmentDelete.as_view(), name='enrollment-delete'),
# ]



# from django.urls import path
# from . import views

# urlpatterns = [
    # # Course URLs
    # path('courses/', views.CourseList.as_view(), name='course-list'),
    # path('courses/create/', views.CourseCreate.as_view(), name='course-create'),
    # path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    # path('courses/<int:pk>/update/', views.CourseUpdate.as_view(), name='course-update'),
    # path('courses/<int:pk>/delete/', views.CourseDelete.as_view(), name='course-delete'),
    # path('courses/<int:pk>/status/', views.CourseEnrollmentStatus.as_view(), name='course-status'),

    # # Student URLs
    # path('students/', views.StudentList.as_view(), name='student-list'),
    # path('students/create/', views.StudentCreate.as_view(), name='student-create'),
    # path('students/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    # path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='student-update'),
    # path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='student-delete'),

    # # Enrollment URLs
    # path('enrollments/', views.EnrollmentList.as_view(), name='enrollment-list'),
    # path('enrollments/create/', views.EnrollmentCreate.as_view(), name='enrollment-create'),
    # path('enrollments/<int:pk>/', views.EnrollmentDetail.as_view(), name='enrollment-detail'),
    # path('enrollments/<int:pk>/delete/', views.EnrollmentDelete.as_view(), name='enrollment-delete'),
# ]