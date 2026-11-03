---
name: lucid-sales-v3
description: Configurar, auditar y probar Ecommerce v3 Pro de Lucid Bot con Lucid Sales para vender productos físicos, incluyendo catálogo, packs, variantes y confirmación de pedidos. Aplicar a esa plantilla; para un bot general de servicios o reservas usar el flujo solicitado, sin imponer V3.
---

# Ecommerce V3 con catálogo verificable

Entregar una configuración operativa o una auditoría precisa de Ecommerce v3 Pro, con pruebas por recorrido. La plantilla observada en el material es **Ecommerce v3 Pro - LucidSales**, ficha oficial `791284`. No confundir su nombre con el plan comercial de una cuenta.

## Preparar el trabajo

Recuperar la cuenta/tienda/bot y autorizaciones ya disponibles. Identificar si la plantilla está instalada antes de instalar o reconectar. Pedir únicamente el dato que realmente falta; una instrucción de configurar el bot no autoriza campañas, compras ni despachos ajenos al alcance.

Entradas necesarias: país/moneda, canal destino, catálogo autorizado, materiales/variantes, cantidades de pack, precios totales, fuente y política de disponibilidad, medios permitidos, pagos, envíos, garantías, responsable humano y origen del pedido. No deducir referencias de proveedor ni material a partir de una foto.

Leer [procedimiento](references/implementation.md) para instalación, configuración o integración. Leer [evidencia y límites](references/evidence.md) al elegir la plantilla o cuando un paso del curso parezca describir la interfaz actual. Para catálogo, leer [contrato local](references/catalog-contract.md). Para puesta en marcha, usar [pruebas de aceptación](references/acceptance.md).

## Flujo de implementación

1. Registrar estado previo del bot correcto: plantilla, versión visible, flujos activos, canal, tienda y automatizaciones que compiten. Conservar instalaciones existentes válidas.
2. Completar la relación Lucid Bot ↔ Lucid Sales y comprobar persistencia. El material confirma la relación, pero no documenta todos sus controles técnicos; observarlos antes de indicar clics o credenciales concretas.
3. Configurar empresa, asistente, reglas generales, pagos y postventa. Separar parámetros del proveedor IA del agente, sus herramientas y el flujo que realmente ejecuta una operación.
4. Cotejar producto → variante → oferta/pack → referencia externa. SKU, ID de producto e ID de variante son objetos distintos. Conservar texto y ceros iniciales de códigos. Las variantes pueden diferir en material, talla, color, diseño y precio.
5. Configurar bundles con cantidad y precio coherentes. La evidencia histórica diferencia precio exterior del bundle simple y precio unitario en el administrador de variantes; no trasladar uno al otro sin comprobar total en la interfaz efectiva. Guardar y reabrir; después verificar la cotización/pedido controlado.
6. Vincular imágenes y reglas por producto. Ante una referencia ambigua, conservar la preferencia y aclarar o derivar; no sustituir por un SKU supuesto. Disponibilidad manual o asumida debe identificarse como tal, nunca como sincronización física comprobada.
7. Revisar entrada a V3, IA, derivación humana y seguimientos instalados. No añadir una bienvenida genérica que duplique o reinicie la conversación de la plantilla. Probar mensajes fragmentados, correcciones y salida a humano.
8. Configurar CRM, garantías, pagos y notificaciones según el hecho que cada estado representa. Un comprobante recibido no confirma pago. Una respuesta del asistente no acredita un pedido. Mover una tarjeta no prueba la ejecución externa.
9. Para compra landing → V3, verificar cada eslabón: pedido persistido, evento recibido, correspondencia del catálogo, correlación de pedido/contacto, flujo destino, canal elegible y respuesta observada. Una app instalada, un interruptor activo o importar productos no prueban esta cadena.
10. Ejecutar casos normal, negativo y repetido; revisar el objeto real antes de reintentar una creación incierta. Conservar evidencia mínima, sin secretos ni datos personales innecesarios.

## Validación local útil

El validador incluido revisa **un manifiesto propio**, no un formato de importación ni una API de Lucid. No se conecta a cuentas.

```sh
python3 scripts/validate_catalog.py assets/catalog-fictional.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Comprueba referencias internas, combinaciones duplicadas, cantidades, conversión entre unidades de inventario y pares/prendas, composición de packs, precio unitario frente a total y relaciones de upsell. Usa `Decimal`, sin redondear silenciosamente un desacuerdo. Sustituir el ejemplo ficticio por datos privados autorizados fuera del repositorio público. Un resultado correcto no demuestra stock, IDs externos, configuración guardada ni funcionamiento del bot.

## Salida requerida

Entregar estado por componente: **diseñado / configurado / probado / activo**, fuente de catálogo y disponibilidad, cambios efectuados, pruebas con entradas y resultados observados, errores pendientes y próximo paso concreto. Para una integración incompleta, nombrar el eslabón faltante; no declarar «solo falta el número» si tampoco se verificó el puente de pedidos.

Separar evidencia histórica, lectura actual, inferencia y prueba. El registro Skool disponible contiene **74 lecciones indexadas y 31 fichas escritas revisadas**, además de fotogramas puntuales de dos lecciones; no son 74 videos estudiados. Lucid Academy es otra colección de 20 grabaciones. No republicar sus transcripciones, grabaciones, claves o ejemplos con datos privados.
