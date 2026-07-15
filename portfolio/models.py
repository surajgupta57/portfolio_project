from django.core.exceptions import ValidationError
from django.db import models


# ---------------------------------------------------------------------------
# Small reusable helpers
# ---------------------------------------------------------------------------
class OrderedModel(models.Model):
    """Adds a manual 'order' field so admins can drag/type ordering."""
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class SingletonModel(models.Model):
    """Base class for models that should only ever have ONE row (e.g. site-wide settings)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton rows can't be deleted from the admin

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ---------------------------------------------------------------------------
# 1. GLOBAL SITE SETTINGS  -> fonts, colours, meta info, footer, branding
# ---------------------------------------------------------------------------
class SiteSettings(SingletonModel):
    # Meta / branding
    site_title = models.CharField(max_length=120, default="Your Name — Portfolio")
    meta_description = models.CharField(max_length=300, blank=True)
    brand_initials = models.CharField(max_length=4, default="SG", help_text="Shown in the small logo mark, e.g. 'SG'.")
    brand_name = models.CharField(max_length=120, default="Your Name")
    favicon = models.ImageField(upload_to="misc/", blank=True, null=True)
    resume_file = models.FileField(upload_to="misc/", blank=True, null=True, help_text="Optional PDF résumé; used by any 'Download résumé' link.")

    # Fonts (any valid Google Fonts family name)
    display_font = models.CharField(max_length=80, default="Fraunces", help_text="Used for all headings.")
    display_font_weights = models.CharField(max_length=120, default="300;450;560;650")
    body_font = models.CharField(max_length=80, default="IBM Plex Sans", help_text="Used for paragraph text.")
    body_font_weights = models.CharField(max_length=120, default="400;500;600")
    mono_font = models.CharField(max_length=80, default="IBM Plex Mono", help_text="Used for labels, nav, tags, code-like text.")
    mono_font_weights = models.CharField(max_length=120, default="400;500")
    base_font_size_px = models.PositiveIntegerField(default=16, help_text="Root font size in pixels.")

    # Colour palette (hex codes) — every colour used across the site
    color_ink = models.CharField(max_length=7, default="#101C30")
    color_ink_2 = models.CharField(max_length=7, default="#17263D")
    color_ink_3 = models.CharField(max_length=7, default="#1E304A")
    color_paper = models.CharField(max_length=7, default="#F6F3EA")
    color_paper_2 = models.CharField(max_length=7, default="#EEE8D9")
    color_emerald = models.CharField(max_length=7, default="#1F6F5C")
    color_emerald_light = models.CharField(max_length=7, default="#2C8B73")
    color_gold = models.CharField(max_length=7, default="#B8912B")
    color_charcoal = models.CharField(max_length=7, default="#1B1F27")
    color_slate = models.CharField(max_length=7, default="#5B6472")
    color_cream = models.CharField(max_length=7, default="#EDE8DC")

    # Layout
    max_width_px = models.PositiveIntegerField(default=1180)
    section_padding_px = models.PositiveIntegerField(default=112)

    # Footer
    footer_text = models.CharField(max_length=200, default="© 2026 Your Name.")
    footer_tagline = models.CharField(max_length=200, blank=True, default="Built with Django.")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "⚙️ Site Settings (fonts, colours, branding)"

    def __str__(self):
        return "Site Settings"

    @property
    def google_fonts_url(self):
        families = [
            f"family={self.display_font.replace(' ', '+')}:wght@{self.display_font_weights}",
            f"family={self.body_font.replace(' ', '+')}:wght@{self.body_font_weights}",
            f"family={self.mono_font.replace(' ', '+')}:wght@{self.mono_font_weights}",
        ]
        return "https://fonts.googleapis.com/css2?" + "&".join(families) + "&display=swap"


# ---------------------------------------------------------------------------
# 2. NAVIGATION
# ---------------------------------------------------------------------------
class NavLink(OrderedModel):
    label = models.CharField(max_length=60)
    section_anchor = models.SlugField(
        max_length=60,
        help_text="The id of the section on the page this should scroll to, e.g. 'about' or 'contact' (no '#').",
    )
    is_cta_button = models.BooleanField(default=False, help_text="Style this link as the highlighted button (usually 'Contact').")
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Nav Link"
        verbose_name_plural = "🧭 Navigation Links"

    def __str__(self):
        return self.label


# ---------------------------------------------------------------------------
# 3. HERO SECTION
# ---------------------------------------------------------------------------
class HeroProfile(SingletonModel):
    eyebrow_text = models.CharField(max_length=100, default="Backend Engineering · Since 2020")
    full_name = models.CharField(max_length=150, default="Your Name")
    role_title = models.CharField(max_length=200, default="Senior Python Django Developer")
    description = models.TextField(default="A short, punchy description of what you do and who you do it for.")
    location = models.CharField(max_length=150, default="Your City, Your Country")

    primary_button_text = models.CharField(max_length=40, default="Get in touch")
    primary_button_link = models.CharField(max_length=100, default="#contact")
    secondary_button_text = models.CharField(max_length=40, default="View experience")
    secondary_button_link = models.CharField(max_length=100, default="#experience")

    ledger_title = models.CharField(max_length=150, default="Project — Module Ledger", help_text="Header text of the rotating card widget on the hero.")
    ledger_live_label = models.CharField(max_length=50, default="In production")

    class Meta:
        verbose_name = "Hero Profile"
        verbose_name_plural = "🏠 Hero Section — Profile"

    def __str__(self):
        return self.full_name


class HeroStat(OrderedModel):
    value = models.CharField(max_length=20, help_text="e.g. '6+'")
    label = models.CharField(max_length=60, help_text="e.g. 'Years Experience'")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Hero Stat"
        verbose_name_plural = "🏠 Hero Section — Stats"

    def __str__(self):
        return f"{self.value} {self.label}"


class LedgerModule(OrderedModel):
    """One rotating card in the hero's animated ledger widget."""
    tag = models.CharField(max_length=40, help_text="e.g. 'Module 01'")
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Ledger Module (hero widget)"
        verbose_name_plural = "🏠 Hero Section — Ledger Modules"

    def __str__(self):
        return self.title


class LedgerLine(OrderedModel):
    module = models.ForeignKey(LedgerModule, related_name="lines", on_delete=models.CASCADE)
    label = models.CharField(max_length=60)
    value = models.CharField(max_length=60)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Ledger Line"
        verbose_name_plural = "Ledger Lines"

    def __str__(self):
        return f"{self.label}: {self.value}"


# ---------------------------------------------------------------------------
# 4. ABOUT SECTION
# ---------------------------------------------------------------------------
class AboutSection(SingletonModel):
    eyebrow_text = models.CharField(max_length=100, default="About")
    heading = models.CharField(max_length=200, default="A short headline about what you build.")
    paragraph_intro = models.TextField(default="An opening paragraph, bold and short.")
    paragraph_body = models.TextField(default="More detail about your background, what you've built, and what you're doing now.", blank=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "👤 About Section — Text"

    def __str__(self):
        return "About Section"


class AboutChip(OrderedModel):
    text = models.CharField(max_length=80)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "About Chip"
        verbose_name_plural = "👤 About Section — Skill Chips"

    def __str__(self):
        return self.text


# ---------------------------------------------------------------------------
# 5. EXPERIENCE / TIMELINE
# ---------------------------------------------------------------------------
class Experience(OrderedModel):
    role_title = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    date_range = models.CharField(max_length=80, help_text="e.g. 'Jan 2026 — Present'")
    location_meta = models.CharField(max_length=120, help_text="e.g. 'Remote · 7 mos'", blank=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Experience"
        verbose_name_plural = "💼 Experience — Timeline Entries"

    def __str__(self):
        return f"{self.role_title} @ {self.organization}"


class ExperienceBullet(OrderedModel):
    experience = models.ForeignKey(Experience, related_name="bullets", on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Experience Bullet Point"
        verbose_name_plural = "Experience Bullet Points"

    def __str__(self):
        return self.text[:60]


class ExperienceTech(OrderedModel):
    experience = models.ForeignKey(Experience, related_name="tech_stack", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Experience Tech Tag"
        verbose_name_plural = "Experience Tech Tags"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# 6. SKILLS (tabbed panel)
# ---------------------------------------------------------------------------
class SkillCategory(OrderedModel):
    name = models.CharField(max_length=80, help_text="e.g. 'Backend & Frameworks'")
    slug = models.SlugField(max_length=80, help_text="Used internally to link the tab to its panel, e.g. 'backend'.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Skill Category (Tab)"
        verbose_name_plural = "🧩 Skills — Categories (Tabs)"

    def __str__(self):
        return self.name


class Skill(OrderedModel):
    category = models.ForeignKey(SkillCategory, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# 7. PROJECTS
# ---------------------------------------------------------------------------
class Project(OrderedModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField(blank=True, help_text="Optional — live site or repo link.")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Project"
        verbose_name_plural = "🚀 Projects"

    def __str__(self):
        return self.title

    @property
    def display_number(self):
        return f"{self.order + 1:02d}"


class ProjectTech(OrderedModel):
    project = models.ForeignKey(Project, related_name="tech_stack", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Project Tech Tag"
        verbose_name_plural = "Project Tech Tags"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# 8. EDUCATION
# ---------------------------------------------------------------------------
class EducationItem(OrderedModel):
    year_range = models.CharField(max_length=60, help_text="e.g. '2016 – 2020'")
    degree = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Education Item"
        verbose_name_plural = "🎓 Education"

    def __str__(self):
        return self.degree


# ---------------------------------------------------------------------------
# 9. TESTIMONIALS
# ---------------------------------------------------------------------------
class Testimonial(OrderedModel):
    quote = models.TextField()
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Testimonial"
        verbose_name_plural = "💬 Testimonials"

    def __str__(self):
        return f"{self.name} — {self.role}"


# ---------------------------------------------------------------------------
# 10. CONTACT
# ---------------------------------------------------------------------------
class ContactSection(SingletonModel):
    eyebrow_text = models.CharField(max_length=100, default="Contact")
    heading = models.CharField(max_length=200, default="Let's build something great.")
    lede = models.TextField(blank=True, default="Open to new roles and freelance projects.")
    form_note = models.CharField(
        max_length=200,
        default="Opens your email client with this message pre-filled — no data leaves your browser.",
    )
    mailto_address = models.EmailField(default="you@example.com")

    class Meta:
        verbose_name = "Contact Section"
        verbose_name_plural = "✉️ Contact — Section Text"

    def __str__(self):
        return "Contact Section"


class ContactInfo(OrderedModel):
    ICON_CHOICES = [
        ("linkedin", "LinkedIn"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("location", "Location"),
        ("github", "GitHub"),
        ("website", "Website"),
        ("other", "Other"),
    ]
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="other")
    label = models.CharField(max_length=150, help_text="e.g. 'LinkedIn — in/your-handle'")
    link = models.CharField(max_length=300, help_text="e.g. 'https://linkedin.com/in/you', 'mailto:you@example.com', 'tel:+91...'")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Contact Info Line"
        verbose_name_plural = "✉️ Contact — Info Lines"

    def __str__(self):
        return self.label
