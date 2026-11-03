import copy
import json
import unittest
from pathlib import Path
from validate_catalog import validate

EXAMPLE = json.loads((Path(__file__).resolve().parents[1] / 'assets/catalog-fictional.json').read_text())


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(EXAMPLE)

    def has_error(self, code):
        result = validate(self.data)
        self.assertFalse(result['ok'])
        self.assertIn(code, [e['code'] for e in result['errors']])

    def test_example_quotes_and_inventory_units(self):
        result = validate(self.data)
        self.assertTrue(result['ok']); self.assertEqual(result['counts']['components'], 4)
        self.assertTrue(any(w['code'] == 'unverified_stock' for w in result['warnings']))

    def test_rounding_difference_is_not_silently_accepted(self):
        self.data['offers'][1].update(price_amount='1.67', advertised_pack_total='10.00')
        self.has_error('pack_total_mismatch')

    def test_total_entered_as_unit_price_is_rejected(self):
        self.data['offers'][1]['price_amount'] = '42.00'
        self.has_error('pack_total_mismatch')

    def test_units_cannot_replace_pack_only_offer(self):
        self.data['offers'][0]['items_per_pack'] = 1
        self.has_error('single_unit_forbidden')

    def test_composition_counts_all_packs(self):
        self.data['quotes'][0]['pack_count'] = 2
        self.data['quotes'][0]['quoted_total'] = '84.00'
        self.has_error('composition_quantity')

    def test_forbidden_material_mix(self):
        self.data['offers'][1]['variant_ids'].append('demo-lycra-black-m')
        self.data['quotes'][0]['selections'][1]['variant_id'] = 'demo-lycra-black-m'
        self.has_error('incompatible_options')

    def test_variant_from_other_product(self):
        self.data['offers'][0]['variant_ids'].append('demo-socks-black')
        self.has_error('variant_wrong_product')

    def test_selection_not_in_offer(self):
        self.data['quotes'][0]['selections'][1]['variant_id'] = 'demo-lycra-black-m'
        self.has_error('ineligible_variant')

    def test_indivisible_stock_reference(self):
        self.data['quotes'][1]['selections'][0]['quantity'] = 11
        self.has_error('fractional_inventory_unit')

    def test_pair_prenda_mismatch(self):
        self.data['offers'][3]['item_unit'] = 'prenda'
        self.has_error('unit_mismatch')

    def test_upsell_must_exist_and_be_optional(self):
        self.data['upsells'][0]['target_offer_id'] = 'missing'
        self.has_error('unknown_upsell_target')
        self.data['upsells'][0]['target_offer_id'] = 'demo-socks-3'
        self.data['upsells'][0]['optional'] = False
        self.has_error('upsell_not_optional')

    def test_duplicate_normalized_component(self):
        self.data['products'][0]['variants'][1]['sku'] = 'DEMO-COT-NEG-M'
        self.has_error('duplicate_component_sku')

    def test_quote_price_and_nonfinite_money(self):
        self.data['quotes'][0]['quoted_total'] = '41.00'
        self.has_error('quote_total_mismatch')
        self.data['offers'][0]['price_amount'] = 'NaN'
        self.has_error('money_string')

    def test_decimal_multiplication_preserves_all_digits(self):
        self.data['offers'][0].update(price_amount='123456789012345678901234567890.01', advertised_pack_total='370370367037037036703703703670.03')
        self.assertTrue(validate(self.data)['ok'])

    def test_malformed_structures_return_errors_not_tracebacks(self):
        for field, value in [('allowed_quantities', None), ('variants', {}), ('variants', [None])]:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(EXAMPLE); data['products'][0][field] = value
                self.assertFalse(validate(data)['ok'])
        self.assertFalse(validate(None)['ok'])
        self.data['quotes'][0]['pack_count'] = True
        self.has_error('positive_integer')


if __name__ == '__main__':
    unittest.main()
