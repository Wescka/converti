"""Contenido SEO útil y específico para las páginas de conversión de Converti.

La capa mantiene el motor de conversión separado del contenido editorial. Solo
expone datos de presentación; no altera capacidades ni rutas.
"""
from __future__ import annotations

from copy import deepcopy

PRIORITY_SLUGS = {
    "pdf-a-word", "word-a-pdf", "jpg-a-pdf", "pdf-a-jpg", "pdf-a-png",
    "png-a-jpg", "jpg-a-png", "png-a-webp", "csv-a-xlsx", "xlsx-a-csv",
}

COMMON = {
    "es": {
        "use_cases_title": "Cuándo te sirve esta conversión",
        "compat_title": "Compatibilidad y qué puedes esperar",
        "issues_title": "Problemas frecuentes y cómo resolverlos",
        "privacy_title": "Privacidad y procesamiento",
        "privacy": [
            "No necesitas crear una cuenta para usar las herramientas públicas.",
            "Los archivos se procesan de forma temporal para realizar la conversión.",
            "Converti no publica ni indexa el contenido de los archivos que subes.",
        ],
        "expectation_prefix": "Resultado esperado:",
        "mobile_note": "También puedes hacerlo desde Android, iPhone o tablet usando el selector de archivos del navegador.",
        "fallback_faq": [
            ("¿La conversión es gratis?", "Sí. Las herramientas públicas de Converti están diseñadas para usarse gratis y sin registro."),
            ("¿Puedo convertir desde el celular?", "Sí. El flujo de selección, conversión y descarga está adaptado a pantallas táctiles."),
            ("¿Qué ocurre si el archivo está dañado o no corresponde a su extensión?", "Converti valida el tipo real del archivo cuando es posible y puede rechazar archivos corruptos, incompatibles o disfrazados con una extensión incorrecta."),
        ],
    },
    "en": {
        "use_cases_title": "When this conversion is useful",
        "compat_title": "Compatibility and what to expect",
        "issues_title": "Common problems and how to solve them",
        "privacy_title": "Privacy and processing",
        "privacy": [
            "You do not need an account to use Converti's public tools.",
            "Files are processed temporarily to perform the conversion.",
            "Converti does not publish or index the contents of uploaded files.",
        ],
        "expectation_prefix": "Expected result:",
        "mobile_note": "You can also convert on Android, iPhone or tablet using your browser's file picker.",
        "fallback_faq": [
            ("Is the conversion free?", "Yes. Converti's public tools are designed to work for free and without registration."),
            ("Can I convert on my phone?", "Yes. File selection, conversion and download controls are adapted to touch screens."),
            ("What if the file is damaged or has the wrong extension?", "Converti validates the real file type when possible and may reject corrupted, incompatible or disguised files."),
        ],
    },
    "fr": {
        "use_cases_title": "Quand cette conversion est utile",
        "compat_title": "Compatibilité et résultat attendu",
        "issues_title": "Problèmes fréquents et solutions",
        "privacy_title": "Confidentialité et traitement",
        "privacy": [
            "Aucun compte n'est nécessaire pour utiliser les outils publics de Converti.",
            "Les fichiers sont traités temporairement pour effectuer la conversion.",
            "Converti ne publie ni n'indexe le contenu des fichiers envoyés.",
        ],
        "expectation_prefix": "Résultat attendu :",
        "mobile_note": "La conversion fonctionne aussi sur Android, iPhone et tablette via le sélecteur de fichiers du navigateur.",
        "fallback_faq": [
            ("La conversion est-elle gratuite ?", "Oui. Les outils publics de Converti sont conçus pour être utilisés gratuitement et sans inscription."),
            ("Puis-je convertir depuis mon téléphone ?", "Oui. La sélection, la conversion et le téléchargement sont adaptés aux écrans tactiles."),
            ("Que se passe-t-il si le fichier est endommagé ou porte une mauvaise extension ?", "Converti vérifie le type réel du fichier lorsque c'est possible et peut refuser les fichiers corrompus, incompatibles ou déguisés."),
        ],
    },
    "pt-br": {
        "use_cases_title": "Quando essa conversão é útil",
        "compat_title": "Compatibilidade e o que esperar",
        "issues_title": "Problemas frequentes e como resolver",
        "privacy_title": "Privacidade e processamento",
        "privacy": [
            "Você não precisa criar uma conta para usar as ferramentas públicas do Converti.",
            "Os arquivos são processados temporariamente para realizar a conversão.",
            "O Converti não publica nem indexa o conteúdo dos arquivos enviados.",
        ],
        "expectation_prefix": "Resultado esperado:",
        "mobile_note": "Você também pode converter no Android, iPhone ou tablet usando o seletor de arquivos do navegador.",
        "fallback_faq": [
            ("A conversão é gratuita?", "Sim. As ferramentas públicas do Converti foram feitas para funcionar gratuitamente e sem cadastro."),
            ("Posso converter pelo celular?", "Sim. A seleção, conversão e download são adaptados para telas sensíveis ao toque."),
            ("O que acontece se o arquivo estiver corrompido ou com extensão errada?", "O Converti valida o tipo real do arquivo quando possível e pode rejeitar arquivos corrompidos, incompatíveis ou disfarçados."),
        ],
    },
}

# Los perfiles contienen hechos específicos que sí aportan utilidad. Los diez
# slugs prioritarios tienen contenido amplio; el resto recibe el contenido base
# existente más privacidad/FAQ común, sin crear texto artificial de relleno.
PROFILES = {
    "pdf-a-word": {
        "es": {
            "use_cases": ["Editar un contrato o carta cuyo original editable ya no tienes.", "Actualizar un CV, informe o propuesta recibida únicamente en PDF.", "Reutilizar texto de un documento en Word sin volver a escribirlo.", "Recuperar contenido de documentos con tablas o imágenes para seguir trabajando."],
            "compatibility": ["Los PDF con texto real suelen ofrecer mejores resultados que los documentos escaneados.", "Tablas, columnas, fuentes incrustadas y diseños muy gráficos pueden requerir pequeños ajustes posteriores.", "Un PDF escaneado necesita OCR para recuperar texto editable; si OCR no está disponible, Converti no fingirá que el resultado es editable."],
            "issues": [("El Word sale desordenado", "Suele ocurrir con PDF de varias columnas, formularios o elementos posicionados. Revisa el DOCX y ajusta esos bloques puntuales."), ("El PDF parece una foto", "Probablemente es un escaneo. Activa OCR cuando esté disponible para intentar reconocer el texto."), ("Faltan caracteres o una fuente cambia", "Algunas fuentes del PDF no existen como fuentes editables equivalentes. Word puede sustituirlas por una alternativa disponible.")],
            "expectation": "Converti intenta recuperar un DOCX editable y conservar la estructura útil. No promete una réplica perfecta cuando el PDF usa maquetación compleja o texto convertido en imagen.",
            "extra_faq": [("¿Se mantienen las tablas?", "Converti intenta conservarlas cuando el motor puede reconstruirlas, pero las tablas complejas o dibujadas como gráficos pueden necesitar corrección manual."), ("¿Puedo editar el archivo después?", "Sí. El objetivo del DOCX resultante es que puedas abrirlo y editarlo en Word o en una suite compatible."), ("¿Conviene PDF o Word para un CV?", "Usa el formato que pida el portal. Word facilita la edición; PDF suele conservar mejor la apariencia final.")],
        },
        "en": {
            "use_cases": ["Edit a contract or letter when the original editable file is no longer available.", "Update a resume, report or proposal that you only received as PDF.", "Reuse document text in Word instead of retyping it.", "Recover content from documents with tables or images for further editing."],
            "compatibility": ["Text-based PDFs usually convert better than scanned documents.", "Tables, columns, embedded fonts and highly visual layouts may need small manual adjustments.", "A scanned PDF needs OCR to recover editable text; if OCR is unavailable, Converti will not pretend the output is editable."],
            "issues": [("The Word file looks disorganized", "This is common with multi-column PDFs, forms or positioned objects. Review the DOCX and adjust those specific blocks."), ("The PDF looks like a photo", "It is probably a scan. Enable OCR when available to attempt text recognition."), ("Characters or fonts change", "Some PDF fonts do not have an editable equivalent. Word may substitute an available font.")],
            "expectation": "Converti aims to recover an editable DOCX while preserving useful structure. It does not promise a pixel-perfect replica for complex layouts or image-only text.",
            "extra_faq": [("Are tables preserved?", "Converti tries to preserve them when the conversion engine can reconstruct them, but complex or graphic tables may require manual correction."), ("Can I edit the result?", "Yes. The DOCX is intended to be opened and edited in Word or a compatible office suite."), ("Should I use PDF or Word for a resume?", "Use the format requested by the employer or portal. Word is easier to edit; PDF usually preserves final appearance better.")],
        },
        "fr": {
            "use_cases": ["Modifier un contrat ou une lettre lorsque le fichier éditable d'origine n'est plus disponible.", "Mettre à jour un CV, rapport ou devis reçu uniquement en PDF.", "Réutiliser du texte dans Word sans tout retaper.", "Récupérer le contenu de documents avec tableaux ou images pour continuer à travailler."],
            "compatibility": ["Les PDF contenant du vrai texte donnent généralement de meilleurs résultats que les documents numérisés.", "Les tableaux, colonnes, polices intégrées et mises en page très graphiques peuvent demander quelques ajustements.", "Un PDF numérisé nécessite l'OCR pour récupérer du texte modifiable ; sans OCR, Converti ne prétend pas fournir un texte éditable."],
            "issues": [("Le Word est désorganisé", "Cela arrive surtout avec les PDF multicolonnes, formulaires ou objets positionnés. Vérifiez le DOCX et ajustez les blocs concernés."), ("Le PDF ressemble à une photo", "Il s'agit probablement d'un scan. Activez l'OCR lorsqu'il est disponible."), ("Des caractères ou polices changent", "Certaines polices PDF n'ont pas d'équivalent éditable ; Word peut les remplacer.")],
            "expectation": "Converti cherche à produire un DOCX modifiable en conservant la structure utile, sans promettre une copie parfaite des mises en page complexes ou des textes sous forme d'image.",
            "extra_faq": [("Les tableaux sont-ils conservés ?", "Converti tente de les reconstruire lorsque le moteur le permet ; les tableaux complexes peuvent nécessiter une correction manuelle."), ("Puis-je modifier le résultat ?", "Oui. Le DOCX est destiné à être ouvert et modifié dans Word ou une suite compatible."), ("PDF ou Word pour un CV ?", "Utilisez le format demandé par le portail. Word est plus facile à modifier ; PDF conserve généralement mieux l'apparence finale.")],
        },
        "pt-br": {
            "use_cases": ["Editar um contrato ou carta quando o arquivo editável original não está mais disponível.", "Atualizar um currículo, relatório ou proposta recebida apenas em PDF.", "Reaproveitar texto em Word sem digitar tudo novamente.", "Recuperar conteúdo de documentos com tabelas ou imagens para continuar editando."],
            "compatibility": ["PDFs com texto real costumam converter melhor do que documentos digitalizados.", "Tabelas, colunas, fontes incorporadas e layouts muito gráficos podem exigir pequenos ajustes.", "Um PDF digitalizado precisa de OCR para recuperar texto editável; sem OCR, o Converti não fingirá que o resultado é editável."],
            "issues": [("O Word fica desorganizado", "Isso é comum em PDFs com várias colunas, formulários ou objetos posicionados. Revise o DOCX e ajuste esses blocos."), ("O PDF parece uma foto", "Provavelmente é uma digitalização. Ative OCR quando estiver disponível."), ("Caracteres ou fontes mudam", "Algumas fontes do PDF não têm equivalente editável e o Word pode substituí-las.")],
            "expectation": "O Converti tenta recuperar um DOCX editável preservando a estrutura útil, sem prometer uma réplica perfeita para layouts complexos ou texto em imagem.",
            "extra_faq": [("As tabelas são preservadas?", "O Converti tenta reconstruí-las quando o mecanismo permite; tabelas complexas podem exigir correção manual."), ("Posso editar o resultado?", "Sim. O DOCX foi feito para ser aberto e editado no Word ou em uma suíte compatível."), ("PDF ou Word para currículo?", "Use o formato solicitado pelo portal. Word é mais fácil de editar; PDF costuma preservar melhor a aparência final.")],
        },
    },
    "word-a-pdf": {
        "es": {"use_cases":["Enviar un CV o informe con una apariencia más estable.","Preparar contratos, cartas o propuestas para imprimir o compartir.","Evitar que otra persona modifique accidentalmente el documento original.","Crear una copia fácil de abrir desde casi cualquier dispositivo."],"compatibility":["DOCX con estilos estándar, imágenes, tablas, encabezados y pies suelen conservarse bien.","Fuentes que no estén instaladas en el servidor pueden sustituirse por otras y cambiar ligeramente el salto de línea.","Documentos con macros, objetos OLE o elementos muy específicos de Word pueden no reproducirse igual."],"issues":[("El PDF cambia de página","Suele deberse a fuentes sustituidas, márgenes extremos o objetos flotantes. Revisa el documento original y usa fuentes comunes."),("Una imagen se mueve","Los objetos flotantes o anclados pueden interpretarse de forma distinta por el motor de oficina."),("El documento tiene muchas páginas","La conversión puede tardar más; evita reenviar varias veces mientras el proceso sigue activo.")],"expectation":"El objetivo es conservar la presentación de Word en un PDF estable. Los documentos que dependen de funciones exclusivas de Microsoft Word pueden variar ligeramente.","extra_faq":[("¿Necesito Microsoft Word?","No en tu dispositivo. Converti usa el motor disponible en el servidor."),("¿Se conservan enlaces?","Los enlaces normales pueden conservarse, aunque depende de cómo estén construidos en el DOCX."),("¿El PDF resultante se puede imprimir?","Sí. El PDF está pensado para compartirse, archivarse o imprimirse.")]},
        "en": {"use_cases":["Share a resume or report with a more stable appearance.","Prepare contracts, letters or proposals for printing and sharing.","Reduce accidental editing of the original document.","Create a copy that opens easily on most devices."],"compatibility":["DOCX files with standard styles, images, tables, headers and footers usually convert well.","Fonts missing on the server may be substituted and slightly change line wrapping.","Macros, OLE objects and Word-specific features may not reproduce exactly."],"issues":[("Page breaks change","This is usually caused by font substitution, extreme margins or floating objects. Use common fonts and review the source."),("An image moves","Floating or anchored objects can be interpreted differently by the office engine."),("The document has many pages","Conversion may take longer; avoid submitting the same job repeatedly while it is still running.")],"expectation":"The goal is to preserve Word's presentation in a stable PDF. Documents that depend on Microsoft Word-only features can vary slightly.","extra_faq":[("Do I need Microsoft Word?","Not on your device. Converti uses the office engine available on the server."),("Are hyperlinks preserved?","Standard links can be preserved, depending on how they are stored in the DOCX."),("Can I print the result?","Yes. The PDF is intended for sharing, archiving and printing.")]},
        "fr": {"use_cases":["Partager un CV ou rapport avec une apparence plus stable.","Préparer contrats, lettres ou propositions pour impression et partage.","Réduire les modifications accidentelles du document d'origine.","Créer une copie facile à ouvrir sur presque tous les appareils."],"compatibility":["Les DOCX avec styles standards, images, tableaux, en-têtes et pieds de page se convertissent généralement bien.","Les polices absentes du serveur peuvent être remplacées et modifier légèrement les retours à la ligne.","Les macros, objets OLE et fonctions propres à Word peuvent différer."],"issues":[("Les sauts de page changent","Cela vient souvent d'une substitution de police, de marges extrêmes ou d'objets flottants."),("Une image se déplace","Les objets flottants ou ancrés peuvent être interprétés différemment par le moteur bureautique."),("Le document est très long","La conversion peut demander plus de temps ; évitez de relancer plusieurs fois le même travail.")],"expectation":"L'objectif est de conserver la présentation Word dans un PDF stable. Les fonctions exclusives à Microsoft Word peuvent varier légèrement.","extra_faq":[("Microsoft Word est-il nécessaire ?","Non sur votre appareil. Converti utilise le moteur bureautique disponible sur le serveur."),("Les liens sont-ils conservés ?","Les liens standards peuvent l'être selon leur structure dans le DOCX."),("Puis-je imprimer le résultat ?","Oui. Le PDF est adapté au partage, à l'archivage et à l'impression.")]},
        "pt-br": {"use_cases":["Enviar um currículo ou relatório com aparência mais estável.","Preparar contratos, cartas ou propostas para impressão e compartilhamento.","Evitar alterações acidentais no documento original.","Criar uma cópia fácil de abrir em praticamente qualquer dispositivo."],"compatibility":["DOCX com estilos padrão, imagens, tabelas, cabeçalhos e rodapés costumam converter bem.","Fontes ausentes no servidor podem ser substituídas e mudar um pouco as quebras de linha.","Macros, objetos OLE e recursos específicos do Word podem não ficar idênticos."],"issues":[("As quebras de página mudam","Isso costuma ocorrer por substituição de fonte, margens extremas ou objetos flutuantes."),("Uma imagem se move","Objetos flutuantes ou ancorados podem ser interpretados de forma diferente pelo mecanismo de escritório."),("O documento tem muitas páginas","A conversão pode demorar mais; evite reenviar o mesmo trabalho enquanto ele ainda está processando.")],"expectation":"O objetivo é preservar a apresentação do Word em um PDF estável. Recursos exclusivos do Microsoft Word podem variar levemente.","extra_faq":[("Preciso do Microsoft Word?","Não no seu dispositivo. O Converti usa o mecanismo disponível no servidor."),("Os links são preservados?","Links padrão podem ser mantidos, dependendo de como estão no DOCX."),("Posso imprimir o resultado?","Sim. O PDF é adequado para compartilhar, arquivar e imprimir.")]},
    },
    "jpg-a-pdf": {
        "es": {"use_cases":["Unir fotos de documentos tomadas con el celular.","Agrupar recibos, facturas o comprobantes en un solo archivo.","Preparar apuntes o páginas escaneadas para enviar por correo.","Crear un documento PDF con varias imágenes en el orden seleccionado."],"compatibility":["Puedes seleccionar una o varias imágenes compatibles.","Las fotografías verticales y horizontales se adaptan sin deformar su relación de aspecto.","La calidad final depende de la resolución original y de los ajustes elegidos."],"issues":[("La foto se ve borrosa","El PDF no puede recuperar detalle que no existe en la imagen original. Usa la fotografía de mayor resolución disponible."),("Las páginas están en otro orden","Selecciona los archivos en el orden deseado antes de convertirlos."),("El PDF pesa demasiado","Reducir la resolución o calidad de imágenes puede disminuir el tamaño, con la correspondiente pérdida de detalle.")],"expectation":"Cada imagen se coloca como una página del PDF sin inventar contenido ni reinterpretar el documento.","extra_faq":[("¿Puedo usar fotos del teléfono?","Sí. En móvil puedes elegir imágenes desde el selector del navegador."),("¿Puedo unir varias fotos?","Sí. La conversión múltiple permite reunir imágenes en un único PDF cuando la herramienta lo admite."),("¿Se estiran las imágenes?","No deberían deformarse; se mantienen sus proporciones dentro de la página.")]},
        "en": {"use_cases":["Combine phone photos of documents.","Group receipts, invoices or proofs into one file.","Prepare scanned notes or pages for email.","Create a multi-page PDF with images in the selected order."],"compatibility":["You can select one or multiple compatible images.","Portrait and landscape photos are fitted without distorting their aspect ratio.","Final quality depends on the source resolution and selected settings."],"issues":[("The photo looks blurry","A PDF cannot restore detail missing from the source image. Use the highest-resolution photo available."),("Pages are in the wrong order","Select files in the desired order before conversion."),("The PDF is too large","Lower image resolution or quality to reduce size, with the expected loss of detail.")],"expectation":"Each image is placed as a PDF page without inventing content or reinterpreting the document.","extra_faq":[("Can I use phone photos?","Yes. On mobile you can choose images from your browser's file picker."),("Can I combine several photos?","Yes, when multiple-image conversion is available, compatible images can be combined into one PDF."),("Are images stretched?","They should keep their proportions and fit within the page.")]},
        "fr": {"use_cases":["Réunir des photos de documents prises avec un téléphone.","Regrouper reçus, factures ou justificatifs dans un seul fichier.","Préparer des notes ou pages numérisées pour envoi par e-mail.","Créer un PDF multipage avec les images dans l'ordre choisi."],"compatibility":["Vous pouvez sélectionner une ou plusieurs images compatibles.","Les photos portrait et paysage sont adaptées sans déformer leurs proportions.","La qualité finale dépend de la résolution source et des réglages choisis."],"issues":[("La photo est floue","Un PDF ne peut pas recréer des détails absents de l'image source. Utilisez la photo de meilleure résolution."),("Les pages sont dans le mauvais ordre","Sélectionnez les fichiers dans l'ordre souhaité avant conversion."),("Le PDF est trop lourd","Réduisez la résolution ou la qualité pour diminuer la taille, avec une perte de détail correspondante.")],"expectation":"Chaque image devient une page PDF sans inventer ni réinterpréter son contenu.","extra_faq":[("Puis-je utiliser des photos du téléphone ?","Oui. Sur mobile, choisissez les images via le sélecteur du navigateur."),("Puis-je réunir plusieurs photos ?","Oui, lorsque la conversion multiple est disponible, plusieurs images compatibles peuvent former un seul PDF."),("Les images sont-elles étirées ?","Elles doivent conserver leurs proportions dans la page.")]},
        "pt-br": {"use_cases":["Juntar fotos de documentos tiradas pelo celular.","Agrupar recibos, notas ou comprovantes em um único arquivo.","Preparar anotações ou páginas digitalizadas para enviar por e-mail.","Criar um PDF com várias páginas na ordem selecionada."],"compatibility":["Você pode selecionar uma ou várias imagens compatíveis.","Fotos verticais e horizontais são ajustadas sem deformar a proporção.","A qualidade final depende da resolução original e das configurações escolhidas."],"issues":[("A foto fica borrada","O PDF não consegue recuperar detalhes que não existem na imagem original. Use a foto com maior resolução."),("As páginas ficam fora de ordem","Selecione os arquivos na ordem desejada antes de converter."),("O PDF fica muito grande","Reduza resolução ou qualidade para diminuir o tamanho, considerando a perda de detalhe.")],"expectation":"Cada imagem vira uma página do PDF sem inventar conteúdo nem reinterpretar o documento.","extra_faq":[("Posso usar fotos do celular?","Sim. No celular, escolha as imagens pelo seletor de arquivos do navegador."),("Posso juntar várias fotos?","Sim. Quando a conversão múltipla está disponível, imagens compatíveis podem ser reunidas em um PDF."),("As imagens são esticadas?","Elas devem manter a proporção e se ajustar à página.")]},
    },
}

# Perfiles compactos para las otras prioridades. Se construyen con datos
# específicos por formato para evitar páginas clonadas.
COMPACT = {
    "pdf-a-jpg": {
        "es": (["Compartir una página concreta de un PDF como imagen.","Insertar páginas de PDF en una presentación o documento.","Crear miniaturas o previsualizaciones de páginas."],["Cada página seleccionada se convierte en una imagen JPG independiente.","JPG usa compresión con pérdida; subir el DPI mejora detalle pero también aumenta el peso."],["Si el texto queda pequeño, aumenta el DPI antes de convertir.","En PDF con muchas páginas, limita el rango para reducir tiempo y tamaño."],"Convierte la apariencia de cada página a imagen; el texto deja de ser editable como texto."),
        "en": (["Share a specific PDF page as an image.","Insert PDF pages into a presentation or document.","Create page thumbnails or previews."],["Each selected page becomes an independent JPG image.","JPG uses lossy compression; higher DPI improves detail but increases file size."],["If text looks too small, increase DPI before conversion.","For long PDFs, limit the page range to reduce processing time and download size."],"The page appearance becomes an image, so text is no longer editable as text."),
        "fr": (["Partager une page précise d'un PDF comme image.","Insérer des pages PDF dans une présentation ou un document.","Créer des miniatures ou aperçus de pages."],["Chaque page sélectionnée devient une image JPG indépendante.","Le JPG utilise une compression avec perte ; un DPI plus élevé augmente le détail et le poids."],["Si le texte est trop petit, augmentez le DPI avant conversion.","Pour un long PDF, limitez la plage de pages afin de réduire le temps et la taille."],"L'apparence de la page devient une image ; le texte n'est donc plus éditable comme texte."),
        "pt-br": (["Compartilhar uma página específica do PDF como imagem.","Inserir páginas do PDF em apresentação ou documento.","Criar miniaturas ou prévias de páginas."],["Cada página selecionada vira uma imagem JPG independente.","JPG usa compressão com perda; DPI maior melhora o detalhe e aumenta o tamanho."],["Se o texto ficar pequeno, aumente o DPI antes da conversão.","Em PDFs longos, limite o intervalo de páginas para reduzir tempo e tamanho."],"A aparência da página vira imagem; o texto deixa de ser editável como texto."),
    },
    "pdf-a-png": {
        "es": (["Extraer páginas con texto, diagramas o gráficos con buena nitidez.","Usar páginas de PDF en diseño, presentaciones o documentación.","Conservar mejor bordes y texto que con una compresión JPG agresiva."],["Cada página se rasteriza como PNG.","PNG suele pesar más que JPG, especialmente en fotografías."],["Si el archivo pesa demasiado, usa menor DPI o considera JPG.","PNG no convierte el texto en texto editable; conserva la página como imagen."],"Útil cuando priorizas nitidez de bordes y gráficos sobre tamaño de archivo."),
        "en": (["Extract pages with text, diagrams or graphics at good sharpness.","Use PDF pages in design, presentations or documentation.","Preserve edges and text better than aggressive JPG compression."],["Each page is rasterized as PNG.","PNG is often larger than JPG, especially for photographs."],["If files are too large, lower DPI or consider JPG.","PNG does not make text editable; it preserves the page as an image."],"Useful when sharp edges and graphics matter more than the smallest file size."),
        "fr": (["Extraire des pages avec texte, schémas ou graphiques avec une bonne netteté.","Utiliser des pages PDF dans des présentations ou documents.","Mieux préserver les contours et le texte qu'avec une forte compression JPG."],["Chaque page est pixellisée en PNG.","Le PNG est souvent plus lourd que le JPG, surtout pour les photos."],["Si le fichier est trop lourd, baissez le DPI ou choisissez JPG.","Le PNG ne rend pas le texte éditable ; il conserve la page comme image."],"Utile lorsque la netteté des contours et graphiques compte plus que la taille minimale."),
        "pt-br": (["Extrair páginas com texto, diagramas ou gráficos com boa nitidez.","Usar páginas de PDF em apresentações ou documentação.","Preservar melhor bordas e texto do que com compressão JPG agressiva."],["Cada página é rasterizada como PNG.","PNG costuma ser maior que JPG, principalmente em fotografias."],["Se o arquivo ficar grande, reduza o DPI ou considere JPG.","PNG não torna o texto editável; preserva a página como imagem."],"Útil quando nitidez de bordas e gráficos importa mais do que o menor tamanho."),
    },
    "png-a-jpg": {
        "es": (["Subir una imagen a servicios que solo aceptan JPG.","Reducir tamaño de fotografías o capturas sin transparencia.","Preparar imágenes para correo, web o mensajería."],["JPG no admite transparencia; las zonas transparentes deben convertirse a un fondo sólido.","La calidad seleccionada determina el equilibrio entre detalle y tamaño."],["Si necesitas transparencia, conserva PNG o usa WEBP.","Texto muy fino o gráficos planos pueden verse peor con compresión JPG alta."],"JPG es adecuado para fotografías; PNG suele ser mejor para transparencia, capturas y gráficos con bordes definidos."),
        "en": (["Upload an image to services that only accept JPG.","Reduce the size of photos or screenshots that do not need transparency.","Prepare images for email, web or messaging."],["JPG does not support transparency; transparent areas must be flattened onto a solid background.","Selected quality controls the tradeoff between detail and file size."],["If transparency is required, keep PNG or use WEBP.","Fine text and flat graphics can look worse with heavy JPG compression."],"JPG is best suited to photographs; PNG is often better for transparency, screenshots and sharp-edged graphics."),
        "fr": (["Envoyer une image vers un service qui n'accepte que le JPG.","Réduire la taille de photos ou captures sans transparence.","Préparer des images pour e-mail, web ou messagerie."],["Le JPG ne gère pas la transparence ; les zones transparentes doivent être aplaties sur un fond uni.","La qualité choisie règle le compromis entre détail et taille."],["Si la transparence est nécessaire, gardez le PNG ou utilisez WEBP.","Le texte fin et les graphiques plats peuvent souffrir d'une forte compression JPG."],"Le JPG convient aux photos ; le PNG reste souvent meilleur pour transparence, captures et contours nets."),
        "pt-br": (["Enviar imagem para serviços que aceitam apenas JPG.","Reduzir tamanho de fotos ou capturas sem transparência.","Preparar imagens para e-mail, web ou mensagens."],["JPG não suporta transparência; áreas transparentes precisam ser achatadas em um fundo sólido.","A qualidade escolhida controla o equilíbrio entre detalhe e tamanho."],["Se precisar de transparência, mantenha PNG ou use WEBP.","Texto fino e gráficos planos podem piorar com compressão JPG forte."],"JPG é indicado para fotos; PNG costuma ser melhor para transparência, capturas e gráficos com bordas nítidas."),
    },
    "jpg-a-png": {
        "es": (["Usar una imagen en flujos que requieren PNG.","Evitar nuevas pérdidas al seguir editando una imagen ya comprimida.","Trabajar con gráficos, capturas o interfaces en herramientas que prefieren PNG."],["Convertir JPG a PNG no recupera detalle perdido por la compresión JPG original.","El archivo PNG resultante puede pesar más aunque visualmente se vea igual."],["Si buscas transparencia, convertir a PNG no elimina automáticamente el fondo de la imagen.","Si solo quieres reducir peso, PNG puede no ser la mejor salida para una fotografía."],"Cambia el contenedor y la compresión; no reconstruye información visual que ya se perdió en el JPG."),
        "en": (["Use an image in workflows that require PNG.","Avoid additional lossy compression while continuing to edit an already compressed image.","Work with screenshots, graphics or interfaces in tools that prefer PNG."],["JPG to PNG cannot restore detail already lost by JPG compression.","The PNG output can be larger even when it looks identical."],["Converting to PNG does not automatically remove the image background.","If your main goal is smaller photo size, PNG may not be the best target."],"It changes the file format and compression, but it cannot reconstruct visual information already lost in the JPG."),
        "fr": (["Utiliser une image dans un flux qui exige le PNG.","Éviter une nouvelle compression avec perte lors de modifications ultérieures.","Travailler avec captures, graphiques ou interfaces dans des outils préférant PNG."],["Le passage JPG vers PNG ne récupère pas les détails déjà perdus par la compression JPG.","Le PNG obtenu peut être plus lourd même si l'image semble identique."],["Passer en PNG ne supprime pas automatiquement l'arrière-plan.","Si votre objectif principal est de réduire le poids d'une photo, PNG n'est pas toujours idéal."],"Le format et la compression changent, mais les informations déjà perdues dans le JPG ne peuvent pas être recréées."),
        "pt-br": (["Usar uma imagem em fluxos que exigem PNG.","Evitar novas perdas ao continuar editando uma imagem já comprimida.","Trabalhar com capturas, gráficos ou interfaces em ferramentas que preferem PNG."],["Converter JPG para PNG não recupera detalhes já perdidos na compressão JPG.","O PNG resultante pode ficar maior mesmo parecendo igual."],["Converter para PNG não remove automaticamente o fundo da imagem.","Se o objetivo é reduzir o tamanho de uma foto, PNG pode não ser a melhor saída."],"O formato e a compressão mudam, mas informações visuais já perdidas no JPG não são reconstruídas."),
    },
    "png-a-webp": {
        "es": (["Optimizar imágenes para una web moderna.","Reducir peso manteniendo transparencia cuando el contenido lo permite.","Preparar recursos visuales para sitios y aplicaciones compatibles con WEBP."],["WEBP admite transparencia y compresión eficiente.","La calidad y el tipo de imagen determinan cuánto se reduce el archivo."],["Comprueba compatibilidad si el archivo va a usarse en software muy antiguo.","Una calidad demasiado baja puede introducir artefactos visibles."],"WEBP suele ofrecer buen equilibrio entre calidad y peso para web, pero conserva el PNG original si necesitas un archivo maestro sin cambios."),
        "en": (["Optimize images for a modern website.","Reduce file size while keeping transparency when appropriate.","Prepare visual assets for WEBP-compatible websites and apps."],["WEBP supports transparency and efficient compression.","Image type and selected quality determine the size reduction."],["Check compatibility when targeting very old software.","Very low quality can introduce visible compression artifacts."],"WEBP often offers a strong quality-to-size balance for the web, but keep the original PNG as a master copy when needed."),
        "fr": (["Optimiser des images pour un site web moderne.","Réduire le poids tout en conservant la transparence lorsque c'est pertinent.","Préparer des ressources visuelles pour sites et applications compatibles WEBP."],["WEBP gère la transparence et une compression efficace.","Le type d'image et la qualité choisie déterminent la réduction de taille."],["Vérifiez la compatibilité pour les logiciels très anciens.","Une qualité trop faible peut créer des artefacts visibles."],"WEBP offre souvent un bon équilibre qualité/poids pour le web, mais gardez le PNG original comme fichier maître si nécessaire."),
        "pt-br": (["Otimizar imagens para um site moderno.","Reduzir tamanho mantendo transparência quando adequado.","Preparar recursos visuais para sites e apps compatíveis com WEBP."],["WEBP suporta transparência e compressão eficiente.","O tipo de imagem e a qualidade escolhida determinam a redução de tamanho."],["Verifique compatibilidade se o arquivo for usado em software muito antigo.","Qualidade muito baixa pode gerar artefatos visíveis."],"WEBP costuma oferecer bom equilíbrio entre qualidade e tamanho para web, mas mantenha o PNG original como arquivo mestre quando necessário."),
    },
    "csv-a-xlsx": {
        "es": (["Abrir datos CSV cómodamente en Excel.","Compartir una tabla con columnas más fáciles de revisar.","Preparar datos exportados desde sistemas administrativos para continuar trabajando."],["Converti interpreta filas y columnas del CSV y crea un libro XLSX.","El separador, la codificación y el formato de fechas/números del CSV pueden influir en el resultado."],["Si todas las columnas aparecen juntas, revisa el delimitador del CSV.","Ceros iniciales, fechas y números largos pueden ser interpretados por hojas de cálculo; revisa campos sensibles después de convertir."],"La conversión organiza los datos en una hoja Excel; no inventa fórmulas, formatos contables ni tipos que no estén claros en el archivo fuente."),
        "en": (["Open CSV data more comfortably in Excel.","Share a table with easier-to-review columns.","Prepare data exported from administrative systems for further work."],["Converti reads CSV rows and columns and creates an XLSX workbook.","Delimiter, encoding and date/number conventions can affect the result."],["If all data appears in one column, check the CSV delimiter.","Leading zeros, dates and long numbers can be interpreted by spreadsheet software; review sensitive fields after conversion."],"The conversion organizes source data into an Excel workbook; it does not invent formulas, accounting formats or ambiguous data types."),
        "fr": (["Ouvrir plus facilement des données CSV dans Excel.","Partager un tableau avec des colonnes plus lisibles.","Préparer des données exportées d'un système administratif pour continuer à travailler."],["Converti lit les lignes et colonnes CSV et crée un classeur XLSX.","Le séparateur, l'encodage et les conventions de dates/nombres peuvent influencer le résultat."],["Si toutes les données sont dans une seule colonne, vérifiez le délimiteur CSV.","Les zéros initiaux, dates et grands nombres peuvent être interprétés par le tableur ; contrôlez les champs sensibles après conversion."],"La conversion organise les données source dans Excel sans inventer de formules, formats comptables ou types ambigus."),
        "pt-br": (["Abrir dados CSV com mais facilidade no Excel.","Compartilhar tabela com colunas mais fáceis de revisar.","Preparar dados exportados de sistemas administrativos para continuar o trabalho."],["O Converti lê linhas e colunas do CSV e cria uma planilha XLSX.","Separador, codificação e convenções de datas/números podem influenciar o resultado."],["Se todos os dados aparecerem em uma coluna, verifique o delimitador do CSV.","Zeros à esquerda, datas e números longos podem ser interpretados pela planilha; revise campos sensíveis depois da conversão."],"A conversão organiza os dados de origem em Excel sem inventar fórmulas, formatos contábeis ou tipos ambíguos."),
    },
    "xlsx-a-csv": {
        "es": (["Exportar una hoja para sistemas que aceptan CSV.","Mover datos entre aplicaciones sin depender del formato de Excel.","Preparar tablas para bases de datos, scripts o herramientas de análisis."],["CSV almacena valores tabulares, no el diseño completo de Excel.","Fórmulas, colores, gráficos, imágenes y varias hojas no se representan como en XLSX."],["Comprueba qué hoja se exporta cuando el libro tiene varias.","Revisa separadores, comillas y codificación si el CSV se usará en otro sistema."],"CSV conserva datos tabulares, pero no debe considerarse una copia visual del libro Excel."),
        "en": (["Export a worksheet for systems that accept CSV.","Move data between applications without depending on Excel format.","Prepare tables for databases, scripts or analysis tools."],["CSV stores tabular values, not the complete Excel presentation.","Formulas, colors, charts, images and multiple worksheets are not represented like XLSX."],["Check which worksheet is exported when the workbook contains several sheets.","Review delimiters, quoting and encoding when the CSV will be imported by another system."],"CSV preserves tabular data but should not be treated as a visual copy of the Excel workbook."),
        "fr": (["Exporter une feuille vers des systèmes acceptant CSV.","Déplacer des données entre applications sans dépendre du format Excel.","Préparer des tableaux pour bases de données, scripts ou outils d'analyse."],["CSV stocke des valeurs tabulaires, pas la présentation complète d'Excel.","Formules, couleurs, graphiques, images et plusieurs feuilles ne sont pas représentés comme dans XLSX."],["Vérifiez quelle feuille est exportée si le classeur en contient plusieurs.","Contrôlez séparateurs, guillemets et encodage si le CSV est destiné à un autre système."],"CSV conserve les données tabulaires mais ne constitue pas une copie visuelle du classeur Excel."),
        "pt-br": (["Exportar uma planilha para sistemas que aceitam CSV.","Mover dados entre aplicativos sem depender do formato Excel.","Preparar tabelas para bancos de dados, scripts ou ferramentas de análise."],["CSV armazena valores tabulares, não toda a apresentação do Excel.","Fórmulas, cores, gráficos, imagens e várias planilhas não são representados como no XLSX."],["Confira qual planilha é exportada quando o arquivo possui várias abas.","Revise delimitadores, aspas e codificação se o CSV for importado por outro sistema."],"CSV preserva dados tabulares, mas não deve ser considerado uma cópia visual do arquivo Excel."),
    },
    "docx-a-txt": {
        "es": (["Extraer texto de un documento Word para copiarlo a sistemas simples.","Crear una versión ligera para notas, scripts o procesamiento de texto.","Recuperar contenido cuando no necesitas diseño, imágenes ni tablas."],["TXT conserva texto plano, no estilos, imágenes, encabezados ni diseño de página.","Las tablas se convierten en texto lineal y pueden perder su disposición visual."],["Si necesitas conservar el formato, mantén DOCX o convierte a PDF.","Revisa saltos de línea cuando el documento original tenga columnas o tablas complejas."],"El objetivo es extraer contenido textual, no reproducir la apariencia de Word."),
        "en": (["Extract Word text for use in simple systems.","Create a lightweight version for notes, scripts or text processing.","Recover content when layout, images and tables are not required."],["TXT keeps plain text, not styles, images, headers or page layout.","Tables become linear text and may lose their visual arrangement."],["If formatting matters, keep DOCX or convert to PDF.","Review line breaks when the source contains columns or complex tables."],"The goal is textual extraction, not visual reproduction of the Word document."),
        "fr": (["Extraire le texte d'un document Word pour des systèmes simples.","Créer une version légère pour notes, scripts ou traitement de texte.","Récupérer le contenu lorsque la mise en page, les images et tableaux ne sont pas nécessaires."],["TXT conserve le texte brut, pas les styles, images, en-têtes ou mise en page.","Les tableaux deviennent du texte linéaire et peuvent perdre leur disposition."],["Si la mise en forme compte, gardez DOCX ou convertissez en PDF.","Vérifiez les sauts de ligne si le document contient colonnes ou tableaux complexes."],"L'objectif est d'extraire le texte, pas de reproduire l'apparence de Word."),
        "pt-br": (["Extrair texto de um documento Word para sistemas simples.","Criar uma versão leve para notas, scripts ou processamento de texto.","Recuperar conteúdo quando layout, imagens e tabelas não são necessários."],["TXT mantém texto simples, não estilos, imagens, cabeçalhos ou layout de página.","Tabelas viram texto linear e podem perder a disposição visual."],["Se a formatação for importante, mantenha DOCX ou converta para PDF.","Revise quebras de linha em documentos com colunas ou tabelas complexas."],"O objetivo é extrair conteúdo textual, não reproduzir a aparência do Word."),
    },
    "docx-a-html": {
        "es": (["Publicar el contenido básico de un Word en una página web.","Reutilizar texto, títulos y listas dentro de un CMS.","Obtener HTML editable para continuar trabajando en código o contenido."],["HTML representa estructura web, no una página Word idéntica.","Estilos avanzados, objetos flotantes y elementos propios de Office pueden simplificarse."],["Revisa imágenes y tablas complejas antes de publicar.","No pegues HTML convertido directamente en producción sin revisar su semántica y estilos."],"La conversión busca una estructura HTML útil y editable, no una copia pixel a pixel del documento Word."),
        "en": (["Publish basic Word content on a web page.","Reuse text, headings and lists inside a CMS.","Get editable HTML for further code or content work."],["HTML represents web structure, not an identical Word page.","Advanced styles, floating objects and Office-specific elements may be simplified."],["Review images and complex tables before publishing.","Do not deploy converted HTML without checking semantics and styling."],"The conversion aims for useful, editable HTML structure rather than a pixel-perfect copy of Word."),
        "fr": (["Publier le contenu de base d'un Word sur une page web.","Réutiliser texte, titres et listes dans un CMS.","Obtenir du HTML modifiable pour poursuivre le travail."],["HTML représente une structure web, pas une page Word identique.","Les styles avancés, objets flottants et éléments propres à Office peuvent être simplifiés."],["Vérifiez images et tableaux complexes avant publication.","Ne publiez pas le HTML converti sans contrôler sémantique et styles."],"La conversion vise une structure HTML utile et modifiable, pas une copie pixel parfaite de Word."),
        "pt-br": (["Publicar conteúdo básico do Word em uma página web.","Reaproveitar texto, títulos e listas em um CMS.","Obter HTML editável para continuar o trabalho em código ou conteúdo."],["HTML representa estrutura web, não uma página Word idêntica.","Estilos avançados, objetos flutuantes e elementos específicos do Office podem ser simplificados."],["Revise imagens e tabelas complexas antes de publicar.","Não publique o HTML convertido sem revisar semântica e estilos."],"A conversão busca uma estrutura HTML útil e editável, não uma cópia pixel a pixel do Word."),
    },
    "mp3-a-wav": {
        "es": (["Editar audio en programas que trabajan mejor con WAV.","Preparar pistas para procesamiento, mezcla o análisis.","Usar audio sin nueva compresión con pérdida durante etapas posteriores."],["Convertir MP3 a WAV no recupera calidad que ya se perdió al comprimir el MP3.","WAV suele ocupar bastante más espacio que MP3."],["Si el archivo pesa demasiado, conserva MP3 para distribución y WAV solo para edición.","La calidad final está limitada por el MP3 original."],"WAV evita añadir otra compresión con pérdida, pero no convierte un MP3 comprimido en una grabación de mayor calidad real."),
        "en": (["Edit audio in software that works better with WAV.","Prepare tracks for processing, mixing or analysis.","Use uncompressed audio for later workflow stages."],["MP3 to WAV cannot restore quality already lost during MP3 compression.","WAV files are usually much larger than MP3."],["If file size is a concern, keep MP3 for distribution and use WAV only for editing.","Final quality is limited by the original MP3."],"WAV avoids adding another lossy compression stage, but it cannot turn a compressed MP3 into higher-quality source audio."),
        "fr": (["Modifier l'audio dans des logiciels préférant WAV.","Préparer des pistes pour traitement, mixage ou analyse.","Utiliser un audio non compressé pour les étapes suivantes."],["MP3 vers WAV ne récupère pas la qualité déjà perdue lors de la compression MP3.","WAV occupe généralement beaucoup plus d'espace que MP3."],["Si la taille compte, gardez MP3 pour diffusion et WAV pour l'édition.","La qualité finale reste limitée par le MP3 d'origine."],"WAV évite une nouvelle compression avec perte, mais ne transforme pas un MP3 compressé en source de meilleure qualité."),
        "pt-br": (["Editar áudio em programas que trabalham melhor com WAV.","Preparar faixas para processamento, mixagem ou análise.","Usar áudio sem nova compressão com perda nas etapas seguintes."],["MP3 para WAV não recupera qualidade já perdida na compressão MP3.","WAV normalmente ocupa muito mais espaço que MP3."],["Se tamanho for importante, mantenha MP3 para distribuição e WAV para edição.","A qualidade final é limitada pelo MP3 original."],"WAV evita adicionar outra compressão com perda, mas não transforma MP3 comprimido em áudio de maior qualidade real."),
    },
    "wav-a-mp3": {
        "es": (["Reducir el tamaño de una grabación para compartirla.","Preparar audio para mensajería, web o dispositivos con espacio limitado.","Crear una copia de distribución a partir de un archivo WAV de trabajo."],["MP3 usa compresión con pérdida; un bitrate mayor suele conservar más detalle y también aumentar el tamaño.","La conversión no mejora una fuente WAV que ya tenga ruido o distorsión."],["Guarda el WAV original si necesitas una copia maestra.","Evita bitrates demasiado bajos para música o voz que necesite claridad."],"MP3 prioriza compatibilidad y tamaño. La calidad depende del archivo original y del bitrate elegido."),
        "en": (["Reduce a recording's size for sharing.","Prepare audio for messaging, web or limited-storage devices.","Create a distribution copy from a WAV working master."],["MP3 uses lossy compression; higher bitrate usually preserves more detail and creates larger files.","Conversion cannot improve noise or distortion already present in the WAV."],["Keep the WAV original if you need a master copy.","Avoid very low bitrates for music or speech that needs clarity."],"MP3 prioritizes compatibility and file size. Quality depends on the source and selected bitrate."),
        "fr": (["Réduire la taille d'un enregistrement pour le partager.","Préparer l'audio pour messagerie, web ou appareils avec peu d'espace.","Créer une copie de diffusion depuis un fichier WAV de travail."],["MP3 utilise une compression avec perte ; un débit plus élevé conserve généralement plus de détails et augmente la taille.","La conversion ne corrige pas le bruit ou la distorsion déjà présents."],["Gardez le WAV original si vous avez besoin d'un fichier maître.","Évitez des débits trop faibles pour musique ou voix nécessitant de la clarté."],"MP3 privilégie compatibilité et taille. La qualité dépend de la source et du débit choisi."),
        "pt-br": (["Reduzir o tamanho de uma gravação para compartilhar.","Preparar áudio para mensagens, web ou dispositivos com pouco espaço.","Criar uma cópia de distribuição a partir de um WAV de trabalho."],["MP3 usa compressão com perda; bitrate maior costuma preservar mais detalhes e aumentar o tamanho.","A conversão não melhora ruído ou distorção já presentes no WAV."],["Mantenha o WAV original se precisar de uma cópia mestre.","Evite bitrates muito baixos para música ou voz que precise de clareza."],"MP3 prioriza compatibilidade e tamanho. A qualidade depende da fonte e do bitrate escolhido."),
    },
    "webp-a-jpg": {
        "es": (["Abrir una imagen WEBP en sistemas que solo aceptan JPG.","Preparar fotografías WEBP para formularios, editores o servicios antiguos.","Compartir una copia compatible sin depender de soporte WEBP."],["JPG no admite transparencia ni animación WEBP.","La conversión puede aumentar o reducir el tamaño según calidad y contenido."],["Si el WEBP tiene transparencia, revisa el fondo del JPG resultante.","Si necesitas conservar animación, JPG no es un formato adecuado."],"La salida busca compatibilidad JPG; funciones propias de WEBP como transparencia o animación no pueden conservarse en JPG."),
        "en": (["Open a WEBP image in systems that only accept JPG.","Prepare WEBP photos for older forms, editors or services.","Share a broadly compatible copy without relying on WEBP support."],["JPG does not support WEBP transparency or animation.","File size may increase or decrease depending on content and selected quality."],["If the WEBP has transparency, review the background in the JPG result.","If animation must be preserved, JPG is not an appropriate target."],"The output prioritizes JPG compatibility; WEBP-specific transparency or animation cannot be preserved in JPG."),
        "fr": (["Ouvrir une image WEBP dans des systèmes qui n'acceptent que JPG.","Préparer des photos WEBP pour formulaires, éditeurs ou services anciens.","Partager une copie largement compatible sans dépendre du support WEBP."],["JPG ne gère ni transparence ni animation WEBP.","La taille peut augmenter ou diminuer selon le contenu et la qualité choisie."],["Si le WEBP contient de la transparence, vérifiez le fond du JPG obtenu.","Si l'animation doit être conservée, JPG n'est pas adapté."],"La sortie privilégie la compatibilité JPG ; transparence et animation propres à WEBP ne peuvent pas être conservées."),
        "pt-br": (["Abrir imagem WEBP em sistemas que aceitam apenas JPG.","Preparar fotos WEBP para formulários, editores ou serviços antigos.","Compartilhar uma cópia compatível sem depender de suporte WEBP."],["JPG não suporta transparência nem animação WEBP.","O tamanho pode aumentar ou diminuir conforme conteúdo e qualidade."],["Se o WEBP tiver transparência, revise o fundo do JPG resultante.","Se precisar manter animação, JPG não é um formato adequado."],"A saída prioriza compatibilidade JPG; transparência e animação específicas do WEBP não podem ser preservadas."),
    },
}

RELATED = {
    "pdf-a-word": [("word-a-pdf", "Word ⇄ PDF"), ("pdf-a-jpg", "PDF → JPG"), ("pdf-a-png", "PDF → PNG"), ("docx-a-txt", "DOCX → TXT"), ("docx-a-html", "DOCX → HTML")],
    "word-a-pdf": [("pdf-a-word", "PDF → Word"), ("docx-a-txt", "DOCX → TXT"), ("docx-a-html", "DOCX → HTML"), ("jpg-a-pdf", "JPG → PDF")],
    "jpg-a-pdf": [("pdf-a-jpg", "PDF → JPG"), ("pdf-a-png", "PDF → PNG"), ("png-a-jpg", "PNG → JPG"), ("jpg-a-png", "JPG → PNG"), ("png-a-webp", "PNG → WEBP")],
    "pdf-a-jpg": [("pdf-a-png", "PDF → PNG"), ("jpg-a-pdf", "JPG → PDF"), ("pdf-a-word", "PDF → Word"), ("png-a-jpg", "PNG → JPG")],
    "pdf-a-png": [("pdf-a-jpg", "PDF → JPG"), ("jpg-a-pdf", "JPG → PDF"), ("pdf-a-word", "PDF → Word"), ("png-a-webp", "PNG → WEBP")],
    "png-a-jpg": [("jpg-a-png", "JPG → PNG"), ("png-a-webp", "PNG → WEBP"), ("jpg-a-pdf", "JPG → PDF"), ("webp-a-jpg", "WEBP → JPG")],
    "jpg-a-png": [("png-a-jpg", "PNG → JPG"), ("png-a-webp", "PNG → WEBP"), ("jpg-a-pdf", "JPG → PDF"), ("webp-a-jpg", "WEBP → JPG")],
    "png-a-webp": [("webp-a-jpg", "WEBP → JPG"), ("png-a-jpg", "PNG → JPG"), ("jpg-a-png", "JPG → PNG"), ("jpg-a-pdf", "JPG → PDF")],
    "csv-a-xlsx": [("xlsx-a-csv", "XLSX → CSV"), ("docx-a-html", "DOCX → HTML")],
    "xlsx-a-csv": [("csv-a-xlsx", "CSV → XLSX"), ("docx-a-txt", "DOCX → TXT")],
}


def _compact_profile(locale: str, slug: str) -> dict:
    entry = COMPACT.get(slug, {}).get(locale)
    if not entry:
        return {}
    use_cases, compatibility, issue_lines, expectation = entry
    # Las incidencias compactas se convierten en pares título/respuesta sin
    # inventar explicaciones adicionales.
    prefix = {
        "es": "Qué revisar",
        "en": "What to check",
        "fr": "À vérifier",
        "pt-br": "O que verificar",
    }[locale]
    return {
        "use_cases": use_cases,
        "compatibility": compatibility,
        "issues": [(prefix, x) for x in issue_lines],
        "expectation": expectation,
        "extra_faq": [],
    }


def enrich_tool_seo(locale: str, slug: str, title: str, description: str, base: dict | None) -> dict:
    """Devuelve contenido enriquecido sin modificar el diccionario original."""
    locale = locale if locale in COMMON else "es"
    out = deepcopy(base or {})
    common = COMMON[locale]
    profile = deepcopy(PROFILES.get(slug, {}).get(locale) or _compact_profile(locale, slug))

    # Para páginas no prioritarias conservamos el contenido ya existente y solo
    # añadimos garantías comunes. No generamos párrafos de relleno.
    if not out.get("intro"):
        out["intro"] = description
    if not out.get("benefits"):
        out["benefits"] = [common["mobile_note"]]
    if not out.get("steps"):
        out["steps"] = []

    if profile:
        out.update({k: v for k, v in profile.items() if v})
        existing_faq = list(out.get("faq") or [])
        out["faq"] = existing_faq + [x for x in profile.get("extra_faq", []) if x not in existing_faq]
        out["related"] = RELATED.get(slug, out.get("related", []))

    existing_faq = list(out.get("faq") or [])
    for item in common["fallback_faq"]:
        if item[0] not in {q for q, _ in existing_faq}:
            existing_faq.append(item)
    out["faq"] = existing_faq[:8]
    out["privacy"] = list(common["privacy"])
    for optional_key, default in (("use_cases", []), ("compatibility", []), ("issues", []), ("expectation", ""), ("related", [])):
        out.setdefault(optional_key, deepcopy(default))

    out["labels"] = {
        "use_cases": common["use_cases_title"],
        "compatibility": common["compat_title"],
        "issues": common["issues_title"],
        "privacy": common["privacy_title"],
        "expectation_prefix": common["expectation_prefix"],
    }
    out["is_priority"] = slug in PRIORITY_SLUGS
    return out
