from django.urls import path, include

from rest_framework.routers import DefaultRouter
# from rest_framework.routers import DefaultRouter

from Company import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('', views.Resume)

urlpatterns = [
    # path('', include(router.urls))
    path('', views.Resume.as_view()),
    path('<str:name>', views.Detail.as_view())
]
