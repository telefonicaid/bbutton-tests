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
import datetime

from iotqatools.orchestator_utils import Orchestrator
from iotqatools.iota_utils import Rest_Utils_IoTA
from common.common import cb_sample_entity_create, cb_sample_entity_recover, \
    ks_get_token, ks_get_token_with_scope, \
    component_verifyssl_check, \
    orc_get_services, orc_get_subservices, orc_delete_service, orc_delete_subservice
from common.test_utils import *
from nose.tools import eq_, assert_in, assert_true, assert_greater_equal, assert_not_in
from pymongo import MongoClient

__logger__ = logging.getLogger("happy_path")
use_step_matcher("re")


@given('a Client of "(?P<SERVICE>.+)" and a Subservice called "(?P<SERVICEPATH>.+)"')
def step_impl(context, SERVICE, SERVICEPATH):
    """
    :type context behave.runner.Context
    :type SERVICE str
    :type SERVICEPATH str
    """
    context.service = SERVICE
    context.servicepath = SERVICEPATH
    context.subservice = "/{}".format(SERVICEPATH)


@step('the "(?P<INSTANCE>.+)" receive the request "(?P<REQUEST>.+)" and action "(?P<ACTION>.+)"')
def happy_path_request_collector(context, INSTANCE, REQUEST, ACTION):
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

        payload_table = dict(context.table)

        # Depends on Orquestator version, in old version is needed:
        # payload_table['ATT_TIMEOUT'] = int(payload_table['ATT_TIMEOUT'])

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

        try:
            context.r = requests.post(url=url,
                                      headers=context.headers,
                                      data=json_payload)

            eq_(context.r.status_code, 201,
                "[ERROR] when calling {} responsed a HTTP {}".format(url, context.r.status_code))
            context.create_service_entity = context.r.content
            print (context.create_service_entity)
        except:
            eq_(True, False, "# Exception # Error Creating SERVICE_ENTITY")

    if INSTANCE == "ORC" and REQUEST == "SERVICE" and ACTION == "CREATE":
        url = str("{0}/v1.0/service".format(context.url_component))
        if context.table:
            json_payload = json.dumps(dict(context.table))
        else:
            json_payload = json.dumps(context.table_create_service)

        print ("\n JSON TABLE SERVICE: \n {}\n".format(json_payload))
        __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))
        context.r = requests.post(url=url,
                                  headers=context.headers,
                                  data=json_payload)

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

    if INSTANCE == "ORC" and REQUEST == "SERVICE" and ACTION == "DELETE":
        # Get list of services if needed
        if "service_id" not in context:
            for service in context.services:
                if context.service == service["name"]:
                    print ("#>> Service Targeted: {} {}".format(service["name"], service["id"]))
                    context.service_id = service["id"]
                    break

        # Get config test env credentials
        context.user_admin = context.config["env_data"]["users"]["user_1"]["user_name"]
        context.password_admin = context.config["env_data"]["users"]["user_1"]["user_password"]
        context.domain_admin = context.config["env_data"]["users"]["user_1"]["user_service"]

        # In case delete using token is needed
        # domain_token = ks_get_token(context,
        #                             service=context.domain_admin,
        #                             user=context.user_admin,
        #                             password=context.password_admin)

        if "service_id" in context:
            delete_response = orc_delete_service(context, context.service_id)
            eq_(204, delete_response,
                "[ERROR] Deleting Service {} \n Orch responded: {}".format(context.service_id, delete_response))
        else:
            eq_(True, False, "[Error] Service to delete ({}) not found".format(context.service))

    if INSTANCE == "ORC" and REQUEST == "SUBSERVICE" and ACTION == "DELETE":
        # Get service id if needed
        if "service_id" not in context:
            for service in context.services:
                if context.service == service["name"]:
                    print ("service retrieved: {} {}".format(service["name"], service["id"]))
                    context.service_id = service["id"]
                    break

        # Get subservice id
        for subservice in context.subservices:
            if "/" + context.subservice == subservice["name"]:
                print ("#>> Subservice Targeted: {} {}".format(subservice["name"], subservice["id"]))
                context.subservice_id = subservice["id"]
                break
            else:
                print ("#>> Subservice Targeted: {} {}".format(subservice["name"], subservice["id"]))

        context.user_admin = context.config["env_data"]["users"]["user_3"]["user_name"]
        context.password_admin = context.config["env_data"]["users"]["user_3"]["user_password"]

        context.token_scope = ks_get_token_with_scope(context, context.token, context.service, context.subservice)

        delete_response = orc_delete_subservice(context,
                                                context.service_id,
                                                context.subservice_id,
                                                context.token_scope)

        eq_(204, delete_response,
            "[ERROR] Deleting Service {} responsed a HTTP {}".format(context.service_id, delete_response))

    if INSTANCE == "IOTA_MQTT" and REQUEST == "DEVICE" and ACTION == "CREATE":
        url = str("{0}/iot/devices".format(context.url_component))

        dictio = dict(context.table)
        print ("\n{}\n".format(dictio))

        # create dict to contain the payload
        payload = dict({})
        payload["devices"] = [dictio]

        context.headers.update({"Fiware-Service": "{}".format(context.service)})
        context.headers.update({"Fiware-ServicePath": "/{}".format(context.servicepath)})

        __logger__.debug("[MQTT] Create Device request: {}, \n url: {}".format(payload, url))
        context.mqtt_create_request = payload
        context.mqtt_create_url = url


@step('subservice "(?P<SERVICEPATH>.+)" under the service is created')
def happy_path_service_creation(context, SERVICEPATH):
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

    context.url_component = "{}://{}:{}".format(context.instance_protocol,
                                                context.instance_ip,
                                                context.instance_port)

    url = "{}/v1.0/service/{}/subservice".format(context.url_component, context.service_id)

    if context.table:
        json_payload = json.dumps(dict(context.table))
    else:
        json_payload = json.dumps(context.table_create_subservice)

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

    context.url_component = "{}://{}:{}".format(context.instance_protocol,
                                                context.instance_ip,
                                                context.instance_port)

    url = "{}/v1.0/service/{}/subservice/{}/register_device".format(context.url_component,
                                                                    context.service_id,
                                                                    context.subservice_id)

    json_payload = json.dumps(dict(context.table))

    __logger__.debug("Create service: {}, \n url: {}".format(json_payload, url))
    try:
        context.r = requests.post(url=url,
                                  headers=context.headers,
                                  data=json_payload)
    except requests.exceptions.RequestException, e:
        print ("#Error {} \n Sending the request: {} with \n{} ".format(e, url, json_payload))
        eq_(True, False, "ERROR: Exception trying to register the Device in ORC")

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
def happy_path_retrieve_token(context, SERVICE_ADMIN, SERVICE_PWD):
    """
    :type context behave.runner.Context
    :type SERVICE_ADMIN str
    :type SERVICE_PWD str
    """

    # Recover a Token
    context.user = SERVICE_ADMIN
    context.password = SERVICE_PWD

    if "service" in context and "servicepath" in context:
        # context.service = context.service
        context.subservice = context.servicepath
    else:
        print ("\n #>> Token data needed FAIL: {} \n".format(context.service))
        return False

    context.token = ks_get_token(context,
                                 service=context.service,
                                 user=context.user,
                                 password=context.password)

    print ("\n #>> Token to use: {} \n".format(context.token))


@step('an admin_token is retrieved')
def step_impl(context):
    """
    :type context behave.runner.Context
    :type SERVICE_ADMIN str
    :type SERVICE_PWD str
    """

    # Recover a Token
    user = context.config["env_data"]["users"]["user_1"]["user_name"]
    password = context.config["env_data"]["users"]["user_1"]["user_password"]
    service = context.config["env_data"]["users"]["user_1"]["user_service"]
    subservice = None

    context.admin_token = ks_get_token(context,
                                       service=service,
                                       user=user,
                                       password=password,
                                       subservice=subservice
                                       )

    print ("\n#>> Admin Token to use: {} \n".format(context.admin_token))


@step('a list of services for admin_cloud is retrieved')
def happy_path_list_services(context):
    """
    :type context behave.runner.Context
    :type SERVICE_ADMIN str
    :type SERVICE_PWD str
    """
    # Recover a Token for a test default user
    context.user_admin = context.config["env_data"]["users"]["user_1"]["user_name"]
    context.password_admin = context.config["env_data"]["users"]["user_1"]["user_password"]
    context.service_admin = context.config["env_data"]["users"]["user_1"]["user_service"]

    context.services = orc_get_services(context)
    print ("\n#>> Services availables: {} \n".format(context.services))

    # Get target service_id
    if "service" in context:
        for service in context.services:
            if context.service == service["name"]:
                context.service_id = service["id"]
                print ("#>> Service info: {} {}".format(service["name"], service["id"]))
                break


@step('a list of subservices for service_admin "(?P<SERVICE_ADMIN>.+)" '
      'and service_pwd "(?P<SERVICE_PWD>.+)" are retrieved')
def happy_path_list_subservices(context, SERVICE_ADMIN, SERVICE_PWD):
    """
    :type context: behave.runner.Context
    :type SERVICE_ADMIN: str
    :type SERVICE_PWD: str
    """
    pass

    context.service_admin = SERVICE_ADMIN
    context.service_password = SERVICE_PWD

    context.subservices = orc_get_subservices(context, context.service_id)


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
    context.device_id = DEVICE_ID
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

    iota_url = "{}/devices?detailed=on".format(iota_url)

    # Add the token to the headers
    headers.update({'X-Auth-Token': context.token})
    # context.r = context.iota.get_listDevices(headers=headers)
    context.r = requests.get(url=iota_url, headers=headers)

    eq_(200, context.r.status_code, "ERROR: Devices request IOTA failed: {}".format(context.r.status_code))

    response = json.loads(context.r.content)

    print ("response".format(context.r.content))
    devices_array = response["devices"]
    print ("devices {}".format(devices_array[0]))
    eq_(DEVICE_ID, devices_array[0]["device_id"], "ERROR: Device not found")
    eq_("BlackButton", devices_array[0]["entity_type"], "ERROR: Device type does not match")
    eq_(context.service, devices_array[0]["service"], "ERROR: Service does not match")
    eq_("/{}".format(context.servicepath), devices_array[0]["service_path"], "ERROR: ServicePath does not match")

    # show returned response
    __logger__.debug("IOTA (devices_list) returns {} ".format(devices_array))

    for device in devices_array:
        __logger__.debug(device)
        if device["device_id"] == DEVICE_ID:
            print ("Device found: {}".format(device))
            eq_(context.service, device["service"])
            eq_("/" + context.subservice, device["service_path"])


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
    data = {"c": measure}
    print ("\nUrl: {},\nData: {}\nHeaders: {}".format(iota_url, data, headers))

    for x in xrange(int(TIMES)):
        context.r = requests.post(url=iota_url, data=data, headers=headers)
        eq_(200, context.r.status_code, "ERROR: MEASURE request IOTA failed: {}".format(context.r.status_code))
        print ("\nResponse: {} #{}-{} ".format(context.r.content, x, datetime.datetime.now()))
        # chop the response:
        iota_answer = context.r.content.split("#")
        context.answer_device_id = iota_answer[1]
        context.answer_mod1 = iota_answer[2]
        context.answer_mod0 = iota_answer[3]

        try:
            if context.answer_mod1.split(",")[3].split(":")[1] == STATUS:
                print ("STATUS CHANGED to {}".format(context.answer_mod1.split(",")[3].split(":")[1]))
                context.final_state = context.answer_mod1.split(",")[3].split(":")[1]
                break
        except:
            print ("Error received in response: {} ".format(context.answer_mod1.split(",")))
            eq_(True, False, "ERROR: Exception trying to chop the response of the iota pulling request")

    time.sleep(float(SECONDS))


@step('the button "(?P<DEVICE_ID>.+)" close the request and receive the final status "(?P<FINAL_STATUS>.+)"')
def step_impl(context, DEVICE_ID, FINAL_STATUS):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    :type FINAL_STATUS str
    """

    if "final_state" in context:
        eq_(FINAL_STATUS,
            context.final_state,
            "# Error final status ({}) does not match the expected result ({})".format(
                FINAL_STATUS,
                context.final_state))


@step('the ThirdParty "(?P<THIRDPARTY>.+)" changed the status to "(?P<OP_RESULT>.+)"')
def step_impl(context, THIRDPARTY, OP_RESULT):
    """
    :type context behave.runner.Context
    :type THIRDPARTY str
    :type OP_RESULT str
    """
    if "NaN" in OP_RESULT:
        OP_RESULT = ""
    # chop the response:
    iota_answer = context.r.content.split("#")
    # chop the expected_result:
    expected = OP_RESULT.split("#")

    print ("\n IOTA resp={} \n".format(iota_answer))
    print ("\n Expected resp={} \n".format(expected))

    # check device_id
    eq_(iota_answer[1], context.device_id, "Device_id does not match")

    # check mod1
    mod1 = expected[1]
    rec_mod1 = iota_answer[2]
    eq_(rec_mod1, mod1,
        "Expected result mod1 does not match \n "
        "Received: {} \n Expected: {}".format(
            rec_mod1, mod1))

    # check mod2
    mod0 = expected[2]
    rec_mod0 = iota_answer[3]
    eq_(rec_mod0, mod0,
        "Expected result mod0 does not match \n "
        "Received: {} \n Expected: {}".format(
            rec_mod0, mod0))

    print ("\n iota resp={} \n".format(iota_answer))

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
    data = {"c": measure}

    print ("\n >> Push info: {}".format(data))

    context.r = requests.post(url=iota_url, data=data, headers=headers)
    print ("\n << {}".format(context.r.status_code))
    print ("<< {}".format(context.r.content))

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


@step('the button "(?P<DEVICE_ID>.+)" is pressed in mode "synchronous" the IOTA should receive the request')
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
    data = {"c": measure}
    print(iota_url)
    print(data)

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


@then('the service "(?P<SERVICE>.+)" should not be listed')
def step_impl(context, SERVICE):
    """
    :type context behave.runner.Context
    :type SERVICE str
    """
    context.execute_steps(u'''
        Given a list of services for admin_cloud is retrieved
        ''')

    assert_not_in(SERVICE, context.services, "Service FOUND IN LIST retrieved: service {}".format(SERVICE))


@when('the device "(?P<DEVICE_ID>.+)" is marked to be deleted')
def step_impl(context, DEVICE_ID):
    """
    :type context behave.runner.Context
    :type DEVICE_ID str
    """
    # TODO: Remove devices from iota PR pending
    # workaround to clean the devices generated during the test execution
    # client = MongoClient("localhost", 27017)
    mongo_instance = context.config["backend"]["mongodb"]["instance"]
    mongo_port = context.config["components"]["backend"]["mongodb"]["port"]

    client = MongoClient(mongo_instance, mongo_port)
    db = client.iotagent
    devices = db.devices
    # result = devices.find()
    result = devices.find({"id": DEVICE_ID}, {"id": 1})
    for doc in result:
        delete = devices.remove({"id": DEVICE_ID})
        print ("Deleted device {}, result: {}".format(DEVICE_ID, delete))


@step("a service and subservice are provisioned")
def service_subservice_default_provision(context):
    """
    :type context: behave.runner.Context
    """
    json_data_s = """{
                                    "DOMAIN_ADMIN_USER": "cloud_admin",
                                    "NEW_SERVICE_ADMIN_PASSWORD": "ADMIN_PASS",
                                    "DOMAIN_NAME": "admin_domain",
                                    "DOMAIN_ADMIN_PASSWORD": "ADMIN_DOMAIN_PASS",
                                    "NEW_SERVICE_NAME": "CHANGE_SERVICE_NAME",
                                    "NEW_SERVICE_ADMIN_USER": "admin_bb",
                                    "NEW_SERVICE_DESCRIPTION": "default service description"
                                    }"""
    payload_service = json.loads(json_data_s)
    payload_service["NEW_SERVICE_NAME"] = context.service
    payload_service["NEW_SERVICE_ADMIN_PASSWORD"] = context.config["env_data"]["users"]["user_2"]["user_password"]
    payload_service["DOMAIN_ADMIN_PASSWORD"] = context.config["env_data"]["users"]["user_1"]["user_password"]
    context.table_create_service = payload_service

    json_data_ss = """{
                    "NEW_SUBSERVICE_DESCRIPTION": "SUBSERVICE NAME DESCRIPTION",
                    "SERVICE_NAME": "CHANGE_SERVICE_NAME",
                    "SERVICE_ADMIN_PASSWORD": "SERVICE_ADMIN_PWD",
                    "NEW_SUBSERVICE_NAME": "CHANGE_SUBSERVICE_NAME",
                    "SERVICE_ADMIN_USER": "admin_bb"
                    }"""

    payload_subservice = json.loads(json_data_ss)
    payload_subservice["NEW_SUBSERVICE_NAME"] = context.servicepath
    payload_subservice["SERVICE_NAME"] = context.service
    payload_subservice["SERVICE_ADMIN_PASSWORD"] = context.config["env_data"]["users"]["user_1"]["user_password"]

    context.table_create_subservice = payload_subservice

    # provision using the common steps
    happy_path_request_collector(context, "ORC", "SERVICE", "CREATE")
    happy_path_service_creation(context, context.servicepath)


@step('service and subservice are deleted with "(?P<ADMIN>.+)" and "(?P<PWD>.+)" credentials')
def service_subservice_default_delete(context, ADMIN, PWD):
    """
    Reused steps in just one step

    """
    happy_path_list_services(context)
    happy_path_retrieve_token(context, ADMIN, PWD)
    happy_path_list_subservices(context, ADMIN, PWD)
    happy_path_request_collector(context, "ORC", "SUBSERVICE", "DELETE")
    happy_path_request_collector(context, "ORC", "SERVICE", "DELETE")
