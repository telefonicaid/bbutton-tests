Feature: Complete path E2E functionality Sync-Async / Sync-Sync
  In order to check if a blackbutton that can order a product
  In a Service servicea1a and Subservice testpizza
  As a client has SYNC BlackButtons: devicea1a_sa_03 and devicea1a_ss_04
  I should validate the ability of the platform to process the buttons requests to a Sync or Async third party


  @ft-syncflow @sf-button-flows @sf-01
  Scenario Outline: SC1 client push the button in the SYNC mode, and third party is SYNC
    Given a Client of "<SERVICE>" and a ThirdParty called "<SERVICEPATH>"
    When a service and subservice are created in the "ORC"
      | key                        | value           |
      | DOMAIN_NAME                | admin_domain    |
      | DOMAIN_ADMIN_USER          | cloud_admin     |
      | DOMAIN_ADMIN_PASSWORD      | password        |
      | NEW_SERVICE_NAME           | <SERVICE>       |
      | NEW_SERVICE_ADMIN_USER     | <SERVICE_ADMIN> |
      | NEW_SERVICE_ADMIN_PASSWORD | <SERVICE_PWD>   |
      | KEYPASS_PORT               | 8080            |
      | KEYSTONE_PORT              | 5000            |
      | NEW_SUBSERVICE_NAME        | <SERVICEPATH>   |
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
      | ATT_INTERACTION_TYPE  | synchronous       |
      | ATT_TIMEOUT           | 120               |
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    And a device "<DEVICE_ID>" of entity_type "<ENTITY_TYPE>" should be provisioned for service and subservice
      | attribute            | value          |
      | TOKEN                | <TOKEN>        |
      | ATT_INTERACTION_TYPE | synchronous    |
      | ATT_GEOLOCATION      | <ATT_LOCATION> |

    Then device "<DEVICE_ID>" should be listed under service and subservice
    And the button "<DEVICE_ID>" pressed in mode "synchronous" the IOTA should receive the request "<BT_REQUEST>"
    And the ThirdParty "TP" changed the status to "<OP_RESULT>"
    #And a close request is sent to finish the operation


    Examples:
      | SERVICE    | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID | ENTITY_TYPE | TOKEN | ATT_LOCATION | BT_REQUEST                        | TP_URL          | OP_RESULT           |
      | service2sy | testpizza   | admin_bb      | 4passw0rd   | device1   | BlackButton | no    | 33,-122      | #1,BT,S,1,1,2000$WakeUp,#0,K1,30$ | TP/sync/request | rgb-66CCDD%3Bt-2%3B |
      | service2sy | testpizza   | admin_bb      | 4passw0rd   | device2   | BlackButton | no    | 15,-2        | #1,BT,S,1,0,#0,K1,0$              | TP/sync/request | NaN                 |
      | service2sy | testpizza   | admin_bb      | 4passw0rd   | device3   | BlackButton | no    | 16,21        | #1,BT,S,0,0,512WakeUp#0,K1,0$,    | TP/sync/request | rgb-66CCDD%3Bt-2%3B |
      | service2sy | testpizza   | admin_bb      | 4passw0rd   | device4   | BlackButton | yes   | 31,-40       | #1,BT,S,1,1,2000$WakeUp,#0,K1,30$ | TP/sync/request | rgb-66CCDD%3Bt-2%3B |



  @ft-syncflow @sf-button-flows @sf-02
  Scenario Outline: SC1 client push the button in the SYNC mode, and third party is SYNC but request is failured



    Examples: