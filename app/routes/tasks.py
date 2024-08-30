from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_blueprint = Blueprint('task', __name__)


@tasks_blueprint.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_task = Task(
        title=data['title'], 
        description=data['description'], 
        priority=data.get('priority', 'Medium'),
        due_date=data['due_date'], 
        user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.id), 201

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.is_completed = data.get('is_completed', task.is_completed)
    task.due_date = data.get('due_date', task.due_date)
    db.session.commit()
    return jsonify({'message': 'Task updated'}), 200

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

@tasks_blueprint.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200