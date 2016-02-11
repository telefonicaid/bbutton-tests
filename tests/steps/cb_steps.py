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
from nose.tools import eq_, assert_in, assert_greater_equal
from common.test_utils import *
from iotqatools.cb_utils import EntitiesConsults, PayloadUtils, NotifyConditions, ContextElements, AttributesCreation, \
    MetadatasCreation

__logger__ = logging.getLogger("cb_utils")


@step(u'I create a subscription in context broker')
def create_subscription(context):
    """
    Create a subscription in CB to Instance-Destiny with Xseconds of duration over changes in ATTribute,
    Example step:
    Given I create a subscription in context broker
      | service   | subservice   | entity_id | entity_pattern | entity_type | attributes_name | notify_url | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SUBSERVICE> | <ID>      | false          | <TYPE>      | <ATTNAME>       | CYGNUS2STH | 1        | ONCHANGE    |                   | None       |
    :param step:
    service: Fiware-service header
    subservice: Fiware-servicePath header
    entity_id: id of the entity
    entity_type: type of the entity
    entity_pattern: true | false - Indicates if the subscription is regexp or not
    attributes_name: list of attributes names to be included in the notification.
    notify_url: destination of the notification
    duration: in seconds
    notify_type: ONCHANGE | ONTIME
    notif_cond_values: list of attributes separated by semi-colon (;) or interval e.g. PT1S
    throttling: time limit for the notification
    """

    assert_in(context.table[0]['notify_type'], ["ONTIME", "ONCHANGE"], "[ERROR] Invalid subscription type")

    cb = context.o['CB']

    # Changes in the entity att that trigger the notification
    ref = context.remember[context.table[0]['notify_url'] + "_url"]
    duration = context.table[0]['duration']

    if context.table[0]['attributes_name'] == "None":
        attributes_list = []
    else:
        attributes_list = context.table[0]['attributes_name'].split(";")

    notify_cond = NotifyConditions()
    cond_values = context.table[0]['notif_cond_values'].split(";")
    getattr(notify_cond, "add_notify_condition_" + context.table[0]['notify_type'].lower())(cond_values)

    entities = EntitiesConsults()
    entities.add_entity(entity_id=context.table[0]['entity_id'],
                        entity_type=context.table[0]['entity_type'],
                        is_pattern=context.table[0]['entity_pattern'])

    if context.table[0]['throttling'] == "None":
        throttling = None
    else:
        throttling = context.table[0]['throttling']

    subscription_pl = PayloadUtils.build_standard_subscribe_context_payload(entities=entities,
                                                                            attributes=attributes_list,
                                                                            reference=ref,
                                                                            duration="PT" + duration + "S",
                                                                            notify_conditions=notify_cond,
                                                                            throttling=throttling)
    # resp = cb.standard_subscribe_context_onchange(subscription_pl)
    resp = getattr(cb, "standard_subscribe_context_" + context.table[0]['notify_type'].lower())(subscription_pl)
    eq_(200, resp.status_code)
    subs_id = json.loads(resp.content)['subscribeResponse']['subscriptionId']
    remember(context, 'subscription_id', subs_id)


@step(
    u'I send a context update to context broker with service "{service}", subservice "{subservice}", ' +
    u'and "{nEntities}" entities with id "{entity_id}" and type "{entity_type}"')
def update_context(context, service, subservice, nEntities, entity_id, entity_type):
    """
    General purpose step to create entities (1..N)
    Creates:
        entity_id,
        entity_id_1
        ...
        entity_id_n-1
    When I send a context update to context broker with service "<SERVICE>", subservice "<SUBSERVICE>",
    and "<N>" entities with id "<ID>" and type "<TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list                            |
      | temperature    | centigrade     | 23              | nombre1,tipo1,valor1                     |
      | pressure       | mmHG           | 990             | nombre1,tipo1,valor1;nombre2,tipo2,valor2|
      | fillLevel      | %              | 90              | None                                     |

    metadata_list: QA list of metadatas separated by semi-colon (;). Each field separated by comma (,).
                   If there is no metadata field use "None"
    """
    if "NaN" in service:
        service = ""
    elif "NaN" in subservice:
        subservice = ""

    if not 'entity_list' in context or context.entity_list is None:
        context.entity_list = []

    context_element = ContextElements()
    for n in range(0, int(nEntities)):
        curr_entity_id = entity_id if n == 0 else entity_id + "_" + str(n)
        # Go through the step and creates the attributes
        attributes = AttributesCreation()
        for attribute in context.table:
            if attribute['metadata_list'] != "None":
                md = MetadatasCreation()
                metadata_list = attribute['metadata_list'].split(";")
                for metadata in metadata_list:
                    ms = metadata.split(",")
                    md.add_metadata(ms[0], ms[1], ms[2])

                # Search and split for several attributes
                if ";" in attribute["attribute_type"]:
                    attribute_names = attribute["attribute_name"].split(";")
                    attribute_types = attribute["attribute_type"].split(";")
                    attribute_values = attribute["attribute_value"].split(";")

                    for i in range(len(attribute_names)):
                        attributes.add_attribute(attribute_names[i],
                                                 attribute_types[i],
                                                 attribute_values[i],
                                                 md)

                else:
                    attributes.add_attribute(attribute['attribute_name'],
                                             attribute['attribute_type'],
                                             attribute['attribute_value'],
                                             md)

            else:
                attributes.add_attribute(attribute['attribute_name'],
                                         attribute['attribute_type'],
                                         attribute['attribute_value'])

        # Compose the payload
        context_element.add_context_element(curr_entity_id, entity_type, attributes, is_pattern=False)

        # store entity data for following steps
        if not any(entity['entity_id'] == curr_entity_id
                   and entity['entity_type'] == entity_type for entity in context.entity_list):
            context.entity_list.append({'entity_id': curr_entity_id,
                                        'entity_type': entity_type})

    payload = PayloadUtils.build_standard_entity_creation_payload(context_element)

    # Launch the requests to CB
    resp = context.o['CB'].standard_entity_creation(payload)
    eq_(200, resp.status_code)
    cb_content_json = json.loads(resp.content)
    __logger__.info(cb_content_json)

    # TestUtils.
    remember(context, "cb_response", resp)


@step(
        'CB should have received the entity update in the entity_id "{entity_id}" and entity_type "{entity_type}" with values from "{msg}"')
def cb_check_mqtt_data(context, entity_id, entity_type, msg):
    """
    :type context: behave.runner.Context
    :type ENT_NAME: str
    :type ENT_TYPE: str
    """

    if "service" and "subservice" in context:
        service = context.service
        subservice = context.subservice
    else:
        service = None
        subservice = None

    # Compose the payload
    __logger__.debug('Entity_id: {}'.format(entity_id))
    entity = EntitiesConsults()
    entity.add_entity(entity_id, entity_type, is_pattern='false')
    payload = PayloadUtils.build_standard_query_context_payload(entity)
    __logger__.debug('Payload is: {}'.format(payload))

    # Make request to CB and retrieve the result
    try:
        initialize_cb(context)
        context.o['CB'].set_service(service)
        context.o['CB'].set_subservice(subservice)
        if 'token' in context.remember:
            context.o['CB'].set_auth_token(context.remember['token'])
        response = context.o['CB'].standard_query_context(payload)
        __logger__.info('Response to query is: {}'.format(response.json()))

        # Add response to the context
        context.remember['cb_response'] = response

        __logger__.debug(response.json()['contextResponses'][0]['statusCode'])
        if 'contextResponses' in response.json():
            assert str(response.json()['contextResponses'][0]['statusCode'][
                           'code']) == '200', 'Incorrect QueryContext response {}'.format(
                    str(response.json()['contextResponses'][0]['statusCode']['code']))
        else:
            raise Exception('The response has no statusCode field')
    except Exception, e:
        __logger__.error('ERROR, cannot retrieve entity data: {}'.format(e))
        print ("error {}".format(e))

    atts_retrieved = context.remember['cb_response'].json()['contextResponses'][0]["contextElement"]["attributes"]

    # Check values
    if not "check_measure" in context:
        context.check_measure = 1

    checks = mqtt_check_multi_measure(sent=msg,
                                      atts_retrieved=atts_retrieved)

    if "special_key" in context and context.special_key is not None:
        checks = checks + mqtt_check_special_measure(keyword=context.special_key,
                                                     sent=msg,
                                                     atts_retrieved=atts_retrieved)

    eq_(checks, context.check_measure, "> No matches from Values or Names retrieved \n#{} vs #{}\n{}".format(checks, context.check_measure, atts_retrieved))


@step('CB should have received the entity update in the entity_id "{entity_id}" and entity_type "{entity_type}" with multiple values from "{msg}"')
def cb_check_mqtt_multi_data(context, entity_id, entity_type, msg):
    context.check_measure = len(dict(json.loads(msg)))
    cb_check_mqtt_data(context, entity_id, entity_type, msg)


@step('CB should have received the entity update with multiple values from "{msg}"')
def cb_check_mqtt_special_data(context, msg):
    context.entity_id = "mqttname"
    context.entity_type = "mqtttype"
    context.check_measure = len(dict(json.loads(msg)))
    context.special_key = mqtt_convenience_atts(dict(json.loads(msg)).keys())

    cb_check_mqtt_data(context, context.entity_id, context.entity_type, msg)
