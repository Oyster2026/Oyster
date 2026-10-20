
from django.db import models


class CompanySettings(models.Model):
    company_name_en = models.CharField(
        "Company Name (English)", max_length=200, blank=True
    )
    company_name_es = models.CharField(
        "Nombre de la empresa (Español)", max_length=200, blank=True
    )
    logo = models.ImageField(
        "Company Logo", upload_to="company/", blank=True, null=True
    )
    tagline_en = models.CharField(max_length=250, blank=True)
    tagline_es = models.CharField(max_length=250, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name_en or self.company_name_es or "Company Settings"

    class Meta:
        verbose_name = "Company Settings"
        verbose_name_plural = "Company Settings"


class PageContent(models.Model):
    slug = models.SlugField(
        unique=True, help_text="Example: about, home, contact"
    )
    title_en = models.CharField(max_length=200, blank=True)
    title_es = models.CharField(max_length=200, blank=True)
    body_en = models.TextField(blank=True)
    body_es = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en or self.title_es or self.slug

    class Meta:
        ordering = ["slug"]
        verbose_name = "Page Content"
        verbose_name_plural = "Page Content"


class Job(models.Model):
    title_en = models.CharField(max_length=200)
    title_es = models.CharField(max_length=200, blank=True)
    description_en = models.TextField()
    description_es = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    application_email = models.EmailField(blank=True)
    application_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en

    class Meta:
        ordering = ["-created_at"]


class VIPMember(models.Model):
    name = models.CharField(max_length=200)
    joined_date = models.DateField(
        help_text="Date the person first became a VIP member"
    )
    membership_date = models.DateField(
        help_text="Date associated with the VIP membership record"
    )
    membership_level = models.CharField(max_length=100)
    daily_income = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    bio_en = models.TextField(blank=True)
    bio_es = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.membership_level}"

    class Meta:
        ordering = ["-joined_date"]


class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=500)
    visited_at = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.ip_address} - {self.visited_at:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ["-visited_at"]
        verbose_name = "Visitor Log"
        verbose_name_plural = "Visitor Logs"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"