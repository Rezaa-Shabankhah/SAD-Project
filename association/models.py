from django.db import models


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_number = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "students"
        managed = False


class User(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, db_column="student_id", on_delete=models.CASCADE)
    email = models.CharField(max_length=150, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "users"
        managed = False


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    status = models.CharField(max_length=10)
    published_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "article"
        managed = False


class ArticleAuthors(models.Model):
    id = models.AutoField(primary_key=True)
    article_id = models.ForeignKey(Article, db_column="article_id", on_delete=models. CASCADE)
    users_id = models.ForeignKey(User, db_column="users_id", on_delete=models. CASCADE)

    class Meta:
        db_table = "article_authors"
        managed = False


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, db_column="author_id", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "announcement"
        managed = False


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    capacity = models.IntegerField()
    registered_count = models.IntegerField()
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "event"
        managed = False


class EventRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, db_column="event_id", on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column="users_id", on_delete=models.CASCADE)
    registered_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "event_registration"
        managed = False


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, db_column="author_id", null=True, on_delete=models.SET_NULL)
    target_type = models.CharField(max_length=20)
    target_id = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "comments"
        managed = False
