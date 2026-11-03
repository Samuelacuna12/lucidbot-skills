# Contrato del manifiesto local

`scripts/validate_catalog.py` es una comprobación offline. **Este JSON no es un payload ni un importador de Lucid/Shopify/Hoko.** Los nombres siguientes son propios de esta herramienta, no campos nativos descubiertos en esas plataformas.

Ejemplo completo: [assets/catalog-fictional.json](../assets/catalog-fictional.json). Todos sus datos, nombres, códigos, precios y cantidades son ficticios. No contiene contactos ni referencias externas reales.

## Estructura

| Campo | Tipo y significado |
|---|---|
| `schema_version` | Entero 1 |
| `currency` | Texto de tres letras mayúsculas; una moneda por manifiesto |
| `products` | Productos lógicos y sus componentes únicos |
| `product.id/name/item_unit` | Identidad propia, nombre y unidad física: por ejemplo prenda o par |
| `sell_mode` | `packs_only` o `units_and_packs`; es una decisión comercial de entrada |
| `allowed_quantities` | Cantidades de artículos permitidas por oferta; no obliga a crear todas las combinaciones |
| `variants` | `id`, `sku` como texto, `options` de texto, `inventory_unit_size`, `availability` |
| `inventory_unit_size` | Número de artículos físicos en una unidad indivisible del inventario de ese componente |
| `availability` | `unknown`, `verified`, `assumed`; el script no comprueba que la declaración sea cierta |
| `offers` | Ofertas comerciales: producto, variantes elegibles, cantidad por pack y precio |
| `allow_mixed` | Permite varias variantes en la misma composición |
| `same_options` | Atributos que deben coincidir entre las variantes elegidas, como material/diseño |
| `price_mode` | `pack_total` o `per_component`; describe el campo que se está auditando |
| `price_amount` | Decimal como cadena; precio del pack o del componente según el modo |
| `advertised_pack_total` | Total comercial autorizado de un pack, como cadena decimal |
| `upsells` | Producto de origen y oferta adicional existente; `optional: true` |
| `quotes` | Oferta, número de packs, variantes/cantidades físicas y total cotizado |

Una variante normalizada se guarda una vez; varias ofertas pueden referenciarla. Por eso duplicar su SKU en este manifiesto es un error. Esto no prohíbe que una plataforma repita una referencia dentro de administradores diferentes de bundles.

Si los precios dependen de la variante, dividir las ofertas/grupos de precio en el manifiesto. La versión 1 usa un precio uniforme por oferta; no representa reglas arbitrarias de precio mixto, envío, impuestos, descuentos acumulados ni multicurrency. Validar esos conceptos en el checkout real con su contrato específico.

## Cálculos

Para `per_component`: `price_amount × items_per_pack = advertised_pack_total`. Para `pack_total`: ambos importes deben coincidir. Se usa aritmética decimal exacta, sin tolerancia ni redondeo automático.

En una cotización: suma de cantidades seleccionadas = artículos por pack × número de packs. El total es precio por pack × número de packs. Si una referencia almacena tres pares indivisibles, la cantidad seleccionada debe ser múltiplo de tres. «Seis pares» no se convierte en «seis paquetes de tres pares».

## Ejecutar y entender el resultado

Desde la carpeta de la skill:

```sh
python3 scripts/validate_catalog.py assets/catalog-fictional.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Salida JSON: `ok`, `errors`, `warnings`, `counts`, `scope`. Códigos de proceso: 0 coherente, 1 errores de contenido, 2 archivo/JSON ilegible. El ejemplo coherente tiene 2 productos, 4 componentes y 5 ofertas; muestra avisos de stock no verificado porque sus existencias son desconocidas.

Errores como `pack_total_mismatch`, `composition_quantity`, `variant_wrong_product`, `incompatible_options` o `fractional_inventory_unit` identifican el desacuerdo concreto. Corregir los datos/autorización o el mapeo, no ocultar el error con un dato ficticio. Precio correcto en JSON no demuestra que se haya guardado igual en Lucid.

El validador no accede a internet, modifica archivos de entrada, valida titularidad de códigos, prueba fotos, ejecuta IA, confirma stock ni crea un pedido. Ejecutarlo con datos privados requiere conservar esos archivos fuera de la publicación pública.
