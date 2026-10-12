import json
import unittest
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[2]

class TestSchemaMeta(unittest.TestCase):
    def test_all_schemas_are_valid_draft_2020_12(self):
        schemas = sorted((ROOT / 'schemas').glob('*.json'))
        self.assertGreaterEqual(len(schemas), 30)
        for path in schemas:
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding='utf-8'))
                jsonschema.Draft202012Validator.check_schema(schema)

    def test_phase2_clean_fixtures_validate(self):
        pairs = [
            ('rights_clean.json', 'rights_profile.schema.json'),
            ('author_identity_penname.json', 'author_identity.schema.json'),
            ('publisher_clean.json', 'publisher_profile.schema.json'),
            ('imprint_clean.json', 'imprint_profile.schema.json'),
            ('edition_manifest_clean.json', 'edition_manifest.schema.json'),
            ('isbn_registry_clean.json', 'isbn_registry.schema.json'),
            ('copyright_page_clean.json', 'copyright_page_data.schema.json'),
            ('legal_deposit_clean.json', 'legal_deposit_obligation.schema.json'),
        ]
        for fixture, schema_name in pairs:
            with self.subTest(fixture=fixture):
                instance = json.loads((ROOT / 'tests/fixtures/phase2' / fixture).read_text())
                schema = json.loads((ROOT / 'schemas' / schema_name).read_text())
                jsonschema.Draft202012Validator(schema).validate(instance)

    def test_phase3_clean_fixtures_validate(self):
        pairs = [
            ('book_model_clean.json', 'book_model.schema.json'),
            ('format_strategy_clean.json', 'format_strategy.schema.json'),
            ('trim_clean.json', 'trim_profile.schema.json'),
            ('fonts_clean.json', 'font_register.schema.json'),
            ('typography_clean.json', 'typography_spec.schema.json'),
            ('page_architecture_clean.json', 'page_architecture.schema.json'),
            ('source_manifest_clean.json', 'production_source_manifest.schema.json'),
            ('pagination_clean.json', 'pagination_manifest.schema.json'),
            ('cover_spec_clean.json', 'cover_spec.schema.json'),
            ('cover_qa_clean.json', 'cover_qa.schema.json'),
            ('proof_plan_clean.json', 'proof_plan.schema.json'),
        ]
        for fixture, schema_name in pairs:
            with self.subTest(fixture=fixture):
                instance = json.loads((ROOT / 'tests/fixtures/phase3' / fixture).read_text())
                schema = json.loads((ROOT / 'schemas' / schema_name).read_text())
                jsonschema.Draft202012Validator(schema).validate(instance)

    def test_phase4_clean_fixtures_validate(self):
        pairs = [
            ('metadata_master_clean.json', 'metadata_master.schema.json'),
            ('positioning_clean.json', 'positioning.schema.json'),
            ('classification_clean.json', 'classification_strategy.schema.json'),
            ('keywords_clean.json', 'keyword_strategy.schema.json'),
            ('descriptions_clean.json', 'retail_descriptions.schema.json'),
            ('author_bios_clean.json', 'author_bios.schema.json'),
            ('pricing_clean.json', 'pricing_model.schema.json'),
            ('wholesale_clean.json', 'wholesale_strategy.schema.json'),
            ('returns_clean.json', 'returns_model.schema.json'),
            ('territories_clean.json', 'territory_strategy.schema.json'),
            ('publication_clean.json', 'publication_strategy.schema.json'),
        ]
        for fixture, schema_name in pairs:
            with self.subTest(fixture=fixture):
                instance = json.loads((ROOT / 'tests/fixtures/phase4' / fixture).read_text())
                schema = json.loads((ROOT / 'schemas' / schema_name).read_text())
                jsonschema.Draft202012Validator(schema).validate(instance)

    def test_phase5_clean_fixtures_validate(self):
        pairs = [
            ('rule_current.json', 'kdp_rule_snapshot.schema.json'),
            ('account_ready.json', 'kdp_account_readiness.schema.json'),
            ('kindle_metadata_clean.json', 'kdp_metadata.schema.json'),
            ('paperback_metadata_clean.json', 'kdp_metadata.schema.json'),
            ('hardcover_metadata_clean.json', 'kdp_metadata.schema.json'),
            ('content_origin_clean.json', 'content_origin_record.schema.json'),
            ('select_wide_clean.json', 'kdp_select_decision.schema.json'),
            ('expanded_distribution_clean.json', 'expanded_distribution_check.schema.json'),
            ('kindle_preview_clean.json', 'kindle_preview_report.schema.json'),
            ('paperback_preview_clean.json', 'print_previewer_report.schema.json'),
            ('proof_approved.json', 'kdp_proof_record.schema.json'),
            ('authorization_approved.json', 'publication_authorization.schema.json'),
            ('listing_clean.json', 'amazon_listing_snapshot.schema.json'),
        ]
        for fixture, schema_name in pairs:
            with self.subTest(fixture=fixture):
                instance = json.loads((ROOT / 'tests/fixtures/phase5' / fixture).read_text())
                schema = json.loads((ROOT / 'schemas' / schema_name).read_text())
                jsonschema.Draft202012Validator(schema).validate(instance)

if __name__ == '__main__':
    unittest.main()
