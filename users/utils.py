from users.models import LogEntry


def log_to_model(level, message, user=None):
    LogEntry.objects.create(level=level, message=message, user=user)
