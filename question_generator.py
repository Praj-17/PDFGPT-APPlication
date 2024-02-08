
import fitz
import requests
import os
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA,ConversationalRetrievalChain
from langchain.llms import OpenAI 
from sentence_transformers import SentenceTransformer
from embedding_generator import EmbeddingGenerator, FaissSearch
import json
import re
import numpy as np


class URLtoPDF():
    def __init__(self) -> None:
          pass
          self.url = "https://drive.google.com/uc?id="
          self.default_save_path = r"pdfs/"
    def extract_file_id(self, url):
        try: 
            file_id = url.split("/file/d/")[1].split("/view")[0] # to get the code of google drive
            return file_id
        except IndexError:
            raise Exception("Invalid Google Drive link.")
    def get_filename(self, url):
        return url.split("/")[-1]


    def download_file_from_url(self,entire_url,):
        
        if not os.path.exists(self.default_save_path):
            os.makedirs(self.default_save_path)
        
        file_name = self.get_filename(entire_url)
        if entire_url.startswith(self.url):
            file_id = self.extract_file_id(entire_url)
            URL = self.url + file_id #downloading the pdf from gdrive
        URL = entire_url
        try:
            response = requests.get(URL)
            print(response)
        except Exception as e:
            print(str(e))

        if response.status_code == 200:
            file_path = os.path.join(self.default_save_path, file_name)
            # Save the PDF to the local folder
            with open(file_path, 'wb') as file:
                file.write(response.content)

            print(f"PDF downloaded and saved to {file_path}")
            return file_path
        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")
            print("exception")
            print(response.status_code)
            print(response.json())
            print("exception Done")
            raise Exception("Failed to download the file from Google Drive.")
    
    def check_existing_files(self,entire_url):
        file_name = self.get_filename(entire_url)
        file_path = os.path.join(self.default_save_path, file_name)
        print(file_path)
        if os.path.exists(file_path):
            return True, file_path

        else:
            print("entered else")
            return False,file_path


class PDFToMap():
    def __init__(self) -> None:
        pass

    def process_page_number_style(self,page_number,  page_number_style):
        if page_number_style == 'number_only':
            return ''.join(re.findall(r'\d', page_number))
        else:
            return page_number

    
    def extract_page_number_single_page(self, pdf_document, index_number, page_number_locations=['lc', 'uc', 'lr', 'll', 'ur', 'ul'], page_number_style = "number_only"):
        """
        page_number_locations is a list of possible locations in decreasing order of priority.
        Supported locations include - [
        lc - lower center
        uc - upper center
        lr - lower right
        ll - lower left
        ur - upper right
        ul - upper left
        ]

        """
        page = pdf_document[index_number]
        rect = page.rect

        for location in page_number_locations:
            bottom_rect = self.get_bottom_rect(rect, location)
            text = page.get_text("text", clip=bottom_rect)
            page_number_str = text.strip()
            page_number_styled = self.process_page_number_style(page_number_style=page_number_style, page_number=page_number_str)

            if page_number_styled and not page_number_styled.isalpha():
                return page_number_styled

        return ""

      

    def get_bottom_rect(self, rect, location):
        if location == 'lc':
            return fitz.Rect(rect.x0, rect.y1 - 30, rect.x1, rect.y1)  # Lower center
        elif location == 'uc':
            return fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y0 + 30)  # Upper center
        elif location == 'lr':
            return fitz.Rect(rect.x1 - 100, rect.y1 - 30, rect.x1, rect.y1)  # Lower right
        elif location == 'll':
            return fitz.Rect(rect.x0, rect.y1 - 30, rect.x0 + 100, rect.y1)  # Lower left
        elif location == 'ur':
            return fitz.Rect(rect.x1 - 100, rect.y0, rect.x1, rect.y0 + 30)  # Upper right
        elif location == 'ul':
            return fitz.Rect(rect.x0, rect.y0, rect.x0 + 100, rect.y0 + 30)  # Upper left
        else:
            raise ValueError("Invalid page_number_location. Supported values: lc, uc, lr, ll, ur, ul")



    def map_page_number_index_number(self,pdf_path, page_number_location, page_number_style):
        """
        It takes in a PDF and collects all page_numbers, maps them in a hash map
        
        
        """
        hash_map = {}
        pdf_document = fitz.open(pdf_path)
        for index_number in range(pdf_document.page_count):
            page_number = self.extract_page_number_single_page(pdf_document=pdf_document, index_number=index_number, page_number_locations = page_number_location, page_number_style = page_number_style)
            if page_number or page_number is not None:
                hash_map[page_number] = index_number+1
        return hash_map
    def get_saved_json_path(self, pdf_path):
        file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".json"
        folder_path = os.path.dirname(pdf_path)
        json_file = os.path.join(folder_path, file_name)
        return json_file
    def save_map_to_json(self, pdf_path, page_number_location, page_number_style):
        hash_map = self.map_page_number_index_number(pdf_path, page_number_location,page_number_style)

        json_file =  self.get_saved_json_path(pdf_path)
        # Save the dictionary to a JSON file
        with open(json_file, 'w') as json_file:
            json.dump(hash_map, json_file)
        print("Json File saved sucessfully!!!")
        return json_file
    
    def get_page_number_from_index_number(self,json_path, page_number):
        # Load the JSON file
        with open(json_path, 'r') as json_file:
            map = json.load(json_file)
        return map.get(page_number, None)

class PDFtoText():
    def __init__(self) -> None:
        pass

    def open_pdf(self, pdf):
        if os.path.exists(str(pdf)) or isinstance(pdf,bytes):
                self.pdf = fitz.open(pdf)
                self.page_count = self.pdf.page_count
                return self.pdf
                # self.pdf.close()
        else:
            raise ValueError(f"PDF path is incorrect", pdf)
    def extract_all_text(self, pdf):
         # Open the PDF file
        self.pdf = self.open_pdf(pdf)
        
        all_text = ''

        # Iterate through all pages
        for page_number in range(self.page_count) :
            # Get the page
            page = self.pdf[page_number]

            # Extract text from the page
            text = page.get_text()
            all_text += text

            # Print or process the extracted text as needed
            # print(f"Page {page_number + 1}:\n{text}\n")
        return all_text
    
    def extract_all_text_page_wise(self, pdf):
         # Open the PDF file
        self.pdf = self.open_pdf(pdf)
        
        all_text = []

        # Iterate through all pages
        for page_number in range(self.page_count) :
            # Get the page
            page = self.pdf[page_number]

            # Extract text from the page
            text = page.get_text()
            all_text.append(text)
        return all_text
    def extract_text_from_single_page(self,pdf, page_number):
        self.pdf = self.open_pdf(pdf)
        if page_number -1> self.page_count:
             raise ValueError("Invlaid pagenumber")
        else:
             return self.pdf[page_number-1].get_text()
    def extract_text_from_interval(self,pdf,page_number, interval =1):
        self.pdf = self.open_pdf(pdf)
        text = ""
        if page_number > self.page_count:
            raise ValueError("Invlaid pagenumber")
        else:
            # Calculate the start and end pages
            start_page = max(0, page_number - interval)
            end_page = min(self.page_count - 1, page_number + interval)

            for page_number in range(start_page, end_page + 1):
                text += self.extract_text_from_single_page(pdf=pdf, page_number=page_number)
        return text

class EmbedPDF(PDFtoText, EmbeddingGenerator):
    def __init__(self) -> None:
        super().__init__()
    def generate_embeddings(self,pdf_path):
        all_text_as_list = self.extract_all_text_page_wise(pdf_path)
        # print(all_text_as_list)
        embeddings = self.generate(all_text_as_list)
        return embeddings
    def get_saved_embedding_path(self, pdf_path):
        file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".npy"
        folder_path = os.path.dirname(pdf_path)
        embedding_file = os.path.join(folder_path, file_name)
        return embedding_file
    def save_generated_embeddings(self,pdf_path):
        embeddings = self.generate_embeddings(pdf_path)
        embedding_file_path = self.get_saved_embedding_path(pdf_path)
        np.save(embedding_file_path,embeddings)
        print("Embeddings_saved_sucessfully")
        return embedding_file_path


class SearchPDF(FaissSearch, EmbedPDF):
    def __init__(self) -> None:
        super().__init__()
    def create_faiss_index_and_embeddings(self,pdf_path):
        embeddings_path = self.save_generated_embeddings(pdf_path)
        index_path = self.save_faiss_index(embeddings_path=embeddings_path)
        return embeddings_path, index_path
    def search_pdf(self,index_path, query, k=1, is_openai= False):
        index = self.load_faiss_index(index_path)
        results = self.search(index=index, query=query, k=k, is_openai=is_openai)
        return results



class RAGImplementation():
    def __init__(self) -> None:
          
        
        pass
         
          
        #   self.client  = OpenAI()

          
    def get_data_chunks(self,text):
         self.text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=5,  length_function=len)
         print(text)
         chunks = self.text_splitter.split_text(text)
         print(chunks)
         print(type(chunks))
         return chunks
    def create_knowledge_hub(self,chunks):
        self.embeddings = OpenAIEmbeddings()
        knowledge_hub = FAISS.from_texts(chunks, self.embeddings)
        return knowledge_hub
    
    def get_answer_LLM(
            self,
            prompt: str,
            knowledge_hub: str,
            chain_type: str = 'refine',
            chain_name = 'retrievalqa',
            chat_history = []
        ) -> str:    
        """
        Prompt: System Prompt 
        knowledge_hub: Document Knowledfehub
        Chain_type: 'refine','stuff','map_reduce'
        chain_name: 'retrievalqa', 'conversationalretrievalchain'
        chat_history : used with conversationalretrievalchain, it will be a list of tuples, looks like this 
        [(question1, answer1), (question2, answer2)]
        
        """
        
        
        if knowledge_hub == "":
            return ""

        # chunks = get_data_chunks(data, chunk_size=chunk_size)  # create text chunks
        # knowledge_hub = create_knowledge_hub(chunks)  # create knowledge hub

        retriever = knowledge_hub.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )
        if chain_name == 'conversationalretrievalchain':
            chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.3, model_name="gpt-3.5-turbo"),
                chain_type=chain_type,
                retriever=retriever)
            result = chain({"question": prompt, "chat_history": chat_history})
            result = result['answer']
        else:
            chain = RetrievalQA.from_chain_type(
                llm=OpenAI(temperature=0.3, model_name="gpt-3.5-turbo"),
                chain_type=chain_type,
                retriever=retriever,
                return_source_documents=True,
            )
            result = chain({"query": prompt})
            result = result['result']

        return result.strip()



class TexttoQuestions(RAGImplementation):
    def __init__(self) -> None:
        super().__init__()
    def extract_questions_answers(self,response):
        # Extract the assistant's message
        # response = response.choices[0].message.content

        # Split the message into lines
        lines = response.split('\n')

        # Initialize lists to hold the questions, options, and answers
        questions = []
        options = []
        answers = []

        # Initialize a list to hold the current question's options
        current_options = {}

        # Iterate over the lines
        for line in lines:
            if line.startswith('Question:'):
                # This is a question, so add it to the questions list
                questions.append((line[len('Question: '):]).strip().strip('"'))
            elif line.startswith('Options:'):
                        # This is the start of the options, so clear the current options list
                        current_options = {}
            elif line.startswith('Answer:'):
                # This is an answer, so add the current options to the options list and the answer to the answers list
                options.append(current_options)
                answers.append((line[len('Answer: '):]).strip().strip('"'))
            elif line.startswith(('a)', 'b)', 'c)', 'd)')):
                # This is an option, so add it to the current options list
                    if line.startswith('a)'):
                        current_options['a'] = ((line[len('a)'):]).strip().strip('"'))
                    elif line.startswith('b)'):
                        current_options['b'] = ((line[len('b)'):]).strip().strip('"'))
                    elif line.startswith('c)'):
                        current_options['c'] = ((line[len('c)'):]).strip().strip('"'))
                    elif line.startswith('d)'):
                        current_options['d'] = ((line[len('d)'):]).strip().strip('"'))
                    
                # current_options.append((line[len('a)'):]).strip().strip('"'))

        # Return the questions, options, and answers as a list of dictionaries
        return [{'question': q, 'options': o, 'answer': a} for q, o, a in zip(questions, options, answers)]
    def get_mcq_questions(self,n,text):
         self.prompt = """Create {n} expert level MCQ questions with 4 options and the correct answer on the following context. Strictly use the following format. Do not number questions,do not return anything else and do not include option number in answer.
            Question: "Question_here"                         
            Options:
            a)
            b)
            c)
            d) 
            Answer: "Answer here"       
            """
 
         prompt = self.prompt.format(n = n)
         print("Creating Knowledge")
         knowledge_hub  = self.create_knowledge_hub(chunks=self.get_data_chunks(text))
         print("Going to ChatGPT")
         questions = self.get_answer_LLM(prompt=prompt, knowledge_hub=knowledge_hub)
         print("Returned from ChatGPT")
         print(questions)
    
         try:
            print("Converting output to Json")
            return self.extract_questions_answers(questions)
         except Exception as e:
             raise Exception("Openai return type not a valid json", str(e))

class ChatCaller(RAGImplementation):
    def __init__(self) -> None:
        self.prompt = """you are a helpful Chat with PDF agent which helps users answer questions from the given knowledge base. For out of context content try answering on your own. Strictly answer in following format. Also, return the page number from which answer is derieved return blank string, if there are more than 1 pages return only the first one. If you have answered it yourself or you don't know the page_number.Do not return anything Answer the question {question}
        Answer: answer_here
        Page: page_number_here
        """
        super().__init__()

    
    def extract_answer_page_number(self, response):
        print(response)
        lines = response.split('\n')
        page_number = lines[-1].split(":")[-1].strip()
        answer = response.replace(lines[-1], "").replace("Answer:", "")
        return {
            "answer": answer,
            "page_number": page_number
        }

       


    def chat(self,text, question, chat_history = []):
         
         prompt = self.prompt.format(question = question)
         knowledge_hub  = self.create_knowledge_hub(self.get_data_chunks(text))
         answer = self.get_answer_LLM(prompt=prompt, knowledge_hub=knowledge_hub, chain_name= 'conversationalretrievalchain', chat_history=chat_history)


         answer_dict = self.extract_answer_page_number(answer)
         try:
            return answer_dict
         except Exception as e:
             raise Exception("Error in chat With PDF", str(e)) 



class BaseURLtoSomething(SearchPDF,URLtoPDF, PDFtoText, PDFToMap):
    def __init__(self) -> None:
        print("initializing base constructor")
        super().__init__()

    def whole_text(self,url, page_number_location = [], page_number_style = "alpha_numeric"):
        check, file_path = self.check_existing_files(url)
        if not check:
            print("Downloading File")
            file_path = self.download_file_from_url(url)
            print("Creating json")
            json_path = self.save_map_to_json(file_path, page_number_location, page_number_style)
            print("Embedding")
            index_path, embedding_path = self.create_faiss_index_and_embeddings(file_path)


        
        json_path = self.get_saved_json_path(file_path)
        embedding_path = self.get_saved_embedding_path(file_path)
        index_path = self.get_saved_index_path(file_path)
        all_paths = {
            "json_path": json_path,
            "embedding_path": embedding_path,
            "index_path": index_path
        }


        return self.extract_all_text(pdf=file_path), all_paths    
    def single_page(self, url, page_number, page_number_location = [], page_number_style = "alpha_numeric"):
        check, file_path = self.check_existing_files(url)
        if not check:
            file_path = self.download_file_from_url(url)
            json_path = self.save_map_to_json(file_path, page_number_location, page_number_style)
            index_path, embedding_path = self.create_faiss_index_and_embeddings(file_path) 

        json_path = self.get_saved_json_path(file_path)
        embedding_path = self.get_saved_embedding_path(file_path)
        index_path = self.get_saved_index_path(file_path)
        all_paths = {
            "json_path": json_path,
            "embedding_path": embedding_path,
            "index_path": index_path
        }
        return self.extract_text_from_single_page(pdf = file_path, page_number=page_number), all_paths
    def page_interval(self, url, page_number, interval, page_number_location = [], page_number_style = "alpha_numeric"):
        check, file_path = self.check_existing_files(url)
        if not check:
            file_path = self.download_file_from_url(url)
            json_path =  self.save_map_to_json(file_path, page_number_location, page_number_style)
            index_path, embedding_path = self.create_faiss_index_and_embeddings(file_path)

        json_path = self.get_saved_json_path(file_path)
        embedding_path = self.get_saved_embedding_path(file_path)
        index_path = self.get_saved_index_path(file_path)
        all_paths = {
            "json_path": json_path,
            "embedding_path": embedding_path,
            "index_path": index_path
        }
        return self.extract_text_from_interval(pdf = file_path, page_number=page_number, interval=interval), all_paths


class ChatWithPDF(BaseURLtoSomething, PDFToMap):
    def __init__(self) -> None:
        self.chat = ChatCaller()
        self.search_faiss = FaissSearch()

        super().__init__()

        print("Intiailizing ChatWithPDF") 
    def chat_with_whole_pdf(self,url,question,page_number_location,page_number_style, chat_history):
        #check if the file is already downloaded
        print("Text, all_paths_collected")
        text, all_paths = self.whole_text(url, page_number_location, page_number_style)
        print("Collecting Answer and page_number")
        answer = self.chat.chat(text=text, chat_history=chat_history,question=question)
        print("Collecting page_number index")
        index_number = self.get_page_number_from_index_number(all_paths['json_path'], answer.get("page_number"))
        print("Searching FAISS")
        results = self.search_faiss.search(index = all_paths["index_path"], query=question, k=1, is_openai= False)
        return answer.get("answer", ""), index_number,results
    def chat_with_single_page(self, url,page_number, question, page_number_location,page_number_style,chat_history = []):
        text, all_paths = self.single_page(url, page_number, page_number_location,page_number_style)
        answer = self.chat.chat(text=text, chat_history=chat_history,question=question)
        index_number = self.get_page_number_from_index_number(all_paths['json_path'], answer.get("page_number"))
        results = self.search_faiss.search(index = all_paths["index_path"], query=question, k=1, is_openai= False)
        return answer.get("answer", ""), index_number,results

    def chat_with_page_interval(self,url,page_number, interval, question,page_number_location, page_number_style,chat_history= []):
        text, all_paths = self.page_interval(url, page_number, interval, page_number_location,page_number_style)
        answer = self.chat.chat(text=text, chat_history=chat_history,question=question)
        index_number = self.get_page_number_from_index_number(all_paths['json_path'], answer.get("page_number"))
        results = self.search_faiss.search(index = all_paths["index_path"], query=question, k=1, is_openai= False)
        return answer.get("answer", ""), index_number,results


class QuestionGenerator(BaseURLtoSomething,TexttoQuestions, RAGImplementation):
    def __init__(self) -> None:
        print("initializing generator")
        super().__init__()
    def generate_mcq_questions_all_text(self,url,n):
        #check if the file is already downloaded
        text , all_paths = self.whole_text(url)
        return self.get_mcq_questions(n,text)
    def generate_mcq_questions_single_page(self,url,page_number, n):
        text , all_paths = self.single_page(url, page_number)
        return self.get_mcq_questions(n,text)
    def generate_mcq_questions_page_interval(self,url,page_number, interval, n):
        text , all_paths = self.page_interval(url, page_number, interval)
        return self.get_mcq_questions(n,text)



if __name__ == '__main__':
    pass

    chatwithpdf = ChatWithPDF()
    answer, index_number, result_page_number =chatwithpdf.chat_with_whole_pdf("https://assets.openstax.org/oscms-prodcms/media/documents/ConceptsofBiology-WEB.pdf", question = "Explain alternation of generations in plant kingdom in detail", page_number_location  = ["lr", "ul"],chat_history=[], page_number_style='number_only')
    print(answer)
    print("Index Number is:", index_number)
    print(result_page_number)

