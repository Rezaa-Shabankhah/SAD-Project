from rest_framework import serializers
from .models import Student, User, Announcement, Article, ArticleAuthors, Event, EventRegistration, Comment

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id","student_number","name","role")

class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    class Meta:
        model = User
        fields = ("id","student","student_id","email","password","created_at")

class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ("id","author","author_name","title","content","created_at")
    def get_author_name(self,obj):
        return obj.author.student.name if getattr(obj,"author",None) and getattr(obj.author,"student",None) else None

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id","title","content","status","published_at","updated_at")

class ArticleAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAuthors
        fields = ("id","article_id","users_id")

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id","title","description","capacity","registered_count","start_at","end_at","created_at")

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ("id","event","user","registered_at")

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ("id","author","author_name","target_type","target_id","content","created_at","updated_at")
    def get_author_name(self,obj):
        return obj.author.student.name if getattr(obj,"author",None) and getattr(obj.author,"student",None) else None
