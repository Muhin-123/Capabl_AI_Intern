from rag.llm import get_llm


llm = get_llm()

response = llm.invoke(
    "Explain database normalization in simple terms."
)

print("\nLLM Response:\n")
print(response.content)