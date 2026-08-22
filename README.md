# Converti — base limpia para continuar el proyecto

Este repositorio contiene **solo los archivos de producción necesarios** de Converti. Se preparó como punto de partida limpio para borrar el repositorio anterior y continuar el desarrollo sin arrastrar ZIPs, versiones V1/V2/V3..., pruebas, capturas, `__pycache__`, temporales ni instaladores antiguos.

## Estado actual

Converti es una aplicación Flask con dos módulos principales:

1. **Conversión de archivos**: imágenes, audio/video, PDF, documentos y datos estructurados según los motores realmente instalados.
2. **Creador de CV**: editor en vivo, 5 plantillas, IA con Gemini, importación PDF/DOCX/CompuTrabajo, generación de correo de postulación y descarga PDF/Word editable.

Idiomas actuales: ES, EN, FR y PT-BR.

Rutas principales:

- `/` — Converti ES
- `/en/`, `/fr/`, `/pt-br/`
- `/convertir` — conversor principal
- `/formatos` — formatos disponibles
- `/ayuda` — ayuda de uso
- `/crear-cv`
- `/en/create-cv`
- `/fr/creer-cv`
- `/pt-br/criar-cv`
- `/privacidad` y versiones localizadas
- páginas SEO dinámicas mediante `tool_page.html`
- `/sitemap.xml`
- `/robots.txt`

## Arquitectura de producción actual

```text
converti.lat
   ↓
Cloudflare
   ↓
Cloudflare Tunnel
   ↓
Redmi / Termux
   ↓
Flask app.py en localhost:5000
```

Render **no forma parte del tráfico actual**.

El archivo principal siempre debe seguir siendo `app.py`.

## Estructura limpia

```text
app.py                     Backend Flask y rutas
capabilities.py            Detección de formatos/motores disponibles
config.py                  Límites y rutas de temporales
converters.py              Motores de conversión
cv_exports.py              Exportación profesional de CV a PDF/DOCX
security_utils.py          Seguridad, MIME, herramientas y rate-limit general
requirements.txt           Dependencias Python
.env.example               Variables de entorno de ejemplo, sin secretos
.gitignore                 Excluye temporales, secretos y basura local

templates/
  index.html
  index_en.html
  index_fr.html
  index_ptbr.html
  create_cv.html
  privacy.html
  privacy_en.html
  privacy_fr.html
  privacy_ptbr.html
  tool_page.html

static/
  css/create_cv.css
  css/site_ui.css
  js/create_cv.js
  images/logo_converti.png
  images/icon1.png
```

## Variables de entorno

Nunca colocar la API key dentro del código o GitHub.

```bash
export GEMINI_API_KEY="TU_KEY"
export GEMINI_MODEL="gemini-3.5-flash-lite"
```

El modelo puede cambiar mediante `GEMINI_MODEL` sin editar el código.

## Motores externos usados en el Redmi

El servidor actual fue preparado para usar:

- FFmpeg / FFprobe
- Pandoc
- ImageMagick
- Tesseract
- MuPDF CLI (`mutool`)
- LibreOffice mediante bridge Termux → Debian/proot

El código detecta los motores disponibles en tiempo real.

## Privacidad y comportamiento del CV

- El CV **no se persiste en localStorage**.
- La IA se ejecuta únicamente cuando el usuario pulsa una acción de mejora/generación.
- No existe un sistema visible de monedas, tokens ni créditos para la IA.
- La clave de Gemini vive únicamente en el servidor.
- Los temporales de conversiones se guardan en `archivos/`, carpeta que se crea automáticamente y está ignorada por Git.
- El original y los resultados temporales siguen la política de limpieza configurada en `config.py`.

## Exportación CV

- PDF: generado con ReportLab.
- Word: generado con `python-docx`, editable y con formato profesional.
- La plantilla **Moderno** tiene una composición Word a dos columnas con barra lateral.
- Las otras plantillas generan actualmente una versión Word limpia/editable de una columna; no son una réplica píxel a píxel del HTML. Si se desea equivalencia exacta entre las 5 plantillas en Word, esa es una mejora futura, no un archivo faltante.

## Estado visual más reciente

- Header unificado con logo oficial y favicon oficial.
- Navegación: Convertir / Formatos / Ayuda / Crear CV.
- Selector de plantillas y colores en el CV.
- El control de exportación aparece solo cuando el CV tiene contenido y está integrado de forma compacta junto a los controles superiores.
- Tipografía principal: Plus Jakarta Sans.
- El módulo CV usa `create_cv.css` y `create_cv.js`; no deben volver a añadirse archivos `create_cv_v2`, `v3`, `v4`, etc.
- `site_ui.css` es el único CSS compartido de navegación/marca.

## Reglas para el próximo ChatGPT/desarrollador

1. **Leer todos los archivos de este repositorio antes de modificarlo.**
2. No reconstruir el proyecto desde ZIPs anteriores.
3. No volver a crear archivos versionados duplicados (`*_v8.css`, `*_v9.js`, etc.). Editar los archivos estables existentes.
4. Mantener `app.py` como archivo principal.
5. Aplicar los cambios globales a ES/EN/FR/PT-BR y a páginas principales, privacidad, herramientas y CV.
6. No cambiar logo, favicon, tipografía o paleta base salvo petición explícita.
7. No guardar contenido del CV en almacenamiento persistente del navegador.
8. No incorporar claves privadas al repositorio.
9. Antes de entregar cambios: compilar Python, validar JS/Jinja y revisar visualmente `/`, `/convertir`, `/formatos`, `/ayuda`, `/crear-cv` y `/privacidad`.
10. Entregar archivos/ZIP listos; evitar hacer que el usuario copie archivos grandes manualmente.

## Instalación limpia en Redmi/Termux

Después de reemplazar el repositorio por esta base:

```bash
cd ~/converti
python -m pip install -r requirements.txt
source ~/.bashrc
python app.py
```

La web debe responder localmente en:

```text
http://127.0.0.1:5000
```

El Cloudflare Tunnel es un servicio externo al repositorio y seguirá apuntando a `localhost:5000`.

## Importante al limpiar GitHub

Subir únicamente el contenido de esta carpeta. No subir:

- ZIPs históricos
- capturas PNG/JPG de pruebas
- archivos DOCX/PDF de QA
- `__pycache__`
- `.pytest_cache`
- carpeta `archivos/`
- `.env`
- scripts `FIX_*`, `ACTUALIZAR_*` o instaladores de versiones anteriores
- demos y HTML de QA


## Auditoría aplicada el 21/08/2026

Esta base incorpora correcciones de producción realizadas sobre el handoff limpio:

- navegación principal mediante rutas reales, sin anchors `#convertir`, `#formatos` ni `#ayuda`;
- páginas localizadas reales para Formatos y Ayuda, incluidas en sitemap;
- `hreflang` corregido y metadescripciones localizadas en las portadas;
- exportación CV con validación estructural de DOCX/PDF antes de entregar el archivo;
- texto de usuario escapado antes de pasar por el motor de marcado de ReportLab;
- importación DOCX/PDF con comprobación de firma/estructura y rechazo de macros en Word;
- parser defensivo para respuestas JSON de IA, incluso si Gemini envía fences Markdown accidentales;
- limpieza temporal oportunista también bajo Gunicorn, no solo ejecutando `python app.py`;
- cabeceras HTTP de seguridad y API sin caché;
- `debug` desactivado por defecto en producción;
- flujo móvil de Converti CV con pestañas Editar / Vista previa y campos táctiles adaptados;
- pruebas estáticas en `tests/test_static_quality.py`.

Ejecutar pruebas estáticas:

```bash
python -m unittest tests/test_static_quality.py -v
```

## Ajuste 2026-08-22 — Exportación Word/PDF y selector de formato
- El DOCX moderno usa anchos de tabla A4 fijos compatibles con Word/LibreOffice para evitar compresión horizontal.
- Se mejoró la legibilidad del DOCX y la paginación: encabezados permanecen con el contenido asociado y descripciones largas pueden continuar en la página siguiente sin perder datos.
- La exportación PDF conserva su flujo multipágina; los bloques excepcionalmente largos pueden dividirse de forma segura para evitar recortes.
- El selector de formato reserva espacio suficiente para mostrar completos `PDF` y `Word` en escritorio y móvil. La regla es común a ES/EN/FR/PT-BR.

## SEO update 2026-08-22

- Se mantienen las 15 landing pages SEO de conversión por idioma.
- Se añadieron 5 nuevas intenciones SEO de Converti CV por idioma (20 páginas nuevas): creador de CV con IA, mejora de CV con IA, optimización de CV de CompuTrabajo, CV para ATS y conversión de CV de CompuTrabajo a Word/PDF.
- `sitemap.xml` incluye ahora las páginas indexables y `lastmod` de esta versión.
- Las páginas de privacidad se mantienen accesibles pero usan `noindex,follow` y se retiraron del sitemap para evitar indexación de páginas sin intención de búsqueda.
- Se reforzaron canonical, hreflang, robots, Open Graph y datos estructurados WebApplication/BreadcrumbList en Converti CV.
- El editor `/crear-cv` enlaza internamente las nuevas landing pages para facilitar descubrimiento y rastreo.
- `robots.txt` permite el sitio público y excluye `/api/` y `/download/` del rastreo.


## Corrección 2026-08-22 — landings SEO de CV
- Se reconstruyó `templates/cv_seo_page.html` con estilos autocontenidos y responsive para evitar conflictos/caché con CSS global.
- Se verificó el layout en escritorio 1648 px y móvil 390 px sin bloques vacíos ni desbordes.
- Se conserva navegación, selector de idioma, canonical, hreflang, schema y enlaces internos.


## SEO reforzado 2026-08-22
La home posiciona conversión de archivos + creación de CV profesional con IA gratis. `/convertir` mantiene intención propia de conversión, `/crear-cv` y `/cv/*` concentran las funciones de currículum, y el sitemap incluye hreflang para ES/EN/FR/PT-BR. Consulte `SEO_AUDIT_2026-08-22.md`.
