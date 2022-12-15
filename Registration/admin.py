from django.contrib import admin
from Registration.models import registrants, centers, statuses, time_slots, vaccination_status, vacancies

# Register your models here.
admin.site.register(registrants)
admin.site.register(centers)
admin.site.register(statuses)
admin.site.register(time_slots)
admin.site.register(vaccination_status)
admin.site.register(vacancies)
