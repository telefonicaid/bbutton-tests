# -*- coding: utf-8 -*-

"""
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.
The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement contract under which the program(s) have
been supplied.
"""

import json
import logging

from behave import *
from nose.tools import eq_, assert_in
from common.test_utils import *
from iotqatools.cb_utils import EntitiesConsults, PayloadUtils, NotifyConditions, ContextElements, AttributesCreation, \
    MetadatasCreation

__logger__ = logging.getLogger("mqtt_steps")


@given(u'the "{KEY}" key contains these values')
def step_impl(context, KEY):
    """
    :type context: behave.runner.Context
    """
    table = context.table
    data_dic = dict({})

    # convert table values into att value
    for row in range(len(table.rows)):
        data_dic.update((dict(zip(table.headings, table[row]))))
        print (data_dic)

    target = None

    if KEY == "ATTS":
        target = "attributes"
    if KEY == "LAZY":
        target = "lazy"
    if KEY == "COMMANDS":
        target = "commands"
    if KEY == "STATIC_ATTS":
        target = "static_attributes"

    # update vale into request
    if "mqtt_create_request" in context:
        context.mqtt_create_request['devices'][0][target] = [data_dic]

    if KEY == "STATIC_ATTS":
        # if it is the last item to update
        updated_payload = json.dumps(context.mqtt_create_request)
        create_response = mqtt_create_device(context,
                                             url=context.mqtt_create_url,
                                             headers=context.headers,
                                             data=updated_payload)
        eq_(201, create_response.status_code)

        print ("\n END \n")
