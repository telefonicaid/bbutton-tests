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

__author__ = 'xvc'

from behave import *
import requests
import logging
import json
import time

from iotqatools.orchestator_utils import Orchestrator
from nose.tools import eq_, assert_in, assert_true, assert_greater_equal
from iotqatools.iota_utils import Rest_Utils_IoTA
from common.common import cb_sample_entity_create, cb_sample_entity_recover, ks_get_token, \
    component_verifyssl_check
from common.test_utils import *

__logger__ = logging.getLogger("happy_path")
use_step_matcher("re")


@given('a Client of "(?P<SERVICE>.+)" and a ThirdParty called "(?P<SERVICEPATH>.+)"')
def step_impl(context, SERVICE, SERVICEPATH):
    """
    :type context behave.runner.Context
    :type SERVICE str
    :type SERVICEPATH str
    """
    context.service = SERVICE
    context.servicepath = SERVICEPATH


@step('the "(?P<INSTANCE>.+)" receive the request "(?P<REQUEST>.+)" and action "(?P<ACTION>.+)"')
def step_impl(context, INSTANCE, REQUEST, ACTION):
    """
    :type context behave.runner.Context
    :type INSTANCE str
    :type REQUEST str
    :type ACTION str
    """
    context.instance = INSTANCE

    # Setup default headers
    context.headers = {}
    context.headers = {"Accept": "application/json", "Content-type": "application/json"}

    # recover the data to send the request
    context.instance_ip = context.config['components'][INSTANCE]['instance']
    context.instance_port = context.config['components'][INSTANCE]['port']
    context.instance_protocol = context.config['components'][INSTANCE]['protocol']

    context.url_component = get_endpoint(context.instance_protocol,
                                         context.instance_ip,
                                         context.instance_port)

    if INSTANCE == "ORC" and REQUEST == "SERVICE_ENTITY" and ACTION == "CREATE":
        url = '{}/v1.0/service/{}/subservice/{}/register_service'.format(context.url_component,
                                                                         context.service_id,
                                                                         context.subservice_id)

        context.headers.update({"Fiware-Service": "{}".format(context.service)})
        context.headers.update({"Fiware-ServicePath": "/{}".format(context.servicepath)})
        print (context.headers)
        payload_table = dict(context.table)
        payload_table['ATT_TIMEOUT'] = int(payload_table['ATT_TIMEOUT'])

        # Properties replacement Var environment
        tp_url = payload_table['ATT_ENDPOINT']
        if "TP" in tp_url:
            tp_endpoint = "{}://{}:{}".format(context.config['components']["TP"]['protocol'],
                                              context.config['components']["TP"]['instance'],
                                              context.config['components']["TP"]['port'])

            payload_table['ATT_ENDPOINT'] = tp_url.replace("TP", tp_endpoint)

        json_payload = json.dumps(payload_table)
        print (json_payload)
        __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))
        context.r = requests.post(url=url,
                                  headers=context.headers,
                                  data=json_payload)

        eq_(context.r.status_code, 201,
            "[ERROR] when calling {} responsed a HTTP {}".format(url, context.r.status_code))
        context.create_service_entity = context.r.content
        print (context.create_service_entity)

    if INSTANCE == "ORC" and REQUEST == "SERVICE" and ACTION == "CREATE":
        url = context.url_component + '/v1.0/service'
        json_payload = json.dumps(dict(context.table))


        # print (json_payload)
        __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))
        context.r = requests.post(url=url,
                                  headers=context.headers,
                                  data=json_payload)

        # print (context.r.content)
        __logger__.debug(context.r.content)
        __logger__.debug(context.r.status_code)
        eq_(context.r.status_code, 201,
            "[ERROR] when calling {} responsed a HTTP {}".format(url, context.r.status_code))
        context.create_service = context.r.content
        jsobject = json.loads(context.create_service)
        context.service_id = jsobject["id"]
        context.token_service = jsobject["token"]
        print ("\n --->>  ID service: {} <<--- \n".format(context.service_id))
        print ("TOKEN service: {} \n".format(context.token_service))


@then('subservice "(?P<SERVICEPATH>.+)" under the service is created')
def step_impl(context, SERVICEPATH):
    """
    :type context behave.runner.Context
    :type SERVICEPATH str
    """
    context.instance = "ORC"

    # Setup default headers
    context.headers = {}
    context.headers = {'Accept': 'application/json', 'Content-type': 'application/json'}

    # recover the data to send the request
    context.instance_ip = context.config['components'][context.instance]['instance']
    context.instance_port = context.config['components'][context.instance]['port']
    context.instance_protocol = context.config['components'][context.instance]['protocol']

    context.url_component = context.instance_protocol + "://" + \
                            context.instance_ip + ":" + \
                            context.instance_port

    url = context.url_component + '/v1.0/service/' + context.service_id + '/subservice'
    json_payload = json.dumps(dict(context.table))

    # print (json_payload)
    __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))
    context.r = requests.post(url=url,
                              headers=context.headers,
                              data=json_payload)

    __logger__.debug(context.r.content)
    __logger__.debug(context.r.status_code)
    eq_(context.r.status_code, 201,
        "[ERROR] when calling {} responsed a HTTP {}".format(url, context.r.status_code))
    context.create_subservice = context.r.content
    jsobject = json.loads(context.create_subservice)
    context.subservice_id = jsobject["id"]
    print ("\n --->>  ID subservice: {} <<---\n".format(context.subservice_id))


@step("device should get registered under service and subservice")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.instance = "ORC"

    # Setup default headers
    context.headers = {}
    context.headers = {'Accept': 'application/json', 'Content-type': 'application/json'}

    # recover the data to send the request
    context.instance_ip = context.config['components'][context.instance]['instance']
    context.instance_port = context.config['components'][context.instance]['port']
    context.instance_protocol = context.config['components'][context.instance]['protocol']

    context.url_component = context.instance_protocol + "://" + \
                            context.instance_ip + ":" + \
                            context.instance_port

    url = context.url_component + '/v1.0/service/' + \
          context.service_id + '/subservice/' + \
          context.subservice_id + '/register_device'

    json_payload = json.dumps(dict(context.table))

    # print (json_payload)
    __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))
    context.r = requests.post(url=url,
                              headers=context.headers,
                              data=json_payload)

    # print(context.r.content)
    __logger__.debug(context.r.content)
    __logger__.debug(context.r.status_code)
    eq_(context.r.status_code, 201,
        "[ERROR] when calling {} responsed a HTTP {}".format(url, context.r.status_code))
    context.add_device = context.r.content
    print ("ID registration: {}".format(context.add_device))


@step('with a service id "(?P<SERVICE_ID>.+)" and subservice id "(?P<SUBSERVICE_ID>.+)"')
def step_impl(context, SERVICE_ID, SUBSERVICE_ID):
    """
    :type context behave.runner.Context
    :type SERVICE_ID str
    :type SUBSERVICE_ID str
    """
    context.service_id = SERVICE_ID
    context.subservice_id = SUBSERVICE_ID


@step('a valid token is retrieved for user "(?P<SERVICE_ADMIN>.+)" and password "(?P<SERVICE_PWD>.+)"')
def step_impl(context, SERVICE_ADMIN, SERVICE_PWD):
    """
    :type context behave.runner.Context
    :type SERVICE_ADMIN str
    :type SERVICE_PWD str
    """
    # Recover a Token
    context.user = SERVICE_ADMIN
    context.password = SERVICE_PWD
    # context.service = context.service
    context.subservice = context.servicepath
    context.token = ks_get_token(context)
    print ("\n #>> Token to use: {} \n".format(context.token))


@step("the new service should be available in the IOTA")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    # Recover created services (if any)
    iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
               context.config["components"]["IOTA"]["instance"] + ":" + \
               context.config["components"]["IOTA"]["port"] + "/iot"

    # TODO: pending to update after issue fixed https://github.com/telefonicaid/iotagent-node-lib/issues/146
    iota_url = iota_url + "/agents/default"

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'fiware-service': context.service,
        'fiware-servicepath': context.servicepath
    }

    # Generate a iota object
    context.iota = Rest_Utils_IoTA(server_root=iota_url, server_root_secure=iota_url)

    # Add the token to the headers
    headers.update({'X-Auth-Token': context.token})
    context.r = context.iota.get_listServices(headers=headers)
    print (context.r.content)

    eq_(200, context.r.status_code, "ERROR: Service request IOTA failed: {}".format(context.r.status_code))
    iota_content_json = json.loads(context.r.content)

    # show returned response
    __logger__.debug("IOTA (service_request) returns {} ".format(iota_content_json))

    service = iota_content_json["service"]
    print ("Service: {}".format(service))


@then('device "(?P<DEVICE_ID>.+)" should be listed under service and subservice')
def step_impl(context, DEVICE_ID):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    """
    # Recover created services (if any)
    iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
               context.config["components"]["IOTA"]["instance"] + ":" + \
               context.config["components"]["IOTA"]["port"] + "/iot"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'fiware-service': context.service,
        'fiware-servicepath': "/{}".format(context.servicepath)
    }

    iota_url = iota_url + "/devices?detailed=on"

    # Add the token to the headers
    headers.update({'X-Auth-Token': context.token})
    # context.r = context.iota.get_listDevices(headers=headers)
    context.r = requests.get(url=iota_url, headers=headers)

    eq_(200, context.r.status_code, "ERROR: Devices request IOTA failed: {}".format(context.r.status_code))

    devices_array = json.loads(context.r.content)
    print ("devices {}".format(context.r.content))
    eq_(DEVICE_ID, devices_array[0]["name"], "ERROR: Device not found")
    eq_("BlackButton", devices_array[0]["type"], "ERROR: Device type does not match")
    eq_(context.service, devices_array[0]["service"], "ERROR: Service does not match")
    eq_("/{}".format(context.servicepath), devices_array[0]["subservice"], "ERROR: ServicePath does not match")


    # show returned response
    __logger__.debug("IOTA (devices_list) returns {} ".format(devices_array))

    for device in devices_array:
        __logger__.debug(device)
        if device["id"] == DEVICE_ID:
            print ("Device found: {}".format(device))
            eq_(context.service, device["service"])
            eq_("/" + context.subservice, device["subservice"])


@then('the button "(?P<DEVICE_ID>.+)" is pulling every "(?P<SECONDS>.+)" seconds '
      'during "(?P<TIMES>.+)" times or until the IOTA request returns status "(?P<STATUS>.+)"')
def step_impl(context, DEVICE_ID, SECONDS, TIMES, STATUS):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type SECONDS str
    :type TIMES str
    :type STATUS str

    SAMPLE:
    setConfig localhost 8885 /thinkingthings/Receive button_xxx_502 900
    btCreate 1 1 1
     Sending the following Black Button create request [#button_xxx_502,#1,BT,C,1,1,2000$WakeUp,#0,K1,30$]
     Answer: #button_xxx_502#1,BT,C,a9d47906-ee8b-493e-94bc-e714a3e7040e,,,0$#0,K1,300$,

    btPolling a9d47906-ee8b-493e-94bc-e714a3e7040e 1
        Sending the following Black Button polling request [#button_xxx_502,#1,BT,P,a9d47906-ee8b-493e-94bc-e714a3e7040e,2000$WakeUp,#0,K1,30$]
        Answer: #button_xxx_502#1,BT,P,0,0:404,,0$#0,K1,300$,
    """
    context.device_id = DEVICE_ID

    # Recover created services (if any)
    iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
               context.config["components"]["IOTA"]["instance"] + ":" + \
               context.config["components"]["IOTA"]["south_port"] + "/thinkingthings"

    # /custom uri
    iota_url = iota_url + "/Receive"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        # 'Accept': "application/json"
    }

    # button_xxx_502,
    # #1,BT,P,a9d47906-ee8b-493e-94bc-e714a3e7040e,2000$WakeUp,
    # #0,K1,30$


    # MODULE 1
    b_module_1_id = 1
    b_module_1_type = "BT"  # Button
    b_module_1_operation = "P"  # [Sync or C(async) + Pooling + X(end) ]
    b_module_1_action = context.bb_request_id
    b_module_1_sleep = "2000$WakeUp"

    b_module_1 = "{0},{1},{2},{3},{4},".format(b_module_1_id,
                                               b_module_1_type,
                                               b_module_1_operation,
                                               b_module_1_action,
                                               b_module_1_sleep)
    # eq_(b_module_1, "1,BT,P,a9d47906-ee8b-493e-94bc-e714a3e7040e,2000$WakeUp,")

    # MODULE 0
    b_module_0_id = 0
    b_module_0_type = "K1"  # Communications module
    b_module_0_sleep = "300$"
    b_module_0 = "{0},{1},{2},".format(b_module_0_id,
                                       b_module_0_type,
                                       b_module_0_sleep)
    eq_(b_module_0, "0,K1,300$,")

    measure = "#{0}#{1}#{2}".format(DEVICE_ID, b_module_1, b_module_0)
    data = {"cadena": measure}
    print (iota_url)
    print (data)
    print (headers)

    for x in xrange(int(TIMES)):
        context.r = requests.post(url=iota_url, data=data, headers=headers)
        print (context.r.status_code)
        print (context.r.content)
        eq_(200, context.r.status_code, "ERROR: MEASURE request IOTA failed: {}".format(context.r.status_code))

        # chop the response:
        iota_answer = context.r.content.split("#")
        context.answer_device_id = iota_answer[1]
        context.answer_mod1 = iota_answer[2]
        context.answer_mod0 = iota_answer[3]

        print (context.answer_mod1.split(","))
        if context.answer_mod1.split(",")[3].split(":")[1] == STATUS:
            print ("STATUS CHANGED to {}".format(context.answer_mod1.split(",")[3].split(":")[1]))
            break
    time.sleep(float(SECONDS))


@step('the button "(?P<DEVICE_ID>.+)" close the request and receive the final status "(?P<FINAL_STATUS>.+)"')
def step_impl(context, DEVICE_ID, FINAL_STATUS):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type FINAL_STATUS str
    """
    # TODO: Close the request to TP


@step('the ThirdParty "(?P<THIRDPARTY>.+)" changed the status to "(?P<OP_RESULT>.+)"')
def step_impl(context, THIRDPARTY, OP_RESULT):
    """
    :type context behave.runner.Context
    :type THIRDPARTY str
    :type OP_RESULT str
    """
    # chop the response:
    iota_answer = context.r.content.split("#")

    print ("\n iota resp={} \n".format(iota_answer))
    eq_(iota_answer[1], context.device_id, "Device id does not match")

    eq_(iota_answer[2].split(",")[5], OP_RESULT,
        "Expected result does not match \n Received: {} \n Expected: {}".format(iota_answer[2].split(",")[5],
                                                                                OP_RESULT))
    # extract the relevant info
    # bb_request_id = context.answer_mod1.split(",")[4]


@when('the button "(?P<DEVICE_ID>.+)" is pressed in mode "asynchronous" the IOTA should receive the request')
def step_impl(context, DEVICE_ID):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type SYNC_MODE str
    """
    SYNC_MODE = "asynchronous"
    context.device_id = DEVICE_ID
    context.sync_mode = SYNC_MODE

    # Recover created services (if any)
    iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
               context.config["components"]["IOTA"]["instance"] + ":" + \
               context.config["components"]["IOTA"]["south_port"] + "/thinkingthings"

    # /custom uri
    iota_url = iota_url + "/Receive"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    measure = "#{},{}".format(DEVICE_ID, context.bt_request)
    data = {"cadena": measure}

    context.r = requests.post(url=iota_url, data=data, headers=headers)
    print (context.r.status_code)
    print (context.r.content)

    eq_(200, context.r.status_code, "ERROR: MEASURE request IOTA failed: {}".format(context.r.status_code))

    # chop the response:
    iota_answer = context.r.content.split("#")
    context.answer_device_id = iota_answer[1]
    context.answer_mod1 = iota_answer[2]
    context.answer_mod0 = iota_answer[3]

    # store the request_id
    context.bb_request_id = context.answer_mod1.split(",")[3]

    # show returned response
    __logger__.debug("IOTA (send_measure) returns {} ".format(context.r.content))


@when('the button "(?P<DEVICE_ID>.+)" is pressed in mode "synchronous" the IOTA should receive the request')
def step_impl(context, DEVICE_ID):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type SYNC_MODE str
    """
    SYNC_MODE = "synchronous"
    context.device_id = DEVICE_ID
    context.sync_mode = SYNC_MODE

    # Recover created services (if any)
    iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
               context.config["components"]["IOTA"]["instance"] + ":" + \
               context.config["components"]["IOTA"]["south_port"] + "/thinkingthings"

    # /custom uri
    iota_url = iota_url + "/Receive"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        # 'Accept': "application/json"
    }

    measure = "#{},{}".format(DEVICE_ID, context.bt_request)
    data = {"cadena": measure}

    context.r = requests.post(url=iota_url, data=data, headers=headers)
    print (context.r.status_code)
    print (context.r.content)

    eq_(200, context.r.status_code, "ERROR: MEASURE request IOTA failed: {}".format(context.r.status_code))

    # show returned response
    __logger__.debug("IOTA (send_measure) returns {} ".format(context.r.content))


@then('the button "(?P<DEVICE_ID>.+)" should have received the final status "(?P<TP_RETURN>.+)"')
def step_impl(context, DEVICE_ID, TP_RETURN):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type TP_RETURN str
    """

    eq_(context.answer_device_id, DEVICE_ID)
    eq_(context.bb_request_id, TP_RETURN,
        "Returned response from ThirdParty does not match: \n {} \n {}\n".format(context.bb_request_id, TP_RETURN))


@step('a button_request "(?P<BT_REQUEST>.+)" for mode "(?P<SYNC_MODE>.+)"')
def step_impl(context, BT_REQUEST, SYNC_MODE):
    """
    :type context behave.runner.Context
    :type BT_REQUEST str
    :type SYNC_MODE str
    """
    print (BT_REQUEST)
    print (SYNC_MODE)
    context.bt_request = BT_REQUEST


@then('the button "(?P<DEVICE_ID>.+)" should have received the final multimodule status "(?P<TP_RETURN>.+)"')
def step_impl(context, DEVICE_ID, TP_RETURN):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type TP_RETURN str
    """
    result = context.answer_mod1.split(",")[3].split(":")[2]
    eq_(result, TP_RETURN, "Returned result does not match \n {} \n {} \n".format(result, TP_RETURN))

    """
    print (iota_url)
    print (headers)
    print (context.r.status_code)
    print (context.r.content)
    """
