from django.contrib import admin
from django.utils.html import format_html
from . import models


# ---------------------------------------------------------------------------
# Site-wide singletons
# ---------------------------------------------------------------------------
@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding & Meta", {
            "fields": ("site_title", "meta_description", "brand_name", "brand_initials", "favicon", "resume_file")
        }),
        ("Fonts", {
            "fields": (
                ("display_font", "display_font_weights"),
                ("body_font", "body_font_weights"),
                ("mono_font", "mono_font_weights"),
                "base_font_size_px",
            ),
            "description": "Use any Google Fonts family name exactly as it appears on fonts.google.com.",
        }),
        ("Colour Palette", {
            "fields": (
                ("color_ink", "color_ink_2", "color_ink_3"),
                ("color_paper", "color_paper_2", "color_cream"),
                ("color_emerald", "color_emerald_light", "color_gold"),
                ("color_charcoal", "color_slate"),
            ),
        }),
        ("Layout", {
            "fields": ("max_width_px", "section_padding_px", "animation_mode"),
        }),
        ("Footer", {
            "fields": ("footer_text", "footer_tagline"),
        }),
    )

    def has_add_permission(self, request):
        return not models.SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.HeroProfile)
class HeroProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("eyebrow_text", "full_name", "role_title", "description", "location")}),
        ("Buttons", {"fields": (
            ("primary_button_text", "primary_button_link"),
            ("secondary_button_text", "secondary_button_link"),
        )}),
        ("Ledger Widget Header", {"fields": ("ledger_title", "ledger_live_label")}),
    )

    def has_add_permission(self, request):
        return not models.HeroProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not models.AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not models.ContactSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ---------------------------------------------------------------------------
# Simple ordered lists
# ---------------------------------------------------------------------------
@admin.register(models.NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "section_anchor", "is_cta_button", "is_visible", "order")
    list_editable = ("order", "is_cta_button", "is_visible")
    ordering = ("order",)


@admin.register(models.HeroStat)
class HeroStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)


@admin.register(models.AboutChip)
class AboutChipAdmin(admin.ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)


@admin.register(models.EducationItem)
class EducationItemAdmin(admin.ModelAdmin):
    list_display = ("degree", "year_range", "order")
    list_editable = ("order",)


@admin.register(models.ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("label", "icon", "link", "order")
    list_editable = ("order",)


# ---------------------------------------------------------------------------
# Hero ledger widget (module -> lines)
# ---------------------------------------------------------------------------
class LedgerLineInline(admin.TabularInline):
    model = models.LedgerLine
    extra = 1


@admin.register(models.LedgerModule)
class LedgerModuleAdmin(admin.ModelAdmin):
    list_display = ("tag", "title", "order")
    list_editable = ("order",)
    inlines = [LedgerLineInline]


# ---------------------------------------------------------------------------
# Experience (timeline entry -> bullets + tech tags), all editable inline
# ---------------------------------------------------------------------------
class ExperienceBulletInline(admin.TabularInline):
    model = models.ExperienceBullet
    extra = 1


class ExperienceTechInline(admin.TabularInline):
    model = models.ExperienceTech
    extra = 1


class ExperienceLinkInline(admin.TabularInline):
    model = models.ExperienceLink
    extra = 1
    fields = ("label", "url", "order")


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role_title", "organization", "date_range", "is_current", "order")
    list_editable = ("order", "is_current")
    inlines = [ExperienceBulletInline, ExperienceTechInline, ExperienceLinkInline]


# ---------------------------------------------------------------------------
# Skills — category (tab) -> skills, editable inline so one screen does it all
# ---------------------------------------------------------------------------
class SkillInline(admin.TabularInline):
    model = models.Skill
    extra = 1


@admin.register(models.SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SkillInline]


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
class ProjectTechInline(admin.TabularInline):
    model = models.ProjectTech
    extra = 1


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "thumb")
    list_editable = ("order",)
    inlines = [ProjectTechInline]

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return "—"
    thumb.short_description = "Preview"


# ---------------------------------------------------------------------------
# Testimonials
# ---------------------------------------------------------------------------
@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_visible", "order")
    list_editable = ("order", "is_visible")


# ---------------------------------------------------------------------------
# Admin site branding
# ---------------------------------------------------------------------------
admin.site.site_header = "Portfolio CMS"
admin.site.site_title = "Portfolio CMS"
admin.site.index_title = "Manage your website"
