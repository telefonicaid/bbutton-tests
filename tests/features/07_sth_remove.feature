Feature: STH (Short Term Historic) component tests for deletion features
  In order to validate the functionality of STH
  As a Long Tail Platform backend checker
  I should validate the ability of STH to remove historical data from database


  @ft-sth @sth-01 @rm-sth
  Scenario Outline: Entity attribute data should be removed from STH but the rest of attributes should remain
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in STH
    And I send a notification with subscription id "aaa111id" and "1" context elements with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME2>     | attrType       | <ATTVALUE2>     |     None      |
    And I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"
    And I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME2>" registered in STH and has samples for "<ATTVALUE2>"
    When I delete from STH all the data associated to
      |  key             |     value      |
      |  service         |  <SERVICE>     |
      |  subservice      |  <SERVICEPATH> |
      |  entity_id       |  <ENTITY_ID>   |
      |  entity_type     |  <ENTITY_TYPE> |
      |  attribute_name  |  <ATTNAME>     |
    Then I check entity with entity id "<ENTITY_ID>" and entity type "<ENTITY_TYPE>" does not have the attribute "<ATTNAME>" registered in STH
    And I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME2>" registered in STH and has samples for "<ATTVALUE2>"

    Examples:
      | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |     ATTNAME2     | ATTVALUE2 |
      | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      | last_operation   |   C.F     |
      | teststhservice | testpath    | entity2   | sensor      | temperature | 21       | humidity         |   40      |


  @ft-sth @sth-02 @rm-sth
  Scenario Outline: All Entity attribute data should be removed from STH but the rest of entities should remain
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in STH
    And I send a notification with subscription id "aaa111id" and "2" context elements with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME2>     | attrType       | <ATTVALUE2>     |     None      |
    And I check attribute "<ATTNAME>" was registered in STH for every entity created and has samples for "<ATTVALUE>"
    And I check attribute "<ATTNAME2>" was registered in STH for every entity created and has samples for "<ATTVALUE2>"
    When I delete from STH all the data associated to
      |  key             |     value      |
      |  service         |  <SERVICE>     |
      |  subservice      |  <SERVICEPATH> |
      |  entity_id       |  <ENTITY_ID>   |
      |  entity_type     |  <ENTITY_TYPE> |
    Then I check entity with entity id "<ENTITY_ID>" and entity type "<ENTITY_TYPE>" does not have the attribute "<ATTNAME>" registered in STH
    And I check entity with entity id "<ENTITY_ID>" and entity type "<ENTITY_TYPE>" does not have the attribute "<ATTNAME2>" registered in STH
    And I check entity with "<ENTITY_ID>_1" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"
    And I check entity with "<ENTITY_ID>_1" and "<ENTITY_TYPE>" has the attribute "<ATTNAME2>" registered in STH and has samples for "<ATTVALUE2>"

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |     ATTNAME2     | ATTVALUE2 |
    | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      | last_operation   |   C.F     |
    | teststhservice | testpath    | entity2   | sensor      | temperature | 21       | humidity         |   40      |

  @ft-sth @sth-03 @rm-sth
  Scenario Outline: All entities attribute data of a subservice should be removed from STH
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in STH
    And I send a notification with subscription id "aaa111id" and "2" context elements with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME2>     | attrType       | <ATTVALUE2>     |     None      |
    And I check attribute "<ATTNAME>" was registered in STH for every entity created and has samples for "<ATTVALUE>"
    And I check attribute "<ATTNAME2>" was registered in STH for every entity created and has samples for "<ATTVALUE2>"
    When I delete from STH all the data associated to
      |  key             |     value      |
      |  service         |  <SERVICE>     |
      |  subservice      |  <SERVICEPATH> |
    Then I check entity with entity id "<ENTITY_ID>" and entity type "<ENTITY_TYPE>" does not have the attribute "<ATTNAME>" registered in STH
    And I check entity with entity id "<ENTITY_ID>" and entity type "<ENTITY_TYPE>" does not have the attribute "<ATTNAME2>" registered in STH
    And I check entity with entity id "<ENTITY_ID>_1" and entity type "<ENTITY_TYPE>" does not have the attribute "<ATTNAME>" registered in STH
    And I check entity with entity id "<ENTITY_ID>_1" and entity type "<ENTITY_TYPE>" does not have the attribute "<ATTNAME2>" registered in STH

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |     ATTNAME2     | ATTVALUE2 |
    | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      | last_operation   |   C.F     |
    | teststhservice | testpath    | entity2   | sensor      | temperature | 21       | humidity         |   40      |
    | teststhservice |     /       | entity1   | sensor      | temperature | 21       | humidity         |   40      |
