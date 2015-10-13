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
from behave import *
import requests
import logging
import json
import time

from iotqatools.orchestator_utils import Orchestrator
from iotqatools.iota_utils import Rest_Utils_IoTA
from common.common import cb_sample_entity_create, cb_sample_entity_recover, ks_get_token, \
    component_verifyssl_check, orc_get_services, orc_delete_service
from common.test_utils import *
from nose.tools import eq_, assert_in, assert_true, assert_greater_equal, assert_not_in
from pymongo import MongoClient

__logger__ = logging.getLogger("sync_flow")
#use_step_matcher("re")

@step(u'the subservice is created in the "{instance}"')
def provision_atorchestrator(context, instance):

    payload_service = dict(context.table[0:12])
    payload_servicepath = dict(context.table[10:17])

    context.headers = {"Accept": "application/json", "Content-type": "application/json"}

    context.instance_ip = context.config['components'][instance]['instance']
    context.instance_port = context.config['components'][instance]['port']
    context.instance_protocol = context.config['components'][instance]['protocol']

    context.url_component = get_endpoint(context.instance_protocol,
                                         context.instance_ip,
                                         context.instance_port)
    # Service provision
    url_service = '{}/v1.0/service'.format(context.url_component)
    json_orcservice = json.dumps(payload_service)

    context.r = requests.post(url=url_service, headers=context.headers, data=json_orcservice)
    context.create_service = context.r.content
    jsobject = json.loads(context.create_service)
    print(context.r)
    print(jsobject)

    context.headers["Fiware-Service"] = context.service
    context.headers["Fiware-ServicePath"] = context.servicepath

    context.service_id = jsobject["id"]
    context.token_service = jsobject["token"]


    """
    json_orcservice = json.dumps(payload_service)
    __logger__.debug("Create service: {}, \n url: {}".format(json_orcservice, url))
    # Subservice provision
    url_servicepath = '{}/v1.0/service/{}/subservice'.format(context.url_component, context.service)
    #context.resp = requests.post(url=url, headers=context.headers, data=json_orcservice)
    #print(context.resp)
    context.create_subservice = context.r.content
    jsobject = json.loads(context.create_subservice)
    context.subservice_id = jsobject["id"]
    """
    assert False




@step(u'the button "{device_id}" is pressed in mode "{sync_mode}" the IOTA should receive the request')
def step_impl(context, device_id, sync_mode):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type SYNC_MODE str
    """
    pass


def delete_method(context):
    url = str("{0}/v1.0/service".format(context.url_component))
    #Get list of services
    for service in context.services:
        if context.service == service["name"]:
            print ("service retrieved: {} {}".format(service["name"], service["id"]))
            context.service_id = service["id"]
            break

    # Get config env credentials
    context.user_admin = "cloud_admin"
    context.password_admin = "password"

    if "service_id" in context:
        delete_response = orc_delete_service(context, context.service_id)
        eq_(204, delete_response,
            "[ERROR] Deleting Service {} responsed a HTTP {}".format(context.service_id, delete_response))
    else:
        eq_(True, False, "[Error] Service to delete ({}) not found".format(context.service))
