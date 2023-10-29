from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone

User = get_user_model()


class Company(models.Model):
    name_regex = RegexValidator(
                regex=r'^[آ-ی\s]+$',
                message='The name should only contain Farsi letters and spaces',
                code='invalid_name'
            )
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    name = models.CharField(max_length=255, validators=[name_regex], verbose_name=_('name'))
    car_count = models.PositiveIntegerField(default=0, verbose_name=_('car count'))

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        db_table = 'company'

    def __str__(self):
        return self.name


class OTPCode(models.Model):
    code = models.CharField(max_length=6, verbose_name=_('code'))
    sent_at = models.DateTimeField(default=timezone.now, verbose_name=_('sent_at'))
    last_sent_at = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False, verbose_name=_('is_expired'))
    is_used = models.BooleanField(default=False, verbose_name=_('is_used'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'), related_name='otp_codes')

    class Meta:
        verbose_name = _('OTPCode')
        verbose_name_plural = _('OTPCodes')
        db_table = 'OTPCode'

    def __str__(self):
        return self.user.username


class Car(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('company'))

    class Meta:
        verbose_name = _('car')
        verbose_name_plural = _('cars')
        db_table = 'car'

    def __str__(self):
        return self.company.name

