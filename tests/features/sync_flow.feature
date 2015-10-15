Feature: Complete path E2E functionality Sync-Async / Sync-Sync
  In order to check if a blackbutton that can order a product
  In a Service servicea1a and Subservice testpizza
  As a client has SYNC BlackButtons: devicea1a_sa_03 and devicea1a_ss_04
  I should validate the ability of the platform to process the buttons requests to a Sync or Async third party


  @ft-syncflow @sf-button-flows @sf-party-sync
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
      | ATT_INTERACTION_TYPE  | <TP_INTERACTION>  |
      | ATT_TIMEOUT           | 120               |
    And a valid token is retrieved for user "<SERVICE_ADMIN>" and password "<SERVICE_PWD>"
    And a device "<DEVICE_ID>" of entity_type "<ENTITY_TYPE>" should be provisioned for service and subservice
      | attribute            | value                  |
      | ATT_INTERACTION_TYPE | <ATT_INTERACTION_TYPE> |
      | ATT_GEOLOCATION      | <ATT_LOCATION>         |


    Then device "<DEVICE_ID>" should be listed under service and subservice
    And the button "<DEVICE_ID>" is pressed in mode "<SYNC_MODE>" the IOTA should receive the request
    And the ThirdParty "<TP_NAME>" changed the status to "<OP_RESULT>"


    Examples:
      | SERVICE    | SERVICEPATH | SERVICE_ADMIN | SERVICE_PWD | DEVICE_ID | ENTITY_TYPE | ATT_INTERACTION_TYPE | ATT_LOCATION | TP_INTERACTION | TP_URL          |
      | service2sy | testpizza   | admin_bb      | 4passw0rd   | device1   | BlackButton | synchronous          | 33,-122      | synchronous    | TP/sync/request |