import csv
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.few_shot import FewShotPromptTemplate

from langchain.prompts.prompt import PromptTemplate
from example_data import examples




load_dotenv()

def load_csv_to_list(file_path):
    data_list = []
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 각 행을 딕셔너리로 변환하여 리스트에 추가
            data_list.append({
                "id": row["questionId"],
                "test": row["test"],
                "expText": row["expText"],
                "answer": row["answer"]
            })
    return data_list

# 파일 경로를 지정하여 함수를 호출
file_path = "./files/question_01.csv"
parsed_data = load_csv_to_list(file_path)

llm = ChatOpenAI(
    temperature=0.1,
    streaming=True,
    callbacks=[
        StreamingStdOutCallbackHandler(),
    ],
)

example_prompt = PromptTemplate.from_template("Human: {question} {solving} {answer}\nAI:{aiAnswer}")


prompt = FewShotPromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
    suffix="""
    Human :
        Question : {question}
        Solving : {solving}
        Answer : {answer}

        당신은 친절한 수학 선생님입니다.
        무조건 한글로 대답해야해.
        단계별로 풀어서 설명해줘.
    """
    ,
    input_variables=["question", "solving", "answer"],
)


chain = prompt | llm

for item in parsed_data:
    id = item["id"]
    question = item["test"]
    solving = item["expText"]
    answer = item['answer']

    response = chain.invoke({"question" : question, "solving" : solving, "answer" : answer})
    print(response)

