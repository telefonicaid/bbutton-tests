Feature: Happy path E2E functionality Sync-Async
  In order to check if a blackbutton that can order a product
  As a client has ASYNC BlackButton for service blueasync3 and subservice testpizza and button_id blue_as_3
  As a client has SYNC  BlackButton for service redsync3 and subservice testpizza and button_id red_ss_3
  I should receive my product after order it

  @ft-blackbutton_as @provision_01_as @skip
  Scenario Outline: SC_1 Service get provisioned in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    When the "<INSTANCE>" receive the request "<REQUEST>" and action "<ACTION>"
      | KEYSTONE_PROTOCOL          | http            |
      | KEYSTONE_HOST              | localhost       |
      | KEYSTONE_PORT              | 5000            |
      | DOMAIN_NAME                | admin_domain    |
      | DOMAIN_ADMIN_USER          | cloud_admin     |
      | DOMAIN_ADMIN_PASSWORD      | password        |
      | NEW_SERVICE_NAME           | <SERVICE>       |
      | NEW_SERVICE_DESCRIPTION    | Service_desc    |
      | NEW_SERVICE_ADMIN_USER     | <SERVICE_ADMIN> |
      | NEW_SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>   |
      | KEYPASS_PROTOCOL           | http            |
      | KEYPASS_HOST               | localhost       |
      | KEYPASS_PORT               | 8080            |
    Then subservice "<SERVICEPATH>" under the service is created
      | KEYSTONE_PROTOCOL          | http            |
      | KEYSTONE_HOST              | localhost       |
      | KEYSTONE_PORT              | 5000            |
      | SERVICE_NAME               | <SERVICE>       |
      | SERVICE_ADMIN_USER         | <SERVICE_ADMIN> |
      | SERVICE_ADMIN_PASSWORD     | <SERVICE_PWD>   |
      | NEW_SUBSERVICE_NAME        | <SERVICEPATH>   |
      | NEW_SUBSERVICE_DESCRIPTION | New subservice  |
    And device should get registered under service and subservice
      | KEYSTONE_PROTOCOL      | http                   |
      | KEYSTONE_HOST          | localhost              |
      | KEYSTONE_PORT          | 5000                   |
      | SERVICE_NAME           | <SERVICE>              |
      | SUBSERVICE_NAME        | <SERVICEPATH>          |
      | SERVICE_ADMIN_USER     | <SERVICE_ADMIN>        |
      | SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>          |
      | SERVICE_USER_NAME      | <SERVICE_ADMIN>        |
      | SERVICE_USER_PASSWORD  | <SERVICE_PWD>          |
      | DEVICE_ID              | <DEVICE_ID>            |
      | PROTOCOL               | TT_BLACKBUTTON         |
      | ENTITY_TYPE            | BlackButton            |
      | ATT_INTERNAL_ID        | <DEVICE_ID>            |
      | ATT_EXTERNAL_ID        | ZZZZ                   |
      | ATT_CCID               | AAA                    |
      | ATT_IMEI               | 1234567890             |
      | ATT_IMSI               | 0987654321             |
      | ATT_INTERACTION_TYPE   | <ATT_INTERACTION_TYPE> |
      | ATT_SERVICE_ID         | S-001                  |
      | ATT_GEOLOCATION        | 40.4188,-3.6919        |
      | IOTA_PROTOCOL          | http                   |
      | IOTA_HOST              | localhost              |
      | IOTA_PORT              | 4041                   |
      | ORION_PROTOCOL         | http                   |
      | ORION_HOST             | localhost              |
      | ORION_PORT             | 10026                  |

    Examples:
      | SERVICE    | SERVICEPATH | INSTANCE | REQUEST | ACTION | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID   | ATT_INTERACTION_TYPE |
      | blueasync3 | testpizza   | ORC      | SERVICE | CREATE | admin_bb      | 4passw0rd   | blue_as_300 | asynchronous         |

  @ft-blackbutton_ss @provision_01_ss @skip
  Scenario Outline: SC_1 Service get provisioned in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    When the "<INSTANCE>" receive the request "<REQUEST>" and action "<ACTION>"
      | KEYSTONE_PROTOCOL          | http            |
      | KEYSTONE_HOST              | localhost       |
      | KEYSTONE_PORT              | 5000            |
      | DOMAIN_NAME                | admin_domain    |
      | DOMAIN_ADMIN_USER          | cloud_admin     |
      | DOMAIN_ADMIN_PASSWORD      | password        |
      | NEW_SERVICE_NAME           | <SERVICE>       |
      | NEW_SERVICE_DESCRIPTION    | Service_desc    |
      | NEW_SERVICE_ADMIN_USER     | <SERVICE_ADMIN> |
      | NEW_SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>   |
      | KEYPASS_PROTOCOL           | http            |
      | KEYPASS_HOST               | localhost       |
      | KEYPASS_PORT               | 8080            |
    Then subservice "<SERVICEPATH>" under the service is created
      | KEYSTONE_PROTOCOL          | http            |
      | KEYSTONE_HOST              | localhost       |
      | KEYSTONE_PORT              | 5000            |
      | SERVICE_NAME               | <SERVICE>       |
      | SERVICE_ADMIN_USER         | <SERVICE_ADMIN> |
      | SERVICE_ADMIN_PASSWORD     | <SERVICE_PWD>   |
      | NEW_SUBSERVICE_NAME        | <SERVICEPATH>   |
      | NEW_SUBSERVICE_DESCRIPTION | New subservice  |
    And device should get registered under service and subservice
      | KEYSTONE_PROTOCOL      | http                   |
      | KEYSTONE_HOST          | localhost              |
      | KEYSTONE_PORT          | 5000                   |
      | SERVICE_NAME           | <SERVICE>              |
      | SUBSERVICE_NAME        | <SERVICEPATH>          |
      | SERVICE_ADMIN_USER     | <SERVICE_ADMIN>        |
      | SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>          |
      | SERVICE_USER_NAME      | <SERVICE_ADMIN>        |
      | SERVICE_USER_PASSWORD  | <SERVICE_PWD>          |
      | DEVICE_ID              | <DEVICE_ID>            |
      | PROTOCOL               | TT_BLACKBUTTON         |
      | ENTITY_TYPE            | BlackButton            |
      | ATT_INTERNAL_ID        | <DEVICE_ID>            |
      | ATT_EXTERNAL_ID        | ZZZZ                   |
      | ATT_CCID               | AAA                    |
      | ATT_IMEI               | 1234567890             |
      | ATT_IMSI               | 0987654321             |
      | ATT_INTERACTION_TYPE   | <ATT_INTERACTION_TYPE> |
      | ATT_SERVICE_ID         | S-001                  |
      | ATT_GEOLOCATION        | 40.4188,-3.6919        |
      | IOTA_PROTOCOL          | http                   |
      | IOTA_HOST              | localhost              |
      | IOTA_PORT              | 4041                   |
      | ORION_PROTOCOL         | http                   |
      | ORION_HOST             | localhost              |
      | ORION_PORT             | 10026                  |

    Examples:
      | SERVICE  | SERVICEPATH | INSTANCE | REQUEST | ACTION | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID  | ATT_INTERACTION_TYPE |
      | redsync3 | testpizza   | ORC      | SERVICE | CREATE | admin_bb      | 4passw0rd   | red_ss_300 | synchronous          |

  @ft-blackbutton_as @provision_02_as
  Scenario Outline: SC_2 User add a BlackButton registered in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    And with a service id "<SERVICE_ID>" and subservice id "<SUBSERVICE_ID>"
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    Then device should get registered under service and subservice
      | KEYSTONE_PROTOCOL      | http                   |
      | KEYSTONE_HOST          | localhost              |
      | KEYSTONE_PORT          | 5000                   |
      | SERVICE_NAME           | <SERVICE>              |
      | SUBSERVICE_NAME        | <SERVICEPATH>          |
      | SERVICE_ADMIN_USER     | <SERVICE_ADMIN>        |
      | SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>          |
      | SERVICE_USER_NAME      | <SERVICE_ADMIN>        |
      | SERVICE_USER_PASSWORD  | <SERVICE_PWD>          |
      | DEVICE_ID              | <DEVICE_ID>            |
      | PROTOCOL               | TT_BLACKBUTTON         |
      | ENTITY_TYPE            | BlackButton            |
      | ATT_INTERNAL_ID        | <DEVICE_ID>            |
      | ATT_EXTERNAL_ID        | ZZZZ                   |
      | ATT_CCID               | AAA                    |
      | ATT_IMEI               | 1234567890             |
      | ATT_IMSI               | 0987654321             |
      | ATT_INTERACTION_TYPE   | <ATT_INTERACTION_TYPE> |
      | ATT_SERVICE_ID         | S-001                  |
      | ATT_GEOLOCATION        | 40.4188,-3.6919        |
      | IOTA_PROTOCOL          | http                   |
      | IOTA_HOST              | localhost              |
      | IOTA_PORT              | 4041                   |
      | ORION_PROTOCOL         | http                   |
      | ORION_HOST             | localhost              |
      | ORION_PORT             | 10026                  |
    Then device "<DEVICE_ID>" should be listed under service and subservice

    Examples:
      | SERVICE    | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID   | SERVICE_ID                       | SUBSERVICE_ID                    | ATT_INTERACTION_TYPE |
      | blueasync3 | testpizza   | admin_bb      | 4passw0rd   | blue_as_301 | 856ff4c399be43109acc0bcd0490d2ae | f685cd1f10e546ad9dbc7c53c0d05baa | asynchronous         |
      | blueasync3 | testpizza   | admin_bb      | 4passw0rd   | blue_as_302 | 856ff4c399be43109acc0bcd0490d2ae | f685cd1f10e546ad9dbc7c53c0d05baa | asynchronous         |
      #| blueasync3 | testpizza   | admin_bb      | 4passw0rd   | blue_as_303 | 856ff4c399be43109acc0bcd0490d2ae | f685cd1f10e546ad9dbc7c53c0d05baa | asynchronous         |
      | redsync3   | testpizza   | admin_bb      | 4passw0rd   | red_ss_301  | 863ad0c4b6664de0937dc05605653209 | 0ce4297d4c784c89b67fc10aa0a1c7e6 | synchronous          |
      | redsync3   | testpizza   | admin_bb      | 4passw0rd   | red_ss_302  | 863ad0c4b6664de0937dc05605653209 | 0ce4297d4c784c89b67fc10aa0a1c7e6 | synchronous          |
      #| redsync3 | testpizza   | admin_bb      | 4passw0rd   | red_ss_303 | 863ad0c4b6664de0937dc05605653209 | d2eb580178774f3c90d8170d0218d16d | synchronous         |


  @ft-blackbutton_as @provision_check_as @daily
  Scenario Outline: SC_3 User check a BlackButton is registered in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    Then device "<DEVICE_ID>" should be listed under service and subservice

    Examples:
      | SERVICE    | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID   |
      | blueasync3 | testpizza   | admin_bb      | 4passw0rd   | blue_as_301 |
      | blueasync3 | testpizza   | admin_bb      | 4passw0rd   | blue_as_302 |
      | redsync3   | testpizza   | admin_bb      | 4passw0rd   | red_ss_301  |
      | redsync3   | testpizza   | admin_bb      | 4passw0rd   | red_ss_302  |

  @ft-blackbutton_as @async_flow_as
  Scenario Outline: SC_4 Client push the button in the ASYNC mode
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    When the button "<DEVICE_ID>" is pressed in mode "<SYNC_MODE>" the IOTA should receive the request
    And the ThirdParty "<THIRDPARTY>" change the status to "<STATUS>"
    Then the button "<DEVICE_ID>" is pulling every "1" seconds during "10" times or until the IOTA request returns status "<STATUS>"

    Examples:
      | SERVICE    | SERVICEPATH | DEVICE_ID   | SYNC_MODE    | THIRDPARTY | STATUS    |
    #  | blueasync3 | testpizza   | blue_as_301 | asynchronous | X          | COMPLETED |
      | blueasync3 | testpizza   | blue_as_302 | asynchronous | X          | COMPLETED |

# ###########################################################################
  # SYNC-SYNC


  @ft-blackbutton_ss @provision_02_ss
  Scenario Outline: SC_2 User add a BlackButton registered in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    And with a service id "<SERVICE_ID>" and subservice id "<SUBSERVICE_ID>"
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    Then device should get registered under service and subservice
      | KEYSTONE_PROTOCOL      | http                   |
      | KEYSTONE_HOST          | localhost              |
      | KEYSTONE_PORT          | 5000                   |
      | SERVICE_NAME           | <SERVICE>              |
      | SUBSERVICE_NAME        | <SERVICEPATH>          |
      | SERVICE_ADMIN_USER     | <SERVICE_ADMIN>        |
      | SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>          |
      | SERVICE_USER_NAME      | <SERVICE_ADMIN>        |
      | SERVICE_USER_PASSWORD  | <SERVICE_PWD>          |
      | DEVICE_ID              | <DEVICE_ID>            |
      | PROTOCOL               | TT_BLACKBUTTON         |
      | ENTITY_TYPE            | BlackButton            |
      | ATT_INTERNAL_ID        | <DEVICE_ID>            |
      | ATT_EXTERNAL_ID        | ZZZZ                   |
      | ATT_CCID               | AAA                    |
      | ATT_IMEI               | 1234567890             |
      | ATT_IMSI               | 0987654321             |
      | ATT_INTERACTION_TYPE   | <ATT_INTERACTION_TYPE> |
      | ATT_SERVICE_ID         | S-001                  |
      | ATT_GEOLOCATION        | 40.4188,-3.6919        |
      | IOTA_PROTOCOL          | http                   |
      | IOTA_HOST              | localhost              |
      | IOTA_PORT              | 4041                   |
      | ORION_PROTOCOL         | http                   |
      | ORION_HOST             | localhost              |
      | ORION_PORT             | 10026                  |
    Then device "<DEVICE_ID>" should be listed under service and subservice

    Examples:
      | SERVICE  | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID  | SERVICE_ID                       | SUBSERVICE_ID                    | ATT_INTERACTION_TYPE |
      | redsync3 | testpizza   | admin_bb      | 4passw0rd   | red_ss_301 | 863ad0c4b6664de0937dc05605653209 | 0ce4297d4c784c89b67fc10aa0a1c7e6 | synchronous          |
      | redsync3 | testpizza   | admin_bb      | 4passw0rd   | red_ss_302 | 863ad0c4b6664de0937dc05605653209 | 0ce4297d4c784c89b67fc10aa0a1c7e6 | synchronous          |
      #| redsync3 | testpizza   | admin_bb      | 4passw0rd   | red_ss_303 | 863ad0c4b6664de0937dc05605653209 | d2eb580178774f3c90d8170d0218d16d | synchronous         |

  @ft-blackbutton_ss @provision_check_ss @daily
  Scenario Outline: SC_3 User check a BlackButton is registered in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    Then device "<DEVICE_ID>" should be listed under service and subservice

    Examples:
      | SERVICE  | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID  |
      | redsync3 | testpizza   | admin_bb      | 4passw0rd   | red_ss_302 |


  @ft-blackbutton_ss @sync_flow_ss
  Scenario Outline: SC_4 Client push the button in the SYNC mode
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    When the button "<DEVICE_ID>" is pressed in mode "<SYNC_MODE>" the IOTA should receive the request
    And the ThirdParty "<THIRDPARTY>" change the status to "<STATUS>"
    Then the button "<DEVICE_ID>" should have received the final status "<TP_RETURN>"
    #And the CB should have been notified

    Examples:
      | SERVICE  | SERVICEPATH | DEVICE_ID  | SYNC_MODE   | THIRDPARTY | STATUS    | TP_RETURN           |
    #  | redsync3 | testpizza   | red_ss_301 | synchronous | X          | COMPLETED | RESULT_FOR_action-1 |
      | redsync3 | testpizza   | red_ss_302 | synchronous | X          | COMPLETED | RESULT_FOR_action-1 |
