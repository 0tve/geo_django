from django import urls
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    urls.path('auth/login/', auth_views.obtain_auth_token, name='login'),
    urls.path('auth/register/', views.RegisterView.as_view(), name='register'),
    urls.path('points/', views.PointCreateView.as_view(),
              name='point-create'),
    urls.path('points/search/', views.PointListView.as_view(),
              name='point-search'),
    urls.path('points/<int:point_id>/messages/',
              views.MessageCreateView.as_view(), name='message-create'),
    urls.path('messages/search/', views.MessageListView.as_view(),
              name='message-search')
]
