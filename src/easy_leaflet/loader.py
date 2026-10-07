from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass
class Leaflet:
    name: str
    text: str


# The worker that reads the PDF files from a folder
class LeafletLoader:

    def __init__(self, data_dir):
        # Remember where the folder is
        self.data_dir = Path(data_dir)

    def list_names(self):
        # Find all PDF files and keep the names without ".pdf"
        names = []
        for path in self.data_dir.glob("*.pdf"):
            names.append(path.stem)
        return sorted(names)

    def load(self, name):
        # 1. Build the path to the file, for example data/benuron.pdf
        path = self.data_dir / f"{name}.pdf"

        # 2. If the file does not exist, stop with a clear message
        if not path.exists():
            raise FileNotFoundError(f"Leaflet not found: {path}")

        # 3. Open the PDF and get the text of each page
        reader = PdfReader(path)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text())

        # 4. Join the pages into one string and return a Leaflet
        text = "\n".join(pages)
        return Leaflet(name=name, text=text)