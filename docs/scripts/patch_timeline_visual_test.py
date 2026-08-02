# -*- coding: utf-8 -*-
"""Add visual language + product testing rows to KP timeline stages."""
from pathlib import Path
import re

ROOT = Path(r"C:\Workspace\projects\flowwow-crm")
WT = Path(r"C:\Users\MiBookPro\.grok\worktrees\projects-flowwow-crm\flowwow-crm-dev")

files = [
    ROOT / "docs" / "landing.html",
    ROOT / "docs" / "offer.html",
    ROOT / "docs" / "kp" / "demo" / "landing.html",
    ROOT / "docs" / "kp" / "demo" / "index.html",
    ROOT / "docs" / "kp" / "_template" / "landing.html",
    ROOT / "docs" / "kp" / "_template" / "index.html",
    WT / "docs" / "landing.html",
    WT / "docs" / "offer.html",
]

new_block = """      <div class="panel timeline">
        <div class="tl-row"><div class="tl-key">Фаза 0</div><div class="tl-val">Решения и разведка<span class="tl-sub">Доступы к маркетплейсу, способ чатов, объём данных</span></div></div>
        <div class="tl-row"><div class="tl-key">Визуал</div><div class="tl-val">Выбор визуального языка<span class="tl-sub">Палитра, тон интерфейса, референсы — согласуем до сборки кабинета; дальше всё в одном стиле</span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 1</div><div class="tl-val">Основа системы<span class="tl-sub">Сервер, база, домен, защита данных</span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 2</div><div class="tl-val">Каркас кабинета<span class="tl-sub">Вход, роли, заказы и клиенты; интерфейс в выбранном визуальном языке</span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 3–4</div><div class="tl-val">Заказы маркетплейса<span class="tl-sub">Приём заказов, статусы в обе стороны, карточка, история</span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 5–7</div><div class="tl-val">Прямые продажи и чаты<span class="tl-sub">Ручные заказы, все чаты в одном окне, уведомления</span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 8–10</div><div class="tl-val">Цифры и витрина<span class="tl-sub">Аналитика, управление ценами, контроль подключений</span></div></div>
        <div class="tl-row"><div class="tl-key">Тесты</div><div class="tl-val">Тестирование продукта<span class="tl-sub">Прогон сценариев с вашей командой, правки по фидбеку, приёмка перед запуском</span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 11–13</div><div class="tl-val">Финал и передача<span class="tl-sub">Бонусы, оплата, укрепление защиты, передача кода</span></div></div>
      </div>"""

pat = re.compile(r'      <div class="panel timeline">.*?</div>\n    </section>', re.S)


def main() -> None:
    for f in files:
        if not f.exists():
            print("MISS", f)
            continue
        text = f.read_text(encoding="utf-8")
        if 'tl-key">Визуал' in text and "Тестирование продукта" in text:
            print("ALREADY", f)
            continue
        m = pat.search(text)
        if not m:
            print("NO MATCH", f)
            i = text.find("panel timeline")
            print("  idx", i)
            continue
        new_text = text[: m.start()] + new_block + "\n    </section>" + text[m.end() :]
        f.write_text(new_text, encoding="utf-8")
        print("OK", f)


if __name__ == "__main__":
    main()
