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
from nose.tools import eq_, assert_in, assert_true, assert_greater_equal
from tests.common.test_utils import *
from iotqatools.cb_utils import CbNgsi10Utils, EntitiesConsults, PayloadUtils, NotifyConditions, ContextElements, \
    AttributesCreation, MetadatasCreation
from iotqatools.iota_utils import Rest_Utils_IoTA
from common.common import cb_sample_entity_create, cb_sample_entity_recover, ks_get_token, component_verifyssl_check, \
    component_version_check
import logging
import ast
import json
import re

__logger__ = logging.getLogger("smoke")
use_step_matcher("re")


@step('service "(?P<service>.+)" and subservice "(?P<subservice>.+)"')
def step_impl(context, service, subservice):
    """
    :type context behave.runner.Context
    """
    context.service = service
    context.subservice = subservice


@step('user "(?P<user>.+)" and password "(?P<password>.+)"')
def step_impl(context, user, password):
    """
    :type context behave.runner.Context
    """
    context.user = user
    context.password = password


@given('the instance of "(?P<INSTANCE>.+)" is accessible')
def step_impl(context, INSTANCE):
    """
    :type context behave.runner.Context
    :type INSTANCE str
    """
    if INSTANCE == "IOTA_LIB":
        context.instance = "IOTA"
    else:
        context.instance = INSTANCE

    context.instance_ip = context.config['components'][context.instance]['instance']
    context.instance_port = context.config['components'][context.instance]['port']
    context.url_component = "{}://{}:{}".format(context.config['components'][context.instance]['protocol'],
                                                context.instance_ip,
                                                context.instance_port)

    context.verify_ssl = component_verifyssl_check(context, context.instance)

    # default headers
    context.headers = {}
    context.headers = {'Accept': 'application/json'}


@when(u'I send a request "(?P<request>.+)" to URI "(?P<uri>.+)"')
def step_impl(context, request, uri):
    context.url_component = "{}{}".format(context.url_component, uri)
    context.kind_request = request
    context.verbose = False

    if uri != "None":
        try:
            print ("Url: {} \n".format(context.url_component))

            if context.verbose:
                print ("Headers: {} \n".format(context.headers))
                print ("Verify ssl: {} \n".format(context.verify_ssl))

            context.r = requests.get(url=context.url_component, headers=context.headers, verify=context.verify_ssl)
        except requests.exceptions.RequestException, e:
            context.r = 'ERROR'
            __logger__.debug('[ERROR] {}', e)
            assert_true(False, msg='[{}] #NETWORK_ERROR at {} \n{}'.format( context.instance,
                                                                            context.url_component,
                                                                            e))
    else:
        context.r = 'ERROR'


@then(u'the result should be "(?P<result>.+)"')
def step_impl(context, result):
    __logger__.info("context".format(context.r))

    eq_(context.r.status_code, int(result),
        "[ERROR] when calling {} responsed a HTTP {}".format(context.url_component, context.r.status_code))


@then(u'the returned version from "CB" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "CB"

    eq_(context.r.status_code, 200,
        "[ERROR] when calling {} responsed a HTTP {}".format(context.url_component, context.r.status_code))
    "<INSTANCE>"

    assert_in('r', context, 'Not response found for component {}'.format(context.instance))

    sstr = context.r.content
    jsobject = json.loads(sstr)
    assert_in('orion', jsobject, 'Not orion part in response ({})'.format(jsobject))
    interior = jsobject['orion']
    assert_in('version', interior, 'Not version in response ({})'.format(interior))
    returned_version = interior['version']
    eq_(returned_version, version,
        '[{}] #VERSION_CONFLICT: found({}) expected({})'.format(comp, returned_version, version))
    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "IOTA" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "IOTA"

    eq_(context.r.status_code, 200,
        "[ERROR] when calling {} responsed a HTTP {}".format(context.url_component, context.r.status_code))
    "<INSTANCE>"

    assert_in('r', context, 'Not response found for component {}'.format(context.instance))

    iota_version = context.r.content
    if context.config['components']["IOTA"]['iota_type'] == "node":
        __logger__.debug(iota_version)
        returned_version = json.loads(iota_version)["version"]
    else:
        returned_version = iota_version.split(" ")[3]
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(comp, returned_version, version))
    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "IOTA_LIB" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "IOTA"

    eq_(context.r.status_code, 200,
        "[ERROR] when calling {} responsed a HTTP {}".format(context.url_component, context.r.status_code))
    "<INSTANCE>"

    assert_in('r', context, 'Not response found for component {}'.format(context.instance))

    iota_version = context.r.content
    if context.config['components']["IOTA"]['iota_type'] == "node":
        __logger__.debug(iota_version)
        returned_version = json.loads(iota_version)["libVersion"]
    else:
        returned_version = iota_version.split(" ")[3]
    eq_(returned_version, version,
        '[IOTA_LIB] Not the correct version: found({}) expected({})'.format(returned_version, version))
    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "IOTM" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "IOTM"

    eq_(context.r.status_code, 200,
        "[ERROR] when calling {} responsed a HTTP {}".format(context.url_component, context.r.status_code))
    "<INSTANCE>"

    assert_in('r', context, 'Not response found for component {}'.format(context.instance))

    iotm_version = context.r.content
    returned_version = iotm_version.split(" ")[7]
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(comp, returned_version, version))
    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "CA" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "CA"

    # Cast version returned (if any)
    returned_version = component_version_check(context, component=comp)

    # compare the version with the expected one
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(comp, returned_version, version))

    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "STH" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "STH"

    # Cast version returned (if any)
    returned_version = component_version_check(context, component=comp)

    # compare the version with the expected one
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(comp, returned_version, version))

    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "CYGNUS" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "CYGNUS"

    # Cast version returned (if any)
    returned_version = component_version_check(context, component=comp)

    # compare the version with the expected one
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(comp, returned_version, version))

    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "PEP" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "PEP"

    # Cast version returned (if any)
    returned_version = component_version_check(context, component=comp)

    # compare the version with the expected one
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(comp, returned_version, version))

    __logger__.debug("{} Version: {}".format(comp, returned_version))


@then(u'the returned version from "ORC" should match the "(?P<version>.+)"')
def step_impl(context, version):
    comp = "ORC"

    # Cast version returned (if any)
    returned_version = component_version_check(context, component=comp)

    # compare the version with the expected one
    eq_(returned_version, version,
        '[{}] Not the correct version: found({}) expected({})'.format(comp, returned_version, version))

    __logger__.debug("{} Version: {}".format(comp, returned_version))


@when('I send a request type "(?P<REQUEST>.+)" and action "(?P<ACTION>.+)"')
def step_impl(context, REQUEST, ACTION):
    """
    :type context behave.runner.Context
    :type REQUEST str
    :type ACTION str
    """

    if REQUEST == "ENTITY" and ACTION == "CREATE":
        # create an CB sample entity
        cb = CbNgsi10Utils(protocol=context.config["components"]["CB"]["protocol"],
                           instance=context.config["components"]["CB"]["instance"],
                           port=context.config["components"]["CB"]["port"],
                           service=context.service,
                           subservice=context.subservice)

        context.r = cb_sample_entity_create(cb)


    elif REQUEST == "ENTITY" and ACTION == "GET":
        # recover a sample entity
        cb = CbNgsi10Utils(protocol=context.config["components"]["CB"]["protocol"],
                           instance=context.config["components"]["CB"]["instance"],
                           port=context.config["components"]["CB"]["port"],
                           service=context.service,
                           subservice=context.subservice)

        context.r = cb_sample_entity_recover(cb)


    elif REQUEST == "TOKEN" and ACTION == "GET":

        # Recover a Token
        context.token_header = ks_get_token(context)
        print ("\n #>> Token to use: {}".format(context.token_header))

        if context.r_ks.status_code == 200:
            ks_content_json = json.loads(context.r_ks.content)
            context.token_id = ks_content_json["token"]["user"]["domain"]["id"]
            print ("Token returned: {}".format(context.token_id))

        # add response to next step validation
        context.r = context.r_ks

    elif REQUEST == "SERVICES" and ACTION == "GET":
        # Recover created services (if any)
        iota_url = context.config["components"]["IOTA"]["protocol"] + "://" + \
                   context.config["components"]["IOTA"]["instance"] + ":" + \
                   context.config["components"]["IOTA"]["port"] + "/iot"

        # if it is the node iota update the url
        if context.config['components']["IOTA"]['iota_type'] == "node":
            iota_url = iota_url + "/agents/default"

        # Recover a Token
        context.token_header = ks_get_token(context)
        print ("\n #>> Token to use: {}".format(context.token_header))

        headers = {
            'content-type': "application/json",
            'accept': "application/json",
            'fiware-service': context.service,
            'fiware-servicepath': context.subservice
        }

        # Generate a iota object
        context.iota = Rest_Utils_IoTA(server_root=iota_url, server_root_secure=iota_url)

        # Add the token to the headers
        headers.update({'X-Auth-Token': context.token_header})
        context.r = context.iota.get_listServices(headers=headers)
        print (context.r.content)

        eq_(200, context.r.status_code, "ERROR: Service request IOTA failed: {}".format(context.r.status_code))
        iota_content_json = json.loads(context.r.content)

        # show returned response
        __logger__.debug("IOTA returns {} ".format(iota_content_json))

        if context.config['components']["IOTA"]['iota_type'] == "node":
            service = iota_content_json["service"]
            print ("Service: {}".format(service))
        else:
            for service in iota_content_json["services"]:
                print ("Service: {}".format(service))

            assert_greater_equal("1", iota_content_json["count"],
                                 'INCORRECT amount of services'
                                 '\n Services number Expected IS >= {} \n Received: {}'.format("1",
                                                                                               iota_content_json[
                                                                                                   "count"]))

            if iota_content_json["count"] >= 0:
                for service in iota_content_json["services"]:
                    if service["service"] == context.service:
                        print ("#> Service_name Found: {}".format(service["service"]))
                        break
                    else:
                        __logger__.debug(
                                "#> Service returned but does not match with headers: {}".format(service["service"]))

    elif REQUEST == "PROTOCOLS" and ACTION == "GET":
        # Recover created services (if any)
        iotm_url = context.config["components"]["IOTM"]["protocol"] + "://" + \
                   context.config["components"]["IOTM"]["instance"] + ":" + \
                   context.config["components"]["IOTM"]["port"] + "/iot/protocols?detailed=on"

        # Recover a Token
        context.token_header = ks_get_token(context)
        print ("\n #>> Token to use: {}".format(context.token_header))

        # Generate a iotM object
        context.iota = Rest_Utils_IoTA(server_root=iotm_url, server_root_secure=iotm_url)

        # Add the token to the headers
        headers = {
            'content-type': "application/json",
            'accept': "application/json",
            'fiware-service': context.service,
            'fiware-servicepath': context.subservice}

        headers.update({'X-Auth-Token': context.token_header})

        context.r = requests.get(iotm_url, headers=headers)
        iotm_content_json = json.loads(context.r.content)
        print ("IOTM returns {} ".format(iotm_content_json))

        # show returned response
        __logger__.debug("IOTM returns {} ".format(iotm_content_json))
        for protocol in iotm_content_json["protocols"]:
            __logger__.debug("Protocol: {}".format(protocol))

        eq_(200, context.r.status_code)

        assert_greater_equal("0", iotm_content_json["count"],
                             'INCORRECT amount of protocols'
                             '\n Protocols number Expected IS >= {} \n Received: {}'.format("0",
                                                                                            iotm_content_json["count"]))
        if iotm_content_json["count"] >= 0:
            for protocol in iotm_content_json["protocols"]:
                print ("#> Protocol_name Found: {}".format(protocol["protocol"]))

    elif REQUEST == "RULES" and ACTION == "GET":
        # Recover created services (if any)
        cep_url = context.config["components"]["CEP"]["protocol"] + "://" + \
                  context.config["components"]["CEP"]["instance"] + ":" + \
                  context.config["components"]["CEP"]["port"] + \
                  context.config["components"]["CEP"]["path_rules"]

        # Default headers
        headers = {
            'content-type': "application/json",
            'accept': "application/json",
            'fiware-service': context.service
        }

        # Recover the rules
        context.r = requests.get(cep_url, headers=headers)

        cep_rules_content_json = json.loads(context.r.content)
        # print ("CEP returns {} ".format(cep_rules_content_json))

        assert_greater_equal("0", cep_rules_content_json["count"],
                             'INCORRECT amount of rules'
                             '\n Protocols number Expected IS >= {} \n Received: {}'.format("0",
                                                                                            cep_rules_content_json[
                                                                                                "count"]))

        # show returned response
        __logger__.debug("CEP returns {} ".format(cep_rules_content_json))
        print ("\n")
        for rule in cep_rules_content_json["data"]:
            __logger__.debug("Rule: {}".format(rule["name"]))
            print ("#> Rule: {} | Active: {} | Card1: {} | Card2: {} ".format(rule["name"], rule["active"],
                                                                              rule["cards"][0]["type"],
                                                                              rule["cards"][1]["type"]))

    else:
        __logger__.error("No request configured")
