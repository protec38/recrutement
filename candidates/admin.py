from django.contrib import admin
from django_transitions.admin import WorkflowAdminMixin

from . import models
from .models import Candidate
from .state_machine import CandidateStatus, CandidateStateMachineMixin


class QuestionCandidateInline(admin.TabularInline):
    model = models.QuestionCandidate
    extra = 0
    readonly_fields = ['question', 'text']
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


class DiplomaInline(admin.TabularInline):
    model = models.Diploma
    extra = 0


class CandidateAdmin(WorkflowAdminMixin, admin.ModelAdmin):
    model = Candidate
    fields = ['first_name', 'last_name', 'birth_date', 'email']
    list_filter = ['status']
    list_display = ['first_name', 'last_name', 'status', 'update']
    inlines = [DiplomaInline, QuestionCandidateInline]

    actions = ['tadada']

    @admin.action(permissions=['change'])
    def tadada(self):
        ...

    def get_actions(self, request):
        actions = super().get_actions(request)
        print(actions)
        status_filter = request.GET.get("status__exact", None)
        triggers = CandidateStateMachineMixin.machine.get_triggers(status_filter)
        for trigger in triggers:
            if self.has_delete_permission(request):  # TODO: change this permission to appropriate one
                def trigger_fun(modeladmin, request, queryset):
                    for candidate in queryset:
                        getattr(candidate, trigger)()
                        candidate.save()

                actions[trigger] = (trigger_fun, trigger, CandidateStatus.TRANSITION_LABELS[trigger]['label'])

        return actions


admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.QuestionTemplate)


