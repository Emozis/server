import asyncio
from pathlib import Path 
from functools import partial

from langchain_openai import ChatOpenAI 
from langchain_upstage import ChatUpstage
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage,HumanMessage

from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from ..core import settings
from ..utils.constants import constants as const


class ChatBot:
    # 초기값
    def __init__(
            self,
            user_info="",
            character_info="",
            chat_history=[]
        ):
        # 입력값에 대한 변수
        self.prompt_info = {
            "user_info": user_info,
            "character_info": character_info
        }

        # 메모리 관련 함수
        self.memory = self._set_memory(chat_history)

        # 프롬프트 관련 변수
        self.system_prompt = "system1.prompt"
        self.prompt_path = Path(__file__).parents[1] / "resources/prompts" / self.system_prompt

        # 체인 만들기
        self.chain = self._make_chain()


    # 시스템 프롬프트 불러오기 
    def _read_prompt(self):
        """시스템 프롬프트 읽기"""
        with open(self.prompt_path, "r") as file:
            prompt = file.read()

        return prompt

    # 템플릿 만들기
    def _make_template(self):
        """템플릿 만들기"""
        system_prompt = self._read_prompt()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),
                ("human", "{input}")
            ]
        )

        new_prompt = prompt.partial(**self.prompt_info)

        return new_prompt
    
    # 메모리 설정
    """메모리 공간 만들기"""
    def _set_memory(self, chat_history):
        memory = ConversationBufferMemory(
            return_messages=True,
            memory_key = "chat_history"
        )

        if len(chat_history) == 0:
            return memory 
        
        # 대화내용 저장하기
        for chat in chat_history:
            if chat["role"] == "user":
                memory.chat_memory.messages.append(
                    HumanMessage(chat["content"])
                )
            else:
                memory.chat_memory.messages.append(
                    AIMessage(chat["content"])
                )
        
        return memory
    
    # 메모리 저장하기
    def _save_memory(self, input, output):
        self.memory.save_context(
            {"human": input},
            {"ai": output}
        )

    # 모델 만들기
    def _set_model(self, model_info):
        model_name = model_info["model"]
        model_params = model_info.copy()

        if "gpt" in model_name:
            model_params["api_key"] = settings.OPENAI_API_KEY
            return ChatOpenAI(**model_params)
        elif "solar" in model_name:
            model_params["api_key"] = settings.UPSTAGE_API_KEY
            return ChatUpstage(**model_params)
        elif "gemini" in model_name:
            model_params["google_api_key"] = settings.GOOGLE_API_KEY
            return ChatGoogleGenerativeAI(**model_params)
        
        return "지원하지 않는 모델입니다."

    # 체인 만들기
    def _make_chain(self):
        # 메모리와 chat_history 연결
        runnable = RunnablePassthrough.assign(
            chat_history=RunnableLambda(
                self.memory.load_memory_variables
            ) | itemgetter("chat_history")
        )

        # 프롬프트
        prompt = self._make_template()

        # 모델 관련 변수
        model = self._set_model(const.chatbot)
        
        # 출력 관리
        output_parser = StrOutputParser()

        # 체인 만들기
        chain = runnable | prompt | model | output_parser 

        return chain
    
    # 대답하기
    ## 테스트 버전
    def invoke(self, input):
        output = self.chain.invoke(
            {"input": input}
        )

        return output
    
    ## 스트리밍 버전
    async def astream(self, input):
        response = self.chain.astream(
            {"input": input}
        )

        output = ""
        async for token in response:
            for char in token:
                await asyncio.sleep(0.02)
                yield char
                output += char

        self._save_memory(input, output)
        # print(self.memory.chat_memory.messages)