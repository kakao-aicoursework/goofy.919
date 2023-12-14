import os

import requests
from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv

from db import query_db
from dto import ChatbotRequest


load_dotenv()
assert os.environ["OPENAI_API_KEY"] is not None

"""
Series of Chains
"""

llm = ChatOpenAI(temperature=0, max_tokens=250, model="gpt-3.5-turbo")

parse_intent_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        template="""
            Your job is to select one intent from the <intent_list>. Intent is a proper noun and is a word surrounded by square brackets.

            <intent_list>
            1. [kakao_sync]: This document introduces KakaoSync and guides you through the inspection and settings required to introduce KakaoSync. The Korean word of kakao sync is 카카오 싱크. 
            2. [kakao_channel]: This document introduces the KakaoTalk Social API. KakaoTalk Social API provides the user's KakaoTalk profile and friend information to implement the service's social functions. You can also send KakaoTalk messages based on the provided KakaoTalk friend information. The Korean word of kakao social is 카카오 소셜.
            3. [kakao_social]: This document introduces the KakaoTalk Channel API. The Korean word of kakao social is 카카오 소셜.
            </intent_list>

            User: {user_message}
            Intent: 
        """
    ),
    verbose=True,
)
answer_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        template="""
            Your job is to answer the query based on information.

            <Information>
            {information}
            <Iinformation>

            <Query>
            {query}
            </Query>
        """
    ),
    verbose=True
)

summary_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        template="""
            Your role is to summarize the answer in 3 sentences or so.
            <answer>
             {expert_answer}
            </answer>
        """
    ),
    verbose=True
)




default_chain = ConversationChain(llm=llm)

"""
business logic
"""


def callback_handler(request: ChatbotRequest):
    msg = request.userRequest.utterance

    context = {}
    intent = parse_intent_chain.run(msg)
    if intent in ["kakao_sync", "kakao_channel", "kakao_social"]:
        infos = query_db(msg)
        information_str = "\n".join(infos)

        context['information'] = information_str
        context['query'] = msg

        output = answer_chain.run(context)
    else:
        output = default_chain.run(msg)

    context["expert_answer"] = output
    answer = summary_chain.run(context)

    response_callback(answer, request)


def response_callback(output_text, request):
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": output_text}}
            ]
        }
    }
    url = request.userRequest.callbackUrl

    if url:
        requests.post(url=url, json=payload)
