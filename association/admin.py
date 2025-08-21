from django.contrib import admin
from .models import Student, User, Article, ArticleAuthors, Announcement, Event, EventRegistration, Comment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "student_number", "name", "role")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "email", "created_at")

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "published_at", "updated_at")
    list_filter = ("status",)

@admin.register(ArticleAuthors)
class ArticleAuthorsAdmin(admin.ModelAdmin):
    list_display = ("id", "article_id", "users_id")

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "created_at")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "capacity", "registered_count", "start_at", "end_at")

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "registered_at")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "target_type", "target_id", "created_at")
    list_filter = ("target_type",)
  
