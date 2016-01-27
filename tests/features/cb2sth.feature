Feature: Context Broker connection with MySQL
  In order to validate the interaction between CB and STH
  As a Long Tail Platform backend checker
  I should validate the ability of the platform to store historical data in a database

  @ft-cb2sth @c2s-01 @rm-entity @rm-subs @rm-sth
  Scenario Outline: A new entity attribute should be stored in STH
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in ContextBroker and STH
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern | entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE> | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | PT2S       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"

    Examples:
      | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |
      | testservice | /testpath   | entity1   | bbutton     | op_status   | C.S      |
      | testservice | /testpath   | entity2   | sensor      | temperature | 21       |

  @ft-cb2sth @c2s-02 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Two consecutive values of an entity attribute should be stored in STH (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in ContextBroker and STH
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE2>      |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>;<ATTVALUE2>"

    Examples:
      | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTVALUE2 |
      | testservice | /testpath   | entity1   | bbutton     | op_status   | C.S      | C.F       |
      | testservice | /testpath   | entity2   | sensor      | temperature | 21       | 23        |


  @ft-cb2sth @c2s-03 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Several attributes of the same entity should be stored in STH
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in ContextBroker and STH
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern | entity_type   | attributes_name      | notify_url  | duration | notify_type | notif_cond_values    | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE> | <ATTNAME>;<ATTNAME2> | cb2sth      | 2        | ONCHANGE    | <ATTNAME>;<ATTNAME2> | PT2S       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME2>     | attrType       | <ATTVALUE2>     |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"
    And I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME2>" registered in STH and has samples for "<ATTVALUE2>"

    Examples:
      | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME2       | ATTVALUE2 |
      | testservice | /testpath   | entity1   | bbutton     | op_status   | C.S      | last_operation | S         |
      | testservice | /testpath   | entity2   | sensor      | temperature | 21       | humidity       | 30        |


  @ft-cb2sth @c2s-04 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Attributes of several entities should be stored in STH (subscription throttling must be None!)
  Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in ContextBroker and STH
    And I create a subscription in context broker
      | service   | subservice    | entity_id | entity_pattern | entity_type   | attributes_name      | notify_url  | duration | notify_type | notif_cond_values    | throttling |
      | <SERVICE> | <SERVICEPATH> | .*        | true           | <ENTITY_TYPE> | <ATTNAME>;<ATTNAME2> | cb2sth      | 2       | ONCHANGE    | <ATTNAME>;<ATTNAME2> | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "<N>" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME2>     | attrType       | <ATTVALUE2>     |     None      |
    Then I check attribute "<ATTNAME>" was registered in STH for every entity created and has samples for "<ATTVALUE>"
    And I check attribute "<ATTNAME2>" was registered in STH for every entity created and has samples for "<ATTVALUE2>"

  Examples:
    | SERVICE     | SERVICEPATH | ENTITY_ID       | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME2       | ATTVALUE2 | N |
    | testservice | /testpath   | entity_bbutton  | bbutton     | op_status   | C.S      | last_operation | S         | 2 |
    | testservice | /testpath   | entity_sensor   | sensor      | temperature | 21       | humidity       | 30        | 2 |

  @ft-cb2sth @c2s-05 @wip @rm-entity @rm-subs @rm-sth
  Scenario Outline: Attributes of several entities with same ID but different capitalization should be stored in STH separately (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in ContextBroker and STH
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID_2>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"
    And I check entity with "<ENTITY_ID_2>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME_2>" registered in STH and has samples for "<ATTVALUE_2>"

  Examples:
    | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_ID_2 | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME_2      | ATTVALUE_2 |
    | testservice | /testpath   | entity1   | ENTITY1     | bbutton     | op_status   | C.S      | last_operation | S          |
    | testservice | /testpath   | entity2   | ENTITY2     | sensor      | temperature | 21       | humidity       | 30         |

  @ft-cb2sth @c2s-06 @wip @rm-entity @rm-subs @rm-sth
  Scenario Outline: Attributes of several entities with same ID and type but different capitalization should be stored in STH separately (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And service and subservice are provisioned in ContextBroker and STH
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE_2>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"
    And I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE_2>" has the attribute "<ATTNAME_2>" registered in STH and has samples for "<ATTVALUE_2>"

  Examples:
    | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ENTITY_TYPE_2 | ATTNAME     | ATTVALUE | ATTNAME_2      | ATTVALUE_2 |
    | testservice | /testpath   | entity1   | bbutton     | BBUTTON      | op_status   | C.S      | last_operation | S          |
    | testservice | /testpath   | entity2   | sensor      | SENSOR       | temperature | 21       | humidity       | 30         |

# TODO: define this behavior. Will this be implemented? ISSUE in CB: first notification of suscription cause problems
#  @ft-cb2sth @c2s-07 @wip @rm-entity @rm-subs @rm-sth
#  Scenario Outline: STH should not store attributes modified before creating the suscription
#  Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
#  And service and subservice are provisioned in ContextBroker and STH
#  And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "<N>" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
#      | attribute_name | attribute_type | attribute_value | metadata_list |
#      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
#      | <ATTNAME2>     | attrType       | <ATTVALUE2>     |     None      |
#  When I create a subscription in context broker
#      | service   | subservice    | entity_id | entity_pattern | entity_type   | attributes_name      | notify_url  | duration | notify_type | notif_cond_values    | throttling |
#      | <SERVICE> | <SERVICEPATH> | .*        | true           | <ENTITY_TYPE> | <ATTNAME>;<ATTNAME2> | cb2sth      | 2        | ONCHANGE    | <ATTNAME>;<ATTNAME2> |     PT2S   |
#  Then I check attribute "<ATTNAME>" is not registered in STH for every entity created
#  And I check attribute "<ATTNAME2>" is not registered in STH for every entity created
#
#  Examples:
#  | SERVICE     | SERVICEPATH | ENTITY_ID       | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME2       | ATTVALUE2 | N |
#  | testservice | /testpath   | entity_bbutton  | bbutton     | op_status   | C.S      | last_operation | S         | 2 |
#  | testservice | /testpath   | entity_sensor   | sensor      | temperature | 21       | humidity       | 30        | 2 |