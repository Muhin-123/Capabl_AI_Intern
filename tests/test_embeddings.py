from rag.embeddings import get_embedding_model


model = get_embedding_model()

text = "Database normalization reduces data redundancy."

embedding = model.embed_query(text)

print("Embedding created successfully!")
print("Embedding size:", len(embedding))
print("First 5 values:", embedding[:5])