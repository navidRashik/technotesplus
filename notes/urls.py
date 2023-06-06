from notes.views import MarkAsRead, NotesViewset, ShareNotesViewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("notes", NotesViewset)
# router.register('share-notes', ShareNotesViewset)


urlpatterns = [
    path("", include(router.urls), name="notes_viwsets"),
    path(
        "share-note/<int:pk>",
        ShareNotesViewset.as_view({"put": "update"}),
        name="share_note",
    ),
    path("mark-as-read/", MarkAsRead.as_view({"post": "create"}), name="mark_as_read"),
]
