
from notes.views import MarkAsRead, NotesViewset, ShareNotesViewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('notes', NotesViewset)
# router.register('share-notes', ShareNotesViewset)
search_user = ShareNotesViewset.as_view(
    {
        "get": "retrieve",
    }
)

urlpatterns = [
    path('', include(router.urls)),
    path('share-note/<int:pk>',
         ShareNotesViewset.as_view({"put": "update"}), name="share_note"),
    path('mark-as-read/', MarkAsRead.as_view({'post': 'create'})),

]
