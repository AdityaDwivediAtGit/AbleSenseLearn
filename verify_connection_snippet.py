from langchain_openai import ChatOpenAI
import os
import httpx

# Configuration provided by user
BASE_URL = "https://genailab.tcs.in"
MODEL_NAME = "azure_ai/genailab-maas-DeepSeek-V3-0324"
API_KEY = "sk-8kFJg-Z38YxPwa4pSuls0g"

print(f"Testing connection to {BASE_URL} with model {MODEL_NAME}...")

try:
    client = httpx.Client(verify=False)

    llm = ChatOpenAI(
        base_url=BASE_URL,
        model=MODEL_NAME,
        api_key=API_KEY,
        http_client=client
    )

    print("Invoking model...")
    response = llm.invoke("Hi")
    print("\n--- Response ---")
    print(response.content)
    print("--- End Response ---")
    print("\nSUCCESS: Connection established and response received.")

except Exception as e:
    print(f"\nFAILURE: {str(e)}")
