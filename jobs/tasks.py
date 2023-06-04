from notes.models import SharedUnseenNotes
from celery import shared_task

@shared_task
def save_shared_note(user_id_list, instance, unseen_notes_usr_pk_list):
        obj_list = []
        for usr_pk in unseen_notes_usr_pk_list:
            obj_list.append(SharedUnseenNotes(shared_to_id=usr_pk, note=instance))
        if unseen_notes_usr_pk_list:
            SharedUnseenNotes.objects.bulk_create(
                objs=obj_list,
                batch_size=len(unseen_notes_usr_pk_list),
                ignore_conflicts=True,
            )
        instance.shared_with.set(user_id_list)
        instance.save()