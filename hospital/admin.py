from django.contrib import admin

from .models import BloodRequest, Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'area', 'contact_no')
    search_fields = ('name', 'city', 'area', 'contact_no')
    list_filter = ('city',)
    ordering = ('name',)


@admin.register(BloodRequest)
class HospitalBloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'blood_group', 'component_type', 'units_needed', 'urgency', 'status', 'request_time')
    list_filter = ('status', 'urgency', 'blood_group', 'component_type', 'request_time')
    search_fields = ('hospital__name', 'hospital__city')
    list_select_related = ('hospital',)
    readonly_fields = ('request_time',)
    actions = ('mark_fulfilled', 'mark_cancelled')

    @admin.action(description='Mark selected requests as fulfilled')
    def mark_fulfilled(self, request, queryset):
        queryset.update(status='FULFILLED')

    @admin.action(description='Mark selected requests as cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
