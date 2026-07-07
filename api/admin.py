from django.contrib import admin
from .models import ParticipantProfile, Skill, Event, Participation, ParticipantSkill

class ParticipantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'institution', 'group_name', 'total_hours')
    list_filter = ('user_type', 'institution')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'institution')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'status', 'date_start', 'organizer')
    list_filter = ('status', 'date_start')
    search_fields = ('title', 'code')
    # Убираем filter_horizontal для skills (используется через промежуточную модель)
    # Вместо этого можно добавить inline для EventSkill, но для простоты оставим так

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'hours_claimed', 'is_verified', 'verified_at')
    list_filter = ('is_verified', 'event')
    search_fields = ('participant__user__first_name', 'participant__user__last_name', 'event__title')

class ParticipantSkillAdmin(admin.ModelAdmin):
    list_display = ('participant', 'skill', 'level', 'updated_at')
    list_filter = ('skill', 'level')

admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(ParticipantSkill, ParticipantSkillAdmin)
