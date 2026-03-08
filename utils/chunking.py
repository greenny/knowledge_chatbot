import os
import tempfile

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _extract_text_binary(file, filename):
  """Extract text from PDF/DOC using unstructured; avoids decode('utf-8') on binary."""
  from unstructured.partition.auto import partition

  suffix = '.pdf' if filename.lower().endswith('.pdf') else '.docx' if filename.lower().endswith('.docx') else '.doc'
  with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
    tmp.write(file.getvalue())
    tmp_path = tmp.name
  try:
    elements = partition(filename=tmp_path)
    return "\n\n".join([el.text for el in elements if getattr(el, "text", None)])
  finally:
    os.unlink(tmp_path)


def split_text(file):
  filename = (file.name or '').lower()
  if filename.endswith(('.pdf', '.doc', '.docx')):
    text_from_file = _extract_text_binary(file, file.name)
  else:
    text_from_file = file.getvalue().decode('utf-8')
  documents = [
    Document(
      page_content=text_from_file,
      metadata={'source': filename}
    )
  ]
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
  return text_splitter.split_documents(documents)
