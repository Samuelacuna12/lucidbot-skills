# Integraciones, APIs, Sheets y aplicaciones web

Base: clases 9 y 15–19. Las recetas históricas requieren cotejo con el contrato vigente antes de ejecutar. No se incluyen credenciales ni recursos de participantes.

## 1. Leer el contrato antes de construir

Para cada integración documentar: proveedor/cuenta, finalidad, método, URL, autenticación, parámetros, cuerpo, respuesta, códigos de error, límites, efecto y forma de consultar el resultado.

- GET suele consultar; POST puede crear o ejecutar; PUT/PATCH/DELETE dependen del contrato. No deducir efectos por nombre solamente.
- Revisar tipo de contenido: un 404 puede devolver HTML, no JSON.
- Un 2xx puede contener error de negocio o no haber actualizado el dato esperado.
- Variables `{{campo}}` de Lucid no se sustituyen por sí solas en Swagger o Postman.
- Usar datos propios de prueba. No compartir colecciones con tokens incrustados.

Swagger sirve para conocer el contrato; un ejemplo en una landing comercial no prevalece sobre él. Si la documentación no define un comportamiento, registrar la incertidumbre antes de inventar parámetros, estados o autenticación.

## 2. Solicitud externa en un flujo

1. Crear campos de entrada con tipos correctos y resultado/error separados.
2. Validar datos antes de llamar: monto, código, identidad, URL o ID según la función.
3. Configurar método, URL, cabeceras y cuerpo exactamente según contrato.
4. Insertar variables mediante serialización correcta; escapar comillas y saltos de línea en JSON.
5. Probar con un fixture propio. Una prueba sin contexto de contacto puede dejar variables sin resolver.
6. Mapear JSONPath: `$` raíz, `$.campo`, `$.lista[0]`. Comprobar raíz objeto/array y ausencia.
7. Conectar Éxito/Fallo. Evaluar éxito de negocio además del HTTP.
8. Guardar ID/correlación y leer el resultado real antes de confirmar.
9. Limpiar o aislar salidas por operación para que un fallo no use un valor anterior.

Usar logs mínimos y sanitizados: método, operación, ID seguro, estado, tiempo, error resumido. El cuerpo completo puede contener datos privados o claves; no convertirlo en una nota visible al cliente.

## 3. Contactos y acciones Lucid

El curso consulta la cuenta y usa `POST /contacts` con `X-ACCESS-TOKEN`. Confirmar la documentación actual de la cuenta antes de ejecutar. La prueba histórica muestra que repetir un teléfono puede devolver éxito sin crear otro contacto; cambiar `email` en raíz no actualiza necesariamente el correo existente. Una acción `set_field_value` y lectura posterior sí demuestran el cambio.

Esto enseña a comprobar el efecto, no a asumir una garantía universal de idempotencia. Separar creación, actualización de campos y ejecución de `send_flow`. No usar nombres/IDs de una cuenta en otra.

## 4. Errores y reintentos

| Situación | Tratamiento |
|---|---|
| 401/403 | Comprobar mecanismo, cuenta, permisos y vigencia sin imprimir secretos |
| 404 | Verificar recurso, ruta y respuesta; no asumir únicamente URL mal escrita |
| 429 | Respetar límite y `Retry-After` cuando exista; no cambiar cuentas para eludirlo |
| 5xx | Leer contexto; puede relacionarse con configuración/entrada además del proveedor |
| Timeout tras escritura | Estado incierto: consultar por ID/correlación antes de repetir |
| 2xx sin resultado esperado | No confirmar; revisar estado de negocio y mapeo |
| JSONPath vacío | Comprobar estructura actual y dato realmente devuelto |

Reintentos acotados y separados para lectura/escritura. Una acción de pago, reserva o llamada necesita especial cuidado por efectos repetidos. No establecer bucles indefinidos de generación IA para reparar un fallo externo.

## 5. Google Sheets

1. Conectar cuenta autorizada al documento necesario, con acceso mínimo suficiente.
2. Elegir pestaña y encabezados estables; anotar nombres exactos y tipos.
3. Definir ID de fila/operación independiente del nombre de persona.
4. Mapear campos del contacto a columnas previstas.
5. Insertar o actualizar según la intención real y verificar la fila resultante.
6. Al consultar, tratar cero, una o varias coincidencias. «Primera fila encontrada» no garantiza la correcta.
7. Actualizar solo columnas previstas; conservar otras.
8. Ante escritura incierta, buscar correlación antes de insertar otra fila.

Compartir «cualquiera con el enlace puede editar» no es requisito general adoptado del curso. La conexión debe tener acceso sin publicar la base de clientes. Guardar una fila no envía WhatsApp ni crea una reserva.

Para galerías, una URL debe servir la imagen correspondiente, no una página contenedora. Verificar datos y enlaces antes de generar tarjetas; un formateador no puede inventar precio o existencia.

## 6. MCP y catálogo para un bot propio

Patrón docente de dos agentes:

1. Agente conversacional recoge búsqueda y guarda una consulta estructurada.
2. Herramienta llama un flujo consultor.
3. Consultor sin memoria innecesaria usa solo herramientas de búsqueda autorizadas.
4. El flujo valida respuesta y devuelve datos al conversacional.
5. Conversacional presenta productos/servicios y pide aclaración si hay varias coincidencias.

La documentación primaria de [Storefront MCP](https://shopify.dev/docs/apps/build/storefront-mcp) describe la migración de catálogo/carrito a `/api/ucp/mcp` y requisitos del perfil de agente. La receta `/api/mcp` de una grabación es histórica; verificar compatibilidad del cliente Lucid antes de conectar. No es configuración de Ecommerce V3.

Confirmar dominio y cuenta: en el curso un servidor equivocado devuelve productos de otra tienda. Limitar herramientas a la función necesaria. El permiso de búsqueda no da acceso administrativo ni autoriza checkout/cobro. Comprobar moneda y unidades; dividir precios entre 100 solo si lo establece el contrato concreto.

Distinguir `sin_resultados`, `fallo_consulta` y `datos_incompletos`. La demostración consigue tarjetas con imágenes y enlaces; no demuestra pedido creado, pago ni stock sincronizado.

## 7. Conversión monetaria como ejemplo de API

Guardar monto y monedas → validar códigos → usar endpoint de conversión que acepte monto → mapear resultado → continuar por Éxito → presentar valor con moneda y vigencia. Un endpoint de tasas no devuelve necesariamente `conversion_result`.

La cifra mostrada en la clase es histórica; no reutilizarla como tasa actual. Redondear para presentación sin perder precisión operativa. Una conversión no crea un pago. La clase lee documentación de pagos, pero no implementa una integración de cobro.

## 8. Apps Script: estructura y despliegue

La clase 19 construye un formulario que guarda una fila y crea contacto Lucid. No demuestra envío WhatsApp. Una adaptación razonada conserva estos pasos:

1. Abrir el documento autorizado y **Extensiones → Apps Script**.
2. Separar lógica de servidor (`Code.gs`) e interfaz (`Index.html`, o nombre elegido exacto).
3. Definir validaciones, columnas, fuente de configuración y respuesta al usuario.
4. Guardar secretos en un mecanismo de servidor restringido, por ejemplo Script Properties cuando sea apropiado; no en HTML ni una hoja pública.
5. Revisar permisos del código propio y la cuenta que ejecuta. No saltar advertencias o crear proyectos para evadir una denegación.
6. Desplegar como aplicación web con acceso acorde al propósito. Ejecutar como propietario usa su autoridad; validar en servidor lo que cada visitante puede hacer.
7. Probar formulario → servidor → fila → llamada externa → resultado real, con fallo parcial y doble envío.
8. Para actualizar sin cambiar URL, editar la implementación existente y seleccionar nueva versión. Guardar código no publica la versión.

La [guía oficial de webapps](https://developers.google.com/apps-script/guides/web) documenta `doGet(e)`/`doPost(e)` y parámetros. Un ID en la URL identifica, pero no autentica. `/dev` corresponde a pruebas de editores; comprobar la URL publicada `/exec` y acceso del destinatario.

No borrar hojas de configuración en producción para renovar esquema: migrar con copia/validación. La clase muestra duplicación de filas al reenviar; no demuestra idempotencia. Diseñar una clave de envío y comprobar protección real.

Las [cuotas oficiales de Apps Script](https://developers.google.com/apps-script/guides/services/quotas) dependen de cuenta/operación. El dato histórico de 90 minutos corresponde a runtime de activadores, no una bolsa general de todas las webapps. Verificar límites vigentes al dimensionar; no afirmar que se reinician a medianoche.

## 9. Páginas con retorno al bot

Una página puede recibir una selección y devolverla al bot, pero requiere identidad y autorización reales:

1. Generar contexto mínimo del trámite; no poner datos privados innecesarios en URL.
2. Usar backend que valide un token opaco, limitado y con vencimiento cuando corresponda.
3. Comprobar identidad, campo permitido y operación antes de escribir.
4. Enviar datos a Lucid desde servidor; nunca exponer la clave en JavaScript del navegador.
5. Registrar correlación y resultado; controlar repetición en servidor.
6. Devolver estado claro al visitante y, si se necesita, activar un flujo explícito verificado.

`user_id` no es universalmente teléfono. `localStorage` puede borrarse y no garantiza un intento por persona. El navegador no siempre permite `window.close()` ni devolver al WhatsApp de origen.

La ruleta de la clase expone clave en frontend y muestra premios aparentemente aleatorios con un resultado fijo; no reproducir esas prácticas. Una promoción fija debe presentarse como fija, o una aleatoria tener probabilidades y reglas reales. Guardar un campo «premio» no crea un cupón externo.

Un QR que apunta a la misma URL puede conservar destino tras actualizar una implementación, pero debe probarse desde un móvil. Un preview con referencia de borrador no demuestra publicación pública. Páginas del bot y conexión de compra con una plantilla ecommerce son proyectos diferentes.

## 10. Resultado de una integración completa

Entregar contrato usado, campos/IDs, acciones, éxito/fallo, evidencia de lectura posterior, permisos mínimos y pendientes. Diferenciar acceso conectado, solicitud aceptada, objeto creado, notificación enviada y efecto recibido. Si falta un endpoint/documento, decir cuál; no inventar que una integración queda activa por tener el código.
