import sqlite3

DB_FILE = 'profile.db'

documents = [
    ('cv', 'contact and summary',
     """Muhammad Adel - AI Engineer / Data Scientist.
Location: New Cairo, Cairo, Egypt. Phone: 01155559888. Email: muhammadaddell@gmail.com.
Professional summary: AI Engineer / Data Scientist with 1+ year of professional experience in AI data annotation,
supported by hands-on machine learning and deep learning projects. Skilled in Python, SQL, machine learning, NLP,
LLMs, time-series modeling, and modern AI/ML tools, with experience applying these skills to real-world and
academic problems."""),

    ('cv', 'professional experience',
     """Muhammad Adel professional experience (from his CV):
Data Annotator at CNTXT AI (UAE), January 2025 - January 2026. Performed data annotation tasks supporting AI dataset
development and model-training workflows. Applied annotation guidelines consistently to maintain data quality and
label accuracy across assigned datasets. Worked within structured processes to review, classify, and prepare data
for AI applications.
Data Entry at Tazkarti, April 2019 - December 2019. Entered and maintained structured records with attention to
accuracy and consistency. Handled repetitive data-processing tasks while following defined formatting and workflow
requirements. Supported day-to-day operational data needs through organized and timely record updates."""),

    ('cv', 'education',
     """Muhammad Adel education: British University in Egypt (BUE), Faculty of Informatics & Computer Science,
graduated 2024."""),

    ('cv', 'selected projects',
     """Muhammad Adel selected projects (from his CV):
Fault Detection and Early Alert for Real Water Desalination Plant (2024): built a real-time fault-detection approach
for a water desalination plant using time-series and deep learning methods. Applied Graph Neural Networks (GNN),
Artificial Neural Networks (ANN), and other deep learning models to process plant data. Focused on early warning of
faults through model-based monitoring of system behavior.
Facial Recognition (academic project): machine-learning-based facial recognition and identification, using
classification techniques to distinguish and identify faces from input data.
Twitter Sentiment Analysis (academic project): NLP classification of Twitter/X posts as positive or negative, with
text preprocessing and machine learning techniques to evaluate sentiment labels on tweet data."""),

    ('cv', 'technical skills',
     """Muhammad Adel technical skills:
Machine Learning & AI: Machine Learning, Deep Learning, NLP, LLMs, Time Series, Reinforcement Learning, ANN, CNN,
RNN, GNN, Transformers, MLOps, Algorithms, AI Planning for Robot Systems.
Frameworks & Data Tools: Scikit-learn, TensorFlow, PyTorch, Keras, FastAPI, MLflow, Pandas, NumPy, Streamlit.
Programming languages: Python, Java, JavaScript, SQL, Assembly Language, PHP, C++, C.
Web & Databases: HTML5, CSS3, Bootstrap 5, Oracle, MySQL, MongoDB.
DevOps & BI: Git, Docker, Power BI.
Core competencies: adaptability and fast learning, problem solving, communication and teamwork, time management."""),

    ('linkedin', 'headline and about',
     """LinkedIn profile of Muhammad Adel.
Headline: AI Engineer / Data Scientist | NLP Intern at Cellula Technologies. Location: New Cairo, Cairo, Egypt.
About: AI Engineer / Data Scientist with more than one year of professional experience in AI data annotation,
supported by hands-on machine learning and deep learning projects. Works with Python, SQL, machine learning, NLP,
LLMs, time-series modeling and modern AI/ML tools. Currently doing the Cellula Technologies NLP internship, building
transformer, LangChain and RAG projects. Languages: Arabic, English."""),

    ('linkedin', 'experience - Cellula Technologies',
     """Muhammad Adel current role: NLP Intern at Cellula Technologies (2026). Weekly applied NLP tasks reviewed by the
Cellula engineering team.
Week 1: toxic content classification (RNN, LSTM, DistilBERT with LoRA, BLIP image captioning, Streamlit app) and
research about quantization.
Week 2: LLM output configuration (temperature, top-k, top-p), the BERT family and the LLaMA family.
Week 3: LangChain (prompt templates, system prompting, few-shot prompting, output parsers, memory), a personal RAG
system, and research about the BigBird transformer."""),

    ('linkedin', 'experience - before Cellula',
     """Muhammad Adel work experience before the Cellula internship:
Data Annotator at CNTXT AI (UAE), January 2025 - January 2026, data annotation for AI dataset development and model
training workflows.
Data Entry at Tazkarti, April 2019 - December 2019, his first job, entering and maintaining structured records."""),

    ('github', 'Cellula_1week_Muhammad_Adel - DistilBERT LoRA classifier',
     """GitHub repository Cellula_1week_Muhammad_Adel (Cellula internship week 1) by Muhammad Adel.
Language: Python. Libraries: PyTorch, transformers, peft, streamlit, nltk.
Toxic content classification app: fine-tunes distilbert-base-uncased with LoRA adapters (r=16, lora_alpha=32,
dropout 0.1, on q_lin and v_lin) with a 2-layer bidirectional LSTM head (bert_lstm) or a 2-layer bidirectional RNN
head (bert_rnn), hidden size 300. Image captioning with Salesforce BLIP (blip-image-captioning-base), the caption is
classified together with the text. max_len = 47 tokens chosen from the token length distribution, seed 42,
2424 rows after cleaning, 485 validation and 485 test rows.
Test results: bert_lstm macro F1 0.907 (accuracy 0.930), bert_rnn macro F1 0.916 (accuracy 0.932).
9 classes: Child Sexual Exploitation, Elections, Non-Violent Crimes, Safe, Sex-Related Crimes, Suicide & Self-Harm,
Unknown S-Type, Violent Crimes, unsafe."""),

    ('github', 'Cellula_1week_Muhammad_Adel - LSTM and RNN from scratch',
     """GitHub repository Cellula_1week_Muhammad_Adel, LSTM/ and RNN/ folders by Muhammad Adel: text classifiers built
from scratch in PyTorch. Input is the query plus the image description, tokenized with NLTK. 2-layer bidirectional
LSTM / RNN, embedding 128, hidden 128, dropout 0.3, masked mean pooling, AdamW, 10 epochs, best checkpoint by
validation macro F1. Test macro F1: LSTM 0.815 (accuracy 0.94), RNN 0.823 (accuracy 0.93).
Task0 folder: quantization research (quantization_research.py)."""),

    ('github', 'Cellula_3week_Muhammad_Adel - personal RAG',
     """GitHub repository Cellula_3week_Muhammad_Adel (Cellula internship week 3) by Muhammad Adel.
Language: Python. Libraries: LangChain, FAISS, sentence-transformers, Streamlit, SQLite3.
Task 1 - personal RAG system: his CV, LinkedIn, GitHub, portfolio and certification information is stored in a
SQLite3 database, split into chunks with TokenTextSplitter, embedded with sentence-transformers/all-MiniLM-L6-v2 and
stored in a FAISS vector database. The Streamlit app retrieves the most similar chunks, sends them to an LLM on
OpenRouter, shows the answer with the source of every chunk, and saves each question and answer in SQLite3.
Task 0 - research about BigBird (sparse attention) with a CPU benchmark of block_sparse vs original_full attention
in Hugging Face: at 4096 tokens block_sparse was 3.7x faster and at 8192 tokens 4.6x faster."""),

    ('portfolio', 'Toxic Content Classifier',
     """Portfolio project of Muhammad Adel: Toxic Content Classifier (Cellula internship, 2026).
Problem: classify user content (a text query plus an image) into 9 safety classes, where some classes have very few
examples. Solution: images are turned into captions with Salesforce BLIP, the caption is joined with the user text,
and a DistilBERT model fine-tuned with LoRA plus a bidirectional LSTM or RNN head predicts the class. No rare class
was deleted, the rare classes were grown with new examples instead.
Results: macro F1 0.907 (LSTM head) and 0.916 (RNN head) on the test split. Deployed as a Streamlit app."""),

    ('portfolio', 'Quantization Research',
     """Portfolio project of Muhammad Adel: Quantization Research (Cellula internship, 2026).
Research about making large models like BERT and LLaMA smaller with quantization, with PyTorch code.
Dynamic INT8 quantization of a small LSTM: size 1.3 MB to 1.0 MB and macro F1 0.727 to 0.726 (almost no loss), but
CPU latency went from 63 ms to 138 ms because the model is tiny. Static INT8 quantization of an MLP: macro F1 0.518
to 0.507."""),

    ('portfolio', 'BigBird Research and Personal RAG',
     """Portfolio project of Muhammad Adel: BigBird research (Cellula internship, 2026). Studied block sparse attention
(window, global and random blocks, block size 64), its linear O(n) complexity compared with BERT's quadratic O(n^2)
attention and with Longformer, and benchmarked it on CPU.
Portfolio project: Personal RAG System (Cellula internship, 2026), LangChain + FAISS + sentence-transformers
retrieval over his own professional information stored in SQLite3, a Streamlit interface, answers that cite their
sources, and a SQLite3 log of all questions and answers."""),

    ('portfolio', 'Water Desalination Fault Detection',
     """Portfolio project of Muhammad Adel: Fault Detection and Early Alert for a Real Water Desalination Plant (2024,
graduation-year project). Real-time fault detection using time-series and deep learning methods: Graph Neural
Networks (GNN), Artificial Neural Networks (ANN) and other deep learning models on real plant data, focused on early
warning of faults."""),

    ('certifications', 'certifications, courses and training',
     """Certifications, courses and training of Muhammad Adel:
Cellula Technologies NLP Internship (2026): toxic content classification, quantization research, LLM sampling
(temperature, top-k, top-p), BERT and LLaMA families, LangChain, RAG and BigBird research.
Artificial Intelligence - Practical On-the-Job Training, ICT HUB Egypt, 30 August 2023 - 20 September 2023,
Grade: Excellent.
Introduction to GEIT, ITIDA, 28 February 2023.
Enterprise Blockchain for Digital Government, ITIDA, 22 February 2023.
Bachelor degree: British University in Egypt, Faculty of Informatics & Computer Science, graduated 2024."""),
]

conn = sqlite3.connect(DB_FILE)
conn.execute('drop table if exists documents')
conn.execute('create table documents '
             '(id integer primary key autoincrement, source text, title text, content text)')
conn.executemany('insert into documents (source, title, content) values (?,?,?)', documents)
conn.execute('create table if not exists qa_log (id integer primary key autoincrement, '
             'timestamp text, question text, answer text, sources text)')
conn.commit()

for source, n in conn.execute('select source, count(*) from documents group by source'):
    print(source, ':', n, 'rows')
conn.close()
print('saved in', DB_FILE)
