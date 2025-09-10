# Quiz Platform API - Machine Test for Aakri Impact

## Overview
A RESTful backend for a quiz platform built with **Django** and **Django REST Framework**.  
The system supports two user roles (**Admin** and **Normal User**) with JWT authentication.

## Features
- 🔐 **Authentication**: User registration and login using JWT  
- 🧑‍💻 **Admin role**:
  - Create categories  
  - Create quizzes  
  - Add questions with options  
- 👤 **Normal User role**:
  - Attempt quizzes  
  - View submission history  
- 🧮 **Automatic scoring system**  
- 🛡 **Role-based permissions**  

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/quiz-platform-api.git
   cd quiz-platform-api

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # venv\Scripts\activate  on windows

3. **Install Dependencies**
    ```bash
    cd quizapi
    pip install -r requirements.txt

4. **Apply Migration**
    ```bash
    python manage.py migrate

5. **Create Superuser**
    ```bash
    python manage.py createsuperuser

6. **Run the Development Server**
    ```bash
    python manage.py runserver

## API Documentation
Access the API documentation at: `https://documenter.getpostman.com/view/31209169/2sB3HnM1Hh`