from django.db import models
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@contextmanager
def TestStep(title: str):
    """
    the purpose of this func is just for decoration for now. but if needed
    we can utilize this method if needed.
    """
    yield
