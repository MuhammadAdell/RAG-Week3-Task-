import os
import sqlite3
import pandas as pd
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from create_vector_db import DB_FILE, build_vector_db


load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.env'),
            override=True)

st.title('My personal RAG')
st.caption('Questions about my cv, linkedin, github, portfolio, certifications, experience')

if not os.path.exists(DB_FILE):
    st.error('no profile.db , run seed_database.py first')
    st.stop()


@st.cache_resource
def get_vector_db():
    return build_vector_db(DB_FILE)


vectorDB, n_docs, n_chunks = get_vector_db()
st.sidebar.write(f'{n_docs} docs / {n_chunks} chunks')

api_key = ((os.environ.get('OPENROUTER_API_KEY') or '').strip()
           or st.sidebar.text_input('openrouter api key', type='password').strip())
llm = None
if api_key:
    llm = ChatOpenAI(
        api_key=api_key,
        base_url='https://openrouter.ai/api/v1',
        model='openrouter/free',
        temperature=0.8,
    )

system_prompt = SystemMessage(
    'Answer only from the notes. No invented dates, companies, numbers or links. '
    'If the notes do not cover it, say so.')

example_prompt = PromptTemplate(
    input_variables=['Question', 'context', 'Answer'],
    template='Question: {Question}\nNotes: {context}\nAnswer: {Answer}')

examples = [
    {'Question': 'how can i contact muhammad?',
     'context': '[1] cv - contact and summary\nNew Cairo, Egypt. 01155559888. muhammadaddell@gmail.com.',
     'Answer': 'Based in New Cairo, Egypt. Phone 01155559888, email muhammadaddell@gmail.com [1].\nSources: cv - contact and summary'},

    {'Question': 'where did muhammad study?',
     'context': '[1] cv - education\nBUE, Faculty of Informatics and Computer Science, 2024.',
     'Answer': 'BUE, Faculty of Informatics and Computer Science, 2024 [1].\nSources: cv - education'},

    {'Question': 'what does muhammad do at cellula?',
     'context': '[1] linkedin - experience - Cellula Technologies\nNLP Intern at Cellula Technologies.',
     'Answer': 'NLP Intern at Cellula Technologies [1].\nSources: linkedin - experience - Cellula Technologies'},

    {'Question': 'where did muhammad work before cellula?',
     'context': '[1] cv - professional experience\nData Annotator at CNTXT AI, Jan 2025 - Jan 2026.\n[2] cv - professional experience\nData Entry at Tazkarti, Apr 2019 - Dec 2019.',
     'Answer': 'Data Annotator at CNTXT AI [1] and Data Entry at Tazkarti [2].\nSources: cv - professional experience'},

    {'Question': 'what is his headline on linkedin?',
     'context': '[1] linkedin - headline and about\nAI Engineer / Data Scientist | NLP Intern at Cellula Technologies.',
     'Answer': 'AI Engineer / Data Scientist, NLP Intern at Cellula Technologies [1].\nSources: linkedin - headline and about'},

    {'Question': 'what skills does he have?',
     'context': '[1] cv - technical skills\nPython, SQL, machine learning, NLP, LLMs, TensorFlow, PyTorch.',
     'Answer': 'Python, SQL, ML, NLP, LLMs, TensorFlow and PyTorch [1].\nSources: cv - technical skills'},

    {'Question': 'what projects are on his cv?',
     'context': '[1] cv - selected projects\nWater desalination fault detection with GNN/ANN.\n[2] cv - selected projects\nFacial recognition academic project.\n[3] cv - selected projects\nTwitter sentiment analysis academic project.',
     'Answer': 'Fault detection on a water desalination plant [1], facial recognition [2], and Twitter sentiment analysis [3].\nSources: cv - selected projects'},

    {'Question': 'what is on his github?',
     'context': '[1] github - LSTM and RNN from scratch\nRNN and LSTM built from scratch.\n[2] github - personal RAG\nLangChain + FAISS over a SQLite3 store.\n[3] github - DistilBERT LoRA classifier\nDistilBERT + LoRA for toxic text.',
     'Answer': 'An RNN/LSTM from scratch [1], a personal RAG app on SQLite3 [2], and a DistilBERT LoRA toxic-text classifier [3].\nSources: github - LSTM and RNN from scratch, github - personal RAG, github - DistilBERT LoRA classifier'},

    {'Question': 'what is in his portfolio?',
     'context': '[1] portfolio - Toxic Content Classifier\nDistilBERT + LoRA + LSTM/RNN, 9 safety classes.\n[2] portfolio - BigBird Research and Personal RAG\nBlock sparse attention study plus a RAG build.\n[3] portfolio - Water Desalination Fault Detection\nGNN/ANN fault detection on a real plant.',
     'Answer': 'Toxic content classifier [1], BigBird research with a personal RAG build [2], and fault detection on a water desalination plant [3].\nSources: portfolio - Toxic Content Classifier, portfolio - BigBird Research and Personal RAG, portfolio - Water Desalination Fault Detection'},

    {'Question': 'what certifications does he have?',
     'context': '[1] certifications - certifications, courses and training\nCellula NLP internship, ICT HUB AI training, GEIT, ITIDA blockchain.',
     'Answer': 'Cellula NLP internship, ICT HUB AI training, GEIT and ITIDA blockchain [1].\nSources: certifications - certifications, courses and training'},

    {'Question': 'summarise his background using cv, linkedin and github',
     'context': '[1] cv - education\nBUE, Informatics and Computer Science, 2024.\n[2] linkedin - headline and about\nAI Engineer / Data Scientist.\n[3] github - personal RAG\nLangChain + FAISS + SQLite3.',
     'Answer': 'BUE Informatics 2024 [1], AI Engineer / Data Scientist [2], built a personal RAG app [3].\nSources: cv - education, linkedin - headline and about, github - personal RAG'},

    {'Question': 'short profile from every source',
     'context': '[1] cv - professional experience\nData Annotator at CNTXT AI.\n[2] linkedin - experience - Cellula Technologies\nNLP Intern at Cellula.\n[3] github - personal RAG\nLangChain + FAISS + SQLite3.\n[4] portfolio - Toxic Content Classifier\nDistilBERT + LoRA classifier.\n[5] certifications - certifications, courses and training\nCellula, ICT HUB, GEIT, ITIDA.',
     'Answer': 'Data Annotator at CNTXT AI [1], NLP Intern at Cellula [2], personal RAG app [3], toxic content classifier [4], Cellula/ICT HUB/GEIT/ITIDA training [5].\nSources: cv - professional experience, linkedin - experience - Cellula Technologies, github - personal RAG, portfolio - Toxic Content Classifier, certifications - certifications, courses and training'},

]

suffix = (
    'Use earlier turns only to resolve follow-ups, not for facts.\n'
    'Cite the notes as [1], [2] and end with a Sources: line. 150 words max.\n\n'
    'Conversation:\n{history}\n\nNotes:\n{context}\n\nQuestion:\n{Question}'
)

template = FewShotPromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
    example_separator='\n\n',
    suffix=suffix,
    input_variables=['history', 'context', 'Question'],
)

if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

tab1, tab2, tab3 = st.tabs(['Ask about me', 'Knowledge base', 'Questions log'])

with tab1:
    with st.form('ask_form', clear_on_submit=False):
        query = st.text_input('question', placeholder='Where did Muhammad work before ?')
        clicked = st.form_submit_button('Answer')

    if clicked and query:
        hits = vectorDB.similarity_search_with_score(query, k=6)
        parts, sources = [], []
        for i, (doc, score) in enumerate(hits, 1):
            label = f"{doc.metadata['source']} - {doc.metadata['title']}"
            parts.append(f'[{i}] {label}\n{doc.page_content}')
            sources.append({'n': i, 'source': label, 'distance': round(float(score), 3)})
        context = '\n\n'.join(parts)
        history = st.session_state.memory.load_memory_variables({})['history']

        if not llm:
            st.warning('no api key , showing retrieved chunks')
            st.dataframe(pd.DataFrame(sources), hide_index=True)
            st.code(context)
            result = '(no api key)'
        else:
            prompt = template.format(history=history, context=context, Question=query)
            try:
                with st.spinner('...'):
                    result = llm.invoke([system_prompt, HumanMessage(prompt)]).content
            except Exception as e:
                st.error(f'model call failed: {type(e).__name__}')
                st.dataframe(pd.DataFrame(sources), hide_index=True)
                result = '(model call failed)'
            else:
                st.session_state.memory.save_context({'input': query}, {'output': result})
                st.markdown(result)
                st.dataframe(pd.DataFrame(sources), hide_index=True)

        conn = sqlite3.connect(DB_FILE)
        conn.execute('create table if not exists qa_log (id integer primary key autoincrement, '
                     'timestamp text, question text, answer text, sources text)')
        conn.execute('insert into qa_log (timestamp, question, answer, sources) values (CURRENT_TIMESTAMP,?,?,?)',
                     (query, result, str(sources)))
        conn.commit()
        conn.close()

with tab2:
    conn = sqlite3.connect(DB_FILE)
    st.dataframe(
        pd.read_sql_query('select id, source, title, content from documents', conn),
        hide_index=True, width='stretch')
    conn.close()

    with st.form('add_doc', clear_on_submit=True):
        source = st.selectbox('source', ['cv', 'linkedin', 'github', 'portfolio',
                                         'certifications', 'experience', 'other'])
        title = st.text_input('title')
        content = st.text_area('content')
        if st.form_submit_button('save') and title and content:
            conn = sqlite3.connect(DB_FILE)
            conn.execute('insert into documents (source, title, content) values (?,?,?)',
                         (source, title, content))
            conn.commit()
            conn.close()
            get_vector_db.clear()
            st.rerun()

with tab3:
    conn = sqlite3.connect(DB_FILE)
    has_log = conn.execute(
        "select name from sqlite_master where type='table' and name='qa_log'").fetchone()
    if has_log:
        st.dataframe(
            pd.read_sql_query('select * from qa_log order by id desc', conn),
            hide_index=True, width='stretch')
        if st.button('clear log'):
            conn.execute('delete from qa_log')
            conn.execute("delete from sqlite_sequence where name='qa_log'")
            conn.commit()
            conn.close()
            st.rerun()
    else:
        st.info('nothing logged yet')
    conn.close()
# python3 -m  streamlit run /Users/muhammadadel/Downloads/Cellula_3week_Muhammad_Adel/Task1/app.py 