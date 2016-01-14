Feature: IotAgent for MQTT

  Scenario: Simple meassure received

  @ft-mqtt @mqtt-measure @mqtt_sc01
  Scenario Outline: SC_1 Simple meassure received
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    When the "ORC" receive the request "SERVICE" and action "CREATE"
