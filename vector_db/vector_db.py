import os
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv()


class FeedbackDB:
    def __init__(self, positive_feedback_file, negative_feedback_file):
        self.embeddings = OpenAIEmbeddings()

        # Load or initialize positive feedback database
        if os.path.exists(positive_feedback_file):
            self.positive_db = FAISS.load_local(
                positive_feedback_file,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            # Initialize with a placeholder document
            self.positive_db = FAISS.from_texts(["placeholder"], self.embeddings)
            self.positive_db.delete([self.positive_db.index_to_docstore_id[0]])

        # Load or initialize negative feedback database
        if os.path.exists(negative_feedback_file):
            self.negative_db = FAISS.load_local(
                negative_feedback_file,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            # Initialize with a placeholder document
            self.negative_db = FAISS.from_texts(["placeholder"], self.embeddings)
            self.negative_db.delete([self.negative_db.index_to_docstore_id[0]])

        self.positive_feedback_file = positive_feedback_file
        self.negative_feedback_file = negative_feedback_file



    def add_feedback(self, query, response, chain_of_thought, feedback_type):
        feedback_dict = {
            "response": response.lower(),
            "chain_of_thought": str(chain_of_thought).lower(),
            "timestamp": str(datetime.now()).lower(),
        }
        document = Document(page_content=query, metadata=feedback_dict)
        
        if feedback_type == "positive":
            self.positive_db.add_documents([document])
            logging.info("Added positive feedback.")
        elif feedback_type == "negative":
            self.negative_db.add_documents([document])
            logging.info("Added negative feedback.")
        else:
            raise ValueError("Feedback type must be 'positive' or 'negative'")
        
        self.positive_db.save_local(self.positive_feedback_file)
        self.negative_db.save_local(self.negative_feedback_file)



    def search_similar_queries(self, query, k=3):
        embedding_vector = self.embeddings.embed_query(query)

        pos_docs_and_scores = self.positive_db.similarity_search_by_vector(
            embedding_vector, k=k
        )
        neg_docs_and_scores = self.negative_db.similarity_search_by_vector(
            embedding_vector, k=k
        )
        positive_results = [
            (doc.page_content, doc.metadata) for doc in pos_docs_and_scores
        ]
        negative_results = [
            (doc.page_content, doc.metadata) for doc in neg_docs_and_scores
        ]
        print(positive_results)
        return positive_results, negative_results
