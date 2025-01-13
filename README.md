# Learning Management Platform API

This project implements a RESTful API for a simple Learning Management Platform (LMP) using Django and Django REST framework.  The API allows for managing courses, students, and enrollments.

## Features

* **Course Management:** Create, read, update, and delete courses.  Includes fields for title, description, start and end dates, capacity, and enrolled students.
* **Student Management:** Create, read, update, and delete student profiles. Includes fields for name, email, age, and gender.  Email uniqueness is enforced.
* **Enrollment Management:** Enroll students in courses, checking for available capacity.  Retrieve enrollments, optionally filtered by course or student.  Cancel enrollments.
* **Data Integrity:**  The number of enrolled students in a course is automatically updated upon enrollment and cancellation.
* **Validation:**  Input validation is implemented to ensure data consistency and prevent invalid operations (e.g., enrolling in a full course).
* **Filtering:**  Courses can be filtered by start and end dates. Enrollments can be filtered by course ID or student ID.
* **RESTful API:**  Uses standard HTTP methods (GET, POST, PUT, DELETE) for all operations.


## Technologies Used

* **Python:**  Programming language.
* **Django:**  Web framework.
* **Django REST Framework:**  For building the API.
* **SQLite (or other supported database):** Database for storing data.


## Setup

1. **Clone the repository:**
   ```bash
   git clone [<(https://github-profile-trophy.vercel.app/?username=Ayoade1st&theme=onedark)>]
