from django.db.models.signals import post_save
from django.dispatch import receiver
from company.models import Car, Company


@receiver(post_save, sender=Company)
def create_initial_cars(sender, instance, created,  **kwargs):
    if created:
        car_counts = instance.car_count

        for _ in range(car_counts):
            Car.objects.create(company=instance)
