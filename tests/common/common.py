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
from nose.tools import eq_
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


def ks_get_token(context):
    ks_url = context.config["components"]["KS"]["protocol"] + "://" + \
             context.config["components"]["KS"]["instance"] + ":" + \
             context.config["components"]["KS"]["port"] + \
             "/v3/auth/tokens"
    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": context.service
                        },
                        "name": context.user,
                        "password": context.password
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
        'fiware-service': context.service,
        'fiware-servicepath': context.subservice
    }

    context.r_ks = requests.request("POST", ks_url, data=payload, headers=headers)
    ks_headers = context.r_ks.headers
    return ks_headers["x-subject-token"]


def component_verifyssl_check(context, component):
    if "verifyssl" in context.config['components'][component]:
        verify_ssl = ast.literal_eval(context.config['components'][component]['verifyssl'])
    else:
        verify_ssl = False

    return verify_ssl
