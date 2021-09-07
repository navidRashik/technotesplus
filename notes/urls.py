
from notes.views import NotesViewset
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('notes',NotesViewset)
urlpatterns=[
    path('',include(router.urls))
]
