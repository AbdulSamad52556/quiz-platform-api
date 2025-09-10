from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    
    # Category endpoints (Admin only)
    path('categories/', views.CategoryView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Quiz endpoints (Admin only)
    path('quizzes/', views.QuizView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:pk>/toggle-active/', views.ToggleQuizActiveView.as_view(), name='toggle-quiz-active'),
    
    # Question endpoints (Admin only)
    path('questions/', views.QuestionView.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:pk>/toggle-active/', views.ToggleQuestionActiveView.as_view(), name='toggle-question-active'),
    
    # Option endpoints
    path('options/', views.OptionView.as_view(), name='option-list'),
    path('options/<int:pk>/', views.OptionDetailView.as_view(), name='option-detail'),

    # User endpoints
    path('quizzes/active/', views.ActiveQuizzesView.as_view(), name='active-quizzes'),
    path('quizzes/<int:quiz_id>/submit/', views.SubmitQuizView.as_view(), name='submit-quiz'),
    path('submissions/history/', views.UserSubmissionHistoryView.as_view(), name='submission-history'),
    
    # Admin endpoints
    path('admin/submissions/', views.AllSubmissionsView.as_view(), name='all-submissions'),

    # Test Auth
    path('test-auth/', views.TestAuthView.as_view(), name='test-auth'),

]