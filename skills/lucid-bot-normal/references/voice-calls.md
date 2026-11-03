# Voz, Lucid Voice y Lucid Calls

Base: clases 13, 16 y 20, más documentación pública. El curso muestra audio saliente y una llamada contestada; no demuestra el resultado final de esa llamada, la extracción posterior ni una operación comercial derivada. Los contratos descritos se contrastaron con Swagger público; deben revisarse de nuevo si cambian o al implementar una cuenta concreta.

## 1. Tres funciones independientes

- **Voz entrante a texto:** transcribe un audio para que el flujo entienda la entrada.
- **Texto a voz (TTS):** convierte la respuesta actual en un archivo de audio.
- **Llamada:** inicia una conversación telefónica con un agente, duración, resultado y posible extracción posterior.

Activar una no activa las otras. Que el modelo genere texto no envía audio; que una solicitud de llamada tenga éxito no significa que alguien contestó.

## 2. Ruta de audio entrante

1. Verificar el tipo de entrada y el mecanismo de transcripción habilitado.
2. Comprobar texto transcrito en el campo que consume el agente.
3. Enviar al mismo flujo conversacional con contexto del turno.
4. Evitar dos respuestas si transcripción y automatismo IA disparan rutas diferentes.
5. Probar audio incomprensible, corto, largo, audio seguido de texto y fallo del proveedor.

La clase 20 diagnostica falta de transcripción al comprobar un interruptor. No generalizar que todas las cuentas usan idéntico ajuste ni cambiar respuestas automáticas sin revisar quién contesta.

## 3. TTS con Lucid Voice

Fuente: [Swagger público Lucid Voice](https://voice.lucidbot.co/api/swagger). El contrato público observado incluye servidores `https://panel.lucidvoice.co/api` y `https://voice.lucidbot.co/api`.

La operación ordinaria es `POST /voice/text2speech`, con cabecera `Authorization` y cuerpo `text`, `voiceId`; `language` aparece como opción. El resultado contiene `isSuccess` y `url`. No añadir `Bearer` por intuición: usar el esquema indicado por el proveedor. Una voz clonada exige derechos/autorización para usarla.

Procedimiento:

1. Conectar cuenta y voz autorizadas; guardar credencial de forma protegida.
2. Generar respuesta actual del agente y continuar por **Éxito**.
3. Si la política requiere audio, preparar texto sin formato que altere la lectura, preservando precios y condiciones.
4. Enviar ese texto, no la frase fija del ensayo, a TTS.
5. Comprobar éxito de negocio y URL nueva no vacía; guardarla asociada al turno.
6. Enviar mensaje de tipo **Audio** usando la URL. Una URL enviada como texto es solo un enlace.
7. En fallo, responder con el texto actual o respaldo compatible según diseño.
8. Verificar audio recibido y contenido correcto, no solo una rama verde.

No guardar una URL vieja en un campo compartido que pueda reutilizarse tras fallo. Probar respuesta larga→corta, error de limpieza, voz inexistente, URL ausente y ausencia de respuesta IA. La rama corta también debe usar texto actual.

El respaldo del curso cubre parcialmente éxito HTTP con URL vacía; no prueba recuperación universal. Cada proveedor puede tener autenticación, campos y respuesta distintos. Si el respaldo falla, terminar de forma controlada; no repetir indefinidamente.

### Streaming

El contrato público añade streaming con NDJSON y piezas como `audioBase64`/`isFinal`. No es intercambiable con mapear `$.url` de una respuesta ordinaria. Implementarlo solo si el cliente sabe procesar el stream y se prueba la reproducción final.

## 4. Preparar Lucid Calls

Fuente principal: [Swagger público Lucid Calls](https://panel.lucidcalls.co/api/swagger). Configurar vía interfaz cuando esta sea la fuente verificable de opciones.

1. Verificar cuenta Calls, bot Lucid conectado y número saliente asignado/autorizado.
2. Crear o revisar agente: nombre, objetivo, modelo/voz disponibles e instrucciones reales.
3. Revisar prompt generado; no aceptar inventos sobre políticas, pedidos o promociones.
4. Definir cuándo puede llamar, a quién y para qué dentro de la autorización del usuario. La guía no autoriza llamadas reales por sí sola.
5. Configurar silencio máximo, duración y cierre. Confirmar semántica en la UI; una explicación del instructor no demuestra tiempos exactos medidos.
6. Configurar campos a recopilar y flujo posterior según las secciones siguientes.
7. Preparar un destinatario propio autorizado y datos de prueba antes de probar una llamada.

No usar cualquier `fromNumber`: debe pertenecer al mecanismo admitido. No falsear país ni números para eludir disponibilidad. Tarifas, saldo, países y voces del curso son históricos.

## 5. Configurar extracción nativa y flujo postllamada

La documentación pública de creación de agentes incluye `extractionFields` y `lucidbotFlowId`. Cada elemento de extracción contiene `target`, `description` y `type` numérico. **El contrato observado no define el enum de `type`; no inventar que un número significa texto, fecha o booleano.** Elegir el campo y su tipo en la interfaz o consultar contrato verificable.

Procedimiento operativo propuesto:

1. En Lucid Bot, crear/identificar campos existentes para el resultado de llamada. Separar datos extraídos, desenlace y estado de negocio confirmado.
2. Comprobar en Calls que el bot conectado es el que contiene esos campos y flujo destino.
3. En el agente, abrir **Qué datos recopila** y seleccionar los campos admitidos. Escribir una descripción por campo: qué cuenta como evidencia, qué hacer si falta, y cómo distinguir negación/corrección.
4. Mantener reglas de ausencia: no inventar valores, no sobrescribir datos confirmados por omisión y no inferir aceptación por silencio.
5. Crear/publicar un flujo postllamada en el bot. Este flujo primero valida identidad, correlación, resultado y campos requeridos; después decide una acción.
6. Seleccionar ese flujo en la configuración posterior de Calls. Guardar y volver a leer la selección.
7. Hacer una llamada propia autorizada. Consultar resultado final; leer los campos del contacto y el historial de ejecución del flujo.
8. Probar rechazo, no respuesta, respuesta ambigua, dato corregido, repetición del resultado y fallo parcial antes de conectar efectos de negocio.

Ejemplo de campos propuestos, no nombres nativos obligatorios:

| Campo | Regla de extracción |
|---|---|
| `motivo_llamada` | Propósito del trámite recibido del sistema, no deducido de otro contacto |
| `intencion_cliente` | Confirmar / rechazar / pedir asesor / indeterminado según respuesta explícita |
| `fecha_solicitada_llamada` | Solo fecha expresada; resolver ambigüedad antes de usar |
| `resumen_llamada` | Hechos y pendientes, sin inventar datos ausentes |
| `operacion_id` | Correlación del trámite, suministrada por el sistema, no adivinada |

La disponibilidad de una llamada terminada o un resumen no acredita confirmación del cliente. El flujo no debe marcar una venta, cancelar pedido o confirmar cita solo porque la llamada se completó. Validar la intención explícita, el objeto correcto y la operación posterior. Conservar datos del pedido fuera de campos compartidos susceptibles a otra llamada simultánea.

La demostración del curso muestra selección de campos/flujo, pero no confirma su ejecución después de la llamada contestada. Esta receta se fundamenta en UI y contrato; exige prueba de extremo a extremo antes de declararla activa.

## 6. IDs y autenticación de Calls

| Operación observada/documentada | Autenticación y precaución |
|---|---|
| `POST /api/auth/login` | Devuelve token; manejar credenciales y JWT solo del lado protegido |
| `GET /api/agents` | JWT `Authorization: Bearer …`; paginación `page`, `limit` (1–100 según contrato revisado) |
| `POST /api/calls` | `x-api-key` según contrato; no sustituir por Bearer |
| `GET /api/calls/{id}` | JWT; consulta de llamada concreta |
| `GET /api/calls/history` | JWT; consulta de historial con filtros admitidos |

La lista de agentes puede estar paginada y su respuesta no está completamente tipada en Swagger observado. No asumir array plano `$`; inspeccionar la respuesta real y mapear su estructura. Resolver nombre con coincidencia única y cuenta correcta, o seleccionar ID explícito. No usar un modelo para escoger entre agentes ambiguos.

El ID de objeto del registro puede ser diferente de `agentId`, usado para la llamada. La clase falla por confundirlos. La documentación observada de `UpdateAgentDto` está vacía: no publicar una receta PATCH como validada ni asumir que acepta todo el esquema de creación.

## 7. Solicitud de llamada

El endpoint observado es `POST https://panel.lucidcalls.co/api/calls`. Campos requeridos: `agentId`, `toNumber`, `fromNumber`; opcionales: `userData`, `lucidbotUserId`. Números en formato admitido (E.164 en la prueba) y origen autorizado.

Plantilla estructural no ejecutable:

```json
{
  "agentId": "AGENT_ID_VERIFICADO",
  "toNumber": "NUMERO_PROPIO_AUTORIZADO_E164",
  "fromNumber": "NUMERO_SALIENTE_ASIGNADO_E164",
  "userData": {
    "contexto": "Resumen mínimo del trámite autorizado, si el prompt usa esta clave"
  },
  "lucidbotUserId": "CONTACT_ID_CORRECTO"
}
```

Las claves dentro de `userData` deben coincidir con el prompt/contrato del agente. En el curso una clave llamada `nombre` transporta un resumen; no copiar esa convención como si fuera un nombre real. No enviar historial completo cuando basta contexto mínimo.

Validar antes del POST: autorización del destinatario, identidad, número, agente, origen, datos y correlación. Guardar pendiente antes del efecto. Si la respuesta es incierta, consultar historial antes de llamar otra vez. Saldo insuficiente es rechazo de solicitud, no llamada realizada.

## 8. Recuperar y verificar el resultado

Separar etapas:

1. Solicitud preparada.
2. HTTP aceptado o rechazado.
3. Registro de llamada creado, con ID cuando esté disponible.
4. Estado de llamada observado.
5. Contestación/conversación acreditada.
6. Resultado final, resumen o transcripción disponibles.
7. Campos extraídos escritos y comprobados.
8. Flujo posterior ejecutado y efecto leído.

No todas las etapas aparecen inmediatamente ni todas se deducen de un solo campo. Dashboard/Swagger público muestran atributos como `status`, `durationSeconds`, `callSuccessful`, resumen/transcripción cuando existan. El contrato observado no enumera todos los estados ni documenta un webhook con firma y reintentos: no inventar esos detalles.

Consultar `GET /api/calls/{id}` o historial usando credencial protegida, o revisar la ficha en **Historial**. Correlacionar destino, agente, fecha y operación; usar ID siempre que esté disponible. Comprobar estado de negocio por una fuente adicional antes de confirmar al cliente.

No reproducir en notas públicas grabaciones, números, tokens ni transcripciones privadas. La grabación del curso acredita una llamada contestada y conversación; no prueba actualización posterior de un pedido. Una respuesta 500 ocurrió con autenticación errónea: no culpar automáticamente al proveedor sin revisar configuración.

## 9. Matriz mínima de prueba Calls

| Caso | Debe observarse |
|---|---|
| Propio autorizado contesta y confirma claramente | Conversación, resultado final, extracción correcta, una sola acción permitida |
| Rechaza o pide asesor | Sin confirmación comercial; derivación prevista |
| No contesta / silencio | Sin aceptación inventada ni datos extraídos ficticios |
| Corrige fecha/contacto | Corrección en campo pertinente y validación posterior |
| ID de agente equivocado | Rechazo/control; no llamar otro agente por azar |
| HTTP incierto | Consulta antes de repetir |
| Resultado repetido | No duplicar CRM/reserva/acción |
| Flujo posterior falla | Estado parcial visible, no declarar negocio completado |

Registrar separado qué se configuró, qué se probó y qué sigue pendiente. Sin número o acceso, conservar el procedimiento y configuración posible; no afirmar llamadas o extracción activas.
