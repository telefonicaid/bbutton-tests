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
      | static_attributes | STATIC_ATTS  |
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

    Examples:
      | SERVICE     | SERVICEPATH  | DEVICE_ID |
      | servicezzq1 | thinkinthing | aaa111    |
