from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.schema import BaseOutputParser
import json
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
class JsonOutputParser(BaseOutputParser):
    def parse(self, text):
        text = text.replace("```", "").replace("json","")
        return json.loads(text)
    
output_parser = JsonOutputParser()

class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-4",
    streaming=True,
    callbacks=[
        ChatCallbackHandler(),
    ],
)


@st.cache_resource(show_spinner="Embedding file...")
def embed_file():
    cache_dir = LocalFileStore(f".cache/embeddings/case1")
    loader = UnstructuredHTMLLoader('case1.html')
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


def paint_history():
    for message in st.session_state["messages"]:
        send_message(
            message["message"],
            message["role"],
            save=False,
        )


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)

def makePythonFile(input):
    # response에서 content 필드 추출
    content = input.content

    # Python 코드 추출
    # "```python"과 "```" 사이의 내용을 추출
    start = content.find("```python") + len("```python\n")
    end = content.rfind("```")
    python_code = content[start:end].strip()

    # 추출된 Python 코드를 파일로 저장
    file_name = "selenium_code.py"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(python_code)

    print(f"파일 '{file_name}'에 코드 저장 완료.")
    return file_name


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
             너는 HTML 을 파싱하는 전문가야. 
             읽어들인 파일에서 사용자 question의 엘리멘트를 찾아서 실행하는 셀레니움코드를 화면에 보여줘. 
             selenium의 driver는 다음과 같다.
            driver = webdriver.Chrome()
            html 파일 경로는 다음과 같다.
            C:/Users/hoqei/IdeaProjects/fullstack-gpt/case1.html


            Context: {context}
            """,
        ),
        ("human", "{question}"),
    ]
)



st.session_state["messages"] = []

choice = st.selectbox(
    "테스트항목 선택하시면 셀레니움코드가 짜잔~",
    (
        "중1(상)",
        "중1(하)",
    ),
)

retriever = embed_file()
paint_history()
if choice != "":
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )
    with st.chat_message("ai"):
        response = chain.invoke(choice)
        file_name = makePythonFile(response)
        with open(file_name, "r", encoding="utf-8") as file:
            exec(file.read())