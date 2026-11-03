# Biblioteca completa y método de estudio

La edición pública contiene las **20 clases y 207 procedimientos**, con fichas, notas íntegras saneadas, límites y correcciones. No distribuye grabaciones, transcripciones literales, capturas privadas, enlaces privados, datos de participantes ni credenciales.

La revisión original combinó transcripción completa y pantallas seleccionadas de los procedimientos. No se reprodujo continuamente cada fotograma. «Estudiado» no significa instalado o probado en una cuenta del lector. Las fichas distinguen lo observado, explicado, configurado y no verificado.

## Cómo consultar sin cargar todo a la vez

La copia autónoma está en [course-knowledge.json](course-knowledge.json). En el repositorio se publica también `knowledge/lucid-bot-normal.json`. El buscador es de solo lectura, sin red, dependencias externas ni acciones en cuentas.

Desde la carpeta de esta skill:

```sh
python3 scripts/course_lookup.py
python3 scripts/course_lookup.py --query "Chat en vivo habilitado" --limit 3
python3 scripts/course_lookup.py --query "reserva disponibilidad" --limit 5
python3 scripts/course_lookup.py --query "llamada extracción" --limit 5
python3 scripts/course_lookup.py --session 20
python3 scripts/course_lookup.py --document lesson-19-notes
python3 scripts/course_lookup.py --validate
```

`--session` devuelve ficha completa y documento de notas correspondiente. `--document` permite recuperar un documento íntegro. `--knowledge` admite una copia alternativa explícita. Las búsquedas ponderan palabras completas y frases; recuperar más resultados o la ficha completa cuando un resumen no resuelva un paso.

## Mapa de las 20 clases

| Clase | Núcleo de aprendizaje | Lectura práctica |
|---|---|---|
| 1 | Cuentas, bot, contactos, permisos, campos, plantillas e Inbox | Arquitectura y flujos |
| 2 | Activos de canal, proveedores IA, ajustes, equipos e intención | Arquitectura; IA |
| 3 | Canales, conflictos de respuestas, editor, plantillas y segmentación | Arquitectura y pruebas de canal |
| 4 | Captura, botones, tipos de datos, reintentos y conexiones | Arquitectura y flujos |
| 5 | Condiciones, operadores, horario, bienvenida y catálogo determinista | Arquitectura y flujos |
| 6 | Rutas de prueba, secuencias, eventos, humano/bot e historial | Arquitectura; CRM/humano |
| 7 | Pipelines, campos, etapas, vencimientos y duplicados | CRM |
| 8 | Seguimiento, calendarios, capacidad, reservas y cancelación | Reservas |
| 9 | Reserva conversacional completa, herramientas IA y Sheets | Reservas; IA; integraciones |
| 10 | Agentes, parámetros, herramientas, multimedia y derivación | IA y herramientas |
| 11 | Confirmación, guardado, contexto tras asesor y agrupación | IA; CRM/humano |
| 12 | Modalidades de agenda, normalización, pagos y cancelación limitada | Reservas; pruebas |
| 13 | Agrupación multimodal, voz, clasificación, CRM y diagnóstico | IA; voz; pruebas |
| 14 | Agenda, JSON mensajes/acciones y divisor que conserve operaciones | IA y JSON |
| 15 | Extracción, handoff con horario, MCP y entradas contextuales | IA; CRM; integraciones |
| 16 | TTS, JSON, transferir/asignar, medios y postbacks | IA; voz; pruebas |
| 17 | Historial, validación, reparto/aviso de asesor y dos agentes MCP | IA; CRM; integraciones |
| 18 | Métodos HTTP, Swagger/Postman, contactos, conversión y errores | Integraciones |
| 19 | Apps Script, despliegue, Sheets, contacto y retorno desde páginas | Integraciones y web |
| 20 | Voice, Calls, campos extraídos, flujo posterior y llamada contestada | Voz y Calls |

Las menciones históricas a una plantilla ecommerce aparecen marcadas como comparación de alcance o ejemplo específico. No son instrucciones para instalarla en el bot normal. La formación de esa plantilla es una colección separada y tiene su propia skill/documento.

## Fuentes oficiales para comprobar capacidades actuales

- [Campos del sistema de Lucid Bot](https://ayuda.lucidbot.co/es/articles/9800935-campos-del-sistema-de-lucid-bot): nombres y referencias.
- [Lucid Voice Swagger](https://voice.lucidbot.co/api/swagger): operaciones y formatos de voz.
- [Lucid Calls Swagger](https://panel.lucidcalls.co/api/swagger): agentes, llamadas y consultas.
- [Apps Script webapps](https://developers.google.com/apps-script/guides/web): despliegue, identidad y parámetros.
- [Cuotas Apps Script](https://developers.google.com/apps-script/guides/services/quotas): límites por cuenta/operación.
- [Shopify Storefront MCP](https://shopify.dev/docs/apps/build/storefront-mcp): contrato actual para catálogo, separado de plantilla V3.

Las fuentes se conservan como referencias, no como promesa de compatibilidad instalada. Verificar versión y cuenta antes de actuar. No adoptar tarifas, límites, modelos o recomendaciones de evasión de controles de una grabación histórica.

## Política de evidencia

1. Procedimiento observado en curso: conservar qué se ve y sus límites.
2. Explicación del instructor: atribuirla como explicación si no se prueba.
3. Corrección documental: indicar fuente primaria y diferencia cuando exista.
4. Adaptación propuesta: marcarla; no presentarla como prueba histórica.
5. Ejecución en una cuenta: registrar por separado entrada, cambios, operación y resultado.

El conocimiento ayuda a construir y diagnosticar. No concede permisos, no modifica cuentas y no prueba que una configuración futura funcione sin validación.
