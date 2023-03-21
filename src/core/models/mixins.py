from django.db import models


class CreatedAtUpdatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="Время последнего изменения"
    )

    class Meta:
        abstract = True
