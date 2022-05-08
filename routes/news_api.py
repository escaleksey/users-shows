from flask import Blueprint
from flask import jsonify
from data.db_session import create_session
from data.news import News

blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates',
    url_prefix='/api/news'
)

@blueprint.route('/')
def get_news():
    db_sess = create_session()
    news = db_sess.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in news]
        }
    )

@blueprint.route('/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )