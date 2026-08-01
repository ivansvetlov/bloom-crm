---
title: Architecture stack
created: 2026-08-01
updated: 2026-08-01
type: concept
tags: [architecture, api, hosting]
sources: [raw/architecture/architecture-plan-full.md]
confidence: medium
---

# Architecture stack (default, не догма)

| Layer | Suggestion |
|-------|------------|
| Frontend | Responsive SPA shell (console CRM) |
| API | Modular monolith (Nest / FastAPI / Go) |
| DB | PostgreSQL |
| Queue | Redis + workers |
| Realtime | WebSocket / SSE |
| Files | S3-compatible (Yandex), РФ |
| Hosting | Yandex Cloud / Timeweb РФ |

## Domains
Identity · Directory · Orders · Catalog · CRM · Inbox · Fulfillment · Delivery · Finance · Analytics · Integrations · Notify

## Patterns
Idempotent events, outbox retry, reconcile cursor, dead-letter + owner alert, audit log

## Связанное
- [[bloom-crm]]
- [[modules-map]]
- [[mvp-scope]]
- [[security-152]]
