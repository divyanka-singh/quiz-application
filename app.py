from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

quizzes = []
quiz_id_counter = 1


def get_quiz_by_id(quiz_id):
    for quiz in quizzes:
        if quiz['id'] == quiz_id:
            return quiz
    return None


def update_quiz_status(quiz):
    now = datetime.now()
    if now < quiz['startDate']:
        quiz['status'] = 'inactive'
    elif now >= quiz['startDate'] and now <= quiz['endDate']:
        quiz['status'] = 'active'
    else:
        quiz['status'] = 'finished'


def get_active_quiz():
    for quiz in quizzes:
        update_quiz_status(quiz)
        if quiz['status'] == 'active':
            return quiz
    return None


@app.route('/quizzes', methods=['POST'])
def create_quiz():
    global quiz_id_counter
    data = request.get_json()
    quiz = {
        'id': quiz_id_counter,
        'question': data['question'],
        'options': data['options'],
        'rightAnswer': data['rightAnswer'],
        'startDate': datetime.strptime(data['startDate'], '%Y-%m-%d %H:%M:%S'),
        'endDate': datetime.strptime(data['endDate'], '%Y-%m-%d %H:%M:%S'),
        'status': 'inactive'
    }
    quiz_id_counter += 1
    quizzes.append(quiz)
    return jsonify({'message': 'Quiz created successfully'}), 201


@app.route('/quizzes/active', methods=['GET'])
def get_active_quiz_endpoint():
    active_quiz = get_active_quiz()
    if active_quiz:
        return jsonify(active_quiz)
    return jsonify({'message': 'No active quiz found'})


@app.route('/quizzes/<int:quiz_id>/result', methods=['GET'])
def get_quiz_result(quiz_id):
    quiz = get_quiz_by_id(quiz_id)
    if quiz:
        update_quiz_status(quiz)
        if quiz['status'] == 'finished':
            return jsonify({'result': quiz['rightAnswer']})
        return jsonify({'message': 'Quiz is still active'})
    return jsonify({'message': 'Quiz not found'})


@app.route('/quizzes/all', methods=['GET'])
def get_all_quizzes():
    return jsonify(quizzes)


if __name__ == '__main__':
    app.run(debug=True)
