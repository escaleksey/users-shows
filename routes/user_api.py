from flask import Blueprint, jsonify, request
from data.db_session import create_session
from data.users import User


blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    url_prefix="/api/user"
)


@blueprint.route('/')
def get_user():
    db_sess = create_session()
    users = db_sess.query(User).all()
    db_sess.close()
    return jsonify(
        {
            'user':
                [item.to_dict(only=('id',
                                    'name',
                                    'about',
                                    'email',
                                    'created_date',
                                    'city_from'))
                 for item in users]
        }
    )



@blueprint.route('/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return jsonify(
        {
            'user':
                user.to_dict(only=('id',
                                    'name',
                                    'about',
                                    'email',
                                    'created_date',
                                    'city_from'))
        }
    )


@blueprint.route('/', methods=['POST'])
def create_job():
    keys = ['id', 'name',
            'about',
            'email',
            'password',
            'city_from']
    print(request.json)
    print(keys)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in keys
                 ):
        return jsonify({'error': 'Bad request'})
    db_sess = create_session()
    exist_user = db_sess.query(User).get(request.json['id'])
    exist_email = db_sess.query(User).get(request.json['email'])
    if exist_user:
        db_sess.close()
        return jsonify({'error': ' Id already exists'})
    if exist_email:
        db_sess.close()
        return jsonify({'error': ' Email already exists'})
    user = User(
        id=request.json['id'],
        name=request.json['name'],
        about=request.json['about'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/<int:user_id>', methods=["PUT"])
def put_job(user_id):
    keys = ['name',
            'about',
            'email',
            'password',
            'city_from']
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if user:
        if not request.json:
            db_sess.close()
            return jsonify({'error': 'Empty request'})
        elif not any(key in request.json for key in keys):
            db_sess.close()
            return jsonify({'error': 'Bad request'})

        for key, new_value in request.json.items():
            setattr(user, key, new_value)

        db_sess.commit()
        db_sess.close()
        return jsonify({'success': 'OK'})
    else:
        db_sess.close()
        return jsonify({'error': 'Not found'})


@blueprint.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = create_session()
    user = db_sess.query(User).get(job_id)
    if user:
        db_sess.delete(user)
        db_sess.commit()
        db_sess.close()
        return jsonify({'success': 'OK'})
    else:
        db_sess.close()
        return jsonify({'error': 'Not found ID'})