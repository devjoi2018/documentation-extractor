#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from fpdf import FPDF
import time
import re
import os


class WebScraper:
    """Clase encargada de realizar el scraping de la web de forma recursiva."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        # Usamos un User-Agent genérico para evitar bloqueos
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; WebScraper/1.0)"})
        self.visited = set()

        # Extraemos el dominio y la ruta base para filtrado de links
        parsed = urlparse(base_url)
        self.base_domain = parsed.netloc
        self.base_path = parsed.path.rstrip('/')  # Puede estar vacío

    def is_valid_link(self, link: str) -> bool:
        """Valida que el link pertenezca al mismo dominio y ruta base."""
        try:
            parsed = urlparse(link)
            # Aceptar solo http y https
            if parsed.scheme not in ('http', 'https'):
                return False
            # El dominio debe ser el mismo
            if parsed.netloc != self.base_domain:
                return False
            # La ruta debe iniciar con la ruta base
            if not parsed.path.startswith(self.base_path):
                return False
            return True
        except Exception as e:
            return False

    def extract_links(self, soup: BeautifulSoup, current_url: str) -> list:
        """Extrae links válidos de la página actual."""
        links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            full_url = urljoin(current_url, href)
            # Eliminamos fragmentos y espacios
            full_url = full_url.split('#')[0].strip()
            if self.is_valid_link(full_url) and full_url not in self.visited:
                links.append(full_url)
        return links

    def get_text_from_page(self, soup: BeautifulSoup) -> str:
        """Extrae el texto limpio de la página."""
        return soup.get_text(separator='\n', strip=True)

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Obtiene y parsea la página web. Si falla, retorna None."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            # Verificamos que el Content-Type sea HTML
            content_type = response.headers.get('Content-Type', '')
            if 'html' not in content_type:
                return None
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            print(f"Error al obtener {url}: {e}")
            return None

    def scrape(self) -> str:
        """Realiza el scraping recursivo y retorna el contenido acumulado en texto."""
        output = ""
        queue = [self.base_url]
        while queue:
            url = queue.pop(0)
            if url in self.visited:
                continue
            print(f"Extrayendo: {url}")
            self.visited.add(url)
            soup = self.fetch_page(url)
            if soup is None:
                continue
            text = self.get_text_from_page(soup)
            # Se agrega el contenido con la URL como encabezado
            output += f"URL: {url}\n{text}\n{'='*80}\n"
            # Se extraen nuevos links y se agregan a la cola
            new_links = self.extract_links(soup, url)
            for link in new_links:
                if link not in self.visited:
                    queue.append(link)
            # Retardo para no saturar al servidor
            time.sleep(0.5)
        return output


class PDFGenerator:
    """Clase encargada de generar un PDF a partir del contenido de texto."""

    def __init__(self, file_name: str):
        # Sanitizamos el nombre del archivo para evitar path traversal
        self.file_name = os.path.basename(file_name)
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def generate_pdf(self, content: str) -> None:
        """Genera el PDF con el contenido dado."""
        self.pdf.add_page()
        # Usar una fuente incorporada que no dependa de archivos externos: 'Arial'
        self.pdf.set_font("Arial", "", 12)
        # Sanitizar el contenido para asegurar que se pueda codificar en latin-1, reemplazando caracteres no compatibles
        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
        # Se agrega el contenido línea por línea
        for line in safe_content.splitlines():
            self.pdf.multi_cell(0, 10, line)
        try:
            self.pdf.output(self.file_name)
            print(f"PDF generado: {self.file_name}")
        except Exception as e:
            print(f"Error al generar el PDF: {e}")


def validar_url(url: str) -> bool:
    """Validación básica de la URL usando expresión regular que admite guiones y números en el dominio."""
    regex = re.compile(
        r'^(http|https)://'
        r'((([A-Za-z0-9-]+\.)+[A-Za-z]{2,})|localhost)'
        r'(:\d+)?'
        r'(/.*)?$'
    )
    return re.match(regex, url) is not None


def main():
    print("\n=== Web Scraper y Generador de PDF ===\n")
    # Solicitar la URL interactivamente
    while True:
        url = input(
            "Ingrese la URL inicial (debe comenzar con http:// o https://): ").strip()
        # Eliminar caracteres conflictivos, por ejemplo, un '@' al inicio
        url = url.lstrip('@')
        if validar_url(url):
            break
        print("URL inválida. Por favor, intente nuevamente.")

    # Solicitar el nombre del archivo PDF de salida
    while True:
        output_file = input(
            "\nIngrese el nombre del archivo PDF de salida: ").strip()
        if output_file:
            if not output_file.lower().endswith('.pdf'):
                output_file += '.pdf'
            try:
                # Verificación de permisos de escritura
                with open(output_file, 'w') as f:
                    pass
                os.remove(output_file)
                break
            except Exception as e:
                print(
                    f"Error: No se puede crear el archivo en la ubicación especificada: {e}")
        else:
            print("Por favor, ingrese un nombre válido para el archivo.")

    print("\nIniciando el proceso de extracción...")
    print("(Esto puede tomar varios minutos dependiendo del tamaño del sitio)\n")

    try:
        scraper = WebScraper(url)
        contenido = scraper.scrape()
        if contenido:
            print("\nGenerando PDF...")
            pdf_generator = PDFGenerator(output_file)
            pdf_generator.generate_pdf(contenido)
            print("\n¡Proceso completado con éxito!")
        else:
            print("\nNo se pudo extraer contenido de la URL proporcionada.")
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError durante el proceso: {e}")


if __name__ == "__main__":
    main()
