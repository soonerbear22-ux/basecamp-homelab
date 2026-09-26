# Architecture

[Overview](../README.md) · [Diagram](../diagrams/basecamp-architecture.md)

Reviewed September 26, 2026 from the project records and a fresh read-only API audit.

## Workload placement

| Host or guest | Role |
| --- | --- |
| Basecamp | Proxmox physical host: i7-9700K, 32 GB RAM, SSD and large HDD |
| core-services — VM 100 | Application interfaces, Docker, metrics, Qdrant, knowledge ingestion, and Homelab API |
| Pi-hole — LXC 101 | DNS filtering separate from the application VM |
| ai-worker — VM 102 | Dedicated RTX 3060 12 GB passthrough; Qwen3-Embedding-4B via Hugging Face Text Embeddings Inference |
| Main Windows PC | Ollama chat inference and ComfyUI image generation; historical voice services |

The September 26 master record identifies Proxmox VE 9.2.0 / pve-manager 9.2.20. This is a recorded version, not a claim that it is the latest release.

## Two distinct AI compute roles

The main PC generates chat responses and images. The Basecamp GPU generates 2560-dimensional embeddings for document ingestion and semantic queries. Embeddings encode text for retrieval; they do not themselves produce a chat answer.

The embedding deployment record identifies the Qwen/Qwen3-Embedding-4B model, float16 inference, and TEI image tag `86-1.9`. Runtime details must be rechecked before rebuilding.

## Knowledge path

Completed documents enter a Samba inbox on core-services. A systemd path unit triggers extraction and chunking, calls ai-worker for embeddings, and writes vectors plus source metadata to Qdrant. Homelab API embeds queries and retrieves relevant chunks. See [pipeline evidence](knowledge-pipeline.md).

## Failure dependencies

All three guests share Basecamp's physical host. Moving Pi-hole outside the Docker VM separates application maintenance from DNS guest maintenance, but does not create physical redundancy. Monitoring hosted on Basecamp shares this failure domain.

The two named large-disk storage destinations share a filesystem. The main PC is a separate dependency for chat and images. A responsive WebUI does not prove every backend is available.
