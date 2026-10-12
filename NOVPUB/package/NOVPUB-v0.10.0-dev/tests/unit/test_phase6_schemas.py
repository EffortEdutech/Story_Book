import json, unittest
from pathlib import Path
try:
    import jsonschema
except Exception:
    jsonschema=None
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase6'; SC=ROOT/'schemas'
M={
'account_ready.json':'ingram_account_readiness.schema.json','metadata_clean.json':'ingram_title_metadata.schema.json','manufacturing_clean.json':'ingram_manufacturing_config.schema.json','isbn_clean.json':'ingram_isbn_reconciliation.schema.json','coexistence_clean.json':'kdp_ingram_coexistence.schema.json','pricing_clean.json':'ingram_market_pricing.schema.json','returns_nonreturnable_clean.json':'ingram_return_policy.schema.json','eproof_clean.json':'ingram_eproof.schema.json','physical_proof_clean.json':'ingram_physical_proof.schema.json','distribution_authorization_clean.json':'ingram_distribution_authorization.schema.json','retailer_listing_clean.json':'retailer_listing_snapshot.schema.json'}
@unittest.skipIf(jsonschema is None,'jsonschema unavailable')
class Phase6SchemaTests(unittest.TestCase):
    def test_clean_fixtures_validate(self):
        for fixture,schema in M.items():
            with self.subTest(fixture=fixture): jsonschema.Draft202012Validator(json.loads((SC/schema).read_text())).validate(json.loads((FX/fixture).read_text()))
if __name__=='__main__': unittest.main()
