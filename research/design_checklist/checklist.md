# API Design Essentials Checklist

## Modeling & Abstractions
- **Get the primitives right**: design around universal concepts (e.g., `PaymentIntent` + `PaymentMethod`).
- **Separate money movement from business logic**: keep payments as a reusable service.
- **Avoid nullable fields**: use join tables or explicit metadata objects.

## Idempotency & Consistency
- **Idempotency keys on all writes** that move money or change state.
- **Exactly-once semantics**: retries must not double-charge or double-refund.
- **Retries are shared responsibility**: server deduplicates, clients reuse keys.

## Reliability & Fault Tolerance
- **Isolate side effects**: database transactions must remain atomic, no network calls inside.
- **Support webhooks + polling**: webhooks for async updates, polling as fallback.
- **Graceful degradation**: fail safely, avoid corrupting financial state.
- **Task queues must be reliable**: ensure ordering + idempotency (DB-backed if needed).

## Safety, Limits, and Controls
- **Rate limiting**: per-endpoint quotas, include headers (`X-RateLimit-Remaining`, `Retry-After`).
- **Kill switches**: ability to disable abusive tenants or endpoints instantly.
- **Error isolation**: one bad request should not block a batch or queue.

## Pagination & Data Access
- **Cursor-based pagination** for large datasets.
- **Always return `next_page` or cursor tokens** in responses.
- **Optional fields**: make expensive fields requestable (`?include=details`).

## Authentication & Developer Experience
- **API keys first**: long-lived keys for simple scripts, OAuth for production use.
- **Fast start principle**: first request should work in <60 seconds.
- **Good documentation**: code samples, migration notes, clear error guides.

## Observability & Debugging
- **Consistent error semantics**: retryable (5xx) vs. non-retryable (4xx).
- **Structured responses**: machine-readable error codes + human-readable messages.
- **Auditability**: trace every request/response with request IDs or idempotency keys.

## Stability & Change Management
- **Never break userspace**: don’t remove or rename fields, only add.
- **Versioning as a last resort**: support old + new in parallel, with clear migration paths.