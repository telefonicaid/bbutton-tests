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

__logger__ = logging.getLogger("sth")


@step(u'service and subservice are provisioned in ContextBroker and STH')
def init_clients(context):

    initialize_sth(context)
    context.o["STH"].set_service(context.service)
    context.o["STH"].set_subservice(context.servicepath)

    initialize_cb(context)
    context.o["CB"].set_service(context.service)
    context.o["CB"].set_subservice(context.servicepath)


@step(u'I check attribute "{attname}" was registered in STH')
def check_attr_exists(context, attname):
    resp = context.o["STH"].request_raw_data(context.remember['entity_type'],
                                             context.remember['entity_id'],
                                             attname,
                                             lastN=1)
    eq_(200, resp.status_code)
    resp_list = json.loads(resp.content)['contextResponses']
    eq_(len(resp_list), 1)
    eq_(resp_list[0]['contextElement']['attributes'][0]['name'], attname)
    eq_(len(resp_list[0]['contextElement']['attributes'][0]['values']), 1)
