import nlpcloud

from src.config import NLP_CLOUD_API_KEY


class NLPCloudService:
    def __init__(self, model_id: str):
        self.client = nlpcloud.Client(model_id, NLP_CLOUD_API_KEY, True)

    def chatbot(self, input_text: str, context: str, history: list) -> dict:
        return self.client.chatbot(input_text, context=context, history=history)
