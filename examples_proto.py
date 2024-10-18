# Importing necessary modules and libraries
import os  # For interacting with the operating system
import getpass  # For securely getting user input (e.g., passwords)
import json  # For handling JSON data
from typing import List, Dict  # For type hinting

# Importing specific modules for document handling and embeddings
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer

# Importing OpenAI embeddings module (commented out)
# from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import (
    cosine_similarity,
)  # For calculating cosine similarity
import numpy as np  # For numerical computing


# Defining a class for simple vector store operations
class SimpleVectorStore:
    def __init__(self, embeddings, documents):
        self.embeddings = embeddings
        self.documents = documents

    # Method for performing similarity search
    def similarity_search(self, query, embed_function, k=5):
        query_embedding = embed_function.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        return [self.documents[i] for i in top_k_indices]


# Defining a class for retrieving examples
class ExampleRetriever:
    OPENAI = "OPENAI_API_KEY"

    def __init__(self, embed_function, keyname=None, directory="examples/examples"):
        self.function = embed_function
        if keyname is not None:
            os.environ[keyname] = getpass.getpass("API Key:")
        docs = []
        for filename in os.listdir(directory):
            if not os.path.isfile(os.path.join(directory, filename)):
                continue
            if not filename.endswith(".json"):
                continue

            with open(os.path.join(directory, filename), "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    for example in data:
                        docs.append(
                            Document(
                                page_content=json.dumps(example["query"]),
                                metadata={
                                    "source": filename,
                                    "solution": example["solution"],
                                },
                            )
                        )
                else:
                    docs.append(
                        Document(
                            page_content=json.dumps(data["query"]),
                            metadata={"source": filename, "solution": data["solution"]},
                        )
                    )

        embeddings = embed_function.encode([doc.page_content for doc in docs])
        self.vectorstore = SimpleVectorStore(embeddings, docs)

    # Method for retrieving examples based on a query
    def retrieve(self, query, k=5):
        response_docs = self.vectorstore.similarity_search(query, self.function, k=k)
        topk = [
            {"query": x.page_content, "solution": x.metadata["solution"]}
            for x in response_docs
        ]
        return topk


# Function for creating a SentenceTransformer model
def bge(model="all-MiniLM-L6-v2", device="cpu"):
    return SentenceTransformer(model, device=device)


# Function for creating an OpenAI embeddings model (commented out)
# def openai(model_name="text-embedding-ada-002"):
#     return OpenAIEmbeddings(model=model_name)
