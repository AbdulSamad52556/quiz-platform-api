from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import CustomUser, Category, Quiz, Question, QuizSubmission, Option
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    CategorySerializer, QuizSerializer, QuestionSerializer,
    QuizSubmissionSerializer, QuizSubmissionHistorySerializer,
    OptionSerializer
)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.role == 'admin')

class IsNormalUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)
    
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuizView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        quizzes = Quiz.objects.filter(is_active=True)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_object(self, pk):
        return get_object_or_404(Quiz, pk=pk)
    
    def get(self, request, pk):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    
    def put(self, request, pk):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        quiz = self.get_object(pk)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        questions = Question.objects.filter(is_active=True)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_object(self, pk):
        return get_object_or_404(Question, pk=pk)
    
    def get(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    def put(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OptionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        options = Option.objects.all()
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OptionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_object(self, pk):
        return get_object_or_404(Option, pk=pk)
    
    def get(self, request, pk):
        option = self.get_object(pk)
        serializer = OptionSerializer(option)
        return Response(serializer.data)
    
    def put(self, request, pk):
        option = self.get_object(pk)
        serializer = OptionSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        option = self.get_object(pk)
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ToggleQuizActiveView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def patch(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        quiz.is_active = not quiz.is_active
        quiz.save()
        return Response({'is_active': quiz.is_active})

class ToggleQuestionActiveView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def patch(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question.is_active = not question.is_active
        question.save()
        return Response({'is_active': question.is_active})

class ActiveQuizzesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        quizzes = Quiz.objects.filter(is_active=True)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id, is_active=True)
        
        # Check if user has already submitted this quiz
        existing_submission = QuizSubmission.objects.filter(
            user=request.user, quiz=quiz
        ).first()
        
        if existing_submission:
            return Response(
                {'error': 'You have already submitted this quiz.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = request.data.copy()
        data['user'] = request.user.id
        data['quiz'] = quiz_id
        
        serializer = QuizSubmissionSerializer(data=data)
        if serializer.is_valid():
            submission = serializer.save(user=request.user, quiz=quiz)
            return Response(QuizSubmissionHistorySerializer(submission).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSubmissionHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        submissions = QuizSubmission.objects.filter(user=request.user)
        serializer = QuizSubmissionHistorySerializer(submissions, many=True)
        return Response(serializer.data)

class AllSubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        submissions = QuizSubmission.objects.all()
        serializer = QuizSubmissionHistorySerializer(submissions, many=True)
        return Response(serializer.data)

class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            "message": "Authentication successful!",
            "user_id": request.user.id,
            "username": request.user.username,
            "role": request.user.role,
            "is_authenticated": request.user.is_authenticated
        })