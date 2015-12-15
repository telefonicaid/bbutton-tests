Feature: Complete path E2E functionality Sync-Async / Sync-Sync
  In order to check if a blackbutton that can order a product
  In a Service servsyncaa and Subservice testpizza
  As a client has SYNC BlackButtons: device1, device2, ...
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
      | KEYSTONE_PORT              | 5001            |
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

    Examples:
      | SERVICE    | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID | ENTITY_TYPE | TOKEN | ATT_LOCATION | BT_REQUEST                         | TP_URL          | OP_RESULT                                  |
      | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | device1   | BlackButton | no    | 33,-122      | #1,BT,S,1,1,2000$WakeUp,#0,K1,30$  | TP/sync/request | #1,BT,S,1,rt-20;rrgb-00FF00;,0$#0,K1,300$, |
      | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | device2   | BlackButton | no    | 15,-2        | #2,BT,S,3,0,#0,K1,0$               | TP/sync/request | #2,BT,S,1,rt-20;rrgb-00FF00;,0$#0,K1,300$, |
      | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | device3   | BlackButton | no    | 16,21        | #3,BT,S,0,0,512WakeUp#0,K1,0$,     | TP/sync/request | #3,BT,S,1,rt-20;rrgb-00FF00;,0$#0,K1,300$, |
      | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | device4   | BlackButton | yes   | 31,-40       | #4,BT,S,9,10,2000$WakeUp,#0,K1,30$ | TP/sync/request | #4,BT,S,1,rt-20;rrgb-00FF00;,0$#0,K1,300$, |


  @ft-syncflow @sf-button-flows @sf-02
  Scenario Outline: SC2 client push the button and device is not registered
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
      | KEYSTONE_PORT              | 5001            |
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
    And a device should be provisioned for service and subservice with certain fields
      | attribute             | value                   |
      | PROTOCOL              | <PROTOCOL>              |
      | DEVICE_ID             | <DEVICE_ID>             |
      | ENTITY_TYPE           | <ENTITY_TYPE>           |
      | SERVICE_NAME          | <SERVICE_NAME>          |
      | SUBSERVICE_NAME       | <SUBSERVICE_NAME>       |
      | SERVICE_USER_NAME     | <SERVICE_USER_NAME>     |
      | SERVICE_USER_PASSWORD | <SERVICE_USER_PASSWORD> |
      | TOKEN                 | <TOKEN>                 |
    Then registration is not successful and device "<DEVICE_ID>" is not listened under the service and subservice

    Examples:
      | PROTOCOL       | DEVICE_ID | ENTITY_TYPE | SERVICE_NAME | SUBSERVICE_NAME | SERVICE_USER_NAME | SERVICE_USER_PASSWORD | TOKEN | SERVICE    | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | TP_URL          |
      | TT_BLACKBUTTON | device_f  | BlackButton | NaN          | NaN             | NaN               | NaN                   | no    | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | TP/sync/request |
      | TT_BLACKBUTTON | device_f  | BlackButton | servsyncaa   | testpizza       | NaN               | NaN                   | no    | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | TP/sync/request |
#      | TT_BLACKBUTTON | device_f  | BlackButton | NaN          | testpizza       | admin_bb          | 4passw0rd             | no    | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | TP/sync/request |
#      | TT_BLACKBUTTON | device_f  | BlackButton | servsyncaa   | NaN             | admin_bb          | 4passw0rd             | no    | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | TP/sync/request |
      | TT_BLACKBUTTON | device_f  | BlackButton | servsyncaa   | testpizza       | NaN               | 4passw0rd             | no    | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | TP/sync/request |


  @ft-syncflow @sf-button-flows @sf-03
  Scenario Outline: SC3 client push the button and device is registered, but conditions fail
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
      | KEYSTONE_PORT              | 5001            |
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
    And a device should be provisioned for service and subservice with certain fields
      | attribute             | value           |
      | PROTOCOL              | TT_BLACKBUTTON  |
      | DEVICE_ID             | <DEVICE_ID>     |
      | ENTITY_TYPE           | <ENTITY_TYPE>   |
      | SERVICE_NAME          | <SERVICE>       |
      | SUBSERVICE_NAME       | <SERVICEPATH>   |
      | SERVICE_USER_NAME     | <SERVICE_ADMIN> |
      | SERVICE_USER_PASSWORD | <SERVICE_PWD>   |
      | TOKEN                 | <TOKEN>         |
    Then device "<DEVICE_ID>" should be listed under service and subservice


    Examples:
      | DEVICE_ID | ENTITY_TYPE | TOKEN | SERVICE    | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | TP_URL          | BT_REQUEST                        |
      | deviceA   | BlackButton | no    | servsyncaa | testpizza   | admin_bb      | 4passw0rd   | TP/sync/request | #1,BT,S,1,1,2000$WakeUp,#0,K1,30$ |