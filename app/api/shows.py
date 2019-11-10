import math
from urllib import parse

from flask import request
from flask_restplus import Namespace, Resource, fields, Api, reqparse

from app import constants, settings, exceptions, utils
from app.models.show import Show
from app.api.utils import authenticate, is_admin

ns = Namespace(
    'Shows',
    description='''Show CRUD operations, encapsulates the operations for show manipulation.'''
)

show_schema = ns.model('Show', {
    'id': fields.String(required=True, description='Unique identifier id for this show'),
    'title': fields.String(required=True, description='Show title'),
    'description': fields.String(required=True, description='Description of the show'),
    'created_at': fields.String(required=True, description='Datetime stamp of record'),
    'dash_src_video_url': fields.String(required=True, description='Dash source video URL'),
    'hls_src_video_url': fields.String(required=True, description='HLS source video URL')
})

KEY_SHOW_ID = 'id'
KEY_SHOW_TITLE = 'title'


class BaseShowResource(Resource):
    @staticmethod
    def serialize(show):
        return {
            KEY_SHOW_ID: show.id,
            KEY_SHOW_TITLE: show.title
        }

    @staticmethod
    def item_path_list(**kwargs):
        utils.LOGGER.info("{} - {}".format(kwargs, parse.urlencode(kwargs)))
        return '{}/{}/shows{}'.format(
            settings.get_var('HOST'), settings.get_var('API_VERSION'),
            '?{}'.format(parse.urlencode(kwargs)) if kwargs else '')


@ns.route('', methods=['GET', 'POST', ], endpoint='show-list')
class ShowListResource(Resource):

    @ns.marshal_list_with(show_schema, envelope='data')
    def get(self, **kwargs):
        utils.LOGGER.debug("Executing GET on predictors.")
        shows = Show.query.order_by(Show.created_at.desc()).all()
        return shows

    @ns.marshal_list_with(show_schema, envelope='data')
    def post(self, **kwargs):
        utils.LOGGER.debug('Executing POST on predictors.')
        data = request.json
        new_show = Show(
            title=data['title'],
            description=data['description'],
            dash_src_video_url=data['dashSrcVideoURL'],
            hls_src_video_url=data['hlsSrcVideoURL']
        )
        new_show.save()
        return new_show, 201


@ns.route('/<show_id>', methods=['GET', 'PATCH', 'DELETE', ], endpoint='show-details')
class PredictorAPI(Resource):
    @ns.doc(params={'show_id': 'The ID of the show you want to retrieve data from.'})
    def get(self, show_id=None):
        utils.LOGGER.debug('Executing GET on shows.')
        show = Show.query.filter_by(id=int(show_id)).first()
        if show is None:
            raise exceptions.ResourceNotFound()
        return show

    @authenticate
    @ns.doc(params={'show_id': 'The ID of the show you want to delete.'})
    def delete(self, show_id=None):
        utils.LOGGER.debug('Executing DELETE on shows.')
        show = Show.query.filter_by(id=int(show_id)).first()
        if show is None:
            raise exceptions.ResourceNotFound()
        return self.format_item(show)