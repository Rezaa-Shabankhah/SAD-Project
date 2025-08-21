from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view),
    path("users/", views.create_user),
    path("announcements/", views.announcements_list_create),
    path("announcements/<int:pk>/", views.announcement_detail),
    path("articles/", views.articles_list_create),
    path("articles/<int:pk>/", views.article_detail),
    path("admin/pending_articles/", views.admin_pending_articles),
    path("admin/articles/<int:pk>/<str:action>/", views.admin_article_action),
    path("events/", views.events_list_create),
    path("events/<int:pk>/", views.event_detail),
    path("events/<int:pk>/join/", views.event_join),
    path("admin/event_participants/", views.event_participants),
    path("comments/", views.comments_list_create),
    path("comments/<int:pk>/", views.comment_delete),
    path("admin/users/", views.admin_users),
]
