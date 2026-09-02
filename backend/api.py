from fastapi import FastAPI
from backend.models.query import Query
from backend.services.query.autocomplete import autocomplete
from backend.services.search.index import build_index
from fastapi.middleware.cors import CORSMiddleware
from backend.services.search_engine import SearchEngine


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

documents = [
    "Python is a programming language",
    "Machine learning uses data",
    "PyTorch is used for deep learning",
    "Python and machine learning are powerful",
    "Data science uses Python",
    
    "Python programming tutorial for beginners",

    "Learn Python from scratch",

    "Advanced Python course",

    

   

    "Natural language processing with Python",

    "Python ebook pdf",



    "Artificial intelligence tutorial pdf",

    "Data science course",

    "Computer vision using Python",

    "Neural network tutorial",

    "TensorFlow complete course",

    "PyTorch beginner guide",

    "Learn data structures in Python",

    "Algorithms course pdf",

    "Java programming tutorial",

    "C++ programming course",

    "JavaScript ebook",

    "HTML CSS complete tutorial",

    "SQL database tutorial",

    "MongoDB course",

    "FastAPI documentation",

    "ElasticSearch beginner guide",

    "Information retrieval systems",

    "Search engine architecture",

    "NLP lecture notes pdf",

    "Deep learning research paper",

    "Python cheat sheet pdf",

    "Software engineering course",
    
    "Programming fundamentals",

    "Coding best practices",

    "Script automation guide",

    "Automobile engineering handbook",

    "Vehicle maintenance tutorial",

    "Artificial intelligence handbook"  
]
index = build_index(documents)
engine=SearchEngine(documents,index)

@app.get("/search")
def search_api(q: str):
    query = Query(q)
    query, results = engine.search(query)

    return {
        "query":query.original_query,
        "tokens":query.tokens,
        "expanded_tokens": query.expanded_tokens,
        "expansion_reason":query.expansion_reason,
        "intents": query.intents,
        "results":results,
        "stats":{

    "documents_scanned": len(documents),
    "returned_results": len(results),
    "original_tokens": len(query.tokens),
    "expanded_tokens": len(query.expanded_tokens),
    "added_terms": len(query.expanded_tokens)-len(query.tokens)

}
    }


@app.get("/suggest")
def suggest(q: str):
    return autocomplete(q, index)


@app.get("/")
def home():
    return {"message": "Smart Search Engine"}


