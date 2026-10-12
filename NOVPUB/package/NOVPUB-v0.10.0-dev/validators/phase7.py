import json
from pathlib import Path
from datetime import date


def _load(value):
    if isinstance(value,(str,Path)):
        return json.loads(Path(value).read_text(encoding='utf-8'))
    return value


def validate_arc_manifest(record):
    d=_load(record); errors=[]
    for f in ('arc_id','source_manuscript_version','format'):
        if not d.get(f): errors.append(f'ARC-001 required field missing: {f}')
    if d.get('review_required') is not False: errors.append('ARC-006 ARC must not require a review')
    if d.get('review_incentive') is True: errors.append('ARC-007 review incentive detected')
    if d.get('approved') is not True or not d.get('approved_by'): errors.append('ARC-010 ARC lacks human approval')
    if d.get('format') in ('PDF','PRINT') and d.get('not_for_resale') is not True: errors.append('ARC-008 advance copy not marked not-for-resale')
    return errors


def validate_arc_recipient(record):
    d=_load(record); errors=[]
    if d.get('review_required') is not False: errors.append('ARC-006 review improperly required')
    if d.get('incentive') is True: errors.append('ARC-007 incentive linked to review')
    if d.get('future_benefit_conditioned_on_review') is True: errors.append('ARC-007 future benefit conditioned on review')
    return errors


def validate_reviewer(record):
    d=_load(record); errors=[]
    rel=str(d.get('relationship_to_author','')).strip().lower().replace(' ','_')
    conflict_rel={'spouse','family','close_friend','employee','business_associate','publisher_staff','coauthor','financial_partner'}
    financial=d.get('financial_interest') is True
    conflict=rel in conflict_rel or financial
    if conflict and d.get('amazon_review_eligible') is True: errors.append('REV-001 conflicted reviewer marked Amazon-eligible')
    if conflict and d.get('conflict_status')=='ELIGIBLE': errors.append('REV-001 reviewer relationship conflict')
    if d.get('paid_promotional_relationship') is True and d.get('amazon_review_eligible') is True: errors.append('REV-001 paid promoter marked Amazon customer-review eligible')
    if d.get('conflict_status')=='UNKNOWN': errors.append('REV-001 reviewer eligibility unresolved')
    return errors


def validate_reviewer_outreach(record):
    d=_load(record); errors=[]
    if d.get('review_requested') and d.get('review_optional') is not True: errors.append('REV-003 review request not explicitly optional')
    if float(d.get('compensation',0) or 0)>0 and d.get('review_requested'): errors.append('REV-002 compensated customer review detected')
    if d.get('positive_review_requested') is True: errors.append('REV-003 positive review requested')
    if d.get('star_rating_requested') not in (None,0): errors.append('REV-003 star-specific review requested')
    if d.get('future_benefit_conditioned_on_review') is True: errors.append('REV-002 future benefit conditioned on review')
    return errors


def validate_review_record(record):
    d=_load(record); errors=[]
    if d.get('marketing_use_approved'):
        if not d.get('source'): errors.append('REV-007 review attribution/source missing')
        if d.get('quote') and d.get('exact_quote_verified') is not True: errors.append('REV-006 review quote not exact-verified')
        if d.get('quote') and d.get('context_preserved') is not True: errors.append('REV-006 review quote context not preserved')
        if str(d.get('permission_status','')).upper() in ('REQUIRED_MISSING','DENIED'): errors.append('REV-008 permission requirement unresolved')
    return errors


def validate_launch_team(record):
    d=_load(record); errors=[]
    if d.get('approved') is not True or not d.get('approved_by'): errors.append('TEAM-001 launch team not human-approved')
    for m in d.get('members',[]):
        rel=str(m.get('relationship','')).lower().replace(' ','_')
        if rel in {'spouse','family','close_friend','employee','business_associate'} and m.get('amazon_review_eligible') is True:
            errors.append(f"TEAM-002 conflicted member marked Amazon-review eligible: {m.get('member_id','?')}")
        if m.get('paid') is True and m.get('disclosure_required') is not True:
            errors.append(f"TEAM-003 paid promotional relationship lacks disclosure control: {m.get('member_id','?')}")
    return errors


def validate_author_central(record):
    d=_load(record); errors=[]
    if not d.get('author_display_name'): errors.append('AUTH-002 author identity missing')
    if not d.get('claimed_books'): errors.append('AUTH-003 no claimed books recorded')
    if d.get('bio_approved') is not True: errors.append('AUTH-005 author biography not approved')
    if d.get('photo_asset') and d.get('photo_rights_confirmed') is not True: errors.append('AUTH-006 author image rights not confirmed')
    if d.get('duplicate_author_identity_detected') is True: errors.append('AUTH-007 duplicate author identity detected')
    if d.get('status') not in ('READY','VERIFIED'): errors.append('AUTH-001 Author Central profile not ready')
    return errors


def validate_retailer_links(record):
    d=_load(record); errors=[]
    for link in d.get('links',[]):
        if not link.get('url'): errors.append('WEB-001 retailer link missing URL')
        if link.get('accessible') is not True: errors.append(f"WEB-001 broken/inaccessible retailer link: {link.get('retailer','?')}")
        if link.get('correct_book') is not True: errors.append(f"WEB-002 wrong book link: {link.get('retailer','?')}")
        if link.get('correct_format') is not True: errors.append(f"WEB-002 wrong edition/format link: {link.get('retailer','?')}")
    return errors


def validate_marketing_claims(claims):
    rows=_load(claims)
    if isinstance(rows,dict): rows=rows.get('claims',[])
    errors=[]
    for c in rows:
        cid=c.get('claim_id','?')
        if c.get('public_use'):
            if c.get('verification_status')=='UNVERIFIED' or c.get('approved') is not True: errors.append(f'MKT-001 unsupported public marketing claim: {cid}')
            if not c.get('evidence') and c.get('type') not in ('EDITORIAL',): errors.append(f'MKT-001 evidence missing: {cid}')
        if c.get('type')=='RANKING' and c.get('public_use'):
            if not all([c.get('marketplace'),c.get('category'),c.get('rank'),c.get('observed_at')]): errors.append(f'LA-004 ranking claim lacks time/category evidence: {cid}')
        txt=str(c.get('claim','')).lower()
        if ('stocked in' in txt or 'in every bookstore' in txt) and c.get('type')=='DISTRIBUTION': errors.append(f'MKT-001 stocking claim requires direct evidence: {cid}')
    return errors


def validate_marketing_asset(asset, approved_claim_ids=None):
    d=_load(asset); errors=[]; allowed=set(approved_claim_ids or [])
    if d.get('approved') is not True: errors.append('MKT-010 campaign asset not approved')
    if allowed:
        for cid in d.get('source_claims',[]):
            if cid not in allowed: errors.append(f'MKT-001 unapproved claim referenced: {cid}')
    for q in d.get('manuscript_quotes',[]):
        if q.get('exact_match') is not True or not q.get('source_hash'): errors.append('MKT-002 manuscript quote lacks exact source match')
    cta=str(d.get('review_call_to_action','')).lower()
    if any(x in cta for x in ['5-star','five-star','positive review','leave 5 stars','leave five stars']): errors.append('MKT-008 review manipulation CTA')
    return errors


def validate_media_kit(record, approved_claim_ids=None):
    d=_load(record); errors=[]
    for f in ('book_factsheet','approved_cover','approved_author_bio'):
        if not d.get(f): errors.append(f'MEDIA-001 required media-kit asset missing: {f}')
    allowed=set(approved_claim_ids or [])
    if allowed:
        for cid in d.get('claims',[]):
            if cid not in allowed: errors.append(f'MEDIA-002 media kit uses unapproved claim: {cid}')
    if d.get('approved') is not True or not d.get('approved_by'): errors.append('MEDIA-003 media kit lacks human approval')
    return errors


def validate_launch_calendar(record, live_listing_ready=False):
    d=_load(record); errors=[]
    resolved=set(d.get('dependencies_resolved',[]))
    seen=set()
    for e in d.get('events',[]):
        eid=e.get('event_id');
        if eid in seen: errors.append(f'CAL-001 duplicate event id: {eid}')
        seen.add(eid)
        for dep in e.get('dependencies',[]):
            if dep not in resolved and dep not in seen: errors.append(f'CAL-002 unresolved dependency {dep} for {eid}')
        if e.get('requires_live_listing') and e.get('status')=='COMPLETE' and not live_listing_ready: errors.append(f'CAL-003 live-listing event completed before listing readiness: {eid}')
    if d.get('approved') is not True or not d.get('approved_by'): errors.append('CAL-004 launch calendar not human-approved')
    return errors


def validate_launch_day(record):
    d=_load(record); errors=[]
    if d.get('critical_failures'): errors.append('LAUNCH-001 critical launch-day failure present')
    if d.get('ready') is not True: errors.append('LAUNCH-002 launch day not marked ready')
    checks=d.get('checks',{})
    for k in ('website_live','retailer_links_valid','campaign_assets_ready','incident_route_active'):
        if checks.get(k) is not True: errors.append(f'LAUNCH-003 required launch check failed: {k}')
    return errors


def validate_launch_metric(record):
    d=_load(record); errors=[]
    if not d.get('source'): errors.append('LA-001 metric source missing')
    if not d.get('retrieved_at'): errors.append('LA-001 retrieval timestamp missing')
    if d.get('metric_class')=='RANK' and 'sales' in str(d.get('metric','')).lower(): errors.append('LA-003 rank represented as sales volume')
    return errors


def validate_launch_authorization(record):
    d=_load(record); errors=[]
    if d.get('soft_launch_complete') is not True: errors.append('G09 soft-launch QA incomplete')
    if d.get('channels_verified') is not True: errors.append('G09 channels not verified')
    if d.get('proof_status')!='PASS': errors.append('G09 physical-proof status not PASS')
    for f in ('website_status','author_central_status','media_kit_status','campaign_assets_status','review_policy_status','incident_process_status'):
        if str(d.get(f,'')).upper() not in ('PASS','READY','VERIFIED','COMPLIANT'): errors.append(f'G09 {f} not ready')
    if d.get('gate_09')!='PASS': errors.append('G09 authorization record does not declare gate PASS')
    if d.get('authorized') is not True or not d.get('authorized_by'): errors.append('G09 human master launch authorization missing')
    return errors


def validate_gate09(upstream_gates, launch_strategy, arc_manifest, launch_team, author_central, retailer_links, media_kit, claims, assets, calendar, launch_day, authorization, human_approval=False):
    errors=[]
    gates=_load(upstream_gates)
    if isinstance(gates,dict) and 'gates' in gates: gates=gates['gates']
    for gid in ('GATE-05','GATE-06','GATE-07','GATE-08'):
        if gates.get(gid) not in ('PASS','NOT_APPLICABLE'): errors.append(f'G09 upstream gate not ready: {gid}')
    ls=_load(launch_strategy)
    if ls.get('approved') is not True or not ls.get('approved_by'): errors.append('G09 launch strategy not approved')
    errors += validate_arc_manifest(arc_manifest)
    errors += validate_launch_team(launch_team)
    errors += validate_author_central(author_central)
    errors += validate_retailer_links(retailer_links)
    claim_rows=_load(claims); claim_rows=claim_rows.get('claims',claim_rows) if isinstance(claim_rows,dict) else claim_rows
    errors += validate_marketing_claims(claim_rows)
    approved_ids={c.get('claim_id') for c in claim_rows if c.get('approved') and c.get('verification_status')!='UNVERIFIED'}
    errors += validate_media_kit(media_kit,approved_ids)
    asset_rows=_load(assets); asset_rows=asset_rows.get('assets',asset_rows) if isinstance(asset_rows,dict) else asset_rows
    for a in asset_rows: errors += validate_marketing_asset(a,approved_ids)
    errors += validate_launch_calendar(calendar,True)
    errors += validate_launch_day(launch_day)
    errors += validate_launch_authorization(authorization)
    if not human_approval: errors.append('G09 human gate approval missing')
    return errors
