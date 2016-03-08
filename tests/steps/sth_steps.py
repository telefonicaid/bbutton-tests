#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2015 Telefonica Investigación y Desarrollo, S.A.U
This file is part of telefonica-iot-qa-tools
orchestrator is free software: you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
orchestrator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public
License along with orchestrator.
If not, seehttp://www.gnu.org/licenses/.
For those usages not covered by the GNU Affero General Public License
please contact with::[iot_support@tid.es]

"""
import json
import logging

from behave import *
from nose.tools import *
from common.test_utils import initialize_sth, initialize_cb
import cb_steps

__logger__ = logging.getLogger("sth")


def _check_attr_exists(context, entity, attname, expected_values):
    """
    Checks if the sth has registered values for an entity and an attribute. If no values, STH returns an empty array
    """

    n_values = len(expected_values)
    # is authenticated?
    token = None
    if 'token_scope' in context:
        token = context.token_scope
    elif 'token' in context:
        token = context.token

    resp = context.o["STH"].request_raw_data(entity['entity_type'],
                                             entity['entity_id'],
                                             attname,
                                             lastN=100,
                                             token=token)
    eq_(200, resp.status_code)

    resp_json = json.loads(resp.content)
    __logger__.info(resp_json)
    resp_list = resp_json['contextResponses']
    eq_(len(resp_list), 1)
    eq_(resp_list[0]['contextElement']['attributes'][0]['name'], attname)
    values = [sample['attrValue'] for sample in resp_list[0]['contextElement']['attributes'][0]['values']]
    eq_(len(values), n_values)
    for i, val in enumerate(expected_values):
        eq_(val, values[i])


@step(u'service and subservice are provisioned in STH')
def init_sth_client(context):
    """
    Configures STH client with service and subservice.
    """
    servicePath = context.servicepath if context.servicepath.startswith("/") else "/" + context.servicepath

    initialize_sth(context)
    context.o["STH"].set_service(context.service)
    context.o["STH"].set_subservice(servicePath)


def init_cb_client(context):
    """
    Configures CB client with service and subservice.
    """
    servicePath = context.servicepath if context.servicepath.startswith("/") else "/" + context.servicepath

    initialize_cb(context)
    context.o["CB"].set_service(context.service)
    context.o["CB"].set_subservice(servicePath)


@step(u'service and subservice are provisioned in ContextBroker and STH')
def init_clients(context):
    """
    Configures CB and STH clients with service and subservice.
    """
    init_sth_client(context)
    init_cb_client(context)


@step(u'I check entity with "{entity_id}" and "{entity_type}" has the attribute "{attname}" registered in STH ' +
      u'and has samples for "{att_values}"')
def check_attr_exists_in_entity(context, entity_id, entity_type, attname, att_values):
    values = att_values.split(";")
    entity = {'entity_id': entity_id, 'entity_type': entity_type}
    _check_attr_exists(context, entity, attname, values)


@step(u'I check attribute "{attname}" was registered in STH for every entity created and ' +
      u'has samples for "{att_values}"')
def check_attr_exists_all_entities(context, attname, att_values):
    values = att_values.split(";")
    for entity in context.entity_list:
        _check_attr_exists(context, entity, attname, values)


@step(u'I check entity with "{entity_id}" and "{entity_type}" does not have the attribute "{attname}" ' +
      u'registered in STH')
def check_attr_not_exist_in_entity(context, entity_id, entity_type, attname):
    entity = {'entity_id': entity_id, 'entity_type': entity_type}
    _check_attr_exists(context, entity, attname, [])  # when attr doesn't exist, STH returns an attr with values = []


@step(u'I send a notification with "{subs_id}" and "{n_elements}" context elements ' +
      u'with id "{entity_id}" and type "{entity_type}"')
def send_notification(context, subs_id, n_elements, entity_id, entity_type):
    """
    Sends a notification to STH with a notification payload containing the number of contextElements specified as param.
    Creates:
        entity_id,
        entity_id_1
        ...
        entity_id_n-1
    Each one containing the attributes specified in context.table.
    """

    def _transform_context_element(el):
        new_el = {
            "contextElement": el,
            "statusCode": {"code": "200", "reasonPhrase": "OK"}
        }

        return new_el

    context_elements = cb_steps.compose_context_elements_list(entity_id, entity_type, n_elements, context)
    element_list = context_elements.get_context_elements()

    # add response statusCode for each contextElement
    context_responses = map(_transform_context_element, element_list)
    payload = {
        "subscription_id": subs_id,
        "originator": "orion.contextBroker.mock",
        "contextResponses": context_responses

    }

    # is authenticated?
    token = None
    if 'token_scope' in context:
        token = context.token_scope
    elif 'token' in context:
        token = context.token
    context.o["STH"].send_notification(payload, token=token)


@step(u'I delete from STH all the data associated to')
def deleteData(context):
    """
    Deletes all the data stored in STH related to the context.table query
    :param context: behave.runner.Context. Must contain a table of the format:
      |  service         |  <SERVICE>     |
      |  subservice      |  <SERVICEPATH> |
      |  entity_id       |  <ENTITY_ID>   |
      |  entity_type     |  <ENTITY_TYPE> |
      |  attribute_name  |  <ATTNAME>     |
      every row is optional but the must contain the needed rows to make the proper query
      Queries:
       * Delete all the data associated to certain attribute of certain entity of certain service and servicepath
       * Delete all the data associated to certain entity of certain service and servicepath
       * Delete all the data associated to certain service and servicepath
    :return:
    """

    # is authenticated?
    token = None
    if 'token_scope' in context:
        token = context.token_scope
    elif 'token' in context:
        token = context.token

    kwargs = dict(context.table)
    #rename needed args

    if "entity_id" in kwargs:
        kwargs["ent_id"] = kwargs.pop("entity_id")
    if "entity_type" in kwargs:
        kwargs["ent_type"] = kwargs.pop("entity_type")
    if "attribute_name" in kwargs:
        kwargs["attribute"] = kwargs.pop("attribute_name")
    if "subservice" in kwargs:
        if kwargs["subservice"].startswith("/"):
            kwargs["subservice"] = kwargs["subservice"]
        else:
            kwargs["subservice"] = "/" + kwargs["subservice"]

    kwargs["token"] = token

    context.o["STH"].delete(**kwargs)