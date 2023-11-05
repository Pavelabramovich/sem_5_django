from django.utils import timezone
import datetime
import config.settings as settings


def timer_processor(request):
    start_time = settings.SITE_START_TIME
    now = timezone.now()

    delta = now - start_time

    seconds = max(3600 - delta.seconds, 0)

    timer_value = str(datetime.timedelta(seconds=0 if seconds == 0 else seconds + 1))

    if timer_value.startswith('0'):
        timer_value = timer_value[2:]

    return {'seconds': seconds, 'tamer_value': timer_value}
