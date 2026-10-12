# Phase 5 — Amazon KDP Adapter Architecture

Phase 5 is a downstream adapter. It consumes approved identity, production and commercial records; it never becomes the source of truth. Current KDP requirements are recorded in dated rule snapshots and refreshed before live execution.

Critical invariants:
- KDP free ISBNs never support the shared KDP + Ingram publisher-owned ISBN architecture.
- Paperback and hardcover ISBNs are distinct.
- KDP Select is an explicit eBook exclusivity decision and cannot coexist with wide distribution of the same digital eBook during an active term.
- KDP Expanded Distribution is disabled when the same paperback ISBN is distributed through Ingram or another service.
- AI-content disclosure is derived from real content provenance and current KDP definitions; it is never guessed.
- Print Previewer does not replace physical proof review.
- Every live Publish action is edition-specific and human-authorized.
