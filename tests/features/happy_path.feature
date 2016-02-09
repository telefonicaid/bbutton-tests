Feature: Happy path E2E functionality Sync-Async
  In order to check if a blackbutton that can order a product
  In a Service serviceqql and Subservice thinkinthing
  As a client has SYNC  BlackButtons: SSqql1011 and SAqql1022
  As a client has ASYNC BlackButtons: ASqql1033 and SSqql1044
  I should validate the lity of the platform to process the buttons requests to a third party


  @ft-happypath @hp-provision @hp_sc01
  Scenario Outline: SC_1 Service and BlackButton get provisioned in BB-platform
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    When the "ORC" receive the request "SERVICE" and action "CREATE"
      | att                        | value           |
      | DOMAIN_NAME                | admin_domain    |
      | DOMAIN_ADMIN_USER          | cloud_admin     |
      | DOMAIN_ADMIN_PASSWORD      | password        |
      | NEW_SERVICE_NAME           | <SERVICE>       |
      | NEW_SERVICE_DESCRIPTION    | <SERVICE>       |
      | NEW_SERVICE_ADMIN_USER     | <SERVICE_ADMIN> |
      | NEW_SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>   |
    Then subservice "<SERVICEPATH>" under the service is created
      | att                        | value           |
      | SERVICE_NAME               | <SERVICE>       |
      | SERVICE_ADMIN_USER         | <SERVICE_ADMIN> |
      | SERVICE_ADMIN_PASSWORD     | <SERVICE_PWD>   |
      | NEW_SUBSERVICE_NAME        | <SERVICEPATH>   |
      | NEW_SUBSERVICE_DESCRIPTION | <SERVICEPATH>   |
    And the "ORC" receive the request "SERVICE_ENTITY" and action "CREATE"
      | att                   | value             |
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
      | att                    | value                  |
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

    Examples:
      | SERVICE     | SERVICEPATH  | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID | ATT_INTERACTION_TYPE | TP_INTERACTION | TP_URL          |
      | serviceqql1 | thinkinthing | admin_bb      | 4passw0rd   | SSqql1011 | synchronous          | synchronous    | TP/sync/request |
      | serviceqql2 | thinkinthing | admin_bb      | 4passw0rd   | SAqql1022 | synchronous          | asynchronous   | TP/async/create |
      | serviceqql3 | thinkinthing | admin_bb      | 4passw0rd   | ASqql1033 | asynchronous         | synchronous    | TP/sync/request |
      | serviceqql4 | thinkinthing | admin_bb      | 4passw0rd   | AAqql1044 | asynchronous         | asynchronous   | TP/async/create |
      | serviceqql5 | thinkinthing | admin_bb      | 4passw0rd   | SSqql1055 | synchronous          | synchronous    | TP/sync/request |

  @ft-happypath @hp-provision-check @hp_sc02
  Scenario Outline: SC_2 User check a BlackButton is registered in BB-platform
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    Then device "<DEVICE_ID>" should be listed under service and subservice

    Examples:
      | SERVICE     | SERVICEPATH  | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID |
      | serviceqql1 | thinkinthing | admin_bb      | 4passw0rd   | SSqql1011 |
      | serviceqql2 | thinkinthing | admin_bb      | 4passw0rd   | SAqql1022 |
      | serviceqql3 | thinkinthing | admin_bb      | 4passw0rd   | ASqql1033 |
      | serviceqql4 | thinkinthing | admin_bb      | 4passw0rd   | AAqql1044 |

  @ft-happypath  @hp-button-flows @hp-button-sync @hp_sc03
  Scenario Outline: SC_3 Client push the button in the SYNC mode
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a button_request "<BT_REQUEST>" for mode "<SYNC_MODE>"
    When the button "<DEVICE_ID>" is pressed in mode "<SYNC_MODE>" the IOTA should receive the request
    And the ThirdParty "<TP_NAME>" changed the status to "<OP_RESULT>"

    Examples:
      | SERVICE     | SERVICEPATH  | DEVICE_ID | SYNC_MODE   | BT_REQUEST                        | TP_NAME | OP_RESULT                                  |
      | serviceqql1 | thinkinthing | SSqql1011 | synchronous | #3,BT,S,4,5,2000$WakeUp,#0,K1,30$ | TP      | #3,BT,S,1,rt-20;rrgb-00FF00;,0$#0,K1,300$, |
      | serviceqql2 | thinkinthing | SAqql1022 | synchronous | #1,BT,S,2,1,2000$WakeUp,#0,K1,30$ | TP      | #1,BT,S,1,rt-20;rrgb-00FF00;,0$#0,K1,300$, |


  @ft-happypath @hp-button-flows @hp-button-async @hp_sc04
  Scenario Outline: SC_4 Client push the button in the ASYNC mode
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a button_request "<BT_REQUEST>" for mode "<SYNC_MODE>"
    When the button "<DEVICE_ID>" is pressed in mode "<SYNC_MODE>" the IOTA should receive the request
    Then the button "<DEVICE_ID>" is pulling every "1" seconds during "10" times or until the IOTA request returns status "<STATUS>"
    And the button "<DEVICE_ID>" close the request and receive the final status "<FINAL_STATUS>"


    Examples:
      | SERVICE     | SERVICEPATH  | DEVICE_ID | SYNC_MODE    | BT_REQUEST                        | STATUS | FINAL_STATUS |
      | serviceqql3 | thinkinthing | ASqql1033 | asynchronous | #1,BT,C,3,2,2000$WakeUp,#0,K1,30$ | C.S    | C.S          |
      | serviceqql4 | thinkinthing | AAqql1044 | asynchronous | #1,BT,C,1,1,2000$WakeUp,#0,K1,30$ | C.S    | C.S          |


  @ft-happypath  @hp-service-clean @hp_sc05
  Scenario Outline: SC_5 Clean SERVICE data generated in happy path scenarios
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a list of services for admin_cloud is retrieved
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    And a list of subservices for service_admin "<SERVICE_ADMIN>" and service_pwd "<SERVICE_PWD>" are retrieved
    When the "ORC" receive the request "SUBSERVICE" and action "DELETE"
    And the "ORC" receive the request "SERVICE" and action "DELETE"
    Then the service "<SERVICE>" should not be listed

    Examples:
      | SERVICE     | SERVICEPATH  | SERVICE_ADMIN | SERVICE_PWD |
      | serviceqql1 | thinkinthing | admin_bb      | 4passw0rd   |
      | serviceqql2 | thinkinthing | admin_bb      | 4passw0rd   |
      | serviceqql3 | thinkinthing | admin_bb      | 4passw0rd   |
      | serviceqql4 | thinkinthing | admin_bb      | 4passw0rd   |
      | serviceqql5 | thinkinthing | admin_bb      | 4passw0rd   |
