# -*- coding: utf-8 -*-
"""Replace Flowwow brand mentions with «маркетплейс»; keep CDN URLs intact."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"research", "crm-course", "transcripts", "scripts"}

REPS = [
    ("мимо Flowwow", "мимо маркетплейса"),
    ("Мимо Flowwow", "Мимо маркетплейса"),
    ("на Flowwow", "на маркетплейсе"),
    ("На Flowwow", "На маркетплейсе"),
    ("во Flowwow", "на маркетплейс"),
    ("Во Flowwow", "На маркетплейс"),
    ("с Flowwow", "с маркетплейса"),
    ("С Flowwow", "С маркетплейса"),
    ("к Flowwow", "к маркетплейсу"),
    ("К Flowwow", "К маркетплейсу"),
    ("из Flowwow", "с маркетплейса"),
    ("Из Flowwow", "С маркетплейса"),
    ("для Flowwow", "для маркетплейса"),
    ("Доступы к Flowwow", "Доступы к маркетплейсу"),
    ("доступы к Flowwow", "доступы к маркетплейсу"),
    ("Заказы Flowwow", "Заказы маркетплейса"),
    ("заказы Flowwow", "заказы маркетплейса"),
    ("Flowwow заказы", "Заказы маркетплейса"),
    ("Flowwow подключён", "Маркетплейс подключён"),
    ("Flowwow · подключено", "Маркетплейс · подключено"),
    ("Flowwow dual", "dual sync маркетплейса"),
    ("Flowwow sync", "Синхронизация маркетплейса"),
    ("= Flowwow", "= маркетплейс"),
    ("· Flowwow", "· Маркетплейс"),
    ("Flowwow →", "Маркетплейс →"),
    ("flowwow —", "маркетплейс —"),
    ("flowwow -", "маркетплейс -"),
    ("· flowwow", "· маркетплейс"),
    ("точек Flowwow", "точек маркетплейса"),
    ("точки Flowwow", "точки маркетплейса"),
    ("курьеры Flowwow", "курьеры маркетплейса"),
    ("аккаунт Flowwow", "аккаунт маркетплейса"),
    ("аккаунта Flowwow", "аккаунта маркетплейса"),
    ("данных Flowwow", "данных маркетплейса"),
    ("сайт Flowwow", "сайт маркетплейса"),
    ("автоматически из Flowwow", "автоматически с маркетплейса"),
    ("BLOOM × FLOWWOW", "BLOOM × MARKETPLACE"),
    ("Bloom × Flowwow", "Bloom × Marketplace"),
    ("Flowwow coral", "marketplace coral"),
    ("(Flowwow → Bloom)", "(маркетплейс → Bloom)"),
    ("Flowwow-inspired", "marketplace-inspired"),
    ("Flowwow", "Маркетплейс"),
    ("FLOWWOW", "МАРКЕТПЛЕЙС"),
    ("flowwow", "маркетплейс"),
]


def should(p: Path) -> bool:
    if p.suffix.lower() not in {".html", ".md", ".json"}:
        return False
    if SKIP.intersection(p.parts):
        return False
    return True


def transform(text: str) -> str:
    placeholders: list[str] = []

    def protect(m: re.Match) -> str:
        placeholders.append(m.group(0))
        return f"__URL_PROTECT_{len(placeholders) - 1}__"

    text = re.sub(r"https?://[^\s\"']*flowwow[^\s\"']*", protect, text, flags=re.I)
    for a, b in REPS:
        text = text.replace(a, b)
    for i, u in enumerate(placeholders):
        text = text.replace(f"__URL_PROTECT_{i}__", u)
    return text


def main() -> None:
    changed: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or not should(p):
            continue
        orig = p.read_text(encoding="utf-8")
        new = transform(orig)
        if new != orig:
            p.write_text(new, encoding="utf-8")
            changed.append(p)

    print(f"changed {len(changed)}")
    for p in changed:
        print(" ", p.relative_to(ROOT.parent))

    left = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or not should(p):
            continue
        t = p.read_text(encoding="utf-8")
        t2 = re.sub(r"https?://[^\s\"']*flowwow[^\s\"']*", "", t, flags=re.I)
        if re.search(r"flowwow", t2, re.I):
            left.append(p)
    print(f"remaining non-url: {len(left)}")
    for p in left:
        print(" ", p)


if __name__ == "__main__":
    main()
