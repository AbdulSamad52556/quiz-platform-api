from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Category, Quiz, Question, QuizSubmission, UserAnswer, Option

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Quiz
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ('question', 'selected_option')

class QuizSubmissionSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True, write_only=True)
    user = UserSerializer(read_only=True)
    quiz = QuizSerializer(read_only=True)
    
    class Meta:
        model = QuizSubmission
        fields = '__all__'
        read_only_fields = ('user', 'quiz', 'score', 'total_questions', 'submitted_at')
    
    def create(self, validated_data):
        user_answers_data = validated_data.pop('user_answers')
        submission = QuizSubmission.objects.create(**validated_data)
        
        score = 0
        total_questions = 0
        
        for answer_data in user_answers_data:
            question = answer_data['question']
            selected_option = answer_data['selected_option']
            
            # Only count active questions
            if question.is_active:
                total_questions += 1

                try:
                    selected_option = Option.objects.get(id=selected_option, question=question)
                    is_correct = selected_option.is_correct
                except Option.DoesNotExist:
                    is_correct = False
                
                if is_correct:
                    score += 1
                
                UserAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )
        
        submission.score = score
        submission.total_questions = total_questions
        submission.save()
        
        return submission

class QuizSubmissionHistorySerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    
    class Meta:
        model = QuizSubmission
        fields = '__all__'