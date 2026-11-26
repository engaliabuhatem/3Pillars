"""
`manage.py check_content` — fail when the content drifts from the rules.

Runs the copy check (seeded English matches the content document), the term
check (no designer/contractor positioning, no HS Group figures) and the
thin-content check (no near-duplicate service or sector pages). Exits non-zero
on any finding, so CI can run it after `seed_content`.
"""

from django.core.management.base import BaseCommand, CommandError

from apps.content import quality


class Command(BaseCommand):
    help = "Check seeded copy, banned terms and near-duplicate pages."

    def handle(self, *args, **options):
        checks = {
            "Copy differs from the content document": quality.copy_mismatches(),
            "Wording that misrepresents 3 Pillars": quality.banned_terms(),
            "Near-duplicate pages": quality.near_duplicates(),
        }
        failed = False
        for title, findings in checks.items():
            if findings:
                failed = True
                self.stderr.write(f"{title}:")
                for line in findings:
                    self.stderr.write(f"  {line}")
            else:
                self.stdout.write(f"OK  {title}: none")
        if failed:
            raise CommandError("Content checks failed.")
