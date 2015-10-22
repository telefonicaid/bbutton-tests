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

import re
import requests
import logging
from iotqatools.cb_utils import CbNgsi10Utils, PayloadUtils
from iotqatools.ks_utils import KeystoneCrud
from iotqatools.iota_utils import Rest_Utils_IoTA
from iotqatools.mysql_utils import Mysql
from common import orc_delete_service, orc_get_services

__logger__ = logging.getLogger("test utils")


@staticmethod
def initialize_log(log_level='INFO'):
    """
    Configuring the CB Utility lib
    """
    # LOG LEVEL: 'CRITICAL','ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
    __logger__ = logging.getLogger("test utils")

    # eval(__logger__+".log_level"+"("+"#>> Test_utils: [LOG] Initialized"+")", log_level)


#@staticmethod
def initialize_cb(context):
    """
    Configuring the CB Utility lib
    """

    context.o['CB'] = CbNgsi10Utils(protocol=context.config["components"]["CB"]['protocol'],
                                    instance=context.config["components"]["CB"]['instance'],
                                    port=context.config["components"]["CB"]['port'])

    endpoint = get_endpoint(instance=context.config["components"]["CB"]["instance"],
                            protocol=context.config["components"]["CB"]["protocol"],
                            port=context.config["components"]["CB"]["port"], path="")

    remember(context, "cb_url", endpoint)
    __logger__.info("#>> Test_utils: [CB] Initialized")


#@staticmethod
def initialize_cygnus2comp(context, comp):
    """
    Configuring the cyguns2mysql Utility lib
    """
    endpoint = get_endpoint(instance=context.config["components"][comp]["cygnus"],
                            protocol=context.config["components"][comp]["protocol"],
                            port=context.config["components"][comp]["cygnus_port"],
                            path=context.config["components"][comp]["cygnus_path"])

    remember(context, "CYGNUS2comp_url", endpoint)
    __logger__.info("#>> Test_utils: [CYGNUS2{}] Initialized".format(comp))


@staticmethod
def initialize_mysql(context):
    """
    Configuring the mysql Utility lib
    """
    context.o['MYSQL'] = Mysql(host=context.config["components"]["MYSQL"]["instance"],
                               port=context.config["components"]["MYSQL"]["port"],
                               user=context.config["components"]["MYSQL"]["user"],
                               password=context.config["components"]["MYSQL"]["password"],
                               database=context.config["components"]["MYSQL"]["defaultservice"],
                               version=context.config["components"]["MYSQL"]["version"],
                               mysql_verify_version="True")

    context.o['MYSQL'].connect()
    __logger__.info("#>> Test_utils: [MYSQL] Initialized")


@staticmethod
def initialize_ks(context):
    # Initialized with default values to be modified later
    context.o['KS'] = KeystoneCrud(username="default_username", password="default_password",
                                   domain="default_domain", ip=context.config["components"]["KS"]["instance"],
                                   port=context.config["components"]['KS']["port"])

    endpoint = get_endpoint(instance=context.config["components"]["KS"]["instance"],
                            protocol=context.config["components"]["KS"]["protocol"],
                            port=context.config["components"]["KS"]["port"], path="")

    remember(context, "KEYSTONE_url", endpoint)
    __logger__.debug("#>> Test_utils: [KEYSTONE] Initialized")


@staticmethod
def initialize_iota(context):
    """
    Configuring the cyguns2mysql Utility lib
    """

    endpoint_measure = get_endpoint(instance=context.config["components"]["IOTA"]["instance"],
                                    protocol=context.config["components"]["IOTA"]["protocol"],
                                    port=context.config["components"]["IOTA"]["port"], path="")

    endpoint = get_endpoint(instance=context.config["components"]["IOTA"]["instance"],
                            protocol=context.config["components"]["IOTA"]["protocol"],
                            port=context.config["components"]["IOTA"]["port"],
                            path=context.config["components"]["IOTA"]["path"])

    endpoint_manager = get_endpoint(instance=context.config["components"]["IOTA"]["instance"],
                                    protocol=context.config["components"]["IOTA"]["protocol"],
                                    port=context.config["components"]["IOTA"]["manager_port"],
                                    path=context.config["components"]["IOTA"]["path"])

    remember(context, "iota_url", endpoint)
    remember(context, "iotam_url", endpoint_manager)
    context.o['MEASURE'] = Gw_Measures_Utils(server_root=endpoint_measure)
    context.o['IOTA'] = Rest_Utils_IoTA(server_root=context.remember['iota_url'],
                                        server_root_secure=context.remember['iota_url'])
    context.o['IOTM'] = Rest_Utils_IoTA(server_root=context.remember['iotam_url'],
                                        server_root_secure=context.remember['iotam_url'])


@staticmethod
def set_service_and_subservice(context, service, subservice):
    """
    retrieves the values of service and subservice from configuration file if applies. Otherwise take the values
     of the scenario. Then it stores the service and subservice in the context.g. Also set the CB objet with service
     and subservice.
    :param service:
    :param subservice:
    :return: stored the service and subservice in context.g
    """
    a = re.compile("^service_.*")
    if a.match(service):
        pass
        remember(context, 'service', get_service_env_data(context, service, "name"))
    else:
        pass
        remember(context, 'service', service)
    b = re.compile("^subservice_.*")
    c = re.compile("^service_[0-9]subservice_[0-9]")
    if b.match(subservice):
        pass
        remember(context, 'subservice', get_subservice_env_data(context, subservice))
    elif c.match(subservice):
        pass
        remember(context, 'subservice', get_service_subservice_env_data(context, subservice))
    else:
        subservice = subservice.replace("//", "/")
        remember(context, 'subservice', subservice)
    context.o['CB'].set_service(context.remember["service"])
    context.o['CB'].set_subservice(context.remember["subservice"])

    return context.config["env_data"]["services"][service]


@staticmethod
def get_service_env_data(context, service, filter="all"):
    a = re.compile("^service_.*")
    b = re.compile("^service_subservice_.*")
    if a.match(service):
        try:
            if filter == "all":
                return context.config["env_data"]["services"][service]
            if filter == "name":
                return context.config["env_data"]["services"][service]["service_name"]
            if filter == "subservices":
                return context.config["env_data"]["services"][service]["subservices"]
        except ValueError, e:
            __logger__.info(e)
            return False
        if b.match(filter):
            try:
                if filter == "service_subservice_0":
                    return context.config["env_data"]["services"][service]["subservices"][0]
                if filter == "service_subservice_1":
                    return context.config["env_data"]["services"][service]["subservices"][1]
                if filter == "service_subservice_2":
                    return context.config["env_data"]["services"][service]["subservices"][2]
                if filter == "service_subservice_3":
                    return context.config["env_data"]["services"][service]["subservices"][3]
                if filter == "service_subservice_4":
                    return context.config["env_data"]["services"][service]["subservices"][4]
            except ValueError, e:
                __logger__.info(e)
                return False
    else:
        return False


@staticmethod
def get_subservice_env_data(context, subservice):
    a = re.compile("^subservice_.*")

    # if it is an id of subservices
    if a.match(subservice):
        try:
            if filter == "name":
                return context.config["env_data"]["subservices"][subservice]
        except ValueError, e:
            __logger__.info(e)
            return False
    else:
        return False


@staticmethod
def get_service_subservice_env_data(context, service_subservice, filters=0):
    a = re.compile("^service_[0-9]subservice_[0-9]")

    # if it is an subservice inside a services
    if a.match(service_subservice):
        s = re.compile("^service_[0-9]")
        ss = re.compile("subservice_[0-9]")
        n = re.compile("[0-9]")

        service = re.findall(s, service_subservice)[0]
        subservice = re.findall(ss, service_subservice)[0]
        ss_number = eval(re.findall(n, subservice)[0])

        try:
            return context.config["env_data"]["services"][service]["subservices"][ss_number]
        except ValueError, e:
            __logger__.info(e)
            return False
    else:
        return False


@staticmethod
def get_user_env_data(context, user, filter):
    a = re.compile("^user_.*")
    if a.match(user):
        try:
            if filter == "all":
                return context.config["env_data"]["users"][user]
            if filter == "name":
                return context.config["env_data"]["users"][user]["user_name"]
            if filter == "password":
                return context.config["env_data"]["users"][user]["user_password"]
            if filter == "service":
                return context.config["env_data"]["users"][user]["user_service"]
            if filter == "subservice":
                return context.config["env_data"]["users"][user]["user_subservice"]
            if filter == "role":
                return context.config["env_data"]["users"][user]["user_role"]
        except ValueError, e:
            print e
            return False
    else:
        return False


@staticmethod
def get_kind_input_from_env_data(input):
    """
    Check if the input data needs to recover info from emv properties file
    :param input:
    :return:
    """
    s = re.compile("^service_[0-9]")
    ss = re.compile("^subservice_[0-9]")
    sub_ss = re.compile("^service_[0-9]subservice_[0-9]")
    user = re.compile("^user_.*")

    if sub_ss.match(input):
        return "service_subservice"
    if ss.match(input):
        return "subservice"
    if s.match(input):
        return "service"
    if user.match(input):
        # TODO: Improve the user extraction #
        return "user"
    return False


@staticmethod
def set_user_service_and_subservice(context, user, service, subservice):
    """
    retrieves the values of service and subservice from configuration file if applies. Otherwise take the values
     of the scenario. Then it stores the service and subservice in the world.g. Also set the CB objet with service
     and subservice.
    :param user:
    :param service:
    :param subservice:
    :return: stored the service and subservice in world.g
    """

    x = re.compile("^user_.*")
    if x.match(user):
        remember(context, 'user', get_user_env_data(context, user, "name"))
    else:
        remember(context, 'user', user)

    a = re.compile("^user_[0-9]service")
    if a.match(service):
        remember(context, 'service', get_user_env_data(context, user, "service"))
    else:
        remember(context, 'service', service)

    b = re.compile("^user_[0-9]subservice")
    if b.match(subservice):
        remember(context, 'subservice', get_user_env_data(context, user, "subservice"))
    else:
        subservice = subservice.replace("//", "/")
        remember(context, 'subservice', subservice)

    # set CB object with service and subservice
    context.o['CB'].set_service(context.remember["service"])
    context.o['CB'].set_subservice(context.remember["subservice"])


@staticmethod
def remove_cb_entities(context):
    if context.o['entities2remove']:
        try:
            for entity in context.o['entities2remove']:
                payload = PayloadUtils.build_standard_entity_delete_payload(entity['context'])
                context.o['CB'].set_service(entity['service'])
                context.o['CB'].set_subservice(entity['subservice'])
                context.o['CB'].standard_entity_delete(payload)
                __logger__.info(" -> DELETED entity")
        except AssertionError, e:
            __logger__.error("ERROR DELETING -> entity {}".format(e))
    else:
        __logger__.info(" -> Nothing to delete ")


#@staticmethod
def remove_mysql_databases(context):
    if context.o['db2remove']:
        try:
            for db in context.o['db2remove']:

                context.o["MYSQL"].drop_database(db)
                __logger__.info(" -> DELETED database: {}".format(db))
        except AssertionError, e:
            __logger__.error("ERROR DELETING -> database {}".format(e))
    else:
        __logger__.info(" -> Nothing to delete ")


#@staticmethod
def remember(context, key, value):
    """Add the value to context remember dict"""
    context.remember[key] = value


def get_endpoint(protocol, instance, port, path=None):
    if not path:
        return "{}://{}:{}".format(protocol, instance, port)
    else:
        return "{}://{}:{}{}".format(protocol, instance, port, path)



def bb_delete_method(context):
    context.url_component = get_endpoint(context.instance_protocol,
                                         context.instance_ip,
                                         context.instance_port)
    url = str("{}/v1.0/service".format(context.url_component))

    #Get list of services
    context.service_admin = "admin_domain"
    context.user_admin = "cloud_admin"
    context.password_admin = "password"
    context.services = orc_get_services(context)
    for service in context.services:
        if context.service == service["name"]:
            context.service_id = service["id"]
            break

    # Get config env credentials
    context.user_admin = "cloud_admin"
    context.password_admin = "password"

    try:
        if "service_id" in context:
            delete_response = orc_delete_service(context, context.service_id)

    except ValueError:
        __logger__.error("[Error] Service to delete ({}) not found".format(context.service))


def devices_delete_method(context):
    if "Fiware-Service" not in context.headers:
        context.headers.update({"Fiware-Service": context.service, "Fiware-ServicePath": context.servicepath})


    context.url_component = get_endpoint(context.instance_protocol,
                                         "localhost",
                                         "4041")

    url = str("{}/iot/devices/{}".format(context.url_component, context.device_id))

    try:
        resp = requests.delete(url=url, headers=context.headers)
        __logger__.info("DEVICE ({}) deleted".format(context.device_id))
    except ValueError:
        __logger__.error("[Error] Device to delete ({}) not found".format(context.device_id))

