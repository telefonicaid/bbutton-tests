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
from iotqautils.cb_utils import EntitiesConsults, PayloadUtils, NotifyConditions, ContextElements, AttributesCreation, \
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
    eval("notify_cond.add_notify_condition_" + context.table[0]['notify_type'].lower() + "(cond_values)")

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
    resp = eval("cb.standard_subscribe_context_" + context.table[0]['notify_type'].lower() + "(subscription_pl)")
    eq_(200, resp.status_code)


@step(
        u'I send an entity update to context broker with service "{service}", subservice "{subservice}", entity_id "{entity_id}", entity_type "{entity_type}", entity_pattern "{entity_pattern}"')
def update_entity(context, service, subservice, entity_id, entity_type, entity_pattern):
    """
    General purpose step to create entities
    When I send an entity update to context broker with service "<SERVICE>", subservice "<SUBSERVICE>",
    entity_id "<ID>", entity_type "<TYPE>", entity_pattern "false"
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
        # Retrieve the service and subservice real value and give to the CB object
    # TestUtils.set_service_and_subservice(context, service, subservice)

    # entity id added to world to be used in CBUPDATE rule if applies
    context.remember['entity_id'] = entity_id
    context.remember['entity_type'] = entity_type
    context.remember['attribute_name'] = context.table[0]['attribute_name']
    # world.g['service'] = service
    # world.g['subservice'] = subservice

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
        context.remember['entity_attribute_name'] = attribute['attribute_name']
        context.remember['entity_attribute_type'] = attribute['attribute_type']
        context.remember['entity_attribute_value'] = attribute['attribute_value']

    # Compose the payload
    context_element = ContextElements()
    context_element.add_context_element(entity_id, entity_type, attributes, is_pattern=entity_pattern)
    payload = PayloadUtils.build_standard_entity_creation_payload(context_element)

    # Add entity to the list fo contexts to be removed
    # entity is a dict with the context, service and subservice
    entity = {'context': context_element, 'service': service, 'subservice': subservice}
    try:
        context.o['entities2remove'].append(entity)
    except KeyError:
        context.o['entities2remove'] = []
        context.o['entities2remove'].append(entity)

    __logger__.info('Added entity to the list of entities to be removed')

    # Launch the requests to CB
    resp = context.o['CB'].standard_entity_creation(payload)
    eq_(200, resp.status_code)
    cb_content_json = json.loads(resp.content)
    __logger__.info(cb_content_json)

    # TestUtils.
    remember(context, "cb_response", resp)