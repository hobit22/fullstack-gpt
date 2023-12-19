import csv
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.few_shot import FewShotPromptTemplate

from langchain.prompts.prompt import PromptTemplate



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


examples =[
    {
        "question" : "$x$에 대한 방정식 $a^2x+a-2ax-2=0$의 해가 무수히 많을 때, 상수 $a$의 값은?",
        "solving" : """
$a^2x+a-2ax-2=0$에서  
$a(a-2)x=-(a-2)$
이다. 이 방정식의 해가 무수히 많으려면 
$a(a-2)=0,\quad -(a-2)=0$
이어야 한다. 따라서 구하는 상수 $a$의 값은 $2$이다. 
        """
        ,
        "answer" : "$2$",
        "aiAnswer": 
        """
이 문제를 해결하기 위해서는 방정식의 기본 이해와 해의 존재 조건을 파악하는 것이 중요합니다. 문제는 주어진 방정식  $a^2x+a-2ax-2=0$의 해가 무수히 많을 때, 상수 
a의 값을 찾는 것입니다.

문제 이해

주어진 방정식:  $a^2x+a-2ax-2=0
구해야 하는 것: 방정식의 해가 무수히 많을 때, 상수 a의 값

해결 방법

1.방정식을 간소화합니다:
     $a^2x+a-2ax-2=0$
     => $a(a-2)x=-(a-2)$
2.방정식의 해가 무수히 많으려면, 방정식의 좌변과 우변이 항상 0이 되어야 합니다. 즉, 
    $a(a-2)=0$ 이고, $-(a-2)=0$이어야 합니다.
3.이 두 조건을 만족하는 a의 값을 찾습니다:
    첫번째 조건 $a(a-2)=0$ 에서 $a=0$ 또는 $a=2$이 됩니다.
    두번째 조건 $-(a-2)=0$ 에서 $a=2$ 가 됩니다.
4.따라서, 두 조건을 모두 만족하는 $a$의 값은 2입니다.

해답
- 상수 $a$ 값은 2입니다.
        """
    },
    
#     {
#         "question" : "태양계에는 수성, 금성, 지구, 화성, 목성, 토성, 천왕성, 해왕성의 $8$개의 행성이 있다. 이들은 물리적 특성에 따라 지구형 행성과 목성형 행성으로 나뉘고, 지구 공전 궤도를 기준으로 내행성과 외행성으로 나뉜다. 수성, 금성, 지구, 화성은 지구형 행성이고, 나머지 $4$개의 행성은 목성형 행성이다. 지구형 행성, 목성형 행성, 내행성, 외행성의 집합을 각각 $A$, $B$, $C$, $D$라고 할 때, 두 집합 $A$, $C$사이의 포함 관계를 기호로 나타면? ",
#         "solving" : """
# 지구형 행성은 수성, 금성, 지구, 화성이므로 
# $A=\{ \hbox\{수성, 금성, 지구, 화성\}\}$
# 이고, 목성형 행성은 목성, 토성, 천왕성, 해왕성이므로 
# $B=\{ \hbox\{목성, 토성, 천왕성, 해왕성\}\}$
# 이다. 또한 내행성은 수성, 금성이므로 
# $C=\{ \hbox\{수성, 금성\}\}$
# 이고, 외행성은 화성, 목성, 토성, 천왕성, 해왕성이므로 
# $D=\{ \hbox\{화성, 목성, 토성, 천왕성, 해왕성\}\}$
# 이다. 따라서 $\hbox\{수성\} \in A$이고, $\hbox\{금성\} \in A$이므로 내행성은 모두 지구형 행성이다. 그러므로
# $C \subset A$
# 이다.
#         """
#         ,
#         "answer" : "$A \supset C$",
#         "aiAnswer": 
#         """
# 이 문제는 집합론과 천문학적 지식을 결합하여 해결합니다. 주어진 정보를 바탕으로 지구형 행성과 내행성에 해당하는 행성들의 집합을 정의하고, 이들 집합 간의 포함 관계를 파악하는 것이 중요합니다.

# 문제 이해
#  - 지구형 행성 집합 $A: 수성, 금성, 지구, 화성
#  - 목성형 행성 집합 $B: 목성, 토성, 천왕성, 해왕성
#  - 내행성 집합 $C: 수성, 금성
#  - 외행성 집합 $D: 화성, 목성, 토성, 천왕성, 해왕성
#  - 구해야 하는 것: 집합 $A와 $C 사이의 포함 관계

# 해결 방법
# 1. 집합 $A와 $C를 정의합니다:
#     $A=\{ \hbox\{수성, 금성, 지구, 화성\}\}$
#     $C=\{ \hbox\{수성, 금성\}\}$
# 2. 집합 $C의 모든 원소는 집합 $A에도 포함됩니다. 즉, $C는 $A의 부분집합입니다.
# 3. 수학적으로, 한 집합이 다른 집합의 부분집합일 때, 큰 집합은 작은 집합을 포함합니다. 따라서, $A는 $C를 포함합니다.
# 4. 이 포함 관계는 수학적 기호로 A⊃C로 표현됩니다.

# 해답
# 두 집합 $A$와 $C$ 사이의 포함 관계는 A⊃C입니다.
#         """
#     }
]

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

