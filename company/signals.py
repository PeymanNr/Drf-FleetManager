from django.db.models.signals import post_save
from django.dispatch import receiver
from company.models import Car


@receiver(post_save, sender=Car)
def update_car_count(sender, instance, **kwargs):
    company = instance.company
    company.car_count = Car.objects.filter(company=company).count()
    company.save()
