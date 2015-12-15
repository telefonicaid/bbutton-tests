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
      | INSTANCE | REQUEST | URI           | HTTP_RESPONSE |
      | CB       | PING    | /version      | 200           |
      | CA       | GET     | /version      | 200           |
      | IOTA     | PING    | /iot/about    | 200           |
      | IOTM     | PING    | /iot/about    | 200           |
      | ORC      | PING    | /v1.0/version | 200           |
      | KS       | GET     | /version      | 404           |
      | TP       | GET     | /sync/request | 405           |
      | STH      | GET     | /version      | 200           |
      | CYGNUS   | GET     | /version      | 200           |
      | PEP      | GET     | /version      | 200           |


  @ready @ft-smoke @smoke02 @check_version
  Scenario Outline: SM_02 Instances are running the proper VERSION
    Given the instance of "<INSTANCE>" is accessible
    When I send a request "<REQUEST>" to URI "<URI>"
    Then the returned version from "<INSTANCE>" should match the "<VERSION>"

    Examples:
      | INSTANCE | REQUEST | URI           | VERSION                                         |
      | CB       | GET     | /version      | 0.26.0                                          |
      | IOTM     | GET     | /iot/about    | 1.2.1                                           |
      | IOTA     | GET     | /iot/about    | 0.5.3                                           |
      | IOTA_LIB | GET     | /iot/about    | 0.8.4                                           |
      | CA       | GET     | /version      | 0.1.4                                           |
      | ORC      | GET     | /v1.0/version | 0.6.2                                          |
      | STH      | GET     | /version      | 0.3.1                                           |
      | PEP      | GET     | /version      | 0.7.1                                           |
      | CYGNUS   | GET     | /version      | 0.11.0.2a9c87fb7fd6156225e2eed7fbc9792f1d9c5dfe |


  @ready @ft-smoke @smoke04 @check_funcionality
  Scenario Outline: SM_03 Instances are WORKING
    Given the instance of "<INSTANCE>" is accessible
    And a Client of "blackbutton01" and a ThirdParty called "testpizza"
    And user "admin_bb" and password "4passw0rd"
    When I send a request type "<REQUEST>" and action "<ACTION>"
    Then the result should be "<HTTP_RESPONSE>"

    Examples:
      | INSTANCE | REQUEST | ACTION | HTTP_RESPONSE |
      | CB       | ENTITY  | CREATE | 200           |
      | CB       | ENTITY  | GET    | 200           |
    #  | KS       | TOKEN     | GET    | 201         |
    #  | IOTM     | PROTOCOLS | GET    | 200         |
    #  | IOTA     | SERVICES  | GET    | 200         |
    #  | ORC      | USER      | GET    | 200         |
    #  | CA       | NOTIFY    | GET    | 200         |
    #  | STH       | STHQUERY    | GET    | 200         |



