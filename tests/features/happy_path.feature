Feature: Happy path E2E functionality Sync-Async
  In order to check if a blackbutton that can order a product
  In a Service servicexyz and Subservice testpizza
  As a client has ASYNC BlackButtons: idbutt123_aa_01 and idbutt123_as_02
  As a client has SYNC  BlackButtons: idbutt123_sa_03 and idbutt123_ss_04
  I should validate the ability of the platform to process the buttons requests to a third party


  @ft-happypath @hp-provision
  Scenario Outline: SC_1 Service and BlackButton get provisioned in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    When the "ORC" receive the request "SERVICE" and action "CREATE"
      | KEYSTONE_PROTOCOL          | http            |
      | KEYSTONE_HOST              | localhost       |
      | KEYSTONE_PORT              | 5000            |
      | DOMAIN_NAME                | admin_domain    |
      | DOMAIN_ADMIN_USER          | cloud_admin     |
      | DOMAIN_ADMIN_PASSWORD      | password        |
      | NEW_SERVICE_NAME           | <SERVICE>       |
      | NEW_SERVICE_DESCRIPTION    | <SERVICE>       |
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
      | NEW_SUBSERVICE_DESCRIPTION | <SERVICEPATH>   |
    And the "ORC" receive the request "SERVICE_ENTITY" and action "CREATE"
      | SERVICE_NAME          | <SERVICE>         |
      | SERVICE_USER_NAME     | admin_bb          |
      | SERVICE_USER_PASSWORD | 4passw0rd         |
      | SUBSERVICE_NAME       | <SERVICEPATH>     |
      | ENTITY_TYPE           | service           |
      | ENTITY_ID             | <SERVICE>         |
      | SERVICE_NAME          | <SERVICE>         |
      | ATT_NAME              | <SERVICEPATH>     |
      | ATT_PROVIDER          | QA Testpizza CORP |
      | PROTOCOL              | TT_BLACKBUTTON    |
      | ATT_ENDPOINT          | <TP_URL>          |
      | ATT_METHOD            | POST              |
      | ATT_AUTHENTICATION    | context-adapter   |
      | ATT_MAPPING           | []                |
      | ATT_INTERACTION_TYPE  | <TP_INTERACTION>  |
      | ATT_TIMEOUT           | 120               |
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
      | ATT_CCID               | AAA                    |
      | ATT_IMEI               | 1234567890             |
      | ATT_IMSI               | 0987654321             |
      | ATT_INTERACTION_TYPE   | <ATT_INTERACTION_TYPE> |
      | ATT_SERVICE_ID         | <SERVICE>              |
      | ATT_GEOLOCATION        | 40.4188,-3.6919        |
      | IOTA_PROTOCOL          | http                   |
      | IOTA_HOST              | localhost              |
      | IOTA_PORT              | 4041                   |
      | ORION_PROTOCOL         | http                   |
      | ORION_HOST             | localhost              |
      | ORION_PORT             | 10026                  |

    Examples:
      | SERVICE   | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID      | ATT_INTERACTION_TYPE | TP_INTERACTION | TP_URL          |
      | servicexyz01 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_aa_0101 | asynchronous         | asynchronous   | TP/async/create |
      | servicexyz02 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_as_0102 | asynchronous         | synchronous    | TP/sync/request |
      | servicexyz03 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_sa_0103 | synchronous          | asynchronous   | TP/async/create |
      | servicexyz04 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_ss_0104 | synchronous          | synchronous    | TP/sync/request |

  @ft-happypath @hp-provision-check
  Scenario Outline: SC_2 User check a BlackButton is registered in BB-platform
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    Then device "<DEVICE_ID>" should be listed under service and subservice

    Examples:
      | SERVICE   | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID      |
      | servicexyz01 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_aa_0101 |
      | servicexyz02 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_as_0102 |
      | servicexyz03 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_sa_0103 |
      | servicexyz04 | testpizza   | admin_bb      | 4passw0rd   | idbutt123_ss_0104 |


  @ft-happypath @hp-button-flows @hp-async-flow
  Scenario Outline: SC_3 Client push the button in the ASYNC mode
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    And a idbutt123_request "<BT_REQUEST>" for mode "<SYNC_MODE>"
    When the button "<DEVICE_ID>" is pressed in mode "<SYNC_MODE>" the IOTA should receive the request
    Then the button "<DEVICE_ID>" is pulling every "1" seconds during "10" times or until the IOTA request returns status "<STATUS>"
    And the button "<DEVICE_ID>" close the request and receive the final status "<FINAL_STATUS>"


    Examples:
      | SERVICE   | SERVICEPATH | DEVICE_ID      | SYNC_MODE    | BT_REQUEST                        | STATUS | STATUS |
      | servicexyz01 | testpizza   | idbutt123_aa_0101 | asynchronous | #1,BT,C,1,1,2000$WakeUp,#0,K1,30$ | C.S    | X      |
      | servicexyz02 | testpizza   | idbutt123_as_0102 | asynchronous | #1,BT,C,3,2,2000$WakeUp,#0,K1,30$ | C.S    | X      |


  @ft-happypath  @hp-buttons-flows @hp-sync-flow
  Scenario Outline: SC_4 Client push the button in the SYNC mode
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    And a idbutt123_request "<BT_REQUEST>" for mode "<SYNC_MODE>"
    When the button "<DEVICE_ID>" is pressed in mode "<SYNC_MODE>" the IOTA should receive the request
    And the ThirdParty "<TP_NAME>" changed the status to "<OP_RESULT>"

    Examples:
      | SERVICE   | SERVICEPATH | DEVICE_ID      | SYNC_MODE   | BT_REQUEST                        | TP_NAME | OP_RESULT           |
      | servicexyz03 | testpizza   | idbutt123_sa_0103 | synchronous | #1,BT,S,2,1,2000$WakeUp,#0,K1,30$ | TP      | rgb-66CCDD%3Bt-2%3B |
      | servicexyz04 | testpizza   | idbutt123_ss_0104 | synchronous | #3,BT,S,3,2,2000$WakeUp,#0,K1,30$ | TP      | rgb-66CCDD%3Bt-2%3B |