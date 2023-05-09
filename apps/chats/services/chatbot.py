from chromadb.errors import NoIndexException
from decouple import config
from langchain import OpenAI, PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma

from django.conf import settings

OPENAI_API_KEY = config("OPENAI_API_KEY")
CHROMADB_DIR = settings.CHROMADB_DIR


class ChromaDB:
    def __init__(self, collection_name: str) -> None:
        self._collection_name = collection_name
        self._chroma = self._get_chroma_instance()

    def insert(self, text: str) -> None:
        self._chroma.add_texts([text])

    def _get_chroma_instance(self) -> Chroma:
        return Chroma(
            collection_name=self._collection_name,
            persist_directory=str(CHROMADB_DIR),
        )

    @staticmethod
    def _format_record_for_db(question: str, answer: str) -> str:
        return f"Human: {question}\nAI: {answer}"


class ChatBot:
    def __init__(self) -> None:
        self._template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context.

        Current conversation:
        {chat_history}
        Human: {question}
        AI:"""
        self.prompt = PromptTemplate.from_template(self._template)
        self.llm = OpenAI(
            temperature=0.0,
            openai_api_key=OPENAI_API_KEY,
            # model_name="gpt-3.5-turbo",
        )


class HistoryChatBot(ChatBot, ChromaDB):
    def __init__(self, collection_name: str) -> None:
        ChatBot.__init__(self)
        ChromaDB.__init__(self, collection_name)

    def ask(self, question: str) -> str:
        try:
            self._ask(question)
        except NoIndexException:
            self.insert("")
        finally:
            answer = self._ask(question)
        record_to_db = self._format_record_for_db(question, answer)
        self.insert(record_to_db)
        return answer

    def _ask(self, question: str) -> str:
        qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self._chroma.as_retriever(),
            condense_question_prompt=self.prompt,
        )
        result = qa({"question": question, "chat_history": []})
        return str(result["answer"])
