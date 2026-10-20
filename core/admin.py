from django.contrib import admin
from .models import CompanySettings, PageContent, Job, VIPMember, VisitorLog, ContactMessage


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ("company_name_en", "company_name_es", "updated_at")

    def has_add_permission(self, request):
        return not CompanySettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = (
        "slug", "title_en", "title_es", "is_published", "updated_at"
    )
    list_filter = ("is_published",)
    search_fields = ("slug", "title_en", "title_es")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title_en", "title_es", "location", "is_active", "created_at"
    )
    list_filter = ("is_active", "location")
    search_fields = (
        "title_en", "title_es", "description_en", "description_es"
    )
    list_editable = ("is_active",)


@admin.register(VIPMember)
class VIPMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "joined_date",
        "membership_date",
        "membership_level",
        "daily_income",
        "currency",
        "is_published",
    )
    list_filter = ("membership_level", "currency", "is_published")
    search_fields = ("name", "membership_level")
    list_editable = ("is_published",)


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "path", "visited_at")
    list_filter = ("visited_at",)
    search_fields = ("ip_address", "path")
    readonly_fields = (
        "ip_address", "path", "visited_at", "user_agent"
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    list_editable = ("is_read",)
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
