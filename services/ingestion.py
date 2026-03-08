import data.vector_store as vstore
from utils.chunking import split_text


def save_file_content(file):
  """Split uploaded file into chunks and persist them in the vector store."""
  chunks = split_text(file)
  vstore.save_to_db(chunks)
