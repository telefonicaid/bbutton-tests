Feature: IotAgent for MQTT

  Scenario: Simple measure received

  @ft-mqtt @mqtt-measure @mqtt_sc01 @mqtt-singlemeassure @rm-mqttdevice
  Scenario Outline: SC_1 Simple measure received
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And the "ORC" receive the request "SERVICE" and action "CREATE"
      | key                        | value        |
      | DOMAIN_NAME                | admin_domain |
      | DOMAIN_ADMIN_USER          | cloud_admin  |
      | DOMAIN_ADMIN_PASSWORD      | 4passw0rd     |
      | NEW_SERVICE_NAME           | <SERVICE>    |
      | NEW_SERVICE_DESCRIPTION    | <SERVICE>    |
      | NEW_SERVICE_ADMIN_USER     | admin_bb     |
      | NEW_SERVICE_ADMIN_PASSWORD | 4passw0rd    |
    And subservice "<SERVICEPATH>" under the service is created
      | key                        | value         |
      | SERVICE_NAME               | <SERVICE>     |
      | SERVICE_ADMIN_USER         | admin_bb      |
      | SERVICE_ADMIN_PASSWORD     | 4passw0rd     |
      | NEW_SUBSERVICE_NAME        | <SERVICEPATH> |
      | NEW_SUBSERVICE_DESCRIPTION | <SERVICEPATH> |
    And the "IOTA_MQTT" receive the request "DEVICE" and action "CREATE"
      | key               | value       |
      | device_id         | <DEVICE_ID> |
      | entity_name       | <ENT_NAME>  |
      | entity_type       | <ENT_TYPE>  |
      | attributes        | ATTS        |
      | lazy              | LAZY        |
      | commands          | COMMANDS    |
      | static_attributes | STATIC_ATTS |
    And the "ATTS" key contains these values
      | object_id | name        | type  |
      | t         | temperature | float |
      | h         | humidity    | float |
    And the "LAZY" key contains these values
      | object_id | name       | type       |
      | l         | luminosity | percentage |
    And the "COMMANDS" key contains these values
      | object_id | name | type   |
      | t         | turn | string |
    And the "STATIC_ATTS" key contains these values
      | name     | type     |
      | serialID | 02598347 |
    When I publish a MQTT message with device_id "<DEVICE_ID>", attribute "<ATT>", msg "<MSG>" and apikey "TEF"
    Then CB should have received the entity update in the entity_id "<ENT_NAME>" and entity_type "<ENT_TYPE>" with values from "<MSG>"
    And a list of services for admin_cloud is retrieved
    And a valid token is retrieved for user "admin_bb" and password "4passw0rd"
    And a list of subservices for service_admin "admin_bb" and service_pwd "4passw0rd" are retrieved
    And the "ORC" receive the request "SUBSERVICE" and action "DELETE"
    And the "ORC" receive the request "SERVICE" and action "DELETE"
    And the service "<SERVICE>" should not be listed

    Examples:
      | SERVICE     | SERVICEPATH  | DEVICE_ID | ENT_NAME  | ENT_TYPE  | ATT        | MSG         |
      | servicebbw1 | thinkinthing | devbbw1   | mqttname  | mqtttype  | attributes | {"T": 31.4} |
      | servicebbw2 | gdl          | devbbw2   | entmqtt   | typemqtt  | attributes | {"H": 200}  |
      | servicebbw3 | trace123     | devbbw3   | mqtt_name | mqtt_type | attributes | {"a": 31.4} |


  @ft-mqtt @mqtt-measure @mqtt_sc02 @mqtt_multiplemeasure @rm-mqttdevice
  Scenario Outline: SC_2 Multiple measure received
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And the "IOTA_MQTT" receive the request "DEVICE" and action "CREATE"
      | key               | value       |
      | device_id         | <DEVICE_ID> |
      | entity_name       | <ENT_NAME>  |
      | entity_type       | <ENT_TYPE>  |
      | attributes        | ATTS        |
      | lazy              | LAZY        |
      | commands          | COMMANDS    |
      | static_attributes | STATIC_ATTS |
    And the "ATTS" key contains these values
      | object_id | name        | type  |
      | t         | temperature | float |
      | h         | humidity    | float |
    And the "LAZY" key contains these values
      | object_id | name       | type       |
      | l         | luminosity | percentage |
    And the "COMMANDS" key contains these values
      | object_id | name | type   |
      | t         | turn | string |
    And the "STATIC_ATTS" key contains these values
      | name     | type     |
      | serialID | 02598347 |
    When I publish a MQTT message with device_id "<DEVICE_ID>", attribute "<ATT>", msg "<MSG>" and apikey "TEF"
    Then CB should have received the entity update in the entity_id "<ENT_NAME>" and entity_type "<ENT_TYPE>" with multiple values from "<MSG>"
    And service and subservice are deleted with "admin_bb" and "4passw0rd" credentials

    Examples:
      | SERVICE         | SERVICEPATH  | DEVICE_ID | ENT_NAME  | ENT_TYPE  | ATT        | MSG                                                       |
      | gdlservicebbw11 | gdltt1       | multibbw1 | mqttname1 | mqtttype1 | attributes | {"T": 31.4, "H":200}                                      |
      | gdlservicebbw22 | thinkinthing | multibbw2 | mqttname3 | 3mqtttype | attributes | {"NORTH": "3.0", "EAST":9.1,"HIGH":9.000001,"Z":9.999999} |


  @ft-mqtt @mqtt-measure @mqtt_sc03 @mqtt_special_values @rm-mqttdevice
  Scenario Outline: SC_3 Special measure received
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And the "IOTA_MQTT" receive the request "DEVICE" and action "CREATE"
      | key               | value       |
      | device_id         | <DEVICE_ID> |
      | entity_name       | mqttname    |
      | entity_type       | mqtttype    |
      | attributes        | ATTS        |
      | lazy              | LAZY        |
      | commands          | COMMANDS    |
      | static_attributes | STATIC_ATTS |
    And the "ATTS" key contains these values
      | object_id | name        | type  |
      | t         | temperature | float |
      | h         | humidity    | float |
    And the "LAZY" key contains these values
      | object_id | name       | type       |
      | l         | luminosity | percentage |
    And the "COMMANDS" key contains these values
      | object_id | name | type   |
      | t         | turn | string |
    And the "STATIC_ATTS" key contains these values
      | name     | type     |
      | serialID | 02598347 |
    When I publish a MQTT message with device_id "<DEVICE_ID>", attribute "attributes", msg "<MSG>" and apikey "TEF"
    Then CB should have received the entity update with multiple values from "<MSG>"
    And service and subservice are deleted with "admin_bb" and "4passw0rd" credentials

    Examples: #mcc:mnc:lac:cell-id:dbm or #volt,stat,charger,charging,Mode,Desc
      | SERVICE     | SERVICEPATH | DEVICE_ID   | MSG                                                                                                  |
      | servespbbw1 | achar1a     | devspecbbw1 | {"tt":"20160122T121208Z","L":4,"T": 30.2,"H":30,"G":0,"M":3784,"V":"L","C1":"00D600070B000D22"}      |
      | servespbbw2 | char1a      | devspecbbw2 | {"tt":"20160122T121208Z","L":4,"T": 31.2,"H":30,"G":0,"M":3784,"V":"L","C1":"AAAABBBBCCCCDDDD"}      |
      | servespbbw3 | char2a      | devspepbbw3 | {"tt":"20160122T121208Z","L":4,"T": 33.2,"H":31,"G":0,"M":3784,"V":"L","P1":"214,7,d22,b00,-64,"}    |
      | servespbbw4 | char2a      | devspepbbw4 | {"tt":"20160122T121208Z","L":4,"T": 34.2,"H":200,"G":0,"M":3784,"V":"L","P1":"999,888,777,666,-55,"} |
      | servespbbw5 | char3a      | devspebbbw5 | {"tt":"20160122T121208Z","L":4,"T": 35.2,"H":10,"G":0,"M":3784,"V":"L","B":"4.70,1,1,1,1,0,"}        |
      | servespbbw6 | char3a      | devspebbbw6 | {"tt":"20160122T121208Z","L":4,"T": 36.2,"H":99,"G":0,"M":3784,"V":"L","B":"0.01,0,0,0,0,0,"}        |

  @ft-mqtt @mqtt-measure @mqtt_sc04 @mqtt-permanent-service
  Scenario Outline: SC_4 Permanent device receive a measure
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
#    And a service and subservice are provisioned
#    And the "IOTA_MQTT" receive the request "DEVICE" and action "CREATE"
#      | key               | value       |
#      | device_id         | <DEVICE_ID> |
#      | entity_name       | mqttname    |
#      | entity_type       | mqtttype    |
#      | attributes        | ATTS        |
#      | lazy              | LAZY        |
#      | commands          | COMMANDS    |
#      | static_attributes | STATIC_ATTS |
#    And the "ATTS" key contains these values
#      | object_id | name        | type  |
#      | t         | temperature | float |
#      | h         | humidity    | float |
#    And the "LAZY" key contains these values
#      | object_id | name       | type       |
#      | l         | luminosity | percentage |
#    And the "COMMANDS" key contains these values
#      | object_id | name | type   |
#      | t         | turn | string |
#    And the "STATIC_ATTS" key contains these values
#      | name     | type     |
#      | serialID | 02598347 |
    When I publish a MQTT message with device_id "<DEVICE_ID>", attribute "attributes", msg "<MSG>" and apikey "TEF"
    Then CB should have received the entity update with multiple values from "<MSG>"

    Examples:
      | SERVICE | SERVICEPATH | DEVICE_ID       | MSG                                                                                             |
      | service | permanent     | devicepermanent | {"tt":"20160119T020426Z","L":4,"T": 24.1,"H":41,"G":0,"M":3811,"V":"N","C1":"00D600070B000D22"}      |

