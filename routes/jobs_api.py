from flask import Blueprint, jsonify, request
from data.db_session import create_session
from data.jobs import Jobs


blueprint = Blueprint(
    'jobs',
    __name__,
    template_folder='templates',
    url_prefix="/api/jobs"
)


@blueprint.route('/')
def get_job():
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'job':
                [item.to_dict(only=('team_leader',
                                    'job',
                                    'work_size',
                                    'collaborators',
                                    'end_date',
                                    'start_date',
                                    'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=('team_leader',
                                     'job',
                                     'work_size',
                                     'collaborators',
                                     'end_date',
                                     'start_date',
                                     'is_finished'))
        }
    )