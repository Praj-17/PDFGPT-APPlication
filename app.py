from flask import Flask, request, jsonify
from question_generator import QuestionGenerator, ChatWithPDF, BaseURLtoSomething, SearchPDF, EmbedPDF
from PDFCrawler import PDFURLCrawler
from enum import Enum
from embedding_generator import FaissSearch
# import warnings

# # Silence all warnings
# warnings.filterwarnings("ignore")


app = Flask(__name__)

class Modes(Enum):
    CHOICE1 = "all"
    CHOICE2 = "single"
    CHOICE3 = "interval"

class Status(Enum):
    CHOICE1 = True
    CHOICE2 = False

class ReturnType:
    def __init__(self, status, reason, questions):
        self.status = status
        self.reason = reason
        self.questions = questions

class InputData:
    def __init__(self, mode, url, num_questions, page_number=None, interval=1):
        self.mode = mode
        self.url = url
        self.num_questions = num_questions
        self.page_number = page_number
        self.interval = interval

generator = QuestionGenerator()
chat = ChatWithPDF()
crawler = PDFURLCrawler()
url_to_somethig = BaseURLtoSomething()
search_pdf = SearchPDF()
embed_pdf = EmbedPDF()
faiss_search = FaissSearch()

@app.route("/", methods=["POST"])
def generate_questions():
    data = request.json
    questions = []
    status = True
    reason = ""
    url = data["url"]
    num = data["num_questions"]
    if request.method == 'POST':

        try:
            if data["mode"] == 'all':
                questions = generator.generate_mcq_questions_all_text(url=url, n=num)
                status = False
            elif data.get("page_number"):
                if data["mode"] == 'single':
                    questions = generator.generate_mcq_questions_single_page(url=url, page_number=data["page_number"], n=num)
                    status = False
                elif data["mode"] == 'interval':
                    questions = generator.generate_mcq_questions_page_interval(url=url, page_number=data["page_number"], n=num, interval=data["interval"])
                    status = False
            else:
                reason = "Please provide a param page_number"

            print(questions)
        except Exception as e:
            reason = "Exception " + str(e)

        if status == False:
            message = "Success"
        else:
            message = "Failure"

        return jsonify({
            'error': status,
            'reason': reason,
            'message': message,
            'data': questions
        })
@app.route("/crawl", methods=["POST"])
def crawl_urls():
    data = request.json
    pdf_urls = []
    status = True
    reason = ""
    url = data["url"]
    depth = data.get('depth', 1)
    if request.method == 'POST':
        crawler = PDFURLCrawler()
        try:
            
            status_code = crawler.check_url_status(url)
            if status_code == 403 or status_code == 400:
                reason = f"Forbidden URL!! Try another URL. Response code {status_code}"
            else:
                pdf_urls = crawler.crawl(url=url, limit = depth, base_url=url)
                print(pdf_urls)
                print(type(pdf_urls))
                status = False
            
        except Exception as e:
            reason = "Exception " + str(e)

        if status == False:
            message = "Success"
        else:
            message = "Failure"

        return jsonify({
            'error': status,
            'reason': reason,
            'message': message,
            'data': pdf_urls
        })
@app.route("/chat", methods=["POST"])
def chatwithpdf():
    data = request.json
    print("entered")
    # data = []
    answer = ""
    status = True
    reason = ""
    url = data["url"]
    interval = 0
    chat_history = []
    page_number_locations = []
    page_number_locations_all = ['lc' ,'uc' ,'lr' ,'ll' ,'ur' ,'ul' ]
    page_number_style = ['number_only', "alpha_numeric"]
    index_number = None
    results = None
    if request.method == 'POST':

        try:
            chat_history = data.get('chat_history', [])
            question = data.get("question", "")
            interval = data.get("interval", 1)
            page_number_locations = data.get("page_number_location", page_number_locations_all)
            page_number_style = data.get("page_number_style", 'alpha_numeric' )
            for i in page_number_locations:
                if  i not in page_number_locations_all:
                        reason = f"Invalid page number location enter from the following {page_number_locations_all}"
                        break
            else:
                if data["mode"] == 'all':
                    answer, index_number, results = chat.chat_with_whole_pdf(url=url, question=question, page_number_location = page_number_locations,page_number_style = page_number_style,  chat_history=chat_history)
                    print("API Response Recieved")
                    print(answer, index_number, results)
                    print(answer, type(index_number), type(results))
                    status = False
                elif data.get("page_number"):
                    if data["mode"] == 'single':
                        answer, index_number, results  = chat.chat_with_single_page(url=url, page_number=data["page_number"], page_number_location=page_number_locations,page_number_style = page_number_style, question=question, chat_history=chat_history)
                        status = False
                    elif data["mode"] == 'interval':
                        if data['interval']:
                            answer, index_number, results  = chat.chat_with_page_interval(url=url, page_number=data["page_number"],  interval=interval, page_number_location=page_number_locations,page_number_style = page_number_style, question=question, chat_history=chat_history)
                            status = False
                        else:
                            reason = "param 'interval' nor provided, defaulting to 1"
                    else:
                        reason = "Please provide  a correct mode"
                else:
                    reason = "Please provide a param page_number"
        
        except Exception as e:
            reason = "Exception " + str(e)
            print(reason)
    

        if status == False:
            message = "Success"
        else:
            message = "Failure"
        response_data = {
        'guid': 0,
        "index_number":index_number ,
        'answer':answer,
        "embedding_results_page": results
    }
        return jsonify({
            'error': status,
            # 'reason': reason,
            'message': message,
             'reason': reason,
            'status': 200,
            'response_data': response_data,
            
        })

@app.route("/hello", methods=["GET"])
def hello_world():
    return jsonify({
            'status': True,
            'reason': ""
        }) 

@app.route("/create_metadata", methods=["POST"])
def create_metadata():
    data = request.json
    page_number_locations_all = ['lc' ,'uc' ,'lr' ,'ll' ,'ur' ,'ul' ]
    page_number_style = ['number_only', "alpha_numeric"]
    page_number_locations = data.get("page_number_location", page_number_locations_all)
    print("page_number_locations", page_number_locations)
    page_number_style = data.get("page_number_style", "alpha_numeric")
    url = data.get("url", None)
    file_path = None
    json_path = None
    status = True
    reason = ""
    index_path = None
    embedding_path = None
    if request.method == 'POST':

            for i in page_number_locations:
                if  i not in page_number_locations_all:
                        reason = f"Invalid page number location enter from the following {page_number_locations_all}"
                        break
            else:
                if url:
                    check, file_path_existing = url_to_somethig.check_existing_files(url)
                    print(check)

                    if not check:
                        print("Creating Metadata now")
                        file_path = url_to_somethig.download_file_from_url(url)
                        json_path =  url_to_somethig.save_map_to_json(file_path, page_number_locations, page_number_style).name
                        embedding_path = embed_pdf.save_generated_embeddings(file_path)
                        index_path = faiss_search.save_faiss_index(embedding_path)
                        status = False
                    else:
                        reason = f"Metadata is already created at {file_path_existing}"
                        status = False
                else:
                    reason = "Please provide a URL"


            data = {
                'file_path': file_path,
                'json_path':json_path,
                'embedding_path': embedding_path ,
                "index_path": index_path
            }
            if status == False:
                    message = "Success"
            else:
                    message = "Failure"

            return jsonify({
                'error': status,
                'message': message,
                'reason': reason,
                'status': 200,
                'check': check,
                'data':data
    })

    


if __name__ == "__main__":

    app.run(debug=True, host='127.0.0.1', port=8000)
