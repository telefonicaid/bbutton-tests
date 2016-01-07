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
from nose.tools import eq_, assert_in
from iotqatools.cb_utils import PayloadUtils, ContextElements, AttributesCreation

import logging
import ast
import json
import re

__logger__ = logging.getLogger("common")

# Sample values for smoke tests
entity_id = 'Sala01'
entity_type = 'Sala'
value = 333


def cb_sample_entity_create(cb):
    """
    Configuring the CB Utility lib
    """
    attr = AttributesCreation()
    attr.add_attribute("temperature",
                       "centigrades",
                       value)
    ce = ContextElements()
    ce.add_context_element(entity_id, entity_type, attr)
    payload = PayloadUtils.build_standard_entity_creation_payload(ce)
    __logger__.debug(payload)

    r = cb.standard_entity_creation(payload)

    eq_(200, r.status_code)
    cb_content_json = json.loads(r.content)
    __logger__.debug(cb_content_json)
    eq_("200", cb_content_json["contextResponses"][0]["statusCode"]["code"],
        'INCORRECT STATUS CODE'
        '\n CB_CODE OBTAINED IS NOT == {} \n Received: {}'.format("200",
                                                                  cb_content_json["contextResponses"][0][
                                                                      "statusCode"][
                                                                      "code"]))
    eq_("OK", cb_content_json["contextResponses"][0]["statusCode"]["reasonPhrase"],
        'INCORRECT reason_Phrase.'
        '\n CB_Reason OBTAINED IS NOT == {} \n Received: {}'.format("OK",
                                                                    cb_content_json["contextResponses"][0][
                                                                        "statusCode"]["reasonPhrase"]))

    __logger__.info("#>> CommonLib: [CB] Entity created")

    return r


def cb_sample_entity_recover(cb):
    """
    Configuring the CB Utility lib
    """

    r = cb.convenience_query_context(entity_id, entity_type)
    __logger__.debug("#>> CommonLib: [CB] Entity: {}".format(r.content))

    eq_(200, r.status_code)
    cb_content_json = json.loads(r.content)
    __logger__.debug(cb_content_json)
    eq_("200", cb_content_json["statusCode"]["code"],
        'INCORRECT STATUS CODE'
        '\n CB_CODE OBTAINED IS NOT == {} \n Received: {}'.format("200",
                                                                  cb_content_json[
                                                                      "statusCode"]["code"]))
    eq_("OK", cb_content_json["statusCode"]["reasonPhrase"],
        'INCORRECT reason_Phrase.'
        '\n CB_Reason OBTAINED IS NOT == {} \n Received: {}'.format("OK",
                                                                    cb_content_json[
                                                                        "statusCode"]["reasonPhrase"]))
    eq_(value, int(cb_content_json["contextElement"]["attributes"][0]["value"]),
        'INCORRECT Value from CB returned.'
        '\n CB_Entity value OBTAINED IS NOT == {} \n Received: {}'.format("OK",
                                                                          cb_content_json["contextElement"][
                                                                              "attributes"][0]["value"]))

    __logger__.info("#>> CommonLib: [CB] Entity recovered")

    return r


def cb_sample_entity_recover(cb):
    """
    Configuring the CB Utility lib
    """

    r = cb.convenience_query_context(entity_id, entity_type)
    __logger__.debug("#>> CommonLib: [CB] Entity: {}".format(r.content))

    eq_(200, r.status_code)
    cb_content_json = json.loads(r.content)
    __logger__.debug(cb_content_json)
    eq_("200", cb_content_json["statusCode"]["code"],
        'INCORRECT STATUS CODE'
        '\n CB_CODE OBTAINED IS NOT == {} \n Received: {}'.format("200",
                                                                  cb_content_json[
                                                                      "statusCode"]["code"]))
    eq_("OK", cb_content_json["statusCode"]["reasonPhrase"],
        'INCORRECT reason_Phrase.'
        '\n CB_Reason OBTAINED IS NOT == {} \n Received: {}'.format("OK",
                                                                    cb_content_json[
                                                                        "statusCode"]["reasonPhrase"]))
    eq_(value, int(cb_content_json["contextElement"]["attributes"][0]["value"]),
        'INCORRECT Value from CB returned.'
        '\n CB_Entity value OBTAINED IS NOT == {} \n Received: {}'.format("OK",
                                                                          cb_content_json["contextElement"][
                                                                              "attributes"][0]["value"]))

    __logger__.info("#>> CommonLib: [CB] Entity recovered")

    return r


def ks_get_token(context, service=None, user=None, password=None, subservice=None):
    if service is "":
        service = context.service
        user = context.user
        password = context.password

    protocol = context.config["components"]["KS"]["protocol"]
    instance = context.config["components"]["KS"]["instance"]
    port = context.config["components"]["KS"]["port"]
    uri = "/v3/auth/tokens"

    ks_url = "{}://{}:{}{}".format(protocol, instance, port, uri)

    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": service
                        },
                        "name": user,
                        "password": password
                    }
                }
            }
        }
    }
    payload = json.dumps(payload)
    __logger__.debug(payload)

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'fiware-service': service,
    }

    if subservice is not None:
        headers.update({'fiware-servicepath': context.subservice})

    context.r_ks = requests.request("POST", ks_url, data=payload, headers=headers)
    ks_headers = context.r_ks.headers
    return ks_headers["x-subject-token"]


def ks_get_token_with_scope(context, token, service_name, subservice_name):
    protocol = context.config["components"]["KS"]["protocol"]
    instance = context.config["components"]["KS"]["instance"]
    port = context.config["components"]["KS"]["port"]
    uri = "/v3/auth/tokens"

    ks_url = "{}://{}:{}{}".format(protocol, instance, port, uri)

    payload = {
        "auth": {
            "identity": {
                "methods": ["token"],
                "token": {
                    "id": token
                }
            },
            "scope": {
                "domain": {
                    "name": service_name
                }
            }
        }
    }

    payload = json.dumps(payload)
    __logger__.debug(payload)

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'fiware-service': service_name,
        'fiware-servicepath': subservice_name
    }

    context.r_ks = requests.request("POST", ks_url, data=payload, headers=headers)
    print (context.r_ks.text)
    ks_headers = context.r_ks.headers
    return ks_headers["x-subject-token"]


def orc_get_services(context):
    orc_url = context.config["components"]["ORC"]["protocol"] + "://" + \
              context.config["components"]["ORC"]["instance"] + ":" + \
              context.config["components"]["ORC"]["port"] + \
              "/v1.0/service"

    headers = {
        'content-type': "application/json"
    }

    payload = {
        'DOMAIN_NAME': context.service_admin,
        'SERVICE_ADMIN_USER': context.user_admin,
        'SERVICE_ADMIN_PASSWORD': context.password_admin
    }
    payload = json.dumps(payload)

    __logger__.debug(orc_url)
    __logger__.debug(payload)

    try:
        context.r_orc = requests.get(orc_url, data=payload, headers=headers)
        # print (context.r_orc.text)
        eq_(context.r_orc.status_code, 200, "Response not valid from ORC instance getting services")
        context.r_orc = json.loads(context.r_orc.content)
        __logger__.debug(context.r_orc["domains"])
        return context.r_orc["domains"]
    except:
        return []


def orc_get_subservices(context, service_id):
    orc_url = "{}://{}:{}/v1.0/service/{}/subservice".format(
            context.config["components"]["ORC"]["protocol"],
            context.config["components"]["ORC"]["instance"],
            context.config["components"]["ORC"]["port"],
            service_id)

    # get token with scope from previous token
    context.token_scope = ks_get_token_with_scope(context, context.token, context.service, context.subservice)
    print ("#>> Token with scope: {}".format(context.token_scope))

    headers = {
        "content-type": "application/json",
        "x-auth-token": context.token_scope
    }

    __logger__.debug(orc_url)
    __logger__.debug(headers)

    try:
        context.r_orc = requests.get(orc_url, headers=headers)
        eq_(context.r_orc.status_code, 200, "Response not valid from ORC instance getting services")
        context.r_orc = json.loads(context.r_orc.content)
        __logger__.debug(context.r_orc["projects"])
        return context.r_orc["projects"]
    except:
        __logger__.debug("No subservices found: []")
        return []


def orc_delete_service(context, service_id):
    orc_url = context.config["components"]["ORC"]["protocol"] + "://" + \
              context.config["components"]["ORC"]["instance"] + ":" + \
              context.config["components"]["ORC"]["port"] + \
              "/v1.0/service/{}".format(service_id)

    headers = {
        'content-type': "application/json"
    }

    payload = {
        'SERVICE_ADMIN_USER': "cloud_admin",
        'SERVICE_ADMIN_PASSWORD': "password"
    }

    payload = json.dumps(payload)

    __logger__.debug(orc_url)
    __logger__.debug(payload)

    try:
        context.r_orc = requests.delete(orc_url, data=payload, headers=headers)
        print (context.r_orc.text)
        eq_(context.r_orc.status_code, 204, "Response not valid from ORC instance deleting service")
        __logger__.debug(context.r_orc)
        print ("Service ({}) DELETED".format(service_id))
        return context.r_orc.status_code
    except:
        return "Error deleting service {}".format(service_id)


def orc_delete_subservice(context, service_id, subservice_id, admin_token=None):
    orc_url = context.config["components"]["ORC"]["protocol"] + "://" + \
              context.config["components"]["ORC"]["instance"] + ":" + \
              context.config["components"]["ORC"]["port"] + \
              "/v1.0/service/{}/subservice/{}".format(service_id, subservice_id)

    headers = {
        "content-type": "application/json",
        "x-auth-token": admin_token
    }

    # access with credentials
    if admin_token is None:
        payload = {
            "SERVICE_NAME": context.service,
            "SUBSERVICE_NAME": "/{}".format(context.subservice),
            "SERVICE_ADMIN_USER": context.user_admin,
            "SERVICE_ADMIN_PASSWORD": context.password_admin
        }
    # access with token
    else:
        payload = {
            "SUBSERVICE_NAME": context.subservice
        }

    payload = json.dumps(payload)

    # print ("url: {}".format(orc_url))
    # print ("headers: {}".format(headers))
    # print ("payload: {}".format(payload))
    __logger__.debug(orc_url)
    __logger__.debug(payload)

    try:
        context.r_orc = requests.delete(orc_url, data=payload, headers=headers)
        eq_(context.r_orc.status_code, 204,
            "Response not valid from ORC instance deleting service REC: {}".format(context.r_orc.status_code))
        __logger__.debug(context.r_orc)
        print ("#>> SUBSERVICE ({}) DELETED [{}]".format(service_id, context.r_orc.status_code))
        return context.r_orc.status_code
    except:
        return "Error deleting service {}\n{}".format(service_id, context.r_orc.text)


def component_verifyssl_check(context, component):
    if "verifyssl" in context.config['components'][component]:
        verify_ssl = ast.literal_eval(context.config['components'][component]['verifyssl'])
    else:
        verify_ssl = False

    return verify_ssl


def component_version_check(context, component):
    eq_(context.r.status_code, 200,
        "[ERROR] when calling {} responsed a HTTP {}".format(context.url_component, context.r.status_code))
    "<INSTANCE>"

    assert_in('r', context, 'Not response found for component {}'.format(context.instance))

    version = context.r.content
    __logger__.debug(version)

    returned_version = json.loads(version)["version"]

    return returned_version


def node_version_checker(context, component, version):
    # Cast version returned (if any)
    returned_version = component_version_check(context, component=component)

    # compare the version with the expected one
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(component, returned_version, version))

    __logger__.debug("{} Version: {}".format(component, returned_version))
