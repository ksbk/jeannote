from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_research_publications_resume_enabled"),
    ]

    operations = [
        # ---------------------------------------------------------------
        # SiteSettings — contact visibility controls
        # ---------------------------------------------------------------
        migrations.AddField(
            model_name="sitesettings",
            name="show_email",
            field=models.BooleanField(
                default=True,
                help_text="Show the contact email address in the footer and contact sections.",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_phone",
            field=models.BooleanField(
                default=False,
                help_text="Show the phone number in the footer and contact sections.",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="show_location",
            field=models.BooleanField(
                default=True,
                help_text="Show the location in the footer identity and legal line.",
            ),
        ),
        # ---------------------------------------------------------------
        # BrandSettings — new singleton table
        # ---------------------------------------------------------------
        migrations.CreateModel(
            name="BrandSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "logo_light",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="site/",
                        help_text=(
                            "Logo optimised for light backgrounds. "
                            "Leave blank to use the master logo (Site Settings → Identity → Logo)."
                        ),
                    ),
                ),
                (
                    "logo_dark",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="site/",
                        help_text=(
                            "Logo optimised for dark or inverse backgrounds. "
                            "Leave blank to use the master logo."
                        ),
                    ),
                ),
                (
                    "logo_icon",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="site/",
                        help_text=(
                            "Square icon or favicon candidate (1:1 aspect ratio). "
                            "Leave blank to use the master logo. "
                            "Recommended size: 512×512 px or larger."
                        ),
                    ),
                ),
                (
                    "logo_display_mode",
                    models.CharField(
                        choices=[
                            ("transparent", "Always on transparent background"),
                            ("safe_card", "On card / padded background"),
                            ("auto", "Auto (default — let the template decide)"),
                        ],
                        default="auto",
                        max_length=20,
                        help_text=(
                            "Controls the CSS context wrapper applied to the logo in the navbar. "
                            "'Auto' works for transparent or legible single-colour logos. "
                            "Use 'On card' to add a padded white background for logos that blend with the nav."
                        ),
                    ),
                ),
                (
                    "logo_max_width",
                    models.PositiveSmallIntegerField(
                        default=160,
                        help_text="Maximum logo width on desktop (px). Default: 160. Keep between 80 and 300.",
                    ),
                ),
                (
                    "logo_max_width_mobile",
                    models.PositiveSmallIntegerField(
                        default=120,
                        help_text="Maximum logo width on mobile (px). Default: 120. Must be ≤ desktop max width.",
                    ),
                ),
                (
                    "typography_preset",
                    models.CharField(
                        choices=[
                            ("balanced", "Balanced — Cormorant Garamond + DM Sans (default)"),
                            ("editorial_serif", "Editorial Serif — serif headings + serif body"),
                            ("modern_clean", "Modern Clean — system sans-serif throughout"),
                            ("technical", "Technical — monospace headings + system sans body"),
                            ("warm_professional", "Warm Professional — Palatino headings + system body"),
                        ],
                        default="balanced",
                        max_length=30,
                        help_text=(
                            "Sets the heading and body type families used across the site. "
                            "Applied via CSS custom properties — no font files are uploaded. "
                            "Web-safe and Google Fonts variants are bundled with the template."
                        ),
                    ),
                ),
                (
                    "color_preset",
                    models.CharField(
                        choices=[
                            ("neutral", "Neutral — warm bronze (default)"),
                            ("blue", "Blue — professional navy"),
                            ("green", "Green — organic forest"),
                            ("burgundy", "Burgundy — confident deep red"),
                            ("amber", "Amber — warm earth"),
                            ("custom", "Custom — use accent color field below"),
                        ],
                        default="neutral",
                        max_length=20,
                        help_text=(
                            "Accent color applied to interactive elements, borders, selection, and emphasis details. "
                            "Choose 'Custom' and set the accent color field below to use your own hex value."
                        ),
                    ),
                ),
                (
                    "accent_color_custom",
                    models.CharField(
                        blank=True,
                        max_length=7,
                        help_text=(
                            "Custom accent hex color, e.g. #B45309. "
                            "Only applied when Color Preset is set to 'Custom'. "
                            "Must be a 6-digit hex including the # prefix."
                        ),
                    ),
                ),
                (
                    "visual_style",
                    models.CharField(
                        choices=[
                            ("crisp", "Crisp — sharp edges, no rounding"),
                            ("balanced", "Balanced — subtle rounding (default)"),
                            ("soft", "Soft — rounded corners throughout"),
                        ],
                        default="balanced",
                        max_length=20,
                        help_text="Controls corner rounding on cards, buttons, and images across the site.",
                    ),
                ),
                (
                    "social_links_display",
                    models.CharField(
                        choices=[
                            ("text", "Text labels only (default)"),
                            ("icons", "Icons only (requires icon_slug on each Social Link)"),
                            ("icons_text", "Icons + text labels"),
                        ],
                        default="text",
                        max_length=20,
                        help_text=(
                            "Controls how social links are rendered in the footer. "
                            "'Icons' and 'Icons + text' require icon_slug to be set on each Social Link entry."
                        ),
                    ),
                ),
            ],
            options={
                "verbose_name": "Brand Settings",
                "verbose_name_plural": "Brand Settings",
            },
        ),
    ]
