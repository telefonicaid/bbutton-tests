Feature: IotAgent for MQTT

  Scenario: Simple meassure received

  @ft-mqtt @mqtt-measure @mqtt_sc01
  Scenario Outline: SC_1 Simple meassure received
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    When the "ORC" receive the request "SERVICE" and action "CREATE"

    Examples:
      | SERVICE     | SERVICEPATH  | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID | ATT_INTERACTION_TYPE | TP_INTERACTION | TP_URL          |
      | servicezzq1 | thinkinthing | admin_bb      | 4passw0rd   | SSzzq1011 | synchronous          | synchronous    | TP/sync/request |
      | servicezzq2 | thinkinthing | admin_bb      | 4passw0rd   | SAzzq1022 | synchronous          | asynchronous   | TP/async/create |
