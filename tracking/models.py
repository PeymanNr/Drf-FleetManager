from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from company.models import Car


class Location(models.Model):
    latitude = models.FloatField(verbose_name=_('latitude'))
    longitude = models.FloatField(verbose_name=_('longitude'))
    speed = models.FloatField(verbose_name=_('speed'))
    car_id = models.ForeignKey(Car, verbose_name=_('car_id'),
                               on_delete=models.CASCADE)
    acceleration = models.FloatField(verbose_name=_('acceleration'))
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name=_('created_at'))

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        db_table = 'location'

    def __str__(self):
        return f'Location for Car {self.car_id} at {self.created_at}'
