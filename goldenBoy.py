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
    model="gpt-3.5-turbo-1106",
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

        through the process of solving a math problem in an interactive and engaging manner. 

        ### Instructions: 
        1. Use Korean as the language of instruction.
        2. Break down the problem step by step, ensuring clarity at each stage.
        3. Encourage the student to actively participate by asking them questions and seeking their input.
        4. Provide relevant examples and real-life applications to help the student understand the concept.
        5. Help the student develop problem-solving skills by guiding them to arrive at the solution independently.

        Context:
        You are working with a student who requires assistance in solving a math problem. The student is struggling with understanding the steps involved and requires a patient and comprehensive explanation in Korean. Your goal is to guide the student through each step, ensuring complete understanding and clarity.

        Outcome:
        The student should gain a thorough understanding of the math problem and should be able to solve similar problems independently..
    """
    ,
    input_variables=["question", "solving", "answer"],
)


chain = prompt | llm

for item in parsed_data[:5]:
    id = item["id"]
    question = item["test"]
    solving = item["expText"]
    answer = item['answer']

    response = chain.invoke({"question" : question, "solving" : solving, "answer" : answer})
    print(response)

