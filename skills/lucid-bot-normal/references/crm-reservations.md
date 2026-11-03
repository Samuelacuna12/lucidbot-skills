# CRM, reservas y atención humana

Base: clases 6–17. Los ejemplos son propuestas adaptables; las políticas, plazos y horarios deben venir del negocio.

## 1. Diseñar el proceso CRM

Elegir qué representa una oportunidad: consulta comercial, servicio, pedido o reserva. Un contacto puede tener varias; no asumir una sola tarjeta para toda su vida.

1. Crear pipeline y etapas del proceso real. Ejemplo propuesto: solicitud recibida → datos completos → cita confirmada → servicio realizado; cancelada como estado/etapa según el diseño elegido.
2. Crear campos necesarios, con responsable y fuente. Los campos del pipeline no son los del contacto.
3. Definir evento de alta único y guardar el ID retornado o una correlación verificable.
4. Antes de mover, consultar que exista la oportunidad correcta. Si falta, tratar la excepción; mover no crea.
5. Actualizar etapa, estado, prioridad, valor y vencimiento según su significado. No confundirlos.
6. Probar dos solicitudes del mismo contacto y una repetición de la misma solicitud.

`Agregar oportunidad` crea otra tarjeta. La referencia `pipelines.<referencia>...` puede resolver la última actualizada; no demuestra que sea la relacionada con la reserva actual. Conservar `operacion_id` y `oportunidad_id` o una clave equivalente que realmente permita resolverla.

Un valor comercial no prueba pago. Una etapa «caliente» no acredita interés humano, autoridad o presupuesto. No mover a ganado por enviar un enlace o recibir un comprobante.

## 2. Evitar duplicados y carreras

Una consulta previa reduce duplicados, pero dos ejecuciones simultáneas pueden ver ausencia y crear ambas. La corrección necesita protección en el ejecutor: clave idempotente soportada, unicidad, serialización u otro mecanismo verificable. Si la plataforma no lo ofrece, documentar límite y reducir puntos de alta; no afirmar garantía inexistente.

Tras timeout, primero consultar el ID/correlación y registros. Repetir una creación sin comprobar puede duplicar CRM, reserva o fila. Registrar «resultado incierto» como estado propio.

Para vencimiento relativo, guardar fecha de referencia → sumar intervalo autorizado → asignar vencimiento a la oportunidad correcta. Los quince días de un ejemplo no crean política de garantía ni tarea automática diaria.

## 3. Crear el calendario

En **Herramientas → Gestor de reservas**:

1. Conectar el proveedor autorizado y comprobar la cuenta/calendario elegidos.
2. Crear calendario con nombre inequívoco y duración del servicio.
3. Definir días, horarios y zona horaria; revisar qué verá el visitante.
4. Configurar descansos/buffers, antelación, horizonte y capacidad real.
5. Definir quién presta el servicio y cómo se resuelven conflictos. Capacidad de grupo no asigna personal automáticamente.
6. Elegir flujos de confirmación, cancelación y recordatorio. Anotar qué efecto hace cada uno.
7. Crear una reserva propia de prueba y comprobar calendario externo, datos, instante y avisos.

Al duplicar calendarios, revisar nombre, duración, enlace y referencia del flujo de confirmación: el duplicado del curso conserva una referencia anterior. Un enlace de reunión no tiene vigencia ilimitada por definición; comprobar el proveedor cuando importe.

## 4. Reserva por enlace

Preparar un botón/enlace del calendario correcto. El enlace facilita que el cliente complete el formulario, pero no significa que ya reservó. Tras la creación, comprobar evento/callback real, ID, fecha y sincronización antes de actualizar CRM o enviar confirmación adicional.

Conservar un responsable de cada efecto. Si el calendario ya envía confirmación y añade CRM, no repetir ambas operaciones en un flujo de chat. Revisar identidad: el visitante puede usar datos diferentes al contacto original; correlacionar con un mecanismo admitido, no con suposiciones.

## 5. Reserva conversacional completa

1. Recoger servicio, duración, nombre/contacto requerido y fecha/zona horaria.
2. Normalizar fecha inicial y calcular final según duración real. No comparar textos de duración ambiguos.
3. Mostrar el resumen y resolver correcciones antes de crear.
4. Ejecutar **Consultar disponibilidad** sobre el calendario adecuado.
5. Si no hay cupo, presentar alternativas verificadas o pedir otra fecha. No confirmar.
6. Si hay disponibilidad, ejecutar **Reservar cita** con datos completos. Cubrir conflicto entre consulta y creación.
7. En **Éxito** de creación, guardar ID de reserva y horario confirmado. Verificar el objeto en el calendario cuando el acceso lo permita.
8. Actualizar la oportunidad vinculada una sola vez.
9. Enviar confirmación con datos actuales, sin repetir el flujo automático del calendario.
10. En **Fallo**, conservar datos, explicar que no quedó confirmada y ofrecer el paso real siguiente.

La salida de disponibilidad no se conecta directamente a «tu cita está reservada». Una función de IA debe llamar este ejecutor; no guardar una etiqueta que simule una cita. La clase 9 completa creación; otras clases solo configuran el puente y no demuestran el final.

### Contrato de resultado propuesto

Este objeto es un contrato de diseño entre ejecutor y agente, **no el esquema oficial de una API Lucid**:

```json
{
  "estado": "creada",
  "reserva_id": "ID_DEVUELTO_POR_EL_CALENDARIO",
  "inicio": "FECHA_ISO_CONFIRMADA",
  "zona_horaria": "ZONA_VERIFICADA",
  "operacion_id": "CORRELACION_DE_ESTA_SOLICITUD"
}
```

Solo el estado creado y una referencia verificable permiten confirmar. `disponible`, `solicitada`, `pendiente` o `resultado_incierto` necesitan mensajes diferentes.

## 6. Cambios y cancelación

Identificar la reserva exacta, verificar autorización del solicitante y usar la acción o enlace soportado. Después, leer estado y sincronización antes de decir cancelada. No cancelar por coincidencia de nombre cuando hay varias reservas.

La clase 12 envía una respuesta por chat después de que el instructor cancela desde la página; no demuestra cancelación automática. Eliminar y cancelar no produjeron necesariamente el mismo comportamiento en el curso. Revisar si se ejecutan notificaciones, liberación de cupo y flujo de cancelación para cada operación.

Para reprogramar, usar la función admitida o una secuencia explícita que no deje dos citas. Si se requiere crear una nueva y cancelar la anterior, tratar los fallos parciales; no borrar primero la cita vigente sin un diseño seguro autorizado.

## 7. Atención humana real

Cuando el cliente pide asesor o una regla lo requiere:

1. Reconocer la petición sin prometer disponibilidad inmediata no comprobada.
2. Cambiar la conversación a humano; comprobar estado efectivo.
3. Detener secuencias y rutas de IA incompatibles. También comprobar el estado humano antes de una salida que ya estaba procesándose.
4. Asignar equipo/asesor según disponibilidad y reglas reales.
5. Guardar un resumen útil: motivo, datos confirmados, operación/IDs, incertidumbre y próximo paso.
6. Notificar al responsable por un canal interno autorizado si está configurado.
7. Verificar asignación y aviso por separado. Asignado no implica aceptado ni leído.

El curso utiliza reparto Round Robin entre administradores/equipos. Revisar disponibilidad, horario, ausencia y reintento. Antes de reasignar, comprobar si ya hay dueño; un evento repetido no debe repartir de nuevo una conversación atendida.

Si no hay asesor disponible, usar cola/responsable alternativo y comunicar horario real. No devolver automáticamente al bot por un fallo de notificación si el cliente pidió humano.

## 8. Avisos al asesor

Un mensaje de comprador y un aviso interno no son el mismo destino. Utilizar directorio profesional autorizado con coincidencia exacta de asesor/ID; no pedir al modelo que adivine un teléfono.

El curso usa una solicitud a `/contacts` con acciones de campos y `send_flow` para un aviso. Antes de adaptarla, revisar el contrato vigente y canal. La demostración verifica aviso en Inbox, no entrega ni lectura WhatsApp.

Copiar varios pedidos a campos mutables del contacto del asesor puede mezclar datos si llegan a la vez. Preferir payload por evento con correlación, o serialización comprobada. Enviar solo información necesaria; no volcar el historial completo ni credenciales.

## 9. Regreso al bot

El evento **Conversación transferida al bot** es distinto de **Chat en vivo habilitado**. Definir quién puede devolver, en qué situación y con qué contexto.

1. Leer cambios hechos por el asesor en campos y objetos reales.
2. Reconstruir contexto mínimo actualizado.
3. Reanudar solo las rutas previstas y no una secuencia antigua ya terminada.
4. Probar que una fecha/precio corregidos prevalecen sobre memoria anterior.

## 10. Pruebas obligadas por la función

Reservas: libre, ocupado, dato ausente, corrección, conflicto después de consultar, doble clic/entrada, timeout, cambio, cancelación real y zona horaria.

CRM: primera solicitud, misma solicitud repetida, dos distintas del mismo contacto, mover sin tarjeta, varias oportunidades y fallo parcial.

Humano: petición directa, fuera de horario, asesor ausente, entrada durante transferencia, generación IA en curso, regreso al bot y negativa de contacto. La matriz con evidencia está en [pruebas y diagnóstico](test-cases.md).
