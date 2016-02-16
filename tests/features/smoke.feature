Feature: Black Button Smoke tests
  In order to validate the proper status of the components
  As a Black button platform backend checker
  I should check if the components are working properly


  @ready @ft-smoke @smoke01 @check_uprunning
  Scenario Outline: SM_01 Instances are UP&Running
    Given the instance of "<INSTANCE>" is accessible
    When I send a request "<REQUEST>" to URI "<URI>"
    Then the result should be "<HTTP_RESPONSE>"

    Examples:
      | INSTANCE  | REQUEST   | URI           | HTTP_RESPONSE |
      | CB        | HEARTBEAT | /version      | 200           |
      | CA        | HEARTBEAT | /version      | 200           |
      | IOTA      | HEARTBEAT | /iot/about    | 200           |
      | IOTM      | HEARTBEAT | /iot/about    | 200           |
      | IOTA_MQTT | HEARTBEAT | /iot/about    | 200           |
      | ORC       | HEARTBEAT | /v1.0/version | 200           |
      | KS        | HEARTBEAT | /version      | 404           |
      | TP        | HEARTBEAT | /sync/request | 405           |
      | STH       | HEARTBEAT | /version      | 200           |
      | CYGNUS    | HEARTBEAT | /version      | 200           |
      | PEP       | HEARTBEAT | /version      | 200           |


  @ready @ft-smoke @smoke02 @check_version
  Scenario Outline: SM_02 Instances are running the proper VERSION
    Given the instance of "<INSTANCE>" is accessible
    When I send a request "<REQUEST>" to URI "<URI>"
    Then the returned version from "<INSTANCE>" should match the "<VERSION>"

    Examples:
      | INSTANCE  | REQUEST | URI           | VERSION                                         |
      | CB        | VERSION | /version      | 0.26.1                                          |
      | IOTM      | VERSION | /iot/about    | 1.2.1                                           |
      | IOTA      | VERSION | /iot/about    | 0.5.5                                           |
      | IOTA_MQTT | VERSION | /iot/about    | 0.1.5                                           |
      | IOTA_LIB  | VERSION | /iot/about    | 0.9.5                                           |
      | CA        | VERSION | /version      | 0.3.0                                           |
      | ORC       | VERSION | /v1.0/version | 0.6.10                                           |
      | STH       | VERSION | /version      | 0.6.0                                           |
      | PEP       | VERSION | /version      | 0.7.2                                           |
      | CYGNUS    | VERSION | /version      | 0.11.0.2a9c87fb7fd6156225e2eed7fbc9792f1d9c5dfe |

  @ready @ft-smoke @smoke03 @check_funcionality
  Scenario Outline: SM_03 Instances are WORKING
    Given the instance of "<INSTANCE>" is accessible
    And a Client of "blackbutton01" and a ThirdParty called "testpizza"
    And user "admin_bb" and password "4pass1w0rd"
    When I send a request type "<REQUEST>" and action "<ACTION>"
    Then the result should be "<HTTP_RESPONSE>"

    Examples:
      | INSTANCE | REQUEST | ACTION | HTTP_RESPONSE |
    #  | CB       | ENTITY  | CREATE | 200           |
    #  | CB       | ENTITY  | GET    | 200           |
    #  | KS       | TOKEN     | GET    | 201         |
    #  | IOTM     | PROTOCOLS | GET    | 200         |
    #  | IOTA     | SERVICES  | GET    | 200         |
    #  | ORC      | USER      | GET    | 200         |
    #  | CA       | NOTIFY    | GET    | 200         |
    #  | STH       | STHQUERY    | GET    | 200         |



