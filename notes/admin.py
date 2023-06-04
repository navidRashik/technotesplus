from django.contrib import admin

from notes.models import Notes, SharedUnseenNotes


# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]
    list_filter = ["id", "title"]
    search_fields = ["id", "title"]


admin.site.register(Notes, NoteAdmin)
admin.site.register(SharedUnseenNotes)
