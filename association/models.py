from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_number = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=10)
    class Meta:
        db_table = "students"
        managed = False
    def __str__(self):
        if self.name:
            return f"{self.name} ({self.student_number})"
        return str(self.student_number)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, db_column="student_id", on_delete=models.CASCADE)
    email = models.CharField(max_length=150, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True)
    class Meta:
        db_table = "users"
        managed = False
    def __str__(self):
        if self.email:
            return self.email
        if getattr(self, "student", None):
            return str(self.student)
        return f"User {self.id}"

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
    def __str__(self):
        return self.title or f"Article {self.id}"

class ArticleAuthors(models.Model):
    id = models.AutoField(primary_key=True)
    article_id = models.ForeignKey(Article, db_column="article_id", on_delete=models.CASCADE)
    users_id = models.ForeignKey(User, db_column="users_id", on_delete=models.CASCADE)
    class Meta:
        db_table = "article_authors"
        managed = False
    def __str__(self):
        a = getattr(self, "article_id", None)
        u = getattr(self, "users_id", None)
        return f"{a} — {u}"

class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, db_column="author_id", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(null=True)
    class Meta:
        db_table = "announcement"
        managed = False
    def __str__(self):
        return self.title or f"Announcement {self.id}"

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
    def __str__(self):
        return self.title or f"Event {self.id}"

class EventRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, db_column="event_id", on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column="users_id", on_delete=models.CASCADE)
    registered_at = models.DateTimeField(null=True)
    class Meta:
        db_table = "event_registration"
        managed = False
    def __str__(self):
        e = getattr(self, "event", None)
        u = getattr(self, "user", None)
        return f"{e} — {u}"

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
    def __str__(self):
        return f"{self.target_type}#{self.target_id} by {self.author or 'unknown'}"
