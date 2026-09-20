from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from dotenv import load_dotenv

from src.chunking import RecursiveChunker
from src.embeddings import (
	EMBEDDING_PROVIDER_ENV,
	GEMINI_EMBEDDING_MODEL,
	LOCAL_EMBEDDING_MODEL,
	OPENAI_EMBEDDING_MODEL,
	GeminiEmbedder,
	LocalEmbedder,
	OpenAIEmbedder,
	_mock_embed,
)
from src.models import Document
from src.store import EmbeddingStore


DATA_DIR = Path("data/ecommerce")
DEFAULT_QUERIES = [
	"Thời gian hỗ trợ đổi trả hàng tại Tiki là bao lâu?",
	"Sản phẩm nào không được đổi trả theo nhu cầu của khách hàng?",
	"Khách hàng cần làm gì để được bảo hành sản phẩm tại Tiki?",
	"Nhà bán cần xử lý kiện hàng trả như thế nào?",
	"Quy trình xử lý đổi trả bảo hành của nhà bán trong mô hình FBT là gì?",
]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
	"""Read simple YAML frontmatter without adding a YAML dependency."""
	text = path.read_text(encoding="utf-8")
	if not text.startswith("---"):
		return {}, text

	_, frontmatter, content = text.split("---", 2)
	metadata: dict[str, str] = {}
	for line in frontmatter.splitlines():
		match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
		if not match:
			continue
		value = match.group(2).strip().strip('"').strip("'")
		metadata[match.group(1)] = value
	return metadata, content.strip()


def select_embedder():
	provider = os.getenv(EMBEDDING_PROVIDER_ENV, "mock").strip().lower()
	try:
		if provider == "local":
			return LocalEmbedder(os.getenv("LOCAL_EMBEDDING_MODEL", LOCAL_EMBEDDING_MODEL))
		if provider == "openai":
			return OpenAIEmbedder(os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL))
		if provider == "gemini":
			return GeminiEmbedder(os.getenv("GEMINI_EMBEDDING_MODEL", GEMINI_EMBEDDING_MODEL))
	except Exception as error:
		print(f"Embedding backend '{provider}' unavailable: {error}")
		print("Falling back to mock embeddings.")
	return _mock_embed


def load_chunked_documents(data_dir: Path, chunk_size: int) -> list[Document]:
	chunker = RecursiveChunker(chunk_size=chunk_size)
	documents: list[Document] = []
	for path in sorted(data_dir.glob("*.md")):
		metadata, content = parse_frontmatter(path)
		metadata = {**metadata, "source": str(path), "doc_id": metadata.get("doc_id", path.stem)}
		chunks = chunker.chunk(content)
		for index, chunk in enumerate(chunks):
			documents.append(
				Document(
					id=f"{path.stem}#{index}",
					content=chunk,
					metadata=metadata,
				)
			)
		print(f"{path.name}: {len(chunks)} chunks")
	return documents


def run_benchmark(data_dir: Path, chunk_size: int, top_k: int) -> None:
	embedder = select_embedder()
	print(f"Embedding backend: {getattr(embedder, '_backend_name', 'custom')}")

	documents = load_chunked_documents(data_dir, chunk_size)
	store = EmbeddingStore(collection_name="ecommerce_recursive", embedding_fn=embedder)
	store.add_documents(documents)
	print(f"Loaded {len(documents)} chunks with chunk_size={chunk_size}")

	for index, query in enumerate(DEFAULT_QUERIES, start=1):
		print(f"\n[{index}] {query}")
		results = store.search(query, top_k=top_k)
		for rank, result in enumerate(results, start=1):
			print(
				f"  {rank}. score={result['score']:.4f} "
				f"doc_id={result['metadata'].get('doc_id')} "
				f"chunk={result['id']}"
			)
			print(f"     {result['content'][:180].replace(chr(10), ' ')}...")


def main() -> None:
	parser = argparse.ArgumentParser(description="Benchmark recursive chunking and embeddings.")
	parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
	parser.add_argument("--chunk-size", type=int, default=500)
	parser.add_argument("--top-k", type=int, default=3)
	args = parser.parse_args()

	load_dotenv(override=False)
	run_benchmark(args.data_dir, args.chunk_size, args.top_k)


if __name__ == "__main__":
	main()
