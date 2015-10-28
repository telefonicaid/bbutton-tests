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


from behave import *
from nose.tools import eq_
import requests
import logging
import json
import time
import random
from iotqatools.mysql_utils import Mysql
from common.test_utils import *

#use_step_matcher("re")

__logger__ = logging.getLogger("cb_cygnus_mysql")


@step(u'I set a MySQL database under name "{service}" and a table under name given by "{servicepath}" and "{entity_id}"')
def db_table_creation(context, service, servicepath, entity_id):
    context.service = str(service)
    context.servicepath = str(servicepath)

    # Connect to mysql
    context.mysql_init = Mysql(host=context.config["components"]["MYSQL"]["instance"],
                       port=context.config["components"], user=context.config["components"]["MYSQL"]["user"],
                       password=context.config["components"]["MYSQL"]["password"],
                       database=context.config["components"]["MYSQL"]["defaultservice"],
                       version=context.config["components"]["MYSQL"]["version"], mysql_verify_version="False")

    context.mysql_init.connect()

    # To be deleted after
    context.o["MYSQL"] = context.mysql_init
    if service not in context.o['db2remove']:
        context.o['db2remove'].append(service)

@step(u'I launch a cygnus connection with "{component}"')
def step_impl(context, component):
    __logger__.info("--> INITIALIZE CYGNUS2{} CONNECTION -->".format(component))
    initialize_cygnus2comp(context, component)

    __logger__.info("--> INITIALIZE CB -->")
    initialize_cb(context)
    context.o["CB"].set_service(context.service)
    context.o["CB"].set_subservice(context.servicepath)


@step('I check value "{attvalue}" in column name "{attname}" of "{servicepath}" table in MySQL')
def step_impl(context, attvalue, attname, servicepath):
    # Pick the returned value from DB:
    table_name = "{}_{}_{}".format(servicepath[1:], context.remember['entity_id'], context.remember['entity_type'])
    resp = context.mysql_init.table_search_columns_last_row(database_name=context.service, table_name=table_name,
                                                       columns=attvalue)
    if resp:
        # Exit from first range in tuple
        returned_value = resp[0]

        context.mysql_init.table_pretty_output(database_name=context.service, table_name=table_name)
        eq_(str(attvalue), str(returned_value), "ASSERT ERROR --> Value in MYSQL table was not updated")


@then('I check values "{values}" in column names "{att_names}" of "{servicepath}" table in MySQL')
def step_impl(context, values, att_names, servicepath):
    servicepath = servicepath[1:]
    att_names = att_names.split(';')
    rows=str(len(att_names))
    print(rows)
    values = values.split(';')
    count = 0
    table_name = "{}_{}_{}".format(servicepath, context.remember['entity_id'], context.remember['entity_type'])

    #table = context.mysql_init.table_search_columns_in_several_rows(database_name=context.service, table_name=table_name,rows=rows, columns='*')
    table =context.mysql_init.table_search_columns_last_row(database_name=context.service, table_name=table_name,
                                                       columns="*")

    #table = table[0]
    # Sketch the attributes sent from CB and check their values
    for name in att_names:
        pass
    print(table)

    #context.mysql_init.table_pretty_output(database_name=context.databasename, table_name=servicepath)
    eq_(count, len(values), "ASSERT ERROR --> Some of the attributes were not passed to the table")
