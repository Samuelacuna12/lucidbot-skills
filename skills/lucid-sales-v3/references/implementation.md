# Procedimiento operativo V3

Esta referencia distingue hechos observados de comprobaciones necesarias. Su evidencia y enlaces están en [evidence.md](evidence.md). La secuencia siguiente es una guía de implementación; no afirma que los controles de cada cuenta o versión sean idénticos.

## Instalación e identidad

- **Escrito en la ficha de instalación:** Store de Lucid Bot → Ecommerce v3 Pro → Install → seleccionar el bot → Install del destino. Para otro país, la ficha indica instalar primero V3 y después la adaptación de país sobre el mismo bot. Comprobar disponibilidad y compatibilidad actual antes de ejecutarlo.
- **Observado en una cuenta:** carpeta LucidSales (V3 Pro), versión visible V3-26.10.14 y flujos principales existentes. Este hallazgo demuestra que una instalación existente se debe inspeccionar, no reinstalar por defecto. No es la versión mínima exigida por esta skill.
- **Pendiente por cuenta:** tienda/bot exactos, permisos, canal y vinculación. Lucid Bot y Lucid Sales son productos distintos. Account ID, ID de bot, contacto, WABA y token tampoco se intercambian.
- La ficha de conexión Lucid Bot ↔ Lucid Sales describe el resultado, pero su copia escrita no contiene el formulario técnico. Inspeccionar la interfaz autorizada o el video correspondiente; no inventar un token, endpoint ni una secuencia de clics.

## Configuración comercial e IA

Completar empresa, descripción, dirección comercial, contacto y nombre del asistente. Configurar métodos reales de pago, políticas, preguntas frecuentes generales y postventa. En Lucid Sales → Lucid Bot → Modelo IA se documenta el acceso al comparativo y selección del modelo; comprobar información vigente, saldo y comportamiento efectivo antes de escoger. No reutilizar límites ni recomendaciones numéricas del curso.

Las reglas adicionales complementan a la plantilla. Antes de modificar contratos internos, localizar qué agente responde, qué herramientas tiene y qué flujos ejecutan. Separar generación de texto del envío y de la creación del pedido. Las funciones IA necesitan vínculo real al agente, parámetros y ruta de éxito/fallo.

Agrupar entradas y dividir salidas son ajustes diferentes. Probar una ráfaga producto/talla/ciudad, una corrección posterior y una conversación nueva para comprobar limpieza y conservación del contexto. Si se usa contenido dinámico, preservar acciones y campos al dividir el texto. La detección «contiene una llave» no valida JSON.

## Catálogo, packs y medios

Orden de revisión: catálogo existente → identidad por variante → precio/moneda → ofertas vendibles → proveedor/stock → medios → reglas conversacionales. No crear productos duplicados para remediar una coincidencia de nombre incompleta.

Separar atributos independientes: familia, material, diseño, color, talla y referencia. «Unicolor» no decide si una prenda es algodón o licra. La imagen permite proponer una referencia visible; la composición, el SKU, el precio y la existencia provienen de la ficha verificada.

Mantener una tabla privada con identificadores del origen y destino. Un producto comercial por pack puede representar varios componentes; no copiar su identificador como si fuera una referencia de una prenda. Si una unidad de inventario contiene tres pares, una oferta de seis pares consume dos unidades de esa referencia, cuando ese modelo de inventario esté confirmado.

### Semántica del precio

La revisión de fotogramas registra dos configuraciones históricas distintas:

| Interfaz del curso | Observación | Límite |
|---|---|---|
| Bundle de producto simple, 00:35 | Cantidad 2 y precio exterior 140.000 | No se observó un checkout guardado |
| Bundle de variantes, 02:20 y 02:49 | Cantidad 2, oferta nominal 120.000, precios de variantes 60.000 | Sustenta precio por componente en ese administrador; versión actual y redondeo por comprobar |

Por tanto, no ingresar el total de un pack en un campo unitario sin verificar cómo lo consume la versión actual. Comparar cantidad comercial, composición, precio persistido, total mostrado y total finalmente creado. Si dividir el total no produce un decimal admitido, documentar la discrepancia; no cambiar el precio comercial ni presentar un total aproximado como exacto.

Un SKU puede estar repetido entre bundles del mismo componente en una plataforma, pero el manifiesto local guarda cada componente una sola vez y lo referencia desde varias ofertas. [catalog-contract.md](catalog-contract.md) describe esa normalización; no implica que Lucid imponga unicidad global de SKU.

### Disponibilidad y fotografías

Separar `desconocida`, `verificada` y `asumida por política explícita`. No fabricar cantidades físicas. Permitir vender sin seguimiento de inventario no sincroniza almacenes. Verificar fecha, fuente, almacén y reserva antes de prometer stock comprobado.

Relacionar imagen de conjunto, individual y detalle con la referencia y material autorizados. Las imágenes generadas deben ser fieles y revisadas; no inventar textura, composición o diseño que el producto no tenga. Nombrar cada archivo de forma identificable, revisar recortes y texto alternativo y comprobar su presentación en el canal. Límites de galería se consultan en la interfaz actual; el límite observado en una cuenta no es universal.

## Canales, entrada y notificaciones

Inspeccionar Ajustes → Canales → WhatsApp en el bot destino. La ficha documenta Gestionar → Enlaces útiles → Plantilla de Mensaje; el alta del canal, requisitos de Meta y elegibilidad concreta deben verificarse en la cuenta. Conexión, entrada al Inbox, arranque del flujo y respuesta son comprobaciones separadas.

La creación histórica de plantillas también se accede desde el Administrador de WhatsApp. Elegir cuenta, nombre, idioma, categoría vigente, encabezado, cuerpo, ejemplos de variables y botones pertinentes. Consultar estado y sincronizar en Lucid si hace falta. No prometer plazo de aprobación ni usar categorías históricas como reglas actuales.

El cuerpo revisado de la lección «Mapeo de plantillas» solo contiene el título: su secuencia técnica está **pendiente de verificar**. En la implementación, observar el bloque correspondiente, vincular cada variable a campos existentes y enviar una prueba autorizada al destinatario controlado. Una muestra para aprobación no es el valor real del contacto. Un aviso de Inbox, una alerta de WhatsApp y un mensaje al cliente tienen destinos distintos.

## Pedidos y puente de landing

Flujos observados en una cuenta: `Flujo Principal - LucidSales` y `Confirmacion landing - LucidSales/Shopify/LandingPage`. También se observó una selección del flujo de confirmación en Lucid Sales. No copiar IDs de otro bot: resolver el flujo que realmente pertenece al destino.

La conexión Shopify mostraba estado conectado y opción Importar productos. La app estaba instalada, pero su panel incrustado no cargaba los controles. No se verificaron el interruptor de sincronización de pedidos ni el evento hacia V3. **Instalar, importar, leer pedidos y recibir un webhook son operaciones distintas.**

**Documentación oficial, no prueba de la cuenta:** abrir la app Lucid Bot en Shopify, entrar en Settings, sincronizar productos, introducir la clave del bot en el campo seguro, actualizar conexión/flujos, seleccionar el flujo, habilitar Sync Orders y guardar. El pedido necesita teléfono; Orders permite revisar resultado y reintento. [Guía oficial Shopify](https://ayuda.lucidbot.co/es/articles/9722085-como-conectar-lucid-bot-con-shopify-utilizando-la-aplicacion-lucid-bot). La [ficha de la app](https://apps.shopify.com/lucid-bot?locale=es) confirma transferencia de pedidos, ejecución de flujo y consulta de estado. La selección del flujo V3 correcto y su comportamiento se verifican en el destino.

Procedimiento de aceptación del puente, aún no una receta de endpoints:

1. Identificar dónde nace el pedido de la landing, su ID persistente y el total/estado real.
2. Observar la integración y evento soportados en esa versión. Registrar campos recibidos y errores sin exponer datos personales en el repositorio.
3. Mapear pedido, contacto, moneda, líneas, variante, cantidad de packs y composición. Diferenciar teléfono del canal de teléfono de entrega.
4. Resolver el flujo de confirmación y canal adecuados. Evitar crear otra orden cuando ya existe una del origen.
5. Correlacionar por tienda/origen/ID de pedido. Comprobar que la protección contra duplicados funciona también con eventos repetidos o concurrentes; una etiqueta o una lectura previa no demuestra exclusión mutua.
6. Ejecutar una compra controlada, verificar el pedido en origen, el evento, campos y oportunidad destino, la respuesta del bot y los importes. Mantener despacho/pago real dentro del alcance autorizado.
7. Repetir el mismo evento y una actualización del pedido. Verificar ausencia de pedido, cobro o mensaje duplicado no deseado.

Si faltan canal, landing o acceso al panel, entregar catálogo/configuración preparados y nombrar el puente pendiente. No sustituirlo por un enlace `wa.me` y llamarlo sincronización de compras.

## CRM, pago, garantías y humano

La ficha CRM describe áreas de leads, carritos, pedidos de chat/landing, logística, garantías, novedades y pagos. Sus automatismos son afirmaciones del curso hasta observar cada transición en el bot destino. Caliente no significa comprador; recuperar un carrito no se atribuye sin pedido/correlación comprobados.

Estados de control documentados: pendiente de confirmación, error al subir, corregido por subir y subido a Lucid Sales. En pagos: esperando comprobante, recibido y confirmado. Aplicar el estado según el hecho verificado. No reintentar una escritura incierta sin consultar si la orden ya existe.

Para garantías: identificar pedido/producto y motivo, guardar evidencia pertinente, abrir el caso y asignar responsable. El plazo y remedio salen de la política vigente del negocio, no de ejemplos de clase. La ficha muestra Garantía → En procesamiento → Resuelta, con gestión humana; no configurar aprobación automática porque una IA reconozca la palabra.

Transferir al humano, asignar asesor, detener seguimientos y enviar aviso son acciones diferentes. Probarlas y el retorno al bot. Después de la intervención humana, reconciliar datos estructurados y resumen pertinente para no recuperar una selección antigua.

## Integraciones opcionales

El texto de la lección Hoko observado documenta Ajustes → Tienda → Integraciones → Hoko → credenciales en su interfaz → Conectar; después Productos → Editar producto → Integración seleccionada → Hoko → Seleccione el producto. No demuestra mapeo por variante, dirección/frecuencia de stock ni envío automático. Usar solo si el usuario eligió Hoko y la correspondencia real es comprobable.

Otras integraciones presentes en el índice no se convierten en pasos conocidos por su título. Ads requiere vínculo real anuncio/producto; eventos de compra exigen un criterio de venta comprobado y deduplicación. No activar campañas o envíos por el solo hecho de configurar el catálogo.
