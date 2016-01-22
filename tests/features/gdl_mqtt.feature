Feature: IotAgent for MQTT

  Scenario: Simple meassure received

  @ft-mqtt @mqtt-measure @mqtt_sc01
  Scenario Outline: SC_1 Simple measure received
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And the "IOTA_MQTT" receive the request "DEVICE" and action "CREATE"
      | key               | value       |
      | device_id         | <DEVICE_ID> |
      | entity_name       | entmqtt     |
      | entity_type       | typemqtt    |
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
    When I publish a MQTT message with device_id "<DEVICE_ID>", attribute "<ATT>" msg "<MSG>" and apikey "<APIKEY>"



    Examples:
      | SERVICE     | SERVICEPATH  | DEVICE_ID | ATT        | MSG  | APIKEY |
      | servicezzw1 | thinkinthing | x001       | attributes | {"T": 31.4}| 1234   |

  @ft-mqtt @mqtt-measure @mqtt_sc02
  Scenario Outline: Send one measure
    Given a Service with name "<service>" and protocol "<protocol>" created
    When I publish a MQTT message with device_id "<device_id>", alias "<alias>" and payload "<value>"
    And I Wait some time
    Then the measure of asset "<device_id>" with measures "<generated_measures>" is received by context broker

    Examples:
      | phenomenon          | service     | protocol | type     | device_id | alias | value     | generated_measures |
      | temperature         | servicemqtt | IoTMqtt  | Quantity | mqtt10    | t     | 35        | <alias>:<value>    |
      | presence            | servicemqtt | IoTMqtt  | Boolean  | mqtt11    | p     | false     | <alias>:<value>    |
      | location            | servicemqtt | IoTMqtt  | Location | mqtt12    | l     | 125.9,3.1 | <alias>:<value>    |
      | alarm               | servicemqtt | IoTMqtt  | Text     | mqtt13    | a     | Danger    | <alias>:<value>    |
      | temperaturainterior | servicemqtt | IoTMqtt  | Quantity | mqtt14    | tint  | -2.5      | <alias>:<value>    |
