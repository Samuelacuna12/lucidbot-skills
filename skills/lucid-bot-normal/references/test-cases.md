# Pruebas, diagnóstico y entrega

Estos casos son especificaciones propuestas a partir de fallos observados en el curso. No representan pruebas realizadas en la cuenta del lector. Ejecutar solo lo autorizado con datos propios y registrar resultados reales.

## 1. Qué demuestra cada evidencia

| Evidencia | Permite afirmar | No permite afirmar |
|---|---|---|
| Prompt guardado | Instrucción configurada | Que el modelo la respeta siempre |
| Herramienta adjunta | Disponible para ese agente | Que fue invocada |
| Nodo verde / 2xx | Rama/solicitud exitosa según ese mecanismo | Operación de negocio completa |
| Campo modificado | Ese valor se guardó | Pago, reserva o entrega real |
| Objeto externo leído | Objeto/estado observado | Que el cliente recibió notificación |
| Mensaje en hilo | Envío visible según estado | Entrega, lectura o interés si no constan |
| Resumen de llamada | Texto generado disponible | Aceptación explícita o acción ejecutada |

Conservar fecha, versión, bot/canal, caso, entrada sanitizada, resultado esperado, observado, IDs no sensibles y próximo paso. No publicar pantallazos con claves o conversaciones reales.

## 2. Matriz de aceptación por componente

| Componente | Caso | Resultado esperado y lectura |
|---|---|---|
| Entrada | Primer y segundo mensaje | Una ruta de respuesta; bienvenida según regla |
| Captura | Formato incorrecto, omisión | Recaptura/salida prevista; no avanzar con dato vacío |
| Corrección | Usuario cambia solo fecha | Fecha actualizada, demás datos conservados |
| Condición | Todas / Cualquiera, dato ausente | Rama correcta comprobada por valores |
| IA | Proveedor falla | Sin respuesta antigua; salida controlada |
| Herramienta | Datos incompletos | No ejecutar efecto; pedir dato necesario |
| JSON | Inválido, acción no autorizada | No ejecutar ni mostrar instrucciones internas |
| Divisor | Texto + acciones + enlace | Acciones intactas, enlace y cifras conservados |
| Entrada agrupada | Mensaje durante generación | No perder ni duplicar entrada nueva |
| Imagen | URL rota, referencia ambigua | Aclaración/fallo, no inventar producto |
| OCR | Comprobante con beneficiario | No inferir pagador ni pago confirmado |
| CRM | Repetición de la misma solicitud | Una oportunidad vinculada |
| CRM | Dos solicitudes de un contacto | Dos procesos distintos sin cruzar IDs |
| Agenda | Libre → creación correcta | ID y hora guardados; confirmación posterior |
| Agenda | Ocupado o conflicto al crear | No confirmar; alternativas reales |
| Cancelación | ID correcto y operación real | Estado cancelado leído antes del aviso |
| Humano | Asesor toma el chat | Bot y seguimientos incompatibles detenidos |
| Secuencia | Negativa/objetivo cumplido | Desuscripción y exclusión efectivas |
| API | Timeout tras POST | Consultar correlación antes de repetir |
| Sheets | Doble envío | Protección comprobada o límite declarado |
| Webapp | Token/ID manipulado | Rechazo del servidor, sin escritura ajena |
| TTS | Largo → corto → fallo | Audio/texto del turno actual, no anterior |
| Calls | Aceptado, no contestado | No registrar venta ni confirmación |
| Postllamada | Extracción correcta, flujo falla | Estado parcial; no afirmar operación final |

No todas las pruebas aplican a todos los bots. Elegir las funciones implementadas y justificar los casos omitidos. Un bot de texto sin Calls no necesita una llamada para validarse.

## 3. Caso completo: veterinaria con agenda y asesor

**Entrada propuesta:** «El bot dice reservado tras consultar disponibilidad, crea varias tarjetas y sigue escribiendo cuando entra el asesor».

### A. Investigar sin asumir la causa

1. Verificar cuenta, bot, calendario y canal con el historial de una prueba propia.
2. Trazar la ruta: captura → consulta → acción de reserva → mensaje. Buscar qué salida produce «reservado».
3. Leer si existe una reserva y su ID; revisar eventos automáticos del calendario.
4. Localizar todas las acciones Agregar oportunidad, llamadas de herramienta, callbacks y eventos que convergen.
5. Verificar `Chat en vivo habilitado`, no el evento opuesto; revisar secuencias y respuestas automáticas.
6. Revisar qué ocurre con una generación IA ya iniciada cuando el asesor toma el chat.

### B. Corrección propuesta según evidencia

- Conectar confirmación exclusivamente al resultado comprobado de creación; guardar ID/horario y cubrir conflicto/fallo.
- Elegir un responsable del alta CRM y relacionar oportunidad con reserva/solicitud. Resolver duplicados de la prueba sin borrar tarjetas reales indiscriminadamente.
- Transferir a humano, detener secuencias incompatibles y comprobar ese estado antes de cada salida tardía. Asignación no sustituye transferencia.
- Al reanudar, recuperar datos actualizados y usar el evento deliberado de vuelta al bot.
- Añadir protección contra repetición en el ejecutor; una etiqueta sola no garantiza concurrencia.

### C. Prueba de corrección

1. Solicitar una fecha libre con datos completos. Leer una reserva y una oportunidad correctas; solo después aparece confirmación.
2. Repetir la misma entrada o callback. Verificar que no aparece una segunda operación.
3. Solicitar otra cita del mismo contacto. Verificar proceso nuevo y IDs separados.
4. Elegir fecha ocupada. Debe ofrecer alternativa sin decir reservado.
5. Provocar fallo controlado antes de crear. No debe inventar ID ni usar el anterior.
6. Simular resultado incierto y consultar antes de reintentar; comprobar resultado real.
7. Cambiar la fecha antes de confirmar. Revisar instante/zona y datos finales.
8. Pedir humano durante una generación IA. Verificar estado, asignación, contexto y ausencia de salida tardía incompatible.
9. Esperar el momento de una secuencia ya programada mientras atiende humano. No debe enviar.
10. Devolver al bot explícitamente tras una corrección del asesor. Responder con el dato nuevo.
11. Cancelar con operación real. Leer estado cancelado y verificar cupo/CRM/avisos según diseño.
12. Registrar rechazo/no contacto. Comprobar todas las entradas y secuencias aplicables.
13. Repetir la ruta en el canal final. Webchat por sí solo no valida WhatsApp.

## 4. Diagnóstico por síntoma

| Síntoma | Revisar primero |
|---|---|
| Bot mudo | Entrada, paso inicial, publicación, agente, Éxito/Fallo, envío y estado humano |
| Dos respuestas | Respuesta automática + flujo, Continuar + callback, eventos y secuencias |
| Herramienta no se ejecuta | Agente efectivo, herramienta adjunta, intención, parámetros y flujo publicado |
| Dato queda literal | Se guardó instrucción sin generación previa |
| JSON sale al usuario | Ruta inválida/fallback, parseo y esquema del procesador |
| Reserva inexistente | Se confundió disponibilidad con creación |
| CRM duplicado | Más de un alta, callback repetido, consulta previa sin protección concurrente |
| Audio viejo | Campo compartido/sin limpiar, rama corta sin asignación actual |
| Campo API vacío | JSONPath/estructura/contexto sin interpolación o respuesta de error |
| App no cambia tras guardar | Falta nueva versión en implementación publicada |
| Llamada rechazada | Cuenta, número autorizado, agente correcto, clave, saldo y cuerpo |
| Postllamada no actualiza | Bot conectado, campos existentes, extracción, flujo seleccionado y registro final |

No corregir un síntoma con cambios masivos de credenciales, historial o cuentas. Primero aislar la capa y preservar evidencia útil.

## 5. Informe de entrega

Entregar un registro con:

- Función solicitada y bot/canal comprobado.
- Arquitectura y ruta de entrada; componentes que cambiaron.
- Campos, IDs y fuentes de verdad sin secretos.
- Operación real, resultado y lectura posterior.
- Casos ejecutados con observado frente a esperado.
- Estado: diseñado, configurado, probado, activo; separar cada uno.
- Fallos/pendientes concretos y siguiente acción necesaria.
- Alcance de autorización conservado y cambios reversibles disponibles cuando corresponda.

Ejemplo de estado honesto: «Flujo y campos configurados; reserva verificada con un contacto propio en Webchat; WhatsApp pendiente de conectar. Calls documentado, sin llamada ejecutada». Evitar «todo listo» cuando aún falta la prueba final.
