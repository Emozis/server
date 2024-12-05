from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
import asyncio
import os 

from ..core import settings, logger
from ..utils.constants import constants


os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = "NONE"

class Gemini:
    def __init__(
        self,
        user_info=None,
        character_info=None,
        chat_history=None
    ) -> None:
        
        # 입력값에 대한 변수
        self.inputs = self._get_inputs(user_info, character_info, chat_history)
        
        # 체인에 대한 변수
        self.template_path = constants.TEMPLATE_PATH
        self.model_name = constants.GEMINI_MODEL
        self.temperature = constants.TEMPERATURE
        self.chain = self._make_chain()

    def _get_inputs(self, user_info, character_info, chat_history):
        """input_data들을 하나의 딕셔너리로 바꾸는 메서드"""
        inputs = {
            "user_info": user_info,
            "character_info" : character_info,
            "chat_history": self._wrap_message(chat_history)
        }

        return inputs
    
    def _wrap_message(self, chat_history):
        """chat_history에 Message 객체 씌우는 메서드"""
        if not chat_history:
            return []

        chat_messages = []
        for log in chat_history:
            if log["role"] == "user":
                chat = HumanMessage(log["content"])
            else:
                chat = AIMessage(log["content"])
            
            chat_messages.append(chat)
        
        return chat_messages
    
    @staticmethod
    def read_template(filepath:str) -> str:
        """프롬프트 파일을 읽고 텍스트로 반환하는 함수

        Args:
            filepath (str): markdown 파일 경로

        Returns:
            str: markdown 파일에서 추출된 텍스트
        """
        file = Path(filepath)
        
        if not file.is_file():
            logger.error(f"❌ File path not found: {filepath}")
            file_text = f"[ERROR] Unable to find the file path. (INPUT PATH: {filepath})"
        else:
            file_text = file.read_text(encoding="utf-8")

        return file_text
    
    def _get_prompts(self):
        """프롬프트 객체 만드는 메서드"""
        template = self.read_template(self.template_path)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        return prompt
    
    def _make_chain(self):
        """Chain 만드는 메서드"""
        prompt = self._get_prompts()

        # 모델 설정
        model = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=settings.GOOGLE_API_KEY
        )

        # 출력 파서 설정
        output_parser = StrOutputParser()

        # 체인 만들기
        chain = prompt | model | output_parser

        return chain

    def add_history(self, input, output):
        self.inputs["chat_history"].extend(
        [
            HumanMessage(content=input),
            AIMessage(content=output)
        ]
    )

    async def astream_yield(self, input):
        self.inputs["input"] = input

        result = self.chain.astream(self.inputs)
        async for token in result:
            # 한글자씩 스트리밍
            for char in token:
                await asyncio.sleep(0.02)
                # await asyncio.sleep(1)
                yield char