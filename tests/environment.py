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

import logging
import json

from nose.tools import assert_true

logging.basicConfig(filename="./tests/logs/behave.log", level=logging.DEBUG)
__logger__ = logging.getLogger("qa")


def merge(a, b, path=None):
    """
    :param a: Destiny dictionary to be merged
    :param b: Dictionary to be included in A
    :param path: if needed to merge in a specific path
    :return: Merged dictionary
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a



def before_all(context):
    """
    Parse the JSON instances configuration file
    :param context: Context to be updated
    :return: None
    """

    try:
        with open("./tests/properties.json") as config_file:
            properties = json.load(config_file)

    except Exception as e:
        __logger__.error("#>> PROPERTIES LOAD: [ERROR] ", e)
        assert_true(False, msg="[ERROR: PROPERTIES FILE IS NOT VALID]")
    __logger__.info("#>> PROPERTIES LOADED: [OK] ")

    # Parse the JSON instances configuration file
    try:
        with open("./tests/instances.json") as instances_file:
            instances = json.load(instances_file)
    except Exception as e:

        __logger__.error("#>> INSTANCES LOAD: [ERROR] ", e)
        assert_true(False, msg="[ERROR: INSTANCES FILE IS NOT VALID]")
    __logger__.info("#>> INSTANCES LOADED: [OK] ")

    context.config = merge(properties, instances)



def before_feature(context, feature):
    # model.init(environment='test')
    if 'specialtag' in feature.tags:
        __logger__.info("***********SPECIAL TAG BEFORE FEATURE --->>>>>>>>")

    context.remember = {}
    context.o = {}


def before_scenario(context, scenario):
    if 'init_db' in context.tags:
        __logger__.info("*********** Init DB to be used in scenario {} --->>>>>>>>".format(scenario))


def after_scenario(context, scenario):
    if 'entity_clean' in context.tags:
        __logger__.info("*********** Cleaning entities in scenario {} --->>>>>>>>".format(scenario))



