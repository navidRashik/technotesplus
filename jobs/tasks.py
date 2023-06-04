from notes.models import Notes, SharedUnseenNotes
from celery import shared_task


@shared_task
def save_shared_note(user_id_list, note_id, unseen_notes_usr_pk_list):
    if not unseen_notes_usr_pk_list:
        return
    obj_list = []
    instance = Notes.objects.get(pk=note_id)
    for usr_pk in unseen_notes_usr_pk_list:
        obj_list.append(SharedUnseenNotes(shared_to_id=usr_pk, note=instance))
    SharedUnseenNotes.objects.bulk_create(
        objs=obj_list,
        batch_size=len(unseen_notes_usr_pk_list),
        ignore_conflicts=True,
    )
    instance.shared_with.set(user_id_list)
