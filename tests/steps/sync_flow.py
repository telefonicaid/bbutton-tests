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
import random

from iotqatools.orchestator_utils import Orchestrator
from iotqatools.iota_utils import Rest_Utils_IoTA
from common.common import cb_sample_entity_create, cb_sample_entity_recover, ks_get_token, \
    component_verifyssl_check, orc_get_services, orc_delete_service
from common.test_utils import *
from nose.tools import eq_, assert_in, assert_true, assert_greater_equal, assert_not_in
from pymongo import MongoClient

__logger__ = logging.getLogger("sync_flow")
#use_step_matcher("re")

@step(u'a service and subservice are created in the "{instance}"')
def provision_atorchestrator(context, instance):

    context.service_admin = "admin_domain"
    context.user_admin = "cloud_admin"
    context.password_admin = "password"
    context.services = orc_get_services(context)
    for service in context.services:
        if context.service == service["name"]:
            __logger__.debug("service retrieved: {} {}".format(service["name"], service["id"]))
            context.service_id = service["id"]
            break

    # Get config env credentials
    context.user_admin = "cloud_admin"
    context.password_admin = "password"

    try:
        if "service_id" in context:
            delete_response = orc_delete_service(context, context.service_id)

    except ValueError:
        __logger__.error("[Error] Service to delete ({}) not found".format(context.service))





    # Composing payloads
    payload_service = dict(context.table[0:6])
    context.user = payload_service["NEW_SERVICE_ADMIN_USER"]
    context.pwd = payload_service["NEW_SERVICE_ADMIN_PASSWORD"]
    payload_service.update({"KEYPASS_PROTOCOL": "http", "KEYPASS_HOST": "localhost"})
    if "NEW_SERVICE_DESCRIPTION" not in payload_service:
        payload_service["NEW_SERVICE_DESCRIPTION"] = payload_service["NEW_SERVICE_NAME"]
    if "SERVICE_NAME" not in payload_service:
        payload_service["SERVICE_NAME"] = payload_service["NEW_SERVICE_NAME"]


    payload_servicepath = dict(context.table[6:])
    payload_servicepath.update({"KEYPASS_PROTOCOL": "http", "KEYPASS_HOST": "localhost", "KEYSTONE_PROTOCOL": "http", "KEYSTONE_HOST": "localhost"})
    if "SERVICE_NAME" not in payload_servicepath:
        payload_servicepath["SERVICE_NAME"] = payload_service["NEW_SERVICE_NAME"]
    if "SERVICE_ADMIN_USER" not in payload_servicepath:
        payload_servicepath["SERVICE_ADMIN_USER"] = payload_service["NEW_SERVICE_ADMIN_USER"]
    if "SERVICE_ADMIN_PASSWORD" not in payload_servicepath:
        payload_servicepath["SERVICE_ADMIN_PASSWORD"] = payload_service["NEW_SERVICE_ADMIN_PASSWORD"]
    if "NEW_SUBSERVICE_DESCRIPTION" not in payload_servicepath:
        payload_servicepath["NEW_SUBSERVICE_DESCRIPTION"] = payload_servicepath["NEW_SUBSERVICE_NAME"]


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
    __logger__.debug("Create service: {}, \n url: {}".format(json_orcservice, url_service))

    context.r = requests.post(url=url_service, headers=context.headers, data=json_orcservice)
    context.create_service = context.r.content
    jsobject = json.loads(context.create_service)

    context.headers["Fiware-Service"] = context.service
    context.headers["Fiware-ServicePath"] = context.servicepath

    context.service_id = jsobject["id"]
    context.token_service = jsobject["token"]


    # ServicePath provision
    context.headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    url_subservice = '{}/v1.0/service/{}/subservice'.format(context.url_component, context.service_id)
    json_servicepath = json.dumps(payload_servicepath)
    __logger__.debug("Create subservice: {}, \n url: {}".format(json_servicepath, url_subservice))
    context.resp = requests.post(url=url_subservice, headers=context.headers, data=json_servicepath)
    context.create_servicepath = context.resp.content
    jsobject_s = json.loads(context.create_servicepath)

    context.subservice_id = jsobject_s["id"]






@step(
    u'a device "{device_id}" of entity_type "{entity_type}" should be provisioned for service and subservice')
def step_impl(context, device_id, entity_type):
    # Preparing device provision
    context.device_id = str(device_id)
    device_payload = dict(context.table)
    if "no" in device_payload["TOKEN"]:
        device_payload.update({"SERVICE_USER_NAME": context.user, "SERVICE_USER_PASSWORD": context.pwd, "SERVICE_NAME": context.service, "SUBSERVICE_NAME": context.subservice})
    else:
        device_payload.update({"SERVICE_NAME": context.service, "SUBSERVICE_NAME": context.subservice})
        context.headers.update({"X-Auth-Token": context.token})
    del device_payload['TOKEN']

    device_payload.update({"PROTOCOL": "TT_BLACKBUTTON", "DEVICE_ID": device_id, "ENTITY_TYPE": entity_type})
    device_payload.update({"SERVICE_ADMIN_USER": context.user, "SERVICE_ADMIN_PASSWORD": context.pwd})
    device_payload.update({"SERVICE_USER_NAME": context.user, "SERVICE_USER_PASSWORD": context.pwd, "SERVICE_NAME": context.service, "SUBSERVICE_NAME": context.subservice})
    #device_payload.update({"IOTA_PROTOCOL": "http", "IOTA_HOST": "localhost", "IOTA_PORT": "4041",
    #                       "ORION_PROTOCOL": "http", "ORION_HOST": "localhost", "ORION_PORT": "10026",
    #                       "KEYSTONE_HOST": "localhost", "KEYSTONE_PORT": "5000"})

    if "NaN" not in device_payload["ATT_GEOLOCATION"]:
        imei = str(random.randint(1000000, 9999999999))
        imsi = str(random.randint(1000000, 9999999999))
        device_payload.update({"ATT_IMEI": imei, "ATT_IMSI": imsi, "ATT_CCID": "AAA", "ATT_SERVICE_ID": context.service})
    else:
        del device_payload['ATT_GEOLOCATION']
        del device_payload["ATT_INTERACTION_TYPE"]

    json_payload = json.dumps(device_payload)

    # Preparing url
    url = context.url_component + '/v1.0/service/' + \
          context.service_id + '/subservice/' + \
          context.subservice_id + '/register_device'

    __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))

    context.resp = requests.post(url=url,
                              headers=context.headers,
                              data=json_payload)


@step(u'a close request is sent to finish the operation')
def close_message(context):
    cl_message = "#1,BT,X,1,0,#0,K1,30$"
    iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
               context.config["components"]["IOTA"]["instance"] + ":" + \
               context.config["components"]["IOTA"]["south_port"] + "/thinkingthings"

    # /custom uri
    iota_url = iota_url + "/Receive"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        # 'Accept': "application/json"
    }

    measure = "#{},{}".format(context.device_id, cl_message)
    data = {"cadena": measure}
    context.r = requests.post(url=iota_url, data=data, headers=headers)

    eq_(200, context.r.status_code, "ERROR: MEASURE request IOTA failed: {}".format(context.r.status_code))
    # show returned response
    __logger__.debug("IOTA (send_measure) returns {} ".format(context.r.content))


@step(
    'the button "{}" pressed in mode "{}" the IOTA should receive the request "{}"')
def send_button(context, device_id, sync_mode, bt_request):
    iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
               context.config["components"]["IOTA"]["instance"] + ":" + \
               context.config["components"]["IOTA"]["south_port"] + "/thinkingthings"

    # /custom uri
    iota_url = iota_url + "/Receive"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        # 'Accept': "application/json"
    }

    measure = "#{},{}".format(device_id, bt_request)
    data = {"cadena": measure}
    context.r = requests.post(url=iota_url, data=data, headers=headers)

    eq_(200, context.r.status_code, "ERROR: MEASURE request IOTA failed: {}".format(context.r.status_code))

    # show returned response
    __logger__.debug("IOTA (send_measure) returns {} ".format(context.r.content))



@step(u"a device should be provisioned for service and subservice with certain fields")
def registration_fields(context):
    payload = dict(context.table)
    if "yes" in payload["TOKEN"]:
        context.headers.update({"X-Auth-Token": context.token})
    del payload['TOKEN']

    for key, value in payload.items():
        if "NaN" in value:
            del payload[key]

    json_payload=json.dumps(payload)
    url = context.url_component + '/v1.0/service/' + \
          context.service_id + '/subservice/' + \
          context.subservice_id + '/register_device'

    __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))

    context.resp_validation = requests.post(url=url, headers=context.headers, data=json_payload)



@step(u'registration is not sucessful and device "{device_id}" is not listened under the service and subservice')
def registration_fail_validation(context, device_id):
    __logger__.debug("ERROR CASE: {}. \nREASON: {}".format(context.resp_validation.status_code, context.resp_validation.text))
    eq_(400, context.resp_validation.status_code, "Device was created successfully")


