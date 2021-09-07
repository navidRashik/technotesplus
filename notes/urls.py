
from notes.views import NotesViewset, ShareNotesViewset
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('notes',NotesViewset)
# router.register('share-notes', ShareNotesViewset)
share_note = ShareNotesViewset.as_view(
    {
        "get": "retrieve",
    }
)

urlpatterns=[
    path('', include(router.urls)),
    path('share-note/search-user', share_note, name='get_user_detail'),
    path('share-note/<int:pk>',
         ShareNotesViewset.as_view({"put": "update"}), name="share_note"),

]
