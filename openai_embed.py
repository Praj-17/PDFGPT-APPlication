import openai
import os
import io
import tiktoken
import numpy
import csv
import openai
from config import encoding_name, openai_model_name,max_tokens


class OpenAIEmbedding():
    def __init__(self, encoding_name = encoding_name, model_name = openai_model_name) -> None:
      self.encoding_name = encoding_name
      self.model_name = model_name
      # self.max_tokens = max_tokens
      self.encoding = tiktoken.get_encoding(encoding_name )

    def embed_sentence(self,sentence):
        encoded_texts = self.encoding.encode(sentence)
        response = None
        embedding = []
        try:
            response = openai.Embedding.create(input = encoded_texts, model = self.model_name, max_tokens =max_tokens)
        except:
            print("OpenAI Error, their server didnt responnd")
        if response:
            embedding = response.get('data', [{}])[0].get('embedding', [])
            embedding = numpy.array(embedding).astype(numpy.float32)
        
        return embedding

if __name__ == "__main__":
   
      
      e = OpenAIEmbedding()
      text = e.embed_sentence("My name is prajwal")


