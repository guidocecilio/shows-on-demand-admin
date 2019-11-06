import math
from urllib import parse
from flask_restplus import Namespace, Resource, fields, Api, reqparse

from admin import constants
from admin import models
from admin import settings
from admin import exceptions
from admin import utils

ns = Namespace(
    'Shows',
    description='''Show CRUD operations, encapsulates the operations for show manipulation.'''
)

KEY_SHOW_ID = 'id'
KEY_SHOW_TITLE = 'title'

"""
A base schema you can use to marshall any GET responses that require pagination.
All that you need is to define schema of your entity and extend this, E.G.


models_list_results = ns.inherit('PaginatedModelsResult', api.PAGINATED_RESULTS_SCHEMA, {
    constants.KEY_ENTITIES: fields.List(
        api.fields.Nested(models_get_schema),
        description='A list of models.'
    )
})
"""
PAGINATED_RESULTS_SCHEMA = ns.model('PaginatedResultsSchema', {
    constants.KEY_TOTAL: fields.Integer(
        required=True,
    ),
    constants.KEY_PAGE_SIZE: fields.Integer(
        required=True,
    ),
    constants.KEY_PAGE_COUNT: fields.Integer(
        required=True,
    ),
    constants.KEY_PAGE_NUMBER: fields.Integer(
        required=True,
    ),
    constants.KEY_FIRST_URI: fields.String(
        required=True,
    ),
    constants.KEY_LAST_URI: fields.String(
        required=True,
    ),
    constants.KEY_NEXT_URI: fields.String(
        required=True,
    ),
    constants.KEY_PREVIOUS_URI: fields.String(
        required=True,
    ),
})

""" Parser you can use as input validation for any GET endpoints that support pagination """
PAGINATION_INPUT = reqparse.RequestParser()
PAGINATION_INPUT.add_argument(
    constants.KEY_PAGE_SIZE,
    type=int,
    required=False,
    help='The size of the page you want.'
)
PAGINATION_INPUT.add_argument(
    constants.KEY_PAGE_NUMBER,
    type=int,
    required=False,
    help='The page number you are looking for'
)


class BaseShowResource(Resource):
    @staticmethod
    def serialize(show):
        return {
            KEY_SHOW_ID: show.id,
            KEY_SHOW_TITLE: show.title
        }

    @staticmethod
    def item_path_list(organization_id, **kwargs):
        utils.LOGGER.info("{} - {}".format(kwargs, parse.urlencode(kwargs)))
        return '{}/{}/shows{}'.format(
            settings.get_var('HOST'), settings.get_var('API_VERSION'),
            '?{}'.format(parse.urlencode(kwargs)) if kwargs else '')


# def q(page=0, page_size=None):
#     query = session.query()
#     listen(query, 'before_compile', apply_limit(page, page_size), retval=True)
#     return query
# def apply_limit(page, page_size):
#     def wrapped(query):
#         if page_size:
#             query = query.limit(page_size)
#             if page:
#                 query = query.offset(page * page_size)
#         return query
#     return wrapped


@ns.route('', methods=['GET', 'POST', ], endpoint='show-list')
class ShowListResource(BaseShowResource):
    PAGE_SIZE = 10

    def get_paginated_list(self, **kwargs):
        page_size = int(kwargs.get(constants.KEY_PAGE_SIZE, self.PAGE_SIZE))
        page_number = int(kwargs.get(constants.KEY_PAGE_NUMBER, 1))
        if page_number < 1:
            page_number = 1
        query_results = models.Show.query().limit(page_size).offset((page_number - 1) * page_size)
        total_items = query_results[constants.KEY_TOTAL]
        page_size = int(kwargs.get(constants.KEY_PAGE_SIZE, self.PAGE_SIZE))
        if page_size > total_items:
            page_size = total_items
        page_number = int(kwargs.get(constants.KEY_PAGE_NUMBER, 1))
        if page_number < 1:
            page_number = 1
        if page_size:
            page_count = math.ceil(total_items / page_size)
        else:
            page_count = 0

        if page_number > page_count:
            page_number = page_count
        first_uri = self.self.item_path_list(**{
            constants.KEY_PAGE_SIZE: page_size,
            constants.KEY_PAitem_path_listGE_NUMBER: 1
        })
        last_uri = self.item_path_list(**{
            constants.KEY_PAGE_SIZE: page_size,
            constants.KEY_PAGE_NUMBER: page_count
        })
        next_uri = self.item_path_list(**{
            constants.KEY_PAGE_SIZE: page_size,
            constants.KEY_PAGE_NUMBER: page_number + 1
        }) if page_number < page_count else ''
        prev_uri = self.item_path_list(**{
            constants.KEY_PAGE_SIZE: page_size,
            constants.KEY_PAGE_NUMBER: page_number - 1
        }) if page_number > 1 else ''

        return {
            constants.KEY_TOTAL: total_items,
            constants.KEY_PAGE_SIZE: page_size,
            constants.KEY_PAGE_COUNT: page_count,
            constants.KEY_PAGE_NUMBER: page_number,
            constants.KEY_FIRST_URI: first_uri,
            constants.KEY_LAST_URI: last_uri,
            constants.KEY_NEXT_URI: next_uri,
            constants.KEY_PREVIOUS_URI: prev_uri,
            constants.KEY_ENTITIES: [self.serialize(show) for show in query_results[constants.KEY_ENTITIES]]
        }

    @ns.expect(PAGINATION_INPUT)
    def get(self, organization_id, **kwargs):
        utils.LOGGER.debug("Executing GET on predictors.")
        return self.get_paginated_list(**kwargs)

    def post(self, organization_id, **kwargs):
        utils.LOGGER.debug('Executing POST on predictors.')
        print(kwargs)
        return {}


@ns.route('/<show_id>', methods=['GET', 'PATCH', 'DELETE', ], endpoint='show-details')
class PredictorAPI(BaseShowResource):
    @ns.doc(params={'show_id': 'The ID of the show you want to retrieve data from.'})
    def get(self, show_id=None):
        utils.LOGGER.debug('Executing GET on shows.')
        show = models.Show.query.filter_by(id=int(show_id)).first()
        if show is None:
            raise exceptions.ResourceNotFound()
        return self.format_item(show)
