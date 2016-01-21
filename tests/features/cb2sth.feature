Feature: Context Broker connection with MySQL
  In order to validate the interaction between CB and STH
  As a Long Tail Platform backend checker
  I should validate the ability of the platform to store historical data in a database

  @ft-cb2sth @c2s-01 @wip @rm-entity @rm-subs @rm-sth
  Scenario Outline: Entities updated should be stored in STH
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in ContextBroker and STH
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern | entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE> | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | PT2S       |
    When I send an entity update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", entity_id "<ENTITY_ID>", entity_type "<ENTITY_TYPE>", entity_pattern "false"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    Then I check attribute "<ATTNAME>" was registered in STH

    Examples:
      | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |
      | testservice | /testpath   | entity1   | bbutton     | op_status   | C.S      |
      | testservice | /testpath   | entity2   | sensor      | temperature | 21       |
