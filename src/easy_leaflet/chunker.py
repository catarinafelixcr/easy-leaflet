from dataclasses import dataclass

@dataclass
class Chunk:
    leaflet_name: str # which leaflet it comes from, for example "benuron"
    index: int # position in the leaflet: 0, 1, 2, ...
    text: str


# The worker that cuts a leaflet into chunks
class Chunker:

    def __init__(self, max_chars=1000, overlap=200):
        self.max_chars = max_chars
        self.overlap = overlap

    def split(self, leaflet):
        # Cut the leaflet text into chunks and return a list of Chunk
        text = leaflet.text
        chunks = []
        start = 0

        while start < len(text):
            # Take the next piece of text
            piece = text[start:start + self.max_chars]
            chunks.append(Chunk(leaflet.name, len(chunks), piece))

            # Move forward, but go back a little so the chunks overlap
            start = start + self.max_chars - self.overlap

        return chunks