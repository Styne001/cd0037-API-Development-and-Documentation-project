import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    # sourcery skip: inline-immediately-returned-variable
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):  # sourcery skip: do-not-use-bare-except
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*/api/*" : {"origins": '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    @cross_origin()
    def retrieve_categories():
        # Implement pagniation
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        
        # If the query returns nothing for categories abort and show error 404
        if len(categories) is None:
            abort(404)

        # return statement should state if the request is successful,
        #  available categories and total categories
        return jsonify({
                    "success": True,
                    "categories": formatted_categories,
                    "total_categories": len(formatted_categories)
                })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    @cross_origin()
    def retrieve_questions():
        # Implement pagniation
        selection = Question.query.order_by(Question.difficulty).order_by(Question.category).all()
        current_questions = paginate_questions(request, selection)
        query_categories = Category.query.all()
        categories = {category.id: category.type for category in query_categories}
        
        # If no questions is found abort and show error 404
        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": None,
                    "categories": categories
                })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    @cross_origin()
    def delete_question(question_id):
        try:
            # Get the question with the id from the Question table
            question = Question.query.filter(Question.id==question_id).one_or_none()

            # If the question does not exist show error 404
            if question is None:
                abort(404)

            # Otherwise delete selected question
            question.delete()
            selection = Question.query.order_by(Question.difficulty).order_by(Question.category).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except Exception:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST'])
    @cross_origin()
    def create_question():
        body = request.get_json()

        # Get the new question, answer, category, difficulty
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.difficulty).order_by(Question.category).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=['POST'])
    @cross_origin()
    def search_question():
        body = request.get_json()
        search = body.get('searchTerm', None)

        try:
            # Get questions having the search term as part of their string
            selection = Question.query.distinct(Question.question).filter(Question.question.ilike('%{}%'.format(search))).all()
            #paginate search_query
            current_question = paginate_questions(request, selection)
            # return search results
            return jsonify({
                'success': True,
                'questions': current_question,
                'search_term': search,
                'total_questions': len(selection)
            })
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:cat_id>/questions')
    @cross_origin()
    def questionsByCategory(cat_id):
        try:
            # Get categories by their id
            query_category = Category.query.filter(Category.id==cat_id).one_or_none()
            if query_category is None:
                abort(404)

            selection = Question.query.join(Category, Question.category==Category.id).filter(Question.category==cat_id)
            #paginate selection
            category_question = paginate_questions(request, selection)
            # return statement for questions in a category
            return jsonify({
                    'success': True,
                    'questions': category_question,
                    'total_questions': len(selection.all())
                })
        except Exception:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def quiz_game():

        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            # If previous_questions does not exist, create an empty list for previous_questions
            if previous_questions is None:
                previous_questions = []

            if quiz_category is None:
                selection = Question.query.all()
            # Get all questions not in previous questions if no category is selected
            if quiz_category['id'] == 0:
                selection = Question.query.filter(Question.id.notin_(previous_questions)).all()
            # If Category is selected, get questions in that category that is not in previous questions
            else:
                selection = Question.query.filter(Question.category==quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()
            
            # If all questions in same category are in previous_questions, question = None
            if not selection:
                question = None
                return jsonify({
                    'success': True
                })
            else:
                # This selects a question at random
                random_question = random.choice(selection)
            
            # format selected question
            question = random_question.format()

            return jsonify({
                'success': True,
                'quiz_category': quiz_category,
                'previous_questions': previous_questions,
                'question': question
            })
        
        except Exception:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    @cross_origin()
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    @cross_origin()
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    @cross_origin()
    def bad_method(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    @cross_origin()
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app

