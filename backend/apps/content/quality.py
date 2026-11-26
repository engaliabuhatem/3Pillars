"""
Content quality checks, run by management commands and by the test suite.

- copy:  every English string seeded from seed_data/content.py appears in the
         content document, word for word.
- terms: no public copy presents 3 Pillars as a designer, supervisor or
         contractor, and no HS Group figures are attached to it.
- thin:  no two service or sector pages share more than 40% of their text.
"""

import html
import re
from itertools import combinations
from pathlib import Path

from django.conf import settings

from .seed_data import content as seed

DOCUMENT = Path(settings.BASE_DIR).parent / "docs" / "content" / "3pillars-content.md"
FRONTEND = Path(settings.BASE_DIR).parent / "src"

#: Strings that are not copy: addresses, identifiers, icons and choice values.
STRUCTURAL_KEYS = {"slug", "path", "link", "icon", "kind", "color", "role_on_site", "service", "related_services",
                   "mega_menu", "hero_primary_link", "hero_secondary_link", "cta_link", "pillar"}

#: English seeded on purpose although the document does not contain it, with the reason.
NOT_FROM_DOCUMENT = {
    "Company": "existing footer column title; the document defines no footer",
    "Work with us": "existing footer column title; the document defines no footer",
    "Capability statement": "existing page kept as it was",
}

#: Wording that would present 3 Pillars as an engineering designer or a contractor.
BANNED = [
    re.compile(r"construction supervision", re.I),
    re.compile(r"design services", re.I),
    re.compile(r"\bcontractor\b", re.I),
    re.compile(r"HS Group[^.\n]{0,80}?\b\d[\d,.]*\s*(?:\+|%|projects|years|offices|staff|employees|engineers|"
               r"countries|clients)", re.I),
]

#: Fields that are editor guidance only, never shown on the site.
PRIVATE_KEYS = {"note", "positioning_note", "primary_keyword", "supporting_keywords", "home_primary_keyword",
                "home_supporting_keywords"}

ARABIC = re.compile(r"[؀-ۿ]")
SHINGLE = 5
THIN_LIMIT = 0.4


def normalise(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("\\|", "|").replace("**", "").replace("\\", "")
    return re.sub(r"\s+", " ", text).strip().casefold()


def english_strings(value, key: str = "", public_only: bool = False):
    """Every English string in the seed data, with the key it sits under."""
    if isinstance(value, dict):
        for k, v in value.items():
            if k in STRUCTURAL_KEYS or k.endswith("_ar") or (public_only and k in PRIVATE_KEYS):
                continue
            yield from english_strings(v, k, public_only)
    elif isinstance(value, list | tuple):
        for item in value:
            yield from english_strings(item, key, public_only)
    elif isinstance(value, str) and value and not ARABIC.search(value):
        if value.startswith("/") or re.fullmatch(r"[a-z0-9_-]+", value):
            return
        yield key, value


#: Admin-only lists: never rendered on the site.
PRIVATE_LISTS = {"CLAIMS_TO_VERIFY", "PRE_LAUNCH_CHECKLIST"}


def seed_values(public_only: bool = False):
    skip = {"CONSULTATION", "RETIRED_PAGES", "LEGAL_LINKS", "SITE_CLEARED", *(PRIVATE_LISTS if public_only else ())}
    names = [n for n in dir(seed) if n.isupper() and n not in skip]
    for name in names:
        for key, text in english_strings(getattr(seed, name), public_only=public_only):
            yield name, key, text


def copy_mismatches() -> list[str]:
    document = normalise(DOCUMENT.read_text(encoding="utf-8"))
    problems = []
    for name, key, text in seed_values():
        if text in NOT_FROM_DOCUMENT:
            continue
        for part in text.split("\n\n"):
            if normalise(part) not in document:
                problems.append(f"{name}.{key}: {part[:90]}")
    return problems


def banned_terms() -> list[str]:
    found = []
    for name, key, text in seed_values(public_only=True):
        found += [f"seed {name}.{key}: “{m.group(0)}”" for pattern in BANNED if (m := pattern.search(text))]
    for path in [*FRONTEND.rglob("*.tsx"), *FRONTEND.rglob("*.ts")]:
        source = path.read_text(encoding="utf-8")
        found += [f"{path.relative_to(FRONTEND.parent)}: “{m.group(0)}”" for pattern in BANNED
                  if (m := pattern.search(source))]
    return found


def shingles(text: str) -> set[tuple[str, ...]]:
    words = re.findall(r"[a-z0-9’']+", normalise(text))
    return {tuple(words[i:i + SHINGLE]) for i in range(max(0, len(words) - SHINGLE + 1))}


def page_text(obj) -> str:
    from .models import Sector

    if isinstance(obj, Sector):
        parts = [obj.intro, obj.our_focus, *obj.list_items.values_list("text", flat=True),
                 *obj.faqs.values_list("answer", flat=True)]
    else:
        parts = [obj.intro, obj.who_we_support, obj.context_body,
                 *(f"{t} {d}" for t, d in obj.capabilities.values_list("title", "description")),
                 *obj.bullets.values_list("text", flat=True), *obj.steps.values_list("body", flat=True),
                 *obj.faqs.values_list("answer", flat=True)]
    return " ".join(p for p in parts if p)


def near_duplicates(limit: float = THIN_LIMIT) -> list[str]:
    """Pairs of service or sector pages whose English text overlaps by more than `limit` (Jaccard)."""
    from .models import Sector, Service

    found = []
    for model in (Service, Sector):
        pages = [(obj, shingles(page_text(obj))) for obj in model.objects.all()]
        for (a, sa), (b, sb) in combinations(pages, 2):
            if sa and sb and (score := len(sa & sb) / len(sa | sb)) > limit:
                found.append(f"{model._meta.verbose_name} “{a}” and “{b}” share {score:.0%} of their text")
    return found
