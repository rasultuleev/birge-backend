from django.contrib import admin
from .models import StudentProfile, Skill, Event, Participation, StudentSkill

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'group_name', 'university', 'total_hours', 'consent_employer')
    list_filter = ('university', 'group_name', 'consent_employer')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'university')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'studentprofile'):
            return qs.filter(university=request.user.studentprofile.university)
        return qs.none()

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'status', 'date_start', 'organizer')
    list_filter = ('status', 'date_start')
    search_fields = ('title', 'code')
    filter_horizontal = ('skills',)

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'hours_claimed', 'is_verified', 'verified_at')
    list_filter = ('is_verified', 'event')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'event__title')

class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'level', 'updated_at')
    list_filter = ('skill', 'level')

admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(StudentSkill, StudentSkillAdmin)
