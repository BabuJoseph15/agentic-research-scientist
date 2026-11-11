from services.llm_service import llm

response = llm.invoke(
    "What is the relationship between rainfall and dengue outbreaks?"
)

print(response.content)