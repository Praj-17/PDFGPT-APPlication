# Application Documentation

## Setup

1. Install Python==3.9.0 (Prefferably)
2. Install requirements (by navigating to the folder)
```
    pip install -r requirements.text
```

3. run the app
```
    python app.py
```

HOST 
`http://127.0.0.1:8000` (localhost)

## Question Generation

endpoint = `/get_mcq_questions`

### Input Parameters 

1. mode = `['all', 'single', 'interval']` Any one of these 

    a.`all`: When you want to extract entire text from a PDF 
    b. `single`: When you want to extract text from a single page  
    c. `interval`: When you want to extract +-n pages from a target page

2. url = A string of `public` url for a PDF file hosted on a google drive  
3. num_questions = Number of questions you want to be created  
4. page_number  = Specific to `single` and `interval` format, specifies target page  
5. interval = Specific to `interval` formatm specifies target interval  

#### input parameters
```
{
    "url": "https://drive.google.com/file/d/1TGEgTeDQAS2NyS36_KXv1ZyIcA0tFTvr/view?usp=drive_link",
    "num_questions": 5,
    "mode": "interval",
    "page_number": 2,
    "interval":2
}
```

#### Output format

```
{
    "status": true,
    "reason": "",
    "questions": [
        {
            "question": "What is the first step in urine formation?",
            "options": [
                "Reabsorption",
                "Secretion",
                "Glomerular filtration",
                "Ultra filtration"
            ],
            "answer": "Glomerular filtration"
        },
        {
            "question": "What is the average amount of blood filtered by the kidneys per minute?",
            "options": [
                "500-600 ml",
                "700-800 ml",
                "900-1000 ml",
                "1100-1200 ml"
            ],
            "answer": "1100-1200 ml"
        },
        {
            "question": "Which type of nephron has a loop of Henle that runs deep into the medulla?",
            "options": [
                "Cortical nephrons",
                "Juxta medullary nephrons",
                "Glomerular nephrons",
                "Peritubular nephrons"
            ],
            "answer": "Juxta medullary nephrons"
        },
        {
            "question": "What are the major forms of nitrogenous wastes excreted by animals?",
            "options": [
                "Ammonia, urea, and uric acid",
                "Carbon dioxide, water, and ions",
                "Proteins, fats, and carbohydrates",
                "Sodium, potassium, and chloride"
            ],
            "answer": "Ammonia, urea, and uric acid"
        },
        {
            "question": "What is the excretory structure in Platyhelminthes, rotifers, some annelids and the cephalochordate – Amphioxus?",
            "options": [
                "Nephridia",
                "Malpighian tubules",
                "Protonephridia or flame cells",
                "Antennal glands"
            ],
            "answer": "Protonephridia or flame cells"
        }
    ]
}
```
## Chat With PDF

endpoint = `/chat`

### Input Parameters 

1. mode = `['all', 'single', 'interval']` Any one of these 

    a.`all`: When you want to extract entire text from a PDF 
    b. `single`: When you want to extract text from a single page  
    c. `interval`: When you want to extract +-n pages from a target page

2. url = A string of `public` url for a PDF file hosted on a google drive  
3. question = quetion asked by user 
4. page_number  = Specific to `single` and `interval` format, specifies target page  
5. interval = Specific to `interval` formatm specifies target interval  
6. chat_history = A list of tuples with question answer pairs 
7. page_number_location = page_number_locations is a list of possible locations in decreasing order of priority.
```
Supported locations include - 
[lc - lower center, 
uc - upper center
lr - lower right
ll - lower left
ur - upper right
ul - upper left]
```

8. page_number_style = Represents how the page numbers are written , are they only numeric or a alpha numeric as in John Deere 

``` ["alpha_numeric", "only_numeric"] ```

#### input parameters
```
{
    "url": "https://ncert.nic.in/textbook/pdf/kebo116.pdf",
    "question": "what is this page about",
    "mode": "interval",
    "page_number": 2,
    "interval":2,
    "chat_history": [(question, answer), (question, answer)]
}
```

#### Output format

```
{
    "error": false,
    "message": "Success",
    "reason": "",
    "response_data": {
        "answer": "This page is primarily about the functions and structures of the kidney, with a focus on the processes of filtration, reabsorption, and secretion. It details how the glomerulus filters blood and forms filtrate in the Bowman’s capsule, and how reabsorption of the filtrate takes place in different parts of the nephrons. It also discusses the role of the juxta glomerular apparatus (JGA) in regulating the Glomerular Filtration Rate (GFR). The page further explains the process of dialysis and kidney transplantation as methods for treating kidney failure. It also defines certain kidney conditions such as renal calculi and glomerulonephritis. The page includes a detailed explanation of the function of the tubules, including the Proximal Convoluted Tubule (PCT), Henle’s Loop, Distal Convoluted Tubule (DCT), and Collecting Duct. It also discusses the mechanism of concentration of the filtrate, particularly the role of Henle’s loop and vasa recta in producing a concentrated urine. Lastly, the page includes exercises and questions for further understanding of the topic.",
        "guid": 0
    },
    "status": 200
}
```
endpoint = `/crawl`

### Input Parameters 

1. url = A string of `public` url for a PDF file hosted on a google drive  
2. depth = A number indicating into how much depth of the webpage you want to go. Depth means a page contains 10 links and depth is 3, it means it will also crawl those 10 links, and links within them.


#### input parameters
```
{
    "url": "https://investor.fb.com/financials/",
    "depth": 1
}
```

#### Output format

```
{
    "data": [
        "https://www.abc.xyz/assets/d4/4f/a48b94d548d0b2fdc029a95e8c63/2022-alphabet-annual-report.pdf",
        "https://ai.google/static/documents/ai-principles-2023-progress-update.pdf",
        "https://www.abc.xyz/assets/9a/bd/838c917c4b4ab21f94e84c3c2c65/goog-10-k-q4-2022.pdf",
        "https://www.abc.xyz/assets/c4/d3/fb142c0f4a78a278d96ad5597ad9/2022q4-alphabet-earnings-release.pdf",
        "https://www.abc.xyz/assets/b1/d0/c66d744443e698fd63a3ae81e12a/2022q3-alphabet-earnings-release.pdf",
        "https://www.abc.xyz/assets/a7/5b/9e5ae0364b12b4c883f3cf748226/goog-exhibit-99-1-q1-2023-19.pdf",
        "https://www.abc.xyz/assets/31/25/fb7b6946475d96b7fa4b9c3e2149/2022q1-alphabet-earnings-release.pdf",
        "https://www.abc.xyz/assets/20/ef/844a05b84b6f9dbf2c3592e7d9c7/2023q2-alphabet-earnings-release.pdf",
        "https://www.abc.xyz/assets/4a/f6/411d938e492e9b66749e2ba1984f/goog-10-q-q2-2023-4.pdf",
        "https://www.abc.xyz/assets/c2/3e/0d6d568e4f56a1d14ca6b70c3443/goog-10-q-q3-2023.pdf",
        "https://www.abc.xyz/assets/0d/4a/646d28c945aba76a5eeeba68e686/2022q2-alphabet-earnings-release.pdf",
        "https://www.abc.xyz/assets/86/99/68122c444c4a93d2228e21ecc16b/20230426-alphabet-10q.pdf",
        "https://www.abc.xyz/assets/fa/0e/606be5234d8c895e5e167d38811f/20220427-alphabet-10q.pdf",
        "https://www.abc.xyz/assets/4a/3e/3e08902c4a45b5cf530e267cf818/2023q3-alphabet-earnings-release.pdf",
        "https://www.abc.xyz/assets/f2/48/c0bc469747b691dd301e91cb10cc/20220726-alphabet-10q.pdf",
        "https://www.abc.xyz/assets/06/a6/2ea9850a4b4584c07fac2c1b517d/20221025-alphabet-10q.pdf"
    ],
    "error": true,
    "message": "Sucess",
    "reason": ""
}
```

endpoint = `/chat`

### Input Parameters 

1. mode = `['all', 'single', 'interval']` Any one of these 

    a.`all`: When you want to extract entire text from a PDF 
    b. `single`: When you want to extract text from a single page  
    c. `interval`: When you want to extract +-n pages from a target page

2. url = A string of `public` url for a PDF file hosted on a google drive  
3. question = quetion asked by user 
4. page_number  = Specific to `single` and `interval` format, specifies target page  
5. interval = Specific to `interval` formatm specifies target interval  
6. chat_history = A list of tuples with question answer pairs 
7. page_number_location = page_number_locations is a list of possible locations in decreasing order of priority.
```
Supported locations include - 
[lc - lower center, 
uc - upper center
lr - lower right
ll - lower left
ur - upper right
ul - upper left]
```

8. page_number_style = Represents how the page numbers are written , are they only numeric or a alpha numeric as in John Deere 

``` ["alpha_numeric", "only_numeric"] ```

#### input parameters
```
{
    "url": "https://ncert.nic.in/textbook/pdf/kebo116.pdf",
    "question": "what is this page about",
    "mode": "interval",
    "page_number": 2,
    "interval":2,
    "chat_history": [(question, answer), (question, answer)]
}
```

#### Output format

```
{
    "error": false,
    "message": "Success",
    "reason": "",
    "response_data": {
        "answer": "This page is primarily about the functions and structures of the kidney, with a focus on the processes of filtration, reabsorption, and secretion. It details how the glomerulus filters blood and forms filtrate in the Bowman’s capsule, and how reabsorption of the filtrate takes place in different parts of the nephrons. It also discusses the role of the juxta glomerular apparatus (JGA) in regulating the Glomerular Filtration Rate (GFR). The page further explains the process of dialysis and kidney transplantation as methods for treating kidney failure. It also defines certain kidney conditions such as renal calculi and glomerulonephritis. The page includes a detailed explanation of the function of the tubules, including the Proximal Convoluted Tubule (PCT), Henle’s Loop, Distal Convoluted Tubule (DCT), and Collecting Duct. It also discusses the mechanism of concentration of the filtrate, particularly the role of Henle’s loop and vasa recta in producing a concentrated urine. Lastly, the page includes exercises and questions for further understanding of the topic.",
        "guid": 0
    },
    "status": 200
}
```
endpoint = `/create_metadata`

This API is to be added from the fronted to the server whenever a new pdf is added, this will create the metadata

### Input Parameters 

1. url = A string of `public` url for a PDF file hosted on a google drive  
2. page_number_location = page_number_locations is a list of possible locations in decreasing order of priority.
```
Supported locations include - 
[lc - lower center, 
uc - upper center
lr - lower right
ll - lower left
ur - upper right
ul - upper left]
```

3. page_number_style = Represents how the page numbers are written , are they only numeric or a alpha numeric as in John Deere 

``` ["alpha_numeric", "only_numeric"] ```


#### input parameters
```
{
    "url": "https://assets.openstax.org/oscms-prodcms/media/documents/ConceptsofBiology-WEB.pdf",
    "page_number_location": ["lc", "lr", "ll"],
    "page_number_style": "alpha_numeric"
}
```

#### Output format

```
{
    "error": false,
    "file_path": "pdfs/ConceptsofBiology-WEB.pdf",
    "json_path": "pdfs\\ConceptsofBiology-WEB.json",
    "message": "Success",
    "reason": "",
    "status": 200
}
```







