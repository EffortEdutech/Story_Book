# Phase 6 — IngramSpark Adapter Architecture

Phase 6 is a downstream wholesale/manufacturing adapter. It consumes the approved NOVPUB edition, production, metadata and commercial records and never becomes the source of publication identity truth.

Critical invariants:
- Shared KDP + Ingram print distribution uses the same publisher-owned ISBN for the same edition.
- KDP Expanded Distribution is disabled for an ISBN distributed through Ingram.
- Ingram free ISBNs and KDP free ISBNs do not cross platforms.
- Cover-template geometry is invalidated by relevant page-count/manufacturing changes.
- Wholesale discount and returnability are explicit commercial decisions, not automatic “industry standard” defaults.
- Returnable-to-non-returnable changes preserve the current 180-day residual-liability window in the rule snapshot.
- eProof approval never substitutes for physical-proof inspection.
- Default NOVPUB policy blocks wholesale distribution activation until GATE-08 passes.
- “Available through Ingram” must never be represented as guaranteed physical bookstore stocking.
