# THE TRIVIA APP

## Introduction

Trivia App offers interesting gaming experience for playing the trivia game with friends, family and colleagues. The API follows the REpresentational State Transfer architectural style (RESTful), all data transfers conform to HTTP/1.1.


## Getting Started

### Pre-requisites and Local Development
- Developers who wish to use this project should have Python3, pip and node installed on their local machines. Here is a link to download Python3 `www.python.org/downloads`.

### Backend
- From the backend folder run pip install requirements.txt to get all the required packages in the requirements file.

- To run the application run the following commands:
    ```
    export FLASK_APP=flaskr
    export FLASK_DEBUG=True
    flask run
    ```
The application is run on `http://127.0.0.1:5000/` by default and is a proxy to the frontend.

### Frontend
- From the frontend folder, run the following commands to start the client:
    ```
    npm install // just once to install dependencies
    npm start // to start the client
    ```


## API Reference
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Trivia app uses conventional HTTP response code to indicate success and failure of an API request, errors are returned as JSON objects in the format

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

Here are some status codes;
- 200 - Ok Everything works as expected.
- 400 - Bad Request The request was not accepted which may be due to wrong or unaccepted request.
- 404 -Not Found The requested resource does not exist.
- 405 - Method not Allowed This can occure when the wrong method is used on a resource.
- 422 - Unprocessable This can occur when the request cannot be processed.

### Endpoint Library

#### GET/categories
- General:
    - Returns a list of categories objects, success value, and total number of categories of questions in the Trivia game.
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
    "categories": [
        {
          "id": 1,
          "type": "Science"
        },
        {
          "id": 2,
          "type": "Art"
        },
        {
          "id": 3,
          "type": "Geography"
        },
        {
          "id": 4,
          "type": "History"
        },
        {
          "id": 5,
          "type": "Entertainment"
        },
        {
          "id": 6,
          "type": "Sports"
        }
    ],    
    "success": true,
    "total_categories": 6
}
```
 

### Endpoint Library

#### GET/questions
- General:
    - Returns a list of questions, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`
```
{
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
          "answer": "Escher",
          "category": 2,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Jackson Pollock",
          "category": 2,
          "difficulty": 2,
          "id": 19,
          "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
          "answer": "Lake Victoria",
          "category": 3,
          "difficulty": 2,
          "id": 13,
          "question": "What is the largest lake in Africa?"
        },
        {
          "answer": "Agra",
          "category": 3,
          "difficulty": 2,
          "id": 15,
          "question": "The Taj Mahal is located in which Indian city?"
        },
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "George Washington Carver",
          "category": 4,
          "difficulty": 2,
          "id": 12,
          "question": "Who invented Peanut Butter?"
        },
        {
          "answer": "Alexander Fleming",
          "category": 1,
          "difficulty": 3,
          "id": 21,
          "question": "Who discovered penicillin?"
        },
        {
          "answer": "Mona Lisa",
          "category": 2,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        {
          "answer": "The Palace of Versailles",
          "category": 3,
          "difficulty": 3,
          "id": 14,
          "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 151
}
```

#### DELETE /books/{book_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list to update the frontend. 
- Sample: `curl -X DELETE http://127.0.0.1:5000/question/16?page=2`
```
{
    "deleted": 16,
    "questions": [
        {
          "answer": "Batists",
          "category": 5,
          "difficulty": 3,
          "id": 24,
          "question": "Crazy People?"
        },
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
          "answer": "The Liver",
          "category": 1,
          "difficulty": 4,
          "id": 20,
          "question": "What is the heaviest organ in the human body?"
        },
        {
          "answer": "One",
          "category": 2,
          "difficulty": 4,
          "id": 18,
          "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
          "answer": "Scarab",
          "category": 4,
          "difficulty": 4,
          "id": 23,
          "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
          "answer": null,
          "category": null,
          "difficulty": null,
          "id": 43,
          "question": null
        }
    ],
    "success": true,
    "total_questions": 150
}
```
 

#### POST /questions
- General:
    - Creates a new book using the submitted title, author and rating. Returns the id of the created book, success value, total books, and book list based on current page number to update the frontend. 
- Sample: ` curl -X POST -H "Content-Type: application/json" -d '{"question": "Life gives you Lemon?", "answer": "Make lemonade", "category": "5", "difficulty": "3"}' http://127.0.0.1:5000/questions'`
```
{
    "created": 156,
    "questions": [
        {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
        },
        {
        "answer": "Jackson Pollock",
        "category": 2,
        "difficulty": 2,
        "id": 19,
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
        },
        {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        },
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
        },
        {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
        },
        {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
        },
        {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 151
}
```
  

#### POST /questions/search
- General:
    - Retrieves questions with search term as part of the string in the question. Returns success value, total questions, and question list with search term as part of the question string. 
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "india"}' http://127.0.0.1:5000/questions/search`
``` {
    "questions": [
        {
          "answer": "Agra",
          "category": 3,
          "difficulty": 2,
          "id": 15,
          "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

#### POST /categories/2/questions
- General:
    - Retrieves questions belonging to a category. Returns success value, total questions in that category, and list of questions in the category.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions` 
```
{
    "questions": [
        {
          "answer": "Mona Lisa",
          "category": 2,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        {
          "answer": "One",
          "category": 2,
          "difficulty": 4,
          "id": 18,
          "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
          "answer": "Jackson Pollock",
          "category": 2,
          "difficulty": 2,
          "id": 19,
          "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

#### POST /quizzes
- General:
    - Retrieves quiz question, category of the quiz questions and previous questions from selected category
- Sample: `curl -X POST 'http://127.0.0.1:5000/quizzes' -H 'Content-Type: application/json' -d '{"previous_questions": [23, 12], "quiz_category":{"id":"4", "type":"History"}}'`


### Authors
Sudhanshu Kulshrestha
Sarah Maris
UAnjali
Celestine Okonkwo


### Acknowledgment
Amazing ALX and Udacity Teams, Special thanks to Coach Caryn and Blessing Odede.

   