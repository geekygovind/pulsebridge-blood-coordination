from django.contrib import admin

from .models import BloodRequest, Donor, Patient

admin.site.site_header = 'PulseBridge Administration'
admin.site.site_title = 'PulseBridge Admin'
admin.site.index_title = 'Manage donors, patients, requests, hospitals, and inventory'


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'area', 'contact_no')
    search_fields = ('name', 'city', 'area', 'contact_no')
    list_filter = ('city',)
    ordering = ('name',)


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'city', 'contact_no', 'is_available', 'last_donation_date', 'registered_at')
    list_filter = ('blood_group', 'city', 'is_available')
    search_fields = ('name', 'city', 'contact_no')
    readonly_fields = ('registered_at',)
    actions = ('mark_available', 'mark_unavailable')

    @admin.action(description='Mark selected donors as available')
    def mark_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description='Mark selected donors as unavailable')
    def mark_unavailable(self, request, queryset):
        queryset.update(is_available=False)


@admin.register(BloodRequest)
class PatientBloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'blood_group', 'component_type', 'units_needed', 'urgency', 'status', 'request_time')
    list_filter = ('status', 'urgency', 'blood_group', 'component_type', 'request_time')
    search_fields = ('patient__name', 'patient__contact_no')
    list_select_related = ('patient',)
    readonly_fields = ('request_time',)
    actions = ('mark_fulfilled', 'mark_cancelled')

    @admin.action(description='Mark selected requests as fulfilled')
    def mark_fulfilled(self, request, queryset):
        queryset.update(status='FULFILLED')

    @admin.action(description='Mark selected requests as cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
