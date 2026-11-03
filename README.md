# Lucid Bot: dos rutas de implementación

Guías, conocimiento en JSON y skills para construir bots conversacionales con IA y configurar Ecommerce V3 de Lucid Sales. Material independiente preparado para Samuel Acuña; no es documentación oficial de Lucid.

## Elige tu ruta

| Necesidad | Documento | JSON autocontenido | Skill |
|---|---|---|---|
| Bot propio de atención, ventas o reservas, sin instalar Ecommerce V3 | [Bots normales con IA](docs/bots-normales-con-ia.md) | [Conocimiento de las 20 clases](knowledge/lucid-bot-normal.json) | [lucid-bot-normal](skills/lucid-bot-normal/SKILL.md) |
| Ecommerce con la plantilla V3 y Lucid Sales | [Bots con plantilla V3](docs/bots-con-plantilla-v3.md) | [Conocimiento de V3](knowledge/lucid-sales-v3.json) | [lucid-sales-v3](skills/lucid-sales-v3/SKILL.md) |

Los JSON contienen procedimientos y explicaciones, no solo enlaces. Para descargarlos, abre el archivo y usa **Download raw file**. También puedes descargar todo desde **Code → Download ZIP**.

## Usarlo con otra IA

1. Entrega el JSON de la ruta que necesitas como archivo de contexto.
2. Indica objetivo, negocio, canal, herramientas disponibles y configuración existente.
3. Pide que distinga lo documentado de lo comprobado en tu cuenta y que ejecute las pruebas relevantes.
4. Conserva IDs y resultados de cada operación. Una respuesta del bot no demuestra que se haya creado un pedido, recibido un pago o enviado una notificación.

Leer estos archivos no entrena permanentemente los pesos de una IA ni le concede acceso a una cuenta. El conocimiento se utiliza como contexto y las conexiones se habilitan por separado.

## Instalar las skills

Copia la carpeta elegida de `skills/` al directorio de skills de tu herramienta. En Codex, el destino habitual es `~/.codex/skills/`. Conserva `SKILL.md`, referencias, scripts y ejemplos dentro de la misma carpeta.

Ejemplos de encargo:

- «Usa `$lucid-bot-normal` para montar un bot de reservas. Necesito consulta de disponibilidad, confirmación real y paso a un asesor».
- «Usa `$lucid-sales-v3` para revisar mi catálogo de packs, conectar el flujo de confirmación y comprobar una compra de prueba».

Cada skill tiene referencias que se cargan según la tarea; no hace falta introducir todo el curso en cada conversación.

## Qué está estudiado y qué falta comprobar

La colección **Lucid Academy** comprende 20 grabaciones: 47.412 segmentos transcritos revisados, 599 pantallas seleccionadas y 207 procedimientos documentados. Se revisó la transcripción completa y pantallas de los procedimientos, no cada fotograma de forma continua.

Los enlaces de Skool son referencias bibliográficas; abrir las lecciones requiere tu propio acceso a esa comunidad. Este repositorio no distribuye ni concede acceso a sus videos.

La formación **Ecommerce V3 en Skool es otra colección**. La guía identifica su cobertura escrita y visual sin presentar un índice de lecciones como videos estudiados. Las rutas de instalación, catálogo y conexión incluyen fuentes; los pasos sin evidencia o que dependen de la versión actual se marcan.

El material distingue cinco estados: estudiado, diseñado, configurado, probado y activo. Las pruebas del instructor no certifican una cuenta de un cliente. Las pruebas locales de los scripts comprueban sus ejemplos, no ejecutan bots de producción.

Para llamadas, se documentan la extracción de campos y el flujo posterior, con validación del desenlace antes de afectar pedidos. Para Shopify, importar catálogo, sincronizar un pedido y entregar un mensaje son comprobaciones separadas.

## Contenido y privacidad

Se incluyen ejemplos ficticios y correcciones de errores observados. No se publican las grabaciones originales, sus enlaces privados, transcripciones crudas, claves, teléfonos de participantes, conversaciones comerciales ni inventario de clientes.

Los modelos, precios, cuotas, interfaces y contratos de API pueden cambiar. Las referencias oficiales están junto al procedimiento correspondiente; consulta el contrato vigente antes de aplicar una integración.
