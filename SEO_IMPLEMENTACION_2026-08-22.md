# Converti — implementación SEO y robustez IA (2026-08-22)

## Objetivo
Mantener Converti rápido, gratuito y centrado en la herramienta, pero dar a cada URL de conversión suficiente contexto útil para responder dudas reales de usuarios y buscadores.

## Cambios SEO
- 15 conversiones × 4 idiomas enriquecidas: 60 landing pages con contenido específico.
- Secciones condicionales: casos de uso, compatibilidad, resultado esperado, problemas frecuentes, privacidad, FAQ y enlaces internos relacionados.
- La herramienta/CTA permanece antes del contenido editorial.
- Diseño responsive existente preservado; las nuevas rejillas pasan a una columna a <=700 px.
- JSON-LD actualizado a `WebApplication` + `BreadcrumbList`.
- Se eliminó `FAQPage` de JSON-LD. Las FAQ visibles permanecen como contenido útil.
- Enlazado relacionado validado contra los slugs reales del proyecto.

## Cambios IA
- `temperature=0.2` y un máximo de 2 intentos para errores temporales/timeout/respuestas inválidas.
- Preservación local de nombre, email, teléfono, ciudad y web.
- Empresa, cargo y periodo laboral no pueden ser reescritos por acciones de mejora.
- Titulación, centro educativo y periodo no pueden ser reescritos por acciones de mejora.
- Idiomas y certificaciones se conservan exactamente en mejoras de un CV existente.
- Si una reescritura añade cifras que no estaban en el CV original, se descarta esa reescritura factual.
- En importaciones PDF/DOCX, una respuesta que introduzca cifras nuevas respecto al texto extraído se rechaza.
- El correo de postulación también usa temperatura baja, validación de salida y reintento acotado.

## Validación realizada
- 23 pruebas automáticas del proyecto: OK.
- 60 combinaciones landing/idioma renderizadas con Jinja `StrictUndefined`: 0 errores.
- 60 páginas comprobadas con contenido rico y enlaces relacionados válidos: 0 errores.
- Prueba aislada del guard de IA: datos inventados de empresa/cargo/fecha/métrica fueron revertidos; importación con cifra inventada fue rechazada.
- Sintaxis Python de `app.py` y `seo_content.py`: OK.
