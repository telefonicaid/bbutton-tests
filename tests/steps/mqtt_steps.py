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
import datetime
import time

from behave import *
from nose.tools import eq_, assert_in
from common.test_utils import *
from common.mqtt_utils import MqttUtils
from iotqatools.cb_utils import EntitiesConsults, PayloadUtils, NotifyConditions, ContextElements, AttributesCreation, \
    MetadatasCreation

mqttl = MqttUtils(host="127.0.0.1", port="1883", user="iota", pwd="iota")
__logger__ = logging.getLogger("mqtt_steps")


@given(u'the "{KEY}" key contains these values')
def step_impl(context, KEY):
    """
    Updates the rest of values and send the request to iotaMQTT
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
        print ("# [MQTT] Creation device: {}".format(create_response.status_code))


@when("a simple measure is sent to IOTA_MQTT")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("iot.eclipse.org", 1883, 60)


# {"tt":"20160119T223001Z","L":3,"T": 22.8,"H":24,"G":0,"M":3835,"V":"L","C1":"00D600070af90d04"}

@step('a Service with name "([^"]*)" and protocol "([^"]*)" created')
def service_created_precond(context, service_name, protocol):
    if protocol:
        context.protocol = protocol

        # if protocol == 'IoTModbus':
        #     functions.service_precond(service_name, protocol, {}, {}, CBROKER_URL_TLG)
        # else:
        #     functions.service_precond(service_name, protocol)


@when('I publish a MQTT message with device_id "{device_id}", attribute "{att}" msg "{msg}" and apikey "{apikey}"')
def step_impl(context, device_id, att, msg, apikey):
    ts = time.time()
    st = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')
    context.st = st
    context.ts = ts

    context.device_id = device_id
    topic = '/{}/{}/{}'.format(apikey, device_id, att)
    print ("\n| Topic {} | MSG {}|".format(topic, msg))

   # format required /apikey/devId/attributes
    mqttl.publish_message(topic=str(topic), payload=str(msg), user="iota", pwd="iota")
