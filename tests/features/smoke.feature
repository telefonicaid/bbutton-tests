Feature: Black Button Smoke tests
  In order to validate the proper status of the components
  As a Black button checker
  I should check if the components are working properly


 # TO CHECK
 # IOTAM  'iotagent_manager'   8081
 # IOTA   'iotagent'           4041
 # CB     'contextBroker'      10026
 # ORC    'orchestrator'       8084
 # KS     'openstack-keystone' 5001

 # 'pepProxyPerseo'
 # 'pepProxyOrion'
 # 'sth'                8666
 # 'portal'             8008
 # 'keypass'            7070


  @ready @ft-smoke @smoke01 @check_uprunning
  Scenario Outline: SM_01 Instances are UP&Running
    Given the instance of "<INSTANCE>" is accessible
    When I send a request "<REQUEST>" to URI "<URI>"
    Then the result should be "<HTTP_RESPONSE>"

    Examples:
      | INSTANCE | REQUEST | URI        | HTTP_RESPONSE |
      | IOTA     | PING    | /iot/about | 200           |
      | IOTM     | PING    | /iot/about | 200           |
      | CB       | PING    | /version   | 200           |
      | ORC      | PING    | /          | 404           |
      | KS       | GET     | /version   | 404           |
    # | CA       | GET     | /version   | x                     |



  @ready @ft-smoke @smoke02 @check_version
  Scenario Outline: SM_02 Instances are running the proper VERSION
    Given the instance of "<INSTANCE>" is accessible
    When I send a request "<REQUEST>" to URI "<URI>"
    Then the returned version from "<INSTANCE>" should match the "<VERSION>"

    Examples:
      | INSTANCE | REQUEST | URI        | VERSION               |
      | CB       | GET     | /version   | 0.24.0 |
    #  | IOTA     | GET     | /iot/about | 0.7.0-next            |
      | IOTM     | GET     | /iot/about | 1.0.1                 |
    # | CA       | GET     | /version   | x                     |
    # | ORC      | GET     | /version   | N/A                   |


  @ready @ft-smoke @smoke04 @check_funcionality
  Scenario Outline: SM_03 Instances are WORKING
    Given the instance of "<INSTANCE>" is accessible
    And service "blackbutton" and subservice "/telepizza"
    And user "admin_bb" and password "4passw0rd"
    When I send a request type "<REQUEST>" and action "<ACTION>"
    Then the result should be "<HTTP_RESPONSE>"

    Examples:
      | INSTANCE | REQUEST   | ACTION | HTTP_RESPONSE |
      | CB       | ENTITY    | CREATE | 200           |
      | CB       | ENTITY    | GET    | 200           |
      | KS       | TOKEN     | GET    | 201           |
    #  | IOTA     | SERVICES  | GET    | 200           |
      | IOTM     | PROTOCOLS | GET    | 200           |
    # | ORC      | USER      | GET    | x             |
    # | CA       | NOTIFY    | GET    | x             |

