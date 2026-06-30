from .models import Activity


def log_activity(action, description, performed_by):

    activity = Activity.objects.create(
        action=action,
        description=description,
        performed_by=performed_by,
    )

   