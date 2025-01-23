from app.modules.embedding.embedder import get_embeddings

def test_get_embeddings():
    texts = ["Python developer", "Data scientist"]
    print("Processing")
    embeddings = get_embeddings(texts)

    # Output the embeddings
    print("=== Embeddings ===")
    for i, embedding in enumerate(embeddings):
        print(f"Text: {texts[i]}")
        print(f"Embedding: {embedding[:5]}...")  # Print first 5 values for brevity

test_get_embeddings()