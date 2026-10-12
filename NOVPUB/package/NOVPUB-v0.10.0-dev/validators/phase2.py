import json
from datetime import date
from pathlib import Path
from .isbn import validate_isbn13, normalize_isbn13

BLOCKING_SEVERITIES = {'blocking', 'major'}


def _load(value):
    if isinstance(value, (str, Path)):
        return json.loads(Path(value).read_text(encoding='utf-8'))
    return value


def validate_rights_profile(profile, findings=None):
    p = _load(profile)
    errors = []
    if not p.get('authors'):
        errors.append('RIGHTS-001 authorship not established')
    if not p.get('copyright_owners'):
        errors.append('RIGHTS-002 copyright owner unresolved')
    if not p.get('publishing_rights_holders') or not p.get('publication_authority'):
        errors.append('RIGHTS-003 publishing authority unresolved')
    if not p.get('territories'):
        errors.append('RIGHTS-004 territorial rights incomplete')
    if not p.get('formats'):
        errors.append('RIGHTS-005 format rights incomplete')
    if p.get('prior_assignment', {}).get('exists') and not p.get('prior_assignment', {}).get('resolved'):
        errors.append('RIGHTS-006 prior publishing/assignment unresolved')
    if findings:
        fs = _load(findings)
        if isinstance(fs, dict):
            fs = fs.get('findings', [])
        if any(f.get('status') == 'open' and f.get('severity') in BLOCKING_SEVERITIES for f in fs):
            errors.append('RIGHTS-010 blocking rights finding unresolved')
    return errors


def validate_permissions(third_party_items, permissions=None):
    items = _load(third_party_items)
    if isinstance(items, dict):
        items = items.get('items', items.get('content', []))
    perms = _load(permissions) if permissions is not None else []
    if isinstance(perms, dict):
        perms = perms.get('permissions', [])
    by_content = {p.get('content_id'): p for p in perms}
    errors = []
    for item in items or []:
        status = item.get('status')
        cid = item.get('content_id', 'UNKNOWN')
        if status == 'unresolved':
            errors.append(f'TPR-001 unresolved third-party content: {cid}')
        if status in {'licensed', 'permission_obtained'}:
            perm = by_content.get(cid)
            if not perm or perm.get('permission_status') != 'obtained' or not perm.get('evidence_file'):
                errors.append(f'TPR-003 permission evidence missing: {cid}')
        if status == 'public_domain_verified' and not item.get('basis'):
            errors.append(f'TPR-008 public-domain claim unverified: {cid}')
    return errors


def validate_author_identity(identity):
    d = _load(identity)
    errors = []
    author = d.get('author_identity', {})
    if not author.get('display_name'):
        errors.append('IDENT-001 author display name missing')
    legal = d.get('legal_identity', {})
    if author.get('pen_name') and legal.get('exposure_policy') not in {'restricted', 'private'}:
        errors.append('IDENT-002 pen-name legal identity exposure policy unsafe')
    return errors


def validate_publisher_profiles(publisher, imprint=None):
    p = _load(publisher)
    errors = []
    if not p.get('publisher_id') or not p.get('legal_name'):
        errors.append('PUB-001 publisher identity incomplete')
    if not p.get('isbn_registrant_name'):
        errors.append('PUB-002 ISBN registrant name missing')
    if not p.get('approved'):
        errors.append('PUB-003 publisher not approved')
    if imprint is not None:
        i = _load(imprint)
        if i.get('parent_publisher_id') != p.get('publisher_id'):
            errors.append('PUB-004 imprint parent mismatch')
        if i.get('status') != 'approved':
            errors.append('PUB-005 imprint not approved')
    return errors


def validate_edition_manifest(manifest):
    d = _load(manifest)
    editions = d.get('editions', [])
    errors = []
    ids = [e.get('edition_id') for e in editions]
    if not editions:
        errors.append('ED-001 no editions defined')
    if len(ids) != len(set(ids)):
        errors.append('ED-002 duplicate edition_id')
    seen_isbn = {}
    for e in editions:
        if e.get('isbn_required') and not e.get('isbn'):
            errors.append(f'ED-003 required ISBN missing: {e.get("edition_id")}')
        isbn = e.get('isbn')
        if isbn:
            normalized = normalize_isbn13(isbn)
            if not validate_isbn13(isbn):
                errors.append(f'ISBN-001 invalid ISBN-13: {e.get("edition_id")}')
            if normalized in seen_isbn and seen_isbn[normalized] != e.get('edition_id'):
                errors.append(f'ISBN-003 ISBN assigned to multiple editions: {normalized}')
            seen_isbn[normalized] = e.get('edition_id')
    return errors


def validate_isbn_registry(registry):
    d = _load(registry)
    entries = d.get('entries', [])
    errors = []
    seen = set()
    for e in entries:
        raw = e.get('isbn13', '')
        normalized = normalize_isbn13(raw)
        if not validate_isbn13(raw):
            errors.append(f'ISBN-001 invalid ISBN-13: {raw}')
        if not e.get('source') or not e.get('evidence'):
            errors.append(f'ISBN-007 assignment evidence missing: {normalized or raw}')
        if normalized in seen:
            errors.append(f'ISBN-003 duplicate registry ISBN: {normalized}')
        seen.add(normalized)
        if e.get('status') in {'assigned', 'published'} and not e.get('edition_id'):
            errors.append(f'ISBN-004 assigned ISBN lacks edition: {normalized}')
    return errors


def validate_isbn_edition_parity(manifest, registry):
    m = _load(manifest)
    r = _load(registry)
    errors = []
    by_isbn = {normalize_isbn13(x.get('isbn13', '')): x for x in r.get('entries', []) if x.get('isbn13')}
    for e in m.get('editions', []):
        if not e.get('isbn_required'):
            continue
        isbn = normalize_isbn13(e.get('isbn', ''))
        rec = by_isbn.get(isbn)
        if not rec:
            errors.append(f'ISBN-007 registry evidence missing for edition: {e.get("edition_id")}')
            continue
        if rec.get('edition_id') != e.get('edition_id'):
            errors.append(f'ISBN-005 edition mapping mismatch: {e.get("edition_id")}')
        if rec.get('format') and rec.get('format') != e.get('format'):
            errors.append(f'ISBN-005 format mismatch: {e.get("edition_id")}')
    return errors


def validate_copyright_page(page, rights, publisher, editions=None):
    c = _load(page)
    r = _load(rights)
    p = _load(publisher)
    errors = []
    if c.get('copyright_owner') not in r.get('copyright_owners', []):
        errors.append('COPY-001 copyright owner mismatch')
    if c.get('publisher') != p.get('legal_name'):
        errors.append('COPY-002 publisher mismatch')
    if editions is not None:
        e = _load(editions)
        valid = {normalize_isbn13(x.get('isbn', '')) for x in e.get('editions', []) if x.get('isbn')}
        for entry in c.get('isbn_entries', []):
            isbn = normalize_isbn13(entry.get('isbn', ''))
            if isbn and isbn not in valid:
                errors.append(f'COPY-003 ISBN not in edition manifest: {isbn}')
    return errors


def validate_rule_freshness(verified_at, max_age_days=30, today=None):
    try:
        verified = date.fromisoformat(str(verified_at)[:10])
    except Exception:
        return ['COMP-010 regulatory source verification date invalid']
    current = today or date.today()
    if verified > current:
        return ['COMP-010 regulatory source verification date is in the future']
    return [] if (current - verified).days <= max_age_days else ['COMP-010 regulatory source stale']


def validate_legal_deposit_plan(plan, freshness_days=30, today=None):
    d = _load(plan)
    errors = []
    if d.get('jurisdiction') != 'Malaysia':
        errors.append('COMP-001 legal-deposit jurisdiction mismatch')
    if not d.get('obligations'):
        errors.append('COMP-004 required deposit not scheduled/registered')
    errors += validate_rule_freshness(d.get('rule_verified_at', ''), freshness_days, today=today)
    if not d.get('source_snapshot'):
        errors.append('COMP-008 legal-deposit source evidence missing')
    return errors


def validate_gate03(rights, third_party, permissions, human_approval=False, findings=None):
    errors = validate_rights_profile(rights, findings=findings) + validate_permissions(third_party, permissions)
    if not human_approval:
        errors.append('G03 human rights-clearance approval missing')
    return errors


def validate_gate04(author_identity, publisher, imprint, editions, registry, copyright_page,
                    legal_deposit_plan, rights, human_approval=False, today=None):
    errors = []
    errors += validate_author_identity(author_identity)
    errors += validate_publisher_profiles(publisher, imprint)
    errors += validate_edition_manifest(editions)
    errors += validate_isbn_registry(registry)
    errors += validate_isbn_edition_parity(editions, registry)
    errors += validate_copyright_page(copyright_page, rights, publisher, editions)
    errors += validate_legal_deposit_plan(legal_deposit_plan, today=today)
    if not human_approval:
        errors.append('G04 human publication-identity approval missing')
    return errors
