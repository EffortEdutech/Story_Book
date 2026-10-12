import json, unittest
from pathlib import Path
try: import jsonschema
except Exception: jsonschema=None
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase8'; SC=ROOT/'schemas'
M={
'sales_clean.json':'sales_record.schema.json','reconciliation_clean.json':'financial_reconciliation.schema.json','payment_clean.json':'payment_record.schema.json','select_clean.json':'select_term.schema.json','optimization_clean.json':'postpub_optimization.schema.json','revision_minor.json':'revision_classification.schema.json','erratum_clean.json':'erratum.schema.json','return_exposure_clean.json':'return_exposure.schema.json','return_record_clean.json':'return_record.schema.json','feedback_preference.json':'feedback.schema.json','deposit_print_clean.json':'legal_deposit_status.schema.json','rights_opportunity_clean.json':'rights_opportunity.schema.json','publication_manifest_clean.json':'publication_manifest.schema.json','provenance_clean.json':'provenance_graph.schema.json','recovery_clean.json':'recovery_manifest.schema.json','postpub_state_clean.json':'post_publication_state.schema.json'}
@unittest.skipIf(jsonschema is None,'jsonschema unavailable')
class Phase8SchemaTests(unittest.TestCase):
    def test_clean_fixtures_validate(self):
        for fixture,schema in M.items():
            data=json.loads((FX/fixture).read_text()); sch=json.loads((SC/schema).read_text())
            if fixture=='sales_clean.json': data=data['records'][0]
            with self.subTest(fixture=fixture): jsonschema.Draft202012Validator(sch).validate(data)
if __name__=='__main__': unittest.main()
