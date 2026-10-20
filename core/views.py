from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import CompanySettings, PageContent, Job, VIPMember
from .forms import ContactMessageForm


def get_site_context(request):
    lang = request.GET.get("lang", request.session.get("site_lang", "en"))

    if lang not in ("en", "es"):
        lang = "en"

    request.session["site_lang"] = lang

    company = CompanySettings.objects.filter(pk=1).first()

    return {
        "lang": lang,
        "company": company,
        "company_name": (
            (company.company_name_es if lang == "es" else company.company_name_en)
            if company else ""
        ),
        "tagline": (
            (company.tagline_es if lang == "es" else company.tagline_en)
            if company else ""
        ),
    }


def home(request):
    context = get_site_context(request)
    context["page"] = PageContent.objects.filter(
        slug="home", is_published=True
    ).first()
    context["jobs"] = Job.objects.filter(is_active=True)[:3]
    context["vip_members"] = VIPMember.objects.filter(is_published=True)[:3]
    return render(request, "core/home.html", context)


def about(request):
    return show_page(request, "about")


def contact(request):
    context = get_site_context(request)

    context["page"] = PageContent.objects.filter(
        slug="contact",
        is_published=True
    ).first()

    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            contact_message = form.save()

            send_mail(
                subject=f"New Contact Message: {contact_message.subject}",
                message=(
                    f"Name: {contact_message.name}\n"
                    f"Email: {contact_message.email}\n"
                    f"Subject: {contact_message.subject}\n\n"
                    f"Message:\n{contact_message.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            context["success"] = True
            form = ContactMessageForm()
    else:
        form = ContactMessageForm()

    context["form"] = form
    context["page_slug"] = "contact"

    return render(request, "core/contact.html", context)


def become_vip(request):
    return show_page(request, "become-vip")


def show_page(request, slug):
    context = get_site_context(request)
    context["page"] = PageContent.objects.filter(
        slug=slug, is_published=True
    ).first()
    context["page_slug"] = slug
    return render(request, "core/page.html", context)


def jobs(request):
    context = get_site_context(request)
    context["jobs"] = Job.objects.filter(is_active=True)
    return render(request, "core/jobs.html", context)


def vip_members(request):
    context = get_site_context(request)
    context["vip_members"] = VIPMember.objects.filter(is_published=True)
    return render(request, "core/vip_members.html", context)
