# coding: utf-8

import datetime
from flask import Blueprint, url_for
from flask import render_template, Response
from ..helpers import require_user
from ..models import Node, Topic, fill_topics, cache


bp = Blueprint('front', __name__)


@bp.route('/')
def home():
    """The homepage of the site."""
    topics = Topic.query.order_by(Topic.id.desc()).limit(16)
    topics = fill_topics(topics)
    nodes = Node.query.order_by(Node.id.desc()).limit(10)

    # blog is a special node, get the latest posts from blog
    blog = Node.query.filter_by(urlname='blog').first()
    if blog:
        blogs = Topic.query.filter_by(
            node_id=blog.id).order_by(Topic.id.desc()).limit(2)
    else:
        blogs = None

    return render_template(
        'index.html', topics=topics, nodes=nodes, blog=blog, blogs=blogs
    )


@bp.route('/feed')
def feed():
    html = cache.get('sitefeed')
    if not html:
        topics = Topic.query.order_by(Topic.id.desc()).limit(16)
        topics = fill_topics(topics)
        now = datetime.datetime.now()
        html = render_template('feed.xml', topics=topics, now=now)
        cache.set('sitefeed', html, 1800)

    return Response(html, content_type='text/xml; charset=utf-8')


@bp.route('/upload', methods=['POST'])
@require_user
def upload():
    """Upload images handler."""
    #TODO
    return ''
