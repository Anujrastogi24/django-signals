# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction, IntegrityError
from .models import Product
import time

@receiver(post_save, sender=Product)
def product_change(sender, instance, created, **kwargs):
    def long_running_task():
        print(f"Long Task: Processing {instance.name} (5 seconds)")
        time.sleep(5)
        print(f"Long Task Done")

    def short_running_task():
        print(f"Short Task: Processing {instance.name} (1 second)")
        time.sleep(1)
        print(f"Short Task Done")

    def medium_running_task():
        print(f"Medium Task: Processing {instance.name} (3 seconds)")
        time.sleep(3)
        print(f"Medium Task Done")

    # Ensure all signal operations happen within the same transaction
    try:
        with transaction.atomic():
            # Execute tasks sequentially
            long_running_task()
            short_running_task()
            medium_running_task()

            print("All tasks finished.")

            if created:
                print(f"Product created: {instance.name}")
            else:
                print(f"Product updated: {instance.name}")

    except IntegrityError as e:
        if "decimal places" in str(e):
            print(f"Transaction rolled back due to decimal point error: {e}")
        else:
            print(f"Transaction rolled back due to other error: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")
