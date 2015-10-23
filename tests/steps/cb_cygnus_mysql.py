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


@step(u'I create a MySQL database under name "{service}" and a table under name given by "{servicepath}" and "{entity_id}"')
def db_table_creation(context, service, servicepath, entity_id):
    # Connect to mysql
    context.mysql_init = Mysql(host=context.config["components"]["MYSQL"]["instance"],
                       port=context.config["components"], user=context.config["components"]["MYSQL"]["user"],
                       password=context.config["components"]["MYSQL"]["password"],
                       database=context.config["components"]["MYSQL"]["defaultservice"],
                       version=context.config["components"]["MYSQL"]["version"], mysql_verify_version="False")

    context.mysql_init.connect()

    # Create database
    __logger__.info(" -> Create database: {}".format(service))
    context.mysql_init.create_database(service)

    context.mysql_init.set_database(service)

    # Create table
    if len(servicepath) is 1:
        servicepath = "default_svpath"

    if "/" in servicepath:
        servicepath.replace("/","")

    table_name = servicepath  #"{}_{}".format(servicepath, entity_id)
    table_fields = "(recvTimeTs VARCHAR(250),\
                recvTime VARCHAR(250),\
                entityId VARCHAR(50),\
                entityType VARCHAR(250),\
                ccid_name VARCHAR(50),\
                ccid_value VARCHAR(250),\
                imsi_name VARCHAR(50),\
                imsi_value VARCHAR(250),\
                imei_name VARCHAR(50),\
                imei_value VARCHAR(250),\
                location_name VARCHAR(50), \
                location_value VARCHAR(250),\
                attrMd VARCHAR(250))"

    context.mysql_init.create_table(name=table_name, database_name=service, fields=table_fields)

    table_exists = context.mysql_init.table_exist(database_name=service, table_name=table_name)

    # Five times attempt to make sure table can be created
    for x in range(0,5):
        if table_exists is None:
            context.mysql_init.connect()
            context.mysql_init.create_table(name=table_name, database_name=service, fields=table_fields)

    # To be deleted after
    context.o["MYSQL"] = context.mysql_init
    if service not in context.o['db2remove']:
        context.o['db2remove'].append(service)

    context.databasename = service

    eq_(table_name, table_exists[0], "ASSERT ERROR --> Creation of a new table in MYSQL was not succesful")



@step(u'I launch a cygnus connection with "{component}"')
def step_impl(context, component):
    __logger__.info("--> INITIALIZE CYGNUS2{} CONNECTION -->".format(component))
    initialize_cygnus2comp(context, component)

    __logger__.info("--> INITIALIZE CB -->")
    initialize_cb(context)



@step('I check value "{attvalue}" in column name "{attname}" of "{servicepath}" table in MySQL')
def step_impl(context, attvalue, attname, servicepath):
    # Pick the returned value from DB:
    resp = context.mysql_init.table_search_columns_last_row(database_name=context.databasename, table_name=servicepath,
                                                            columns=attname)
    if resp:
        # Exit from first range in tuple
        returned_value = resp[0]
        context.mysql_init.table_pretty_output(database_name=context.databasename, table_name=servicepath)
        eq_(attvalue, returned_value, "ASSERT ERROR --> Value in MYSQL table was not updated")


@then('I check values "{values}" in column names "{att_names}" of "{servicepath}" table in MySQL')
def step_impl(context, values, att_names, servicepath):
    att_names = att_names.split(';')
    values = values.split(';')
    count = 0

    table = context.mysql_init.table_search_columns_last_row(database_name=context.databasename, table_name=servicepath, columns="*")
    #table = table[0]
    print(table)
    # Sketch the attributes sent from CB and check their values
    for name in att_names:
        if name == "temperature":
            index = att_names.index(name)
            if values[index] == table[3]:
                count += 1
        elif name == "lastIP":
            index = att_names.index(name)
            if values[index] == table[5]:
                count += 1
        elif name == "device":
            index = att_names.index(name)
            if values[index] == table[7]:
                count += 1
        elif name == "Phenomenons":
            index = att_names.index(name)
            if values[index] == table[9]:
                count += 1
        elif name == "status":
            index = att_names.index(name)
            if values[index] == table[11]:
                count += 1
        elif name == "fill_level":
            index = att_names.index(name)
            if values[index] == table[13]:
                count += 1
        elif name == "test1":
            index = att_names.index(name)
            if values[index] == table[15]:
                count += 1
        elif name == "test2":
            index = att_names.index(name)
            if values[index] == table[17]:
                count += 1

    #context.mysql_init.table_pretty_output(database_name=context.databasename, table_name=servicepath)
    eq_(count, len(values), "ASSERT ERROR --> Some of the attributes were not passed to the table")
