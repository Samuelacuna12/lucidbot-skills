# Pruebas y entrega

Cada fila empieza **pendiente**. Guardar por ejecución: entrada, resultado esperado, respuesta real, campos pertinentes, referencia del objeto comprobado, fecha/canal y resultado. Conservar los identificadores y datos personales en el registro privado del proyecto, nunca en el repositorio público.

| Caso | Comprobación que decide el resultado |
|---|---|
| Saludo nuevo y contacto existente | Una sola entrada al vendedor; contexto conservado cuando corresponde |
| Producto por nombre y cambio a otro | Catálogo/reglas/medios del producto nuevo; no arrastre de selección antigua |
| Algodón frente a licra; talla/color/referencia | Coincide la identidad estructurada; no deducción solo visual |
| Pack permitido y cantidad no ofrecida | Total y composición exactos; no venta individual si solo se ofrecen packs |
| Precio no divisible entre componentes | Total persistido y total del pedido coinciden; discrepancia registrada, sin redondeo supuesto |
| Upsell rechazado/aceptado | Rechazo no agrega línea; aceptación suma oferta/cantidad correctas |
| Agotado, desconocido y disponibilidad manual | Tres respuestas distintas; no presentar dato asumido como inventario en tiempo real |
| Imagen conocida y ambigua | Foto correcta; aclaración antes de asignar referencia incierta |
| Varios mensajes seguidos, pregunta y corrección | Agrupación no pierde cambio, no duplica salida, conserva datos confirmados |
| Dato de entrega incompleto | Pide solo faltante; no crea operación incompleta ni confirma envío |
| Pedido creado en landing | ID de origen correlacionado, flujo correcto, mensaje observado en destino |
| Mismo evento dos veces | No duplica pedido ni acciones comerciales; comprobar protección real |
| Timeout después de crear pedido | Consulta antes de reintentar; no trata incertidumbre como fallo definitivo |
| Comprobante de prueba recibido | Permanece pendiente hasta validación efectiva; no marca pagado por imagen |
| Petición de garantía | Caso ligado a pedido/producto y responsable; política real, sin aprobación inventada |
| Humano, baja y retorno al bot | Cambia atención/asignación, detiene rutas incompatibles, retoma datos actuales |
| Notificación interna | Llega al responsable correcto; cliente no recibe información interna |
| Error de IA/integración | Salida controlada; error no se interpreta como producto inexistente o stock cero |

## Ejemplo normal — diseñado, no ejecutado en Lucid

Una tienda ficticia vende una oferta de seis prendas de algodón por EUR 42.00. El cliente elige tres negras M y tres azules L dentro de esa oferta. La suma es seis; ambas variantes comparten material y diseño permitidos. Declina las medias. El resumen conserva producto, composición, total y entrega. Después de confirmación, se verifica una sola orden y se informa su estado real. El validador local incluye un ejemplo equivalente, pero no envía mensajes ni crea la orden.

## Ejemplo de error — reproducido localmente

Una oferta declara seis artículos a EUR 10.00 total y precio unitario EUR 1.67. El cálculo da EUR 10.02. El validador devuelve `pack_total_mismatch`; no lo corrige ni aprueba automáticamente. Para la cuenta real, revisar semántica y precisión del campo, corregir la configuración permitida y volver a probar el total del pedido. No modificar el precio autorizado solo para que la división cuadre.

## Formato de cierre

```text
Alcance y cuenta destino: registro privado
Plantilla y versión observadas:
Catálogo: diseñado / configurado / probado
Fuente de disponibilidad: verificada / desconocida / política manual explícita
Canal: no conectado / conectado / recepción y envío comprobados
Puente de pedidos: diseñado / configurado / probado
IA, humano, CRM y avisos: estado y evidencia por función
Casos ejecutados y fallidos:
Activación y alcance efectivo:
Pendiente concreto y siguiente acción:
```

No agrupar todo como «listo» si solo se guardaron los flujos. No enviar una compra de prueba a logística real ni marcar un pedido real pagado sin pago verificado para provocar un evento. Usar un entorno o pedido de prueba separado dentro de la autorización disponible.
