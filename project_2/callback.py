import logging

import os
import aiohttp
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

from dto import ChatbotRequest

# 환경 변수 처리 필요!
with open("./key.txt", "r") as f:
    openai_key = f.read().strip()
    os.environ["OPENAI_API_KEY"] = openai_key
logger = logging.getLogger("Callback")

PROMPT_TEMPLATE_PATH = "./prompt_template/project_data_카카오싱크.txt"
RETURN_MESSAGE_TEMPLATE_PATH = "./prompt_template/return_message_guide.txt"


def create_chain(llm, template_path, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            template=read_prompt_template(template_path),
        ),
        output_key=output_key,
        verbose=True,
    )


async def callback_handler(request: ChatbotRequest) -> str:
    # ===================== start =================================

    llm = ChatOpenAI(temperature=0.1, max_tokens=500, model="gpt-3.5-turbo-16k")

    # advisor template setting
    advisor_chain = create_chain(llm, RETURN_MESSAGE_TEMPLATE_PATH, "answer")

    preprocess_chain = SequentialChain(
        chains=[
            advisor_chain,
        ],
        input_variables=["system_role", "question", "info"],
        verbose=True,
    )

    context = dict(
        system_role="messanger application QA advidor",  # TODO
        question=request.userRequest.utterance,
        info=read_prompt_template(PROMPT_TEMPLATE_PATH)
    )
    context = preprocess_chain(context)
    contents = advisor_chain(context)

    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": contents['answer']
                    }
                }
            ]
        }
    }

    # ===================== end =================================
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format
    url = request.userRequest.callbackUrl
    if url:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=payload, ssl=False) as resp:
                await resp.json()


def read_prompt_template(file_path: str) -> str:
    with open(file_path, 'r') as f:
        promt_template = f.read()
        return promt_template
