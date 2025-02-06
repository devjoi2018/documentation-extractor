# Extractor de Documentación Web

Este script de Python es una herramienta especializada diseñada específicamente para extraer documentación técnica de sitios web y convertirla en un formato PDF optimizado para su uso con NotebookLM de Google. Esta herramienta facilita la creación de fuentes de conocimiento personalizadas para el aprendizaje acelerado y la comprensión profunda de documentación técnica.

## 🎯 Objetivo Principal

El objetivo principal de este script es facilitar la extracción y preparación de documentación técnica para su uso en [NotebookLM de Google](https://notebooklm.google.com/). Al convertir la documentación web en un formato PDF estructurado, permite:

- **Aprendizaje Acelerado**: Cargar documentación técnica completa en NotebookLM para interactuar con ella de manera más efectiva.
- **Consultas Inteligentes**: Realizar preguntas específicas sobre la documentación y obtener respuestas precisas.
- **Comprensión Profunda**: Analizar y entender mejor la documentación técnica a través de la IA conversacional de NotebookLM.

### 📚 Uso con NotebookLM

1. Ejecuta el script para extraer la documentación de tu interés
2. Dirígete a [NotebookLM](https://notebooklm.google.com/) y accede con tu cuenta de Google
3. Sube el PDF generado como fuente de conocimiento
4. Comienza a interactuar con la documentación de manera inteligente

Por ejemplo, puedes extraer documentación de:

- https://python.langchain.com/docs/get_started/introduction
- https://docs.pytest.org/en/stable/
- https://fastapi.tiangolo.com/tutorial/
- Y cualquier otra documentación técnica que necesites estudiar

## 🚀 Características Principales

- **Extracción Recursiva**: Navega automáticamente por todas las subpáginas dentro del dominio y ruta base especificados.
- **Generación de PDF**: Convierte todo el contenido extraído en un documento PDF organizado.
- **Respeto al Servidor**: Implementa delays entre peticiones para no sobrecargar los servidores.
- **Validación de URLs**: Asegura que solo se procesen URLs válidas y dentro del dominio objetivo.
- **Manejo de Errores**: Sistema robusto de manejo de errores y excepciones.
- **Interfaz por Consola**: Interfaz amigable que guía al usuario en el proceso.

## 📋 Requisitos Previos

Asegúrate de tener Python 3.6 o superior instalado en tu sistema. Se recomienda usar un entorno virtual para evitar conflictos con otros proyectos:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🔧 Instalación

1. Clona este repositorio o descarga el archivo `main.py`
2. Crea y activa el entorno virtual como se indica arriba
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

1. Ejecuta el script:

   ```bash
   python main.py
   ```

2. Sigue las instrucciones en pantalla:

   - Ingresa la URL inicial (debe comenzar con http:// o https://)
   - Proporciona un nombre para el archivo PDF de salida

3. El script comenzará a:

   - Extraer contenido de la URL proporcionada
   - Buscar y seguir enlaces dentro del mismo dominio
   - Generar un PDF con todo el contenido extraído

4. Una vez generado el PDF:
   - Súbelo a NotebookLM como fuente de conocimiento
   - Comienza a hacer preguntas y a interactuar con la documentación
   - Aprovecha la IA para entender mejor el contenido

## 🛠️ Funcionamiento Interno

El script está compuesto por dos clases principales:

### WebScraper

- Maneja la extracción recursiva de contenido
- Valida y sigue enlaces dentro del mismo dominio
- Implementa retrasos para no sobrecargar servidores
- Extrae texto limpio de las páginas HTML

### PDFGenerator

- Genera documentos PDF a partir del contenido extraído
- Maneja la codificación de caracteres especiales
- Organiza el contenido de manera legible

## ⚠️ Consideraciones

- El script respeta los dominios y no navega fuera de la ruta base especificada
- Implementa retrasos de 0.5 segundos entre peticiones
- Verifica permisos de escritura antes de generar el PDF
- Sanitiza el contenido para manejar caracteres especiales

## 📝 Beneficios del Uso con NotebookLM

1. **Aprendizaje Personalizado**

   - Interactúa con la documentación de manera conversacional
   - Obtén explicaciones detalladas de conceptos complejos
   - Realiza preguntas específicas sobre la documentación

2. **Optimización del Tiempo**

   - Encuentra rápidamente la información que necesitas
   - Comprende conceptos complejos más rápidamente
   - Reduce el tiempo de lectura y búsqueda manual

3. **Mejor Comprensión**

   - Obtén ejemplos personalizados
   - Aclara dudas específicas
   - Profundiza en temas de interés

4. **Acceso Rápido**
   - Toda la documentación en un solo lugar
   - Búsqueda inteligente dentro del contenido
   - Referencias cruzadas automáticas
