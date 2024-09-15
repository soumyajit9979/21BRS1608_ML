from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import warnings
from pymongo import MongoClient
from datetime import datetime
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

warnings.filterwarnings("ignore")

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db=client.get_database()
user_collection = db.users
query_collection = db.queries

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.2, convert_system_message_to_human=True)

pdf_loader = PyPDFLoader("./data/doc.pdf")
pages = pdf_loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
context = "\n\n".join(str(p.page_content) for p in pages)
texts = text_splitter.split_text(context)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 5})

template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.

Context:
{context}

Question: {question}
Top K Results: 5
Threshold: 0.5

Provide the top 5 answers based on the context, where each answer should include:
1. The answer text.
2. The similarity score of the answer.

Only include results where the similarity score is greater than or equal to the threshold, also give each answer in new line. 

Format your response as a list of answers with their similarity scores:
1. Answer 1: [Answer Text] (Score: [Similarity Score])
2. Answer 2: [Answer Text] (Score: [Similarity Score])
...
5. Answer 5: [Answer Text] (Score: [Similarity Score])

If no results meet the threshold, say "No relevant answers found." 
Thanks for asking!"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vector_index,
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user', methods=['POST'])
def handle_user():
    data = request.get_json()
    user_type = data.get('user_type')
    user_name = data.get('user_name', '')
    
    if user_type == 'new':
        user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        user_collection.insert_one({"user_id": user_id, "frequency": 1, "user_name": user_name})
        return jsonify({"status": "new", "user_id": user_id})
    elif user_type == 'old':
        user_id = data.get('user_id', '')
        user = user_collection.find_one({"user_id": user_id})
        if user:
            if user['frequency'] >= 5:
                return jsonify({"error": "User limit exceeded"}), 403
            user_collection.update_one({"user_id": user_id}, {"$inc": {"frequency": 1}})
            return jsonify({"status": "existing", "user_id": user_id})
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Invalid user type"}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        user_id = data.get('user_id', '')
        question = data.get('question', '')

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        user = user_collection.find_one({"user_id": user_id})
        if user:
            if user['frequency'] >= 5:
                return jsonify({"error": "User limit exceeded"}), 403
            user_collection.update_one({"user_id": user_id}, {"$inc": {"frequency": 1}})
        else:
            return jsonify({"error": "User not found"}), 404

        result = qa_chain({"query": question})

        query_collection.insert_one({
            "user_id": user_id,
            "question": question,
            "answer": result["result"],
            "timestamp": datetime.utcnow()
        })

        return jsonify({
            'answer': result["result"],
            'sources': [doc.page_content for doc in result["source_documents"]]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/search')
def queries():
    return render_template('queries.html')

@app.route('/user/queries', methods=['POST'])
def get_user_queries():
    data = request.get_json()
    user_id = data.get('user_id', '')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    queries = list(query_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(5))
    return jsonify({
        'queries': [{"question": q["question"], "answer": q["answer"], "timestamp": q["timestamp"].strftime('%Y-%m-%d %H:%M:%S')} for q in queries]
    })

if __name__ == "__main__":
    app.run(debug=True)
