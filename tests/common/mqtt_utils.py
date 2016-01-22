# -*- coding: utf-8 -*-
"""
Copyright 2015 Telefonica Investigación y Desarrollo, S.A.U

This file is part of telefonica-iot-qa-tools

iot-qa-tools is free software: you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

iot-qa-tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with iot-qa-tools.
If not, seehttp://www.gnu.org/licenses/.

For those usages not covered by the GNU Affero General Public License
please contact with::[iot_support@tid.es]
"""

__author__ = 'xvc'

import pystache
import requests
import json
import mosquitto

from iotqatools.iot_logger import get_logger
from requests.exceptions import RequestException
from iotqatools.iot_tools import PqaTools


# Utilities
def check_valid_json(payload):
    """
    Checks if the argument is a JSON transformation valid, and return it in JSON
    :param json:
    :return:
    """
    if type(payload) is str or type(payload) is unicode:
        try:
            return json.loads(str(payload).replace('\'', '"'))
        except Exception as e:
            raise ValueError('JSON parse error in your string, check it: {string}'.format(string=payload))
    elif type(payload) is dict:
        return payload
    else:
        raise ValueError('The payloads can be only a string or a dict')


class MqttUtils(object):
    """
    Basic funcionality for mqtt protocol
    """

    def __init__(self, host, service=None, subservice=None, port="1883", user="user", pwd=None):
        """
            MQTT Utils constructor
        :param instance:
        :param service:
        :param subservice:
        :param port:
        :param user:
        :param pwd:
        :return:
        """
        # Assign the values
        self.default_endpoint = "{}:{}".format(host, port)
        self.host = host
        self.port = port
        self.service = service
        self.subservice = subservice
        self.user = user
        self.pwd = pwd


    def mqtt_connect(self, host, port, timeout, user, pwd):
        print '[MQTT] Connect'
        mqttc = mosquitto.Mosquitto(user)
        mqttc.username_pw_set(user, pwd)
        mqttc.on_connect = self.on_connect
        mqttc.on_publish = self.on_publish
        mqttc.on_subscribe = self.on_subscribe
        mqttc.on_message = self.on_message
        mqttc.on_disconnect = self.on_disconnect

        try:
            mqttc.connect(host, int(port), int(timeout))
        except:
            print ('[MQTT] MosquittoMQ server is DOWN')
        return mqttc

    # Aux functions
    def on_connect(self, mosq, obj, rc):
        if rc == 0:
            print("[MQTT] Connected successfully.")

    def on_message(self, mosq, obj, msg):
        print("[MQTT] Message received on topic {} with QoS {} and payload {}".format(
                msg.topic, msg.qos, msg.payload))
        mosq.disconnect()

    def on_publish(self, mosq, obj, mid):
        print("[MQTT] Message {} published.".format(mid))

    def on_subscribe(self, mosq, obj, mid, qos_list):
        print("[MQTT] Subscribe with mid {} received.".format(mid))

    def on_disconnect(self, mosq, obj, rc):
        print("[MQTT] Disconnected successfully.")

    def publish_message(self, topic, payload, user, pwd):
        mqttc = self.mqtt_connect(self.host, int(self.port), 60, user, pwd)
        mqttc.publish(str(topic), str(payload), 0, False)
        mqttc.loop(10)

    def susbcribe(self, topic, qos, user, pwd):
        print '[MQTT] Subscribed'
        mqttc = self.mqtt_connect(self.host, int(self.port), 60, user, pwd)
        mqttc.subscribe(topic, 0)
        mqttc.loop(0)
        rc = 0
        while rc == 0:
            rc = mqttc.loop()
