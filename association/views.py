from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Student, User, Announcement, Article, ArticleAuthors, Event, EventRegistration, Comment
from .serializers import StudentSerializer, UserSerializer, AnnouncementSerializer, ArticleSerializer, EventSerializer, CommentSerializer

@api_view(["POST"])
def login_view(request):
    sid = request.data.get("student_number")
    email = request.data.get("email")
    password = request.data.get("password")
    if not sid:
        return Response({"detail":"student_number required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        student = Student.objects.get(student_number=sid)
    except Student.DoesNotExist:
        return Response({"detail":"student not found"},status=status.HTTP_404_NOT_FOUND)
    try:
        user = User.objects.get(student_id=student.id)
    except User.DoesNotExist:
        student_data = StudentSerializer(student).data
        return Response({"student":student_data,"user":None})
    if email is None and password is None:
        student_data = StudentSerializer(student).data
        user_data = UserSerializer(user).data
        return Response({"student":student_data,"user":user_data})
    if user.email == email and user.password == password:
        student_data = StudentSerializer(student).data
        user_data = UserSerializer(user).data
        combined = {**student_data,**{"id":user.id,"email":user.email,"password":user.password,"created_at":user.created_at}}
        return Response({"user":combined})
    return Response({"detail":"invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def create_user(request):
    student_number = request.data.get("student_number")
    email = request.data.get("email")
    password = request.data.get("password")
    if not (student_number and email and password):
        return Response({"detail":"student_number,email,password required"},status=status.HTTP_400_BAD_REQUEST)
    student = get_object_or_404(Student, student_number=student_number)
    if User.objects.filter(student_id=student.id).exists():
        return Response({"detail":"user exists"},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create(student_id=student.id,email=email,password=password)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

@api_view(["GET","POST"])
def announcements_list_create(request):
    if request.method == "GET":
        anns = Announcement.objects.select_related("author__student").all()
        return Response(AnnouncementSerializer(anns,many=True).data)
    author_id = request.data.get("author_id")
    title = request.data.get("title")
    content = request.data.get("content")
    if not (author_id and title and content):
        return Response({"detail":"author_id,title,content required"},status=status.HTTP_400_BAD_REQUEST)
    author = get_object_or_404(User, id=author_id)
    ann = Announcement.objects.create(author=author, title=title, content=content)
    return Response(AnnouncementSerializer(ann).data, status=status.HTTP_201_CREATED)

@api_view(["GET","PUT","DELETE"])
def announcement_detail(request, pk):
    ann = get_object_or_404(Announcement, id=pk)
    if request.method == "GET":
        return Response(AnnouncementSerializer(ann).data)
    role = request.data.get("role")
    if request.method == "PUT":
        if role not in ("MEMBER","ADMIN"):
            return Response({"detail":"forbidden"},status=status.HTTP_403_FORBIDDEN)
        ann.title = request.data.get("title",ann.title)
        ann.content = request.data.get("content",ann.content)
        ann.save()
        return Response(AnnouncementSerializer(ann).data)
    if request.method == "DELETE":
        if role not in ("MEMBER","ADMIN"):
            return Response({"detail":"forbidden"},status=status.HTTP_403_FORBIDDEN)
        ann.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET","POST"])
def articles_list_create(request):
    if request.method == "GET":
        status_filter = request.query_params.get("status","APPROVED")
        arts = Article.objects.filter(status=status_filter)
        return Response(ArticleSerializer(arts,many=True).data)
    title = request.data.get("title")
    content = request.data.get("content")
    user_id = request.data.get("user_id")
    if not (title and content and user_id):
        return Response({"detail":"title,content,user_id required"},status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User,id=user_id)
    st = "APPROVED" if getattr(user,"student",None) and user.student.role=="ADMIN" else "PENDING"
    art = Article.objects.create(title=title,content=content,status=st)
    ArticleAuthors.objects.create(article_id=art, users_id=user)
    return Response(ArticleSerializer(art).data,status=status.HTTP_201_CREATED)

@api_view(["GET","PUT","DELETE"])
def article_detail(request, pk):
    art = get_object_or_404(Article, id=pk)
    if request.method == "GET":
        return Response(ArticleSerializer(art).data)
    role = request.data.get("role")
    if role != "ADMIN":
        return Response({"detail":"forbidden"},status=status.HTTP_403_FORBIDDEN)
    if request.method == "PUT":
        art.title = request.data.get("title",art.title)
        art.content = request.data.get("content",art.content)
        art.save()
        return Response(ArticleSerializer(art).data)
    if request.method == "DELETE":
        art.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def admin_pending_articles(request):
    arts = Article.objects.filter(status="PENDING")
    return Response(ArticleSerializer(arts,many=True).data)

@api_view(["POST"])
def admin_article_action(request, pk, action):
    role = request.data.get("role")
    if role != "ADMIN":
        return Response({"detail":"forbidden"},status=status.HTTP_403_FORBIDDEN)
    art = get_object_or_404(Article, id=pk)
    if action == "approve":
        art.status = "APPROVED"
    else:
        art.status = "REJECTED"
    art.save()
    return Response(ArticleSerializer(art).data)

@api_view(["GET","POST"])
def events_list_create(request):
    if request.method == "GET":
        evs = Event.objects.all()
        return Response(EventSerializer(evs,many=True).data)
    title = request.data.get("title")
    description = request.data.get("description")
    capacity = request.data.get("capacity")
    role = request.data.get("role")
    if role != "ADMIN":
        return Response({"detail":"forbidden"},status=status.HTTP_403_FORBIDDEN)
    ev = Event.objects.create(title=title,description=description,capacity=int(capacity),registered_count=0)
    return Response(EventSerializer(ev).data,status=status.HTTP_201_CREATED)

@api_view(["GET"])
def event_detail(request, pk):
    ev = get_object_or_404(Event,id=pk)
    return Response(EventSerializer(ev).data)

@api_view(["POST"])
def event_join(request, pk):
    user_id = request.data.get("user_id")
    user = get_object_or_404(User,id=user_id)
    ev = get_object_or_404(Event,id=pk)
    if EventRegistration.objects.filter(event=ev,user=user).exists():
        return Response({"detail":"already joined"},status=status.HTTP_400_BAD_REQUEST)
    if ev.registered_count >= ev.capacity:
        return Response({"detail":"event full"},status=status.HTTP_400_BAD_REQUEST)
    EventRegistration.objects.create(event=ev,user=user)
    ev.registered_count += 1
    ev.save()
    return Response({"detail":"joined"},status=status.HTTP_201_CREATED)

@api_view(["GET"])
def event_participants(request):
    event_id = request.query_params.get("event_id")
    if not event_id:
        return Response({"detail":"event_id required"},status=status.HTTP_400_BAD_REQUEST)
    regs = EventRegistration.objects.filter(event_id=event_id).select_related("user__student")
    out = [{"student_number":r.user.student.student_number,"name":r.user.student.name} for r in regs]
    return Response(out)

@api_view(["GET","POST"])
def comments_list_create(request):
    if request.method == "GET":
        tt = request.query_params.get("target_type")
        tid = request.query_params.get("target_id")
        if not (tt and tid):
            return Response([],status=status.HTTP_200_OK)
        comms = Comment.objects.filter(target_type=tt,target_id=tid).select_related("author__student").order_by("created_at")
        return Response(CommentSerializer(comms,many=True).data)
    author_id = request.data.get("author_id")
    target_type = request.data.get("target_type")
    target_id = request.data.get("target_id")
    content = request.data.get("content")
    if not (author_id and target_type and target_id and content):
        return Response({"detail":"author_id,target_type,target_id,content required"},status=status.HTTP_400_BAD_REQUEST)
    author = get_object_or_404(User,id=author_id)
    c = Comment.objects.create(author=author,target_type=target_type,target_id=target_id,content=content)
    return Response(CommentSerializer(c).data,status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def comment_delete(request, pk):
    role = request.data.get("role")
    if role != "ADMIN":
        return Response({"detail":"forbidden"},status=status.HTTP_403_FORBIDDEN)
    c = get_object_or_404(Comment,id=pk)
    c.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def admin_users(request):
    us = User.objects.select_related("student").all()
    return Response(UserSerializer(us,many=True).data)
