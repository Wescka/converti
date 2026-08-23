# PT-BR routing fix — 2026-08-23

Corregido sin cambiar la lógica del convertidor, CV, Gemini, Cloudflare ni el diseño responsive.

## Problema
Algunos enlaces internos PT-BR apuntaban a `/pt-br/convertir/<slug>` mientras la ruta canónica real era `/pt-br/converter/<slug>`, generando 404 observados en producción.

## Corrección
- Todos los enlaces PT-BR internos usan `/pt-br/converter/<slug>`.
- Se mantienen URLs canónicas del sitemap bajo `/pt-br/converter/`.
- Se agregan redirecciones 301 de compatibilidad:
  - `/pt-br/convertir` -> `/pt-br/converter`
  - `/pt-br/convert` -> `/pt-br/converter`
  - `/pt-br/convertir/<slug>` -> `/pt-br/converter/<slug>`
  - `/pt-br/convert/<slug>` -> `/pt-br/converter/<slug>`
- Slugs desconocidos siguen devolviendo 404.

## Verificación
- 15 slugs idénticos en ES/EN/FR/PT-BR = 60 landings canónicas coherentes.
- 33 pruebas automáticas OK.
- No quedan enlaces internos PT-BR con prefijo incorrecto.
- Python compila correctamente.
