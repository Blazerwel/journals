from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import pymysql
import google.generativeai as genai
import numpy as np

# Step 1: Initialize Pinecone
pinecone = Pinecone(api_key="pcsk_3rh5fW_TGzca7wx6pze1UQVqhn1schQqyDnN73jMJdPb3grnkixHVFQzsCjgokMg6J3haA")
# Define the index name and embedding dimension
index_name = "database"
embedding_model = "all-MiniLM-L6-v2"
dimension = 384  # Based on the embedding model you choose
# # Step 2: Create Pinecone index (if not already created)
# if index_name not in pinecone.list_indexes().names():
#     pinecone.create_index(
#         name=index_name,
#         dimension=384,
#         metric="cosine",  # Use cosine similarity for embeddings
#         spec=ServerlessSpec(
#             cloud="aws",  # Adjust as necessary
#             region="us-east-1",  # Adjust to your region
#         ),
#     )

# # Initialize embedding list
# embedding_list = []

# Connect to the Pinecone index
index = pinecone.Index(index_name)

# # Step 3: Connect to MySQL and fetch data
# conn = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="",  # Your MySQL password if set
#     database="journals_db",
# )

# cursor = conn.cursor()
# cursor.execute("SELECT ID, extracted_text FROM Journals WHERE ID>1033 AND ID<=1035")  # Replace table and column names as needed
# results = cursor.fetchall()  # Fetch all rows

# # Process the results into a format suitable for embedding
# articles = [{"id": str(row[0]), "content": row[1]} for row in results]

# # Close the database connection
# conn.close()

# Step 4: Generate embeddings using Sentence Transformers
model = SentenceTransformer(embedding_model)

# for article in articles:
#     embeddings = model.encode(article["content"])
#     embedding_list.append({"id": article["id"], "embedding": embeddings, "text": article["content"]})

# # Step 5: Upsert articles into Pinecone
# # Upsert the embeddings into Pinecone
# upsert_data = [
#     {"id": str(article["id"]), "values": article["embedding"], "metadata": {"text": article["text"]}}
#     for article in embedding_list
# ]

# index.upsert(vectors=upsert_data)
# print("Articles have been uploaded to Pinecone.")

# # Step 6: Query Pinecone for similar articles
query_text = "what is angiogenisis "  # Replace with your desired query
query_embedding = model.encode([query_text])[0].tolist()
# Perform the similarity search
result = index.query(vector=query_embedding, top_k=3, include_metadata=True)

# Combine matched content
full_content = ""
for match in result["matches"]:
    content = match["metadata"]["text"]
    full_content += content + ","

# Step 7: Use Google Generative AI to answer the question
genai.configure(api_key='AIzaSyCLTs_6N2XUSFcF5UzTXChl9Pw-spBSoOo')
model = genai.GenerativeModel("gemini-1.5-flash")

# Prepare the prompt
prompt = f"Using the content below, answer this question: {full_content}, question: {query_text}"

# Call the API
try:
    response = model.generate_content(prompt)
    sorted_titles = response.text.strip()
    print("Generated Answer:")
    print(sorted_titles)
except Exception as e:
    print(f"Error generating categories: {e}")
# 382
# 768
# 1000-1050
# 1200-1250
