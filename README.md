# Quiz Platform API - Machine Test for Aakri Impact

## Overview
A RESTful backend for a quiz platform built with Django and Django REST Framework. Supports two user roles (Admin and Normal User) with JWT authentication.

## Features
- User registration and login with JWT authentication
- Admin can create categories, quizzes, questions with options
- Users can attempt quizzes and view their submission history
- Automatic scoring system
- Role-based permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quiz-platform-api.git
cd quiz-platform-api

2. Create a virtual environment: 
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
```bash
pip install -r requirements.txt

4. Apply migrations:
```bash
python manage.py migrate

5. Create a superuser:
```bash
python manage.py createsuperuser

6. Run the development server:
```bash
cd quizapi
python manage.py runserver


API DOCUMENTATION: https://documenter.getpostman.com/view/31209169/2sB3HnM1Hh