TOPIC_SPACE = [
     "programming",
    "language",
    "backend",
    "web",
    "automation",
    "scripting",
    "machine_learning",
    "deep_learning",
    "artificial_intelligence",
    "computer_vision",
    "nlp",
    "data_science",
    "data_analysis",
    "scientific_computing",
    "mathematics",
    "database"
]

KNOWLEDGE_BASE = {
   
# PYTHON
"python": {
     "document_boost": 1.2,
    "category": "language",
    "aliases": ["py"],
    "topics": {
        "programming": 1.0,
        "language": 1.0,
        "backend": 0.8,
        "automation": 0.8,
        "scripting": 0.8,
        "data_science": 0.7,
        "machine_learning": 0.7,
        "web": 0.6
    },
    "relations": [
        "programming",
        "coding",
        "script",
        "fastapi",
        "django",
        "flask",
        "numpy",
        "pandas",
        "pytorch",
        "tensorflow"
    ]
    
},

# PYTORCH
"pytorch": {
    "document_boost": 1.1,
    "category": "framework",
    "aliases": ["torch"],
    "topics": {
        "artificial_intelligence": 1.0,
        "deep_learning": 1.0,
        "machine_learning": 0.9,
        "computer_vision": 0.8,
        "nlp": 0.8,
        "data_science": 0.6
    },
    "relations": [
        "python",
        "tensorflow",
        "machine learning",
        "deep learning",
        "neural network",
        "computer vision",
        "nlp"
    ]
},


# TENSORFLOW
"tensorflow": {
      "document_boost": 1.1,
    "category": "framework",
    "aliases": ["tf"],
    "topics": {
        "artificial_intelligence": 1.0,
        "deep_learning": 1.0,
        "machine_learning": 0.9,
        "computer_vision": 0.8,
        "nlp": 0.7,
        "data_science": 0.6
    },
    "relations": [
        "python",
        "pytorch",
        "machine learning",
        "deep learning",
        "neural network",
        "computer vision",
        "nlp"
    ]
},


# NUMPY
"numpy": {
      "document_boost": 1.05,
    "category": "library",
    "aliases": ["np"],
    "topics": {
        "python": 1.0,
        "data_science": 1.0,
        "scientific_computing": 1.0,
        "machine_learning": 0.8,
        "mathematics": 0.8
    },
    "relations": [
        "python",
        "pandas",
        "scipy",
        "matrix",
        "array"
    ]
},

# PANDAS
"pandas": {
      "document_boost": 1.05,
    "category": "library",
    "aliases": ["pd"],
    "topics": {
        "python": 1.0,
        "data_science": 1.0,
        "data_analysis": 1.0,
        "machine_learning": 0.8,
        "database": 0.6
    },
    "relations": [
        "python",
        "numpy",
        "csv",
        "dataframe",
        "excel"
    ]
},


# MACHINE LEARNING
"machine learning": {
    "aliases": ["ml"],
    "topics": {
        "artificial_intelligence": 1.0,
        "machine_learning": 1.0,
        "data_science": 0.9,
        "deep_learning": 0.7
    },
    "relations": [
        "deep learning",
        "python",
        "tensorflow",
        "pytorch",
        "scikit-learn"
    ]
},

# DEEP LEARNING


"deep learning": {
    "aliases": ["dl"],
    "topics": {
        "artificial_intelligence": 1.0,
        "deep_learning": 1.0,
        "machine_learning": 0.9,
        "computer_vision": 0.8,
        "nlp": 0.8
    },
    "relations": [
        "machine learning",
        "tensorflow",
        "pytorch",
        "neural network"
    ]
},


# NLP
"nlp": {
    "aliases": [
        "natural language processing"
    ],
    "topics": {
        "artificial_intelligence": 1.0,
        "nlp": 1.0,
        "deep_learning": 0.8,
        "machine_learning": 0.8
    },
    "relations": [
        "python",
        "pytorch",
        "transformer",
        "bert",
        "llm"
    ]
},


"scipy": {
    "aliases": [],
    "topics": {
        "python": 1.0,
        "scientific": 1.0
    },
    "relations": [
        "numpy"
    ]
},

"machine_learning": {
    "aliases": [
        "ml"
    ],
    "topics": {
        "machine_learning": 1.0,
        "deep_learning": 0.7
    },
    "relations": [
        "tensorflow",
        "pytorch",
        "sklearn"
    ]
},

"deep_learning": {
    "aliases": [
        "dl"
    ],
    "topics": {
        "deep_learning": 1.0
    },
    "relations": [
        "tensorflow",
        "pytorch"
    ]
},

"sklearn": {
    "aliases": [
        "scikit-learn"
    ],
    "topics": {
        "machine_learning": 1.0,
        "python": 0.9
    },
    "relations": [
        "python",
        "numpy",
        "pandas"
    ]
},
}



