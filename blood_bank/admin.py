from django.contrib import admin

from .models import BloodBank, BloodTransfer, BloodUnit


@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'area', 'contact_no')
    search_fields = ('name', 'city', 'area', 'contact_no')
    list_filter = ('city',)
    ordering = ('name',)


@admin.register(BloodUnit)
class BloodUnitAdmin(admin.ModelAdmin):
    list_display = ('blood_bank', 'blood_group', 'component_type', 'units', 'status', 'donation_date', 'expiry_date')
    list_filter = ('status', 'blood_group', 'component_type', 'blood_bank')
    search_fields = ('blood_bank__name', 'blood_bank__city')
    list_select_related = ('blood_bank',)
    date_hierarchy = 'expiry_date'
    actions = ('mark_available', 'mark_reserved', 'mark_expired')

    @admin.action(description='Mark selected units as available')
    def mark_available(self, request, queryset):
        queryset.update(status='AVAILABLE')

    @admin.action(description='Mark selected units as reserved')
    def mark_reserved(self, request, queryset):
        queryset.update(status='RESERVED')

    @admin.action(description='Mark selected units as expired')
    def mark_expired(self, request, queryset):
        queryset.update(status='EXPIRED')


@admin.register(BloodTransfer)
class BloodTransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'blood_bank', 'units_provided', 'transfer_time')
    search_fields = ('blood_bank__name', 'request__id')
    list_select_related = ('request', 'blood_bank')
    readonly_fields = ('transfer_time',)
