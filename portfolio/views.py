from django.shortcuts import render
from . import models


def home(request):
    context = {
        "hero": models.HeroProfile.load(),
        "hero_stats": models.HeroStat.objects.all(),
        "ledger_modules": models.LedgerModule.objects.prefetch_related("lines").all(),

        "about": models.AboutSection.load(),
        "about_chips": models.AboutChip.objects.all(),

        "experiences": models.Experience.objects.prefetch_related("bullets", "tech_stack", "site_links").all(),

        "skill_categories": models.SkillCategory.objects.prefetch_related("skills").all(),

        "projects": models.Project.objects.prefetch_related("tech_stack").all(),

        "education_items": models.EducationItem.objects.all(),

        "testimonials": models.Testimonial.objects.filter(is_visible=True),

        "contact": models.ContactSection.load(),
        "contact_info": models.ContactInfo.objects.all(),
    }
    return render(request, "portfolio/index.html", context)
