from django.core.management.base import BaseCommand
from portfolio import models


class Command(BaseCommand):
    help = "Populates the database with starter content so the site isn't empty on first run. Edit everything afterwards in /admin/."

    def handle(self, *args, **options):
        # ---- Site settings ----
        s = models.SiteSettings.load()
        s.site_title = "Suraj Shankar Gupta — Senior Python Django Developer"
        s.meta_description = "Suraj Shankar Gupta — Senior Python Django Developer specializing in ERP, SaaS and backend systems architecture."
        s.brand_initials = "SG"
        s.brand_name = "Suraj Shankar Gupta"
        s.footer_text = "© 2026 Suraj Shankar Gupta."
        s.footer_tagline = "Built with Django."
        s.save()

        # ---- Nav ----
        models.NavLink.objects.all().delete()
        for i, (label, anchor, cta) in enumerate([
            ("About", "about", False),
            ("Experience", "experience", False),
            ("Skills", "skills", False),
            ("Projects", "projects", False),
            ("Education", "education", False),
            ("Contact", "contact", True),
        ]):
            models.NavLink.objects.create(label=label, section_anchor=anchor, is_cta_button=cta, order=i)

        # ---- Hero ----
        hero = models.HeroProfile.load()
        hero.eyebrow_text = "Backend Engineering · Since 2020"
        hero.full_name = "Suraj Shankar Gupta"
        hero.role_title = "Senior Python Django Developer — ERP, SaaS & Backend Solutions Architect"
        hero.description = (
            "I design and build the backend systems businesses actually run on — multi-tenant ERP "
            "platforms, accounting engines, and REST APIs that hold up under production load. "
            "Six-plus years turning operational chaos into scalable software."
        )
        hero.location = "Gorakhpur, Uttar Pradesh, India"
        hero.primary_button_text = "Get in touch"
        hero.primary_button_link = "#contact"
        hero.secondary_button_text = "View LinkedIn"
        hero.secondary_button_link = "https://www.linkedin.com/in/suraj-shankar-gupta/"
        hero.ledger_title = "Munshiiji ERP — Inside the build"
        hero.ledger_live_label = "Shipped & maintained"
        hero.save()

        models.HeroStat.objects.all().delete()
        for i, (val, label) in enumerate([("6+", "Years Experience"), ("7", "ERP Modules Shipped"), ("4+", "Companies & Clients")]):
            models.HeroStat.objects.create(value=val, label=label, order=i)

        models.LedgerModule.objects.all().delete()
        ledger_data = [
            ("Module 01", "Inventory Management", "Stock tracking, warehouse management, stock adjustments, and opening-stock automation.",
             [("Stock Movements", "Live"), ("Warehouses Tracked", "Multi-site"), ("Adjustments", "Automated")]),
            ("Module 02", "Accounting & Ledger", "Ledger management, chart of accounts, payment collection, and outstanding tracking.",
             [("Chart of Accounts", "Configured"), ("Payment Collection", "Enabled"), ("Outstanding Tracking", "Active")]),
            ("Module 03", "CRM", "Customer relationships, sales pipeline, and follow-ups tied directly into billing.",
             [("Pipeline Sync", "Real-time"), ("Client Records", "Centralized"), ("Notifications", "WhatsApp")]),
            ("Module 04", "GST Billing", "Compliant invoicing and GST billing workflows built for Indian business regulations.",
             [("Tax Compliance", "GST-ready"), ("Invoicing", "Automated"), ("Reports", "Exportable")]),
            ("Module 05", "Financial Reporting", "Consolidated financial reports across inventory, sales, purchase, and accounting data.",
             [("Report Types", "12+"), ("Refresh", "Scheduled"), ("Access Control", "Role-based")]),
        ]
        for i, (tag, title, desc, lines) in enumerate(ledger_data):
            m = models.LedgerModule.objects.create(tag=tag, title=title, description=desc, order=i)
            for j, (label, value) in enumerate(lines):
                models.LedgerLine.objects.create(module=m, label=label, value=value, order=j)

        # ---- About ----
        about = models.AboutSection.load()
        about.eyebrow_text = "About"
        about.heading = "Backend systems that businesses run on."
        about.paragraph_intro = (
            "I'm a Python backend engineer with 6+ years building scalable SaaS products, ERP systems, "
            "REST APIs, and business-automation software. My core work sits in designing and shipping "
            "robust backend systems with Python, Django, Django REST Framework, PostgreSQL, AWS, and Linux."
        )
        about.paragraph_body = (
            "I've built across Inventory Management, Accounting & Finance, GST Billing, CRM, Education "
            "Technology, and Business Automation — currently leading backend development for Munshiiji ERP, "
            "a cloud ERP platform covering Inventory, Sales, Purchase, Accounting, CRM, GST Billing, and "
            "Financial Reporting on a scalable multi-tenant SaaS architecture."
        )
        about.save()

        models.AboutChip.objects.all().delete()
        for i, chip in enumerate([
            "Python & Django", "Django REST Framework", "SaaS & Multi-Tenant Architecture", "ERP Development",
            "PostgreSQL", "AWS & Linux", "Payment Gateways", "Performance Optimization",
        ]):
            models.AboutChip.objects.create(text=chip, order=i)

        # ---- Experience ----
        models.Experience.objects.all().delete()
        exp_data = [
            ("Lead Software Developer", "Smart Engineering & Automation Solutions", "Oct 2025 — Present", "New Delhi", True,
             ["Lead development of a Django-based CRM and business management platform supporting lead management, quotations, follow-ups, and sales pipeline workflows.",
              "Built employee productivity tracking, internal communication, notifications, product catalogue management, and bulk data import modules.",
              "Designed role-based access controls, operational dashboards, and scalable backend workflows for secure multi-user operations.",
              "Automated application deployment, database backups, monitoring, and production maintenance to improve platform reliability."],
             ["Python", "Django", "PostgreSQL", "CRM", "Linux"]),
            ("Freelance Software Developer — ERP & SaaS", "Munshiiji ERP Solutions", "Jul 2025 — Oct 2025", "Remote", False,
             ["Developed a multi-tenant cloud ERP covering inventory, warehouses, accounting, CRM, sales, purchasing, GST billing, and financial reporting.",
              "Implemented stock tracking, opening stock, adjustments, ledgers, chart of accounts, payment collection, and outstanding tracking.",
              "Integrated WhatsApp notifications, payment gateways, and reporting services; optimized queries and managed production deployment and security."],
             ["Python", "Django", "DRF", "PostgreSQL", "AWS"]),
            ("Freelance Python/Django Developer", "Independent", "Oct 2023 — Present", "Remote", True,
             ["Delivered production web applications, ERP systems, inventory solutions, REST APIs, and business automation workflows for clients across industries.",
              "Integrated payment, WhatsApp, SMS, and email services; administered AWS/Linux hosting, SSL, backups, application security, and ongoing support.",
              "Developed WordPress business websites with SEO, performance, and security optimization."],
             ["Python", "Django", "PostgreSQL", "AWS", "Linux", "WordPress"]),
            ("Freelance Software Developer", "Smart Engineering & Automation Solutions", "Oct 2023 — Apr 2025", "New Delhi", False,
             ["Developed and maintained Django applications and relational databases from requirements through testing, deployment, documentation, and support.",
              "Improved application reliability, security, and performance through debugging, testing, query optimization, and stakeholder collaboration."],
             ["Python", "Django", "PostgreSQL", "REST APIs"]),
            ("Backend Developer — Ezyschooling", "Ashmay Technologies Private Limited", "Mar 2022 — Aug 2023", "Delhi", False,
             ["Enhanced a Django/PostgreSQL school admissions platform using AWS S3 and Elasticsearch; resolved backend bottlenecks and admission-form issues.",
              "Built and tested REST API integrations using Postman and Apache JMeter, including WhatsApp and payment settlement workflows.",
              "Introduced operational improvements reported to increase productivity by 50%."],
             ["Django", "PostgreSQL", "Amazon S3", "Elasticsearch", "Postman", "JMeter"]),
            ("Software Developer — Government Projects", "Shreyas Technosoft Pvt. Ltd.", "Mar 2021 — Feb 2022", "Pune, Maharashtra", False,
             ["Built Django REST API backends and web applications for Green Hydrogen India, NEERI recruitment, and eco-campus initiatives.",
              "Developed PostgreSQL data workflows and generated TXT, CSV, and JSON reports using Python and Django."],
             ["Python", "Django", "Django REST Framework", "PostgreSQL"]),
            ("Co-Founder & Software Developer", "Roomsmate", "Nov 2019 — Mar 2021", "Nagpur, Maharashtra", False,
             ["Co-founded and developed a responsive Django/PostgreSQL platform connecting students and professionals with hostels, PGs, rentals, and roommates."],
             ["Python", "Django", "PostgreSQL", "HTML", "CSS"]),
        ]
        for i, (role, org, dates, meta, current, bullets, tech) in enumerate(exp_data):
            e = models.Experience.objects.create(
                role_title=role, organization=org, date_range=dates, location_meta=meta, is_current=current, order=i
            )
            for j, b in enumerate(bullets):
                models.ExperienceBullet.objects.create(experience=e, text=b, order=j)
            for j, t in enumerate(tech):
                models.ExperienceTech.objects.create(experience=e, name=t, order=j)

        # ---- Skills ----
        models.SkillCategory.objects.all().delete()
        skill_data = [
            ("Backend & Frameworks", "backend", ["Python", "Django", "Django REST Framework", "REST API Design", "ORM & Query Optimization"]),
            ("Database & Architecture", "data", ["PostgreSQL", "SaaS & Multi-Tenant Architecture", "Database Design & Optimization", "Role-Based Access Control"]),
            ("Cloud & Infrastructure", "cloud", ["AWS", "Amazon S3", "Linux Server Administration", "SSL Configuration", "Elasticsearch", "Production Deployment & Monitoring"]),
            ("Integrations", "integrations", ["Payment Gateways", "WhatsApp API", "SMS Gateways", "Email Services", "Third-Party API Integration"]),
            ("Frontend & Tooling", "tools", ["HTML / CSS / JavaScript", "jQuery", "Bootstrap", "WordPress", "Git / GitHub", "Postman", "Apache JMeter"]),
        ]
        for i, (name, slug, skills) in enumerate(skill_data):
            cat = models.SkillCategory.objects.create(name=name, slug=slug, order=i)
            for j, sk in enumerate(skills):
                models.Skill.objects.create(category=cat, name=sk, order=j)

        # ---- Projects ----
        models.Project.objects.all().delete()
        proj_data = [
            ("Munshiiji ERP", "A cloud-based, multi-tenant ERP platform for Inventory, Sales, Purchase, Accounting, CRM, GST Billing, and Financial Reporting — built for businesses to run their core operations in one place.", ["Python", "Django", "DRF", "PostgreSQL"]),
            ("Ezyschooling.com", "A platform for parents and schools offering simplified online admissions, parenting advice, and education news — backend rebuilt for scale and search performance.", ["Django", "PostgreSQL", "AWS S3", "Elasticsearch"]),
            ("Green Hydrogen India Forum", "REST-API-driven backend for a public discussion forum, plus a companion MVT-based eco-campus website.", ["Python 3", "Django", "PostgreSQL"]),
            ("NEERI Recruitment Portal", "A recruitment portal built with a small team for NEERI, handling listings and candidate workflows end to end.", ["Python", "Django", "PostgreSQL"]),
        ]
        for i, (title, desc, tech) in enumerate(proj_data):
            p = models.Project.objects.create(title=title, description=desc, order=i)
            for j, t in enumerate(tech):
                models.ProjectTech.objects.create(project=p, name=t, order=j)

        # ---- Education ----
        models.EducationItem.objects.all().delete()
        edu_data = [
            ("2016 – 2020", "B.E., Computer Science", "S.B. Jain Institute of Technology, Management & Research, Nagpur — Webmaster, IEEE Student Branch; Technical Co-Head, Suigeneris (departmental forum)."),
            ("Class of 2016", "High School Diploma", "SFS."),
        ]
        for i, (yr, degree, desc) in enumerate(edu_data):
            models.EducationItem.objects.create(year_range=yr, degree=degree, description=desc, order=i)

        # ---- Testimonials ----
        models.Testimonial.objects.all().delete()
        testi_data = [
            ("Suraj is such a delightful person to have around. He makes sure all deadlines are met, and to the highest standard — hardworking, dedicated, innovative, and always open to ideas and suggestions.",
             "Ankit Parsana", "Tech Lead, Full Stack Architect — managed Suraj directly"),
            ("Suraj was a fantastic co-worker — thorough in everything he does, very dedicated and capable, and always there to help whenever needed.",
             "Amruta Jagtap", "Mobile Application Developer"),
        ]
        for i, (quote, name, role) in enumerate(testi_data):
            models.Testimonial.objects.create(quote=quote, name=name, role=role, order=i)

        # ---- Contact ----
        contact = models.ContactSection.load()
        contact.eyebrow_text = "Contact"
        contact.heading = "Let's build something reliable."
        contact.lede = "Open to lead backend / senior Python roles, ERP & SaaS engineering engagements, and freelance projects."
        contact.form_note = "Opens your email client with this message pre-filled — no data leaves your browser."
        contact.mailto_address = "ssepadrauna@gmail.com"
        contact.save()

        models.ContactInfo.objects.all().delete()
        contact_data = [
            ("linkedin", "LinkedIn — in/suraj-shankar-gupta", "https://www.linkedin.com/in/suraj-shankar-gupta/"),
            ("email", "Email — ssepadrauna@gmail.com", "mailto:ssepadrauna@gmail.com"),
            ("phone", "Phone — +91 86683 29719", "tel:+918668329719"),
            ("location", "Location — Gorakhpur, Uttar Pradesh, India", "#"),
        ]
        for i, (icon, label, link) in enumerate(contact_data):
            models.ContactInfo.objects.create(icon=icon, label=label, link=link, order=i)

        self.stdout.write(self.style.SUCCESS(
            "Starter content loaded. Log into /admin/ and edit every section — "
            "no code changes needed."
        ))
