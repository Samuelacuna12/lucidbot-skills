# Arquitectura, datos y flujos

Procedimientos derivados de las clases 1–6 y contrastados con los casos posteriores. Los nombres de menús describen las pantallas del curso: confirmar su ubicación actual. Son instrucciones de implementación, no una afirmación de que el bot del lector ya esté configurado.

## 1. Delimitar el bot y el resultado

Antes de construir, escribir una ficha con cinco elementos: negocio, canal de entrada, intención del cliente, operación que debe ocurrir y evidencia que la confirma. Ejemplo propuesto: una clínica recibe una solicitud de cita por chat; recoge servicio y fecha; consulta el calendario; crea la cita; responde con el ID y horario confirmados. La frase «te esperamos» no es la evidencia.

1. Entrar al bot correcto; comprobar nombre y Account ID. No confundir cuenta de comunidad, bot, usuario/contacto, proveedor IA, cuenta del canal o calendario.
2. Inventariar flujos publicados, puntos de entrada, respuestas automáticas, eventos, secuencias, calendarios y agentes. Guardar una referencia de la versión anterior antes de cambiar componentes compartidos.
3. Identificar quién contesta al primer mensaje y a los siguientes. Dos mecanismos conectados a la misma entrada producen dobles respuestas.
4. Elegir un contacto de prueba propio o una ruta delimitada. Un Webchat público no autentica al tester; una condición basada solo en canal puede afectar a visitantes reales.
5. Mantener separados entorno de prueba y función operativa. Tras reutilizar un flujo, revisar eventos antiguos que aún lo invoquen.

La conexión del canal es una etapa independiente. Una prueba Webchat no comprueba entrada desde anuncios, comentarios, Messenger o WhatsApp. No cambiar número, credenciales ni permisos para corregir un flujo sin comprobar primero qué falla y qué está autorizado.

## 2. Modelo de datos

| Capa | Uso | Ejemplo propuesto | Error que evita |
|---|---|---|---|
| Campo del contacto | Datos y estado de esa conversación/persona | `servicio_solicitado`, `fecha_solicitada`, `reserva_id` | Mezclar datos entre clientes |
| Campo del bot | Configuración compartida | `horario_atencion`, política real | Convertir una política en dato variable por cliente |
| Campo del sistema | Entrada, identidad y estado suministrados por Lucid | `last_input`, `last_input_type` | Leer tiempo como contenido |
| Oportunidad CRM | Proceso comercial concreto | ID, etapa, valor y vencimiento | Usar la última tarjeta para otro pedido |
| Objeto externo | Resultado autoritativo | Reserva, fila, pago o llamada con ID | Confundir texto del bot con operación |
| Contexto del modelo | Conversación relevante para responder | Resumen y últimos cambios | Tratar memoria como base de datos |

Crear campos con nombres estables y tipos apropiados. Un campo definido sin valor no equivale a un campo poblado. Guardar la selección canónica: `duracion_minutos=60` permite comparar exactamente; el texto `1 hora` no coincide con `1`. Una condición «contiene 1» puede confundir 1 con 12.

Teléfono de canal, teléfono de entrega, identificador de contacto y correo son datos diferentes. No reemplazar la identidad del canal por un número extraído del mensaje. Fechas necesitan zona horaria e instante inequívoco; cantidades numéricas no deben llevar separadores ambiguos o símbolos de moneda si la operación espera números.

Para cada campo definir: fuente, tipo, ausencia, corrección, vida útil y quién puede cambiarlo. La última corrección explícita del cliente actualiza el dato pertinente; no borrar otro campo por ausencia en una extracción.

La [documentación de campos del sistema](https://ayuda.lucidbot.co/es/articles/9800935-campos-del-sistema-de-lucid-bot) es la referencia para nombres y límites actuales. No reconstruir nombres desde una transcripción automática. Las notas e historiales pueden contener datos internos: no enviarlos completos al cliente.

## 3. Crear un flujo determinista

1. Abrir **Flujos de trabajo**, crear un flujo con nombre descriptivo y fijar su **Paso inicial**.
2. Añadir **Enviar mensaje**, seleccionar canal compatible y contenido. Insertar variables mediante el selector de campos para evitar nombres mal escritos.
3. Si debe esperar un dato, usar la acción de **Obtener información del usuario**. Elegir tipo, pregunta, campo de destino y manejo de respuesta inválida.
4. Conectar la salida que confirma datos guardados a la validación. Conectar también omisión, tiempo agotado o fallo cuando existan.
5. Añadir condición y comparar el campo ya guardado. Preparar ambas rutas; un dato faltante debe pedir lo necesario o derivar, no caer en una confirmación.
6. Conectar la operación real y sus salidas de éxito/fallo.
7. Publicar. Probar entrada, respuesta, campo y siguiente paso en Inbox o canal elegido.

**Continuar** puede ejecutarse sin que el usuario responda. No unirlo a la misma acción que también ejecuta un callback de respuesta salvo que ese sea el diseño verificado. Un nodo suelto no es una entrada. Una espera añade tiempo, pero no recoge información ni bloquea otras ejecuciones.

Los botones pueden abrir una URL, guardar una selección o saltar a un flujo según tipo. Verificar el efecto: un botón que dice «Reservar» puede abrir una página sin crear nada. Listas y carruseles dependen del canal; su funcionamiento en uno no acredita otro.

## 4. Validar y corregir datos

Un recorrido útil es: preguntar → guardar → validar → mostrar resumen → confirmar o corregir → ejecutar. Para corregir un solo dato, volver a su captura y conservar los demás. No obligar a empezar todo de nuevo por un correo mal escrito.

- Validación de formato: email, teléfono, número, fecha.
- Validación de negocio: servicio existente, duración compatible, monto permitido, horario real.
- Validación contra fuente: disponibilidad, referencia de catálogo o estado externo.
- Confirmación del usuario: que esa sea su selección; no acredita pago ni stock.

Un teléfono con formato válido puede pertenecer a otra persona. Una dirección larga puede ser incorrecta. Los mínimos de longitud/monto de las clases eran reglas de ejemplo; sustituirlos por reglas reales y, cuando corresponda, comprobación externa.

## 5. Condiciones, horarios y bienvenida

La condición **Todas** corresponde a requisitos simultáneos; **Cualquiera**, a alternativas. Probar tabla de verdad mínima: ambos verdaderos, uno falso y dato ausente. Revisar el orden de ramas y la diferencia entre «es» y «no es».

Separar horario comercial del bot, horario del asesor, horario del calendario y ventana del canal. Cada uno controla algo diferente. Fuera de horario, informar el horario real y el siguiente paso sin prometer atención inmediata.

Para una bienvenida una vez: comprobar estado/etiqueta, enviar la bienvenida y marcar la ejecución donde corresponda. Probar la segunda entrada y la vuelta de un cliente existente. No borrar etiquetas reales globalmente para reiniciar una prueba; usar un contacto de prueba. Una etiqueta no evita carreras si dos entradas llegan a la vez: necesitará serialización o deduplicación en el mecanismo que ejecute.

## 6. Eventos y transferencia

En **Herramientas → Desencadenadores y acciones**: seleccionar evento, condición o valor si aplica, acción, guardar y comprobar si quedó habilitado. En el curso, varios se crean apagados.

| Evento | Significado operativo |
|---|---|
| Chat en vivo habilitado | Pasa a atención humana |
| Conversación transferida al bot | Se devuelve al bot |
| Campo cambiado | Reacciona al cambio de valor, también manual |
| Etiqueta aplicada | Reacciona a la aplicación, no a una compra demostrada |

No confundir evento con acción. Un evento puede generar otro y formar un bucle. Si «campo cambiado» vuelve a escribir ese campo o llama un flujo que lo hace, comprobar repetición. Un aviso interno debe ir al operador correcto; no enviarlo como mensaje al comprador.

Transferir, asignar, notificar y detener secuencias son cuatro efectos distintos. El [procedimiento de atención humana](crm-reservations.md) define cómo comprobarlos.

## 7. Secuencias e inactividad

1. Crear y publicar cada flujo de la secuencia, con un propósito claro.
2. En **Herramientas → Secuencias de mensajes**, añadir flujos y demoras.
3. Definir días y horas permitidos. Las demoras se suman y las restricciones pueden posponer un envío.
4. Vincular la suscripción a la entrada correcta. Si se quiere reiniciar por una nueva respuesta entrante, desuscribir y volver a suscribir de forma deliberada; no reiniciar por mensajes salientes.
5. Antes de cada envío, comprobar baja, negativa, estado humano, operación terminada y restricciones del canal.
6. Desuscribir al cumplirse el objetivo o detenerse la conversación, y verificarlo en el historial.
7. Probar repetición, retorno, cambio de flujo y una respuesta que llega justo antes del envío.

Una baja almacenada no detiene automáticamente una secuencia ni otra entrada que no la compruebe. Cambiar de flujo tampoco demuestra desuscripción. No crear un segundo seguimiento si ya existe otro con la misma finalidad. No activar campañas o recontactos por aplicar esta guía sin autorización del usuario.

## 8. Canal y plantillas

Distinguir plantilla de Lucid (estructura reutilizable del bot) de plantilla WhatsApp (mensaje sujeto al proceso y condiciones del canal). Revisar variables requeridas, categoría, destinatario de prueba, estado de aprobación y ventana vigente. Aprobación no demuestra envío; envío no demuestra entrega ni lectura.

La clase incluye mensajes masivos y recomendaciones históricas de conexión. Son material de aprendizaje, no permiso para ejecutar campañas ni garantías sobre elegibilidad o tarifas actuales. Comprobar la documentación oficial del canal al implementar una función que dependa de ella.

## 9. Diagnóstico mínimo de un flujo mudo o repetido

Revisar en este orden: entrada real → paso inicial → versión publicada → campos antes de la condición → rama elegida → operación → salida conectada → estado humano → permisos/canal. Para duplicación, revisar respuestas automáticas, eventos, Continuar, callbacks, secuencias y llamadas de herramientas que converjan. Registrar qué camino produjo cada mensaje antes de borrar o reconstruir el bot.
