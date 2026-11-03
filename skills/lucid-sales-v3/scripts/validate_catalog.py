#!/usr/bin/env python3
"""Validate an offline, normalized sales manifest. Never calls Lucid or a network."""
import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path


def validate(data):
    errors, warnings = [], []

    def error(code, path, message):
        errors.append({'code': code, 'path': path, 'message': message})

    def rows(value, path):
        if not isinstance(value, list):
            error('expected_array', path, 'Se esperaba una lista.'); return []
        return value

    def text(value, path):
        if not isinstance(value, str) or not value.strip():
            error('expected_text', path, 'Se requiere texto no vacío.'); return None
        return value

    def integer(value, path):
        if type(value) is not int or value < 1:
            error('positive_integer', path, 'Se requiere entero positivo, no booleano.'); return None
        return value

    def money(value, path):
        if not isinstance(value, str) or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?', value):
            error('money_string', path, 'Importe decimal como cadena, sin símbolos.'); return None
        try:
            result = Decimal(value)
            if not result.is_finite() or result <= 0:
                raise InvalidOperation
            return result
        except InvalidOperation:
            error('invalid_money', path, 'El importe debe ser decimal finito y positivo.'); return None

    def unique(index, value, obj, path):
        identity = text(value, path)
        if identity is None: return False
        if identity in index:
            error('duplicate_id', path, 'Identificador duplicado.'); return False
        index[identity] = obj
        return True

    def multiply(value, count):
        with localcontext() as context:
            context.prec = max(28, len(value.as_tuple().digits) + len(str(count)) + 2)
            return value * count

    if not isinstance(data, dict):
        return {'ok': False, 'errors': [{'code': 'expected_object', 'path': '$', 'message': 'La raíz debe ser un objeto.'}], 'warnings': []}
    if type(data.get('schema_version')) is not int or data.get('schema_version') != 1:
        error('schema_version', 'schema_version', 'Versión admitida: 1.')
    currency = data.get('currency')
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isalpha() or not currency.isupper():
        error('currency', 'currency', 'Usar un código de moneda de tres letras mayúsculas; confirmar su vigencia aparte.')

    products, variants, offers, skus = {}, {}, {}, {}
    def report():
        return {'ok': not errors, 'errors': errors, 'warnings': warnings,
                'counts': {'products': len(products), 'components': len(variants), 'offers': len(offers)},
                'scope': 'Coherencia local; no verifica cuentas, stock, enlaces, moneda vigente ni pedidos reales.'}
    for i, product in enumerate(rows(data.get('products'), 'products')):
        path = f'products[{i}]'
        if not isinstance(product, dict): error('expected_object', path, 'Producto debe ser objeto.'); continue
        if not unique(products, product.get('id'), product, path+'.id'): continue
        text(product.get('name'), path+'.name'); text(product.get('item_unit'), path+'.item_unit')
        if product.get('sell_mode') not in ['packs_only', 'units_and_packs']:
            error('sell_mode', path+'.sell_mode', 'Usar packs_only o units_and_packs.')
        allowed = rows(product.get('allowed_quantities'), path+'.allowed_quantities')
        for n in allowed: integer(n, path+'.allowed_quantities')
        if product.get('sell_mode') == 'packs_only' and 1 in allowed:
            error('single_unit_forbidden', path+'.allowed_quantities', 'Packs exclusivos no admiten cantidad 1.')
        if not allowed: error('no_quantities', path, 'Definir cantidades vendibles.')
        combinations = set()
        product_variants = rows(product.get('variants'), path+'.variants')
        if not product_variants: error('no_variants', path, 'Debe existir al menos un componente.')
        for j, variant in enumerate(product_variants):
            vp = f'{path}.variants[{j}]'
            if not isinstance(variant, dict): error('expected_object', vp, 'Variante debe ser objeto.'); continue
            if not unique(variants, variant.get('id'), (product, variant), vp+'.id'): continue
            sku = text(variant.get('sku'), vp+'.sku')
            if sku:
                if sku in skus: error('duplicate_component_sku', vp+'.sku', 'Este manifiesto normalizado debe referenciar el mismo componente, no duplicarlo.')
                skus[sku] = variant
            opts = variant.get('options')
            if not isinstance(opts, dict) or not opts:
                error('options', vp+'.options', 'Declarar atributos de la variante.'); opts = {}
            for key, value in opts.items(): text(key, vp+'.options.key'); text(value, vp+'.options.'+str(key))
            signature = json.dumps(opts, sort_keys=True, ensure_ascii=False)
            if signature in combinations: error('duplicate_combination', vp+'.options', 'Combinación repetida dentro del producto.')
            combinations.add(signature)
            integer(variant.get('inventory_unit_size'), vp+'.inventory_unit_size')
            availability = variant.get('availability')
            if availability not in ['unknown', 'verified', 'assumed']:
                error('availability', vp+'.availability', 'Usar unknown, verified o assumed.')
            elif availability != 'verified':
                warnings.append({'code': 'unverified_stock', 'path': vp, 'message': 'No prueba existencias físicas; no prometer stock verificado.'})

    if not products: error('empty_catalog', 'products', 'Definir al menos un producto.')
    if errors: return report()
    offer_prices = {}
    for i, offer in enumerate(rows(data.get('offers'), 'offers')):
        path = f'offers[{i}]'
        if not isinstance(offer, dict): error('expected_object', path, 'Oferta debe ser objeto.'); continue
        if not unique(offers, offer.get('id'), offer, path+'.id'): continue
        pid = offer.get('product_id'); product = products.get(pid) if isinstance(pid, str) else None
        if not product: error('unknown_product', path+'.product_id', 'Producto no definido.')
        n = integer(offer.get('items_per_pack'), path+'.items_per_pack')
        if product and n:
            if n not in product.get('allowed_quantities', []): error('quantity_not_offered', path+'.items_per_pack', 'Cantidad no autorizada por producto.')
            if product.get('sell_mode') == 'packs_only' and n == 1: error('single_unit_forbidden', path, 'No ofrecer unidades en un producto exclusivo de packs.')
            if offer.get('item_unit') != product.get('item_unit'): error('unit_mismatch', path+'.item_unit', 'La oferta y el producto usan distinta unidad (por ejemplo, pares frente a prendas).')
        ids = rows(offer.get('variant_ids'), path+'.variant_ids')
        if not ids: error('no_eligible_variants', path, 'Oferta sin variantes elegibles.')
        seen = set()
        for identity in ids:
            if not isinstance(identity, str): error('variant_id', path+'.variant_ids', 'Referencia de variante debe ser texto.'); continue
            if identity in seen: error('duplicate_eligible_variant', path+'.variant_ids', 'Variante repetida en oferta.')
            seen.add(identity)
            found = variants.get(identity)
            if not found: error('unknown_variant', path+'.variant_ids', 'Variante no definida.')
            elif found[0].get('id') != pid: error('variant_wrong_product', path+'.variant_ids', 'Variante pertenece a otro producto.')
        if type(offer.get('allow_mixed')) is not bool: error('mixed_flag', path+'.allow_mixed', 'Declarar allow_mixed como booleano.')
        same = rows(offer.get('same_options', []), path+'.same_options')
        for option in same:
            if not text(option, path+'.same_options'): continue
            for identity in ids:
                if isinstance(identity, str) and identity in variants and option not in variants[identity][1].get('options', {}): error('missing_option', path+'.same_options', 'Todas las variantes deben declarar el atributo que se conservará.')
        amount = money(offer.get('price_amount'), path+'.price_amount')
        total = money(offer.get('advertised_pack_total'), path+'.advertised_pack_total')
        mode = offer.get('price_mode')
        if mode not in ['pack_total', 'per_component']: error('price_mode', path+'.price_mode', 'Usar pack_total o per_component.')
        if amount is not None and total is not None and n and mode in ['pack_total', 'per_component']:
            calculated = amount if mode == 'pack_total' else multiply(amount, n)
            if calculated != total: error('pack_total_mismatch', path, f'Calculado {calculated}; declarado {total}. No se redondea ni corrige automáticamente.')
            offer_prices[offer['id']] = calculated

    if not offers: error('no_offers', 'offers', 'Definir al menos una oferta vendible.')
    if errors: return report()
    for i, upsell in enumerate(rows(data.get('upsells', []), 'upsells')):
        path = f'upsells[{i}]'
        if not isinstance(upsell, dict): error('expected_object', path, 'Upsell debe ser objeto.'); continue
        source, target = upsell.get('source_product_id'), upsell.get('target_offer_id')
        if not isinstance(source, str) or source not in products: error('unknown_upsell_source', path, 'Producto de origen inexistente.')
        if not isinstance(target, str) or target not in offers: error('unknown_upsell_target', path, 'Oferta adicional inexistente.')
        elif offers[target].get('product_id') == source: error('self_upsell', path, 'El ejemplo de upsell adicional requiere otro producto; modelar cambios de pack como otra oferta.')
        if upsell.get('optional') is not True: error('upsell_not_optional', path, 'Un upsell se agrega tras aceptación, no de forma obligatoria.')

    for i, order in enumerate(rows(data.get('quotes', []), 'quotes')):
        path = f'quotes[{i}]'
        if not isinstance(order, dict): error('expected_object', path, 'Cotización debe ser objeto.'); continue
        offer_id = order.get('offer_id'); offer = offers.get(offer_id) if isinstance(offer_id, str) else None
        if not offer: error('unknown_offer', path, 'Oferta no definida.'); continue
        count = integer(order.get('pack_count'), path+'.pack_count')
        total = money(order.get('quoted_total'), path+'.quoted_total')
        quantities, used, option_values = 0, set(), {}
        for j, selected in enumerate(rows(order.get('selections'), path+'.selections')):
            sp = f'{path}.selections[{j}]'
            if not isinstance(selected, dict): error('expected_object', sp, 'Selección debe ser objeto.'); continue
            identity = selected.get('variant_id'); q = integer(selected.get('quantity'), sp+'.quantity')
            if not isinstance(identity, str) or identity not in variants: error('unknown_variant', sp, 'Variante no definida.'); continue
            if identity in used: error('duplicate_selection', sp, 'Consolidar la cantidad del mismo componente en una sola línea.')
            used.add(identity)
            if identity not in offer.get('variant_ids', []): error('ineligible_variant', sp, 'La oferta no admite esta variante.')
            variant = variants[identity][1]
            if q:
                quantities += q; base = variant.get('inventory_unit_size')
                if type(base) is int and base > 0 and q % base: error('fractional_inventory_unit', sp, 'La selección divide una unidad indivisible de inventario.')
            for name in offer.get('same_options', []):
                if isinstance(name, str): option_values.setdefault(name, set()).add(variant.get('options', {}).get(name))
        if not offer.get('allow_mixed') and len(used) > 1: error('mixed_not_allowed', path, 'La oferta exige una sola variante.')
        if any(len(values) > 1 for values in option_values.values()): error('incompatible_options', path, 'La composición mezcla atributos que esta oferta exige conservar.')
        n = offer.get('items_per_pack')
        if count and type(n) is int and quantities != count*n: error('composition_quantity', path, 'Los componentes no suman la cantidad de todos los packs.')
        if count and total is not None and offer_id in offer_prices and total != multiply(offer_prices[offer_id], count): error('quote_total_mismatch', path, 'Cotización distinta del precio de los packs seleccionados.')
    return report()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.catalog.read_text(encoding='utf-8'))
        result = validate(data)
    except (OSError, ValueError) as exc:
        print(json.dumps({'ok': False, 'errors': [{'code': 'read_error', 'message': str(exc)}]}, ensure_ascii=False)); return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
