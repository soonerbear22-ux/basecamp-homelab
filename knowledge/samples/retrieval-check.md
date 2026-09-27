# Basecamp public retrieval check

## Workload placement

Basecamp separates application services, DNS, and GPU embeddings into three guests. The main PC supplies chat inference. This is synthetic public test content, not a copy of the private operational corpus.

## Recovery order

Recover the hypervisor and storage first, then DNS and the guests, then Docker, embeddings, the vector database, the API, and user interfaces. Check dependencies before restarting healthy services.
