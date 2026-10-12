import json, unittest
from pathlib import Path
try: import jsonschema
except Exception: jsonschema=None
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase7'; SC=ROOT/'schemas'
M={
'launch_strategy_clean.json':'launch_strategy.schema.json','arc_clean.json':'arc_manifest.schema.json','arc_recipient_clean.json':'arc_recipient.schema.json','reviewer_clean.json':'reviewer.schema.json','outreach_clean.json':'reviewer_outreach.schema.json','review_clean.json':'review_record.schema.json','launch_team_clean.json':'launch_team.schema.json','author_central_clean.json':'author_central_profile.schema.json','links_clean.json':'retailer_link.schema.json','media_kit_clean.json':'media_kit.schema.json','claims_clean.json':'marketing_claim.schema.json','asset_clean.json':'marketing_asset.schema.json','calendar_clean.json':'launch_calendar.schema.json','launch_day_clean.json':'launch_day_checklist.schema.json','metric_clean.json':'launch_metric.schema.json','authorization_clean.json':'launch_authorization.schema.json'}
@unittest.skipIf(jsonschema is None,'jsonschema unavailable')
class Phase7SchemaTests(unittest.TestCase):
    def test_clean_fixtures_validate(self):
        for fixture,schema in M.items():
            data=json.loads((FX/fixture).read_text()); sch=json.loads((SC/schema).read_text())
            if schema=='marketing_claim.schema.json': data=data['claims'][0]
            with self.subTest(fixture=fixture): jsonschema.Draft202012Validator(sch).validate(data)
if __name__=='__main__': unittest.main()
