---
title: Photo gate
created: 2026-08-01
updated: 2026-08-01
type: concept
tags: [ops, order-lifecycle, product]
sources: [raw/architecture/architecture-plan-full.md, raw/research/courier-ux-everest-hybrid.md]
confidence: high
---

# Photo gate

Переход **assembled → out_for_delivery** (или `photo_ready`) требует **before-photo** букета (Flowwow-паттерн «фото до выезда»).

После доставки опционально after-photo.

UI: блок «нужно фото» блокирует кнопку «В доставку» / «Передан курьеру».

## Связанное
- [[order-lifecycle]]
- [[delivery]]
- [[flowwow]]
- [[mvp-scope]]
