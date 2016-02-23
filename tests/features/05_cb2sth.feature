Feature: Context Broker connection with STH (Short Term Historic)
  In order to validate the interaction between CB and STH
  As a Long Tail Platform backend checker
  I should validate the ability of the platform to store historical data in a database

  @ft-cb2sth @c2s-01 @rm-entity @rm-subs @rm-sth
  Scenario Outline: A new entity attribute should be stored in STH
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern | entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE> | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | PT2S       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"

    Examples:
      | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |
      | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      |
      | teststhservice | testpath    | entity2   | sensor      | temperature | 21       |

  @ft-cb2sth @c2s-02 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Two consecutive values of an entity attribute should be stored in STH (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
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
      | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTVALUE2 |
      | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      | C.F       |
      | teststhservice | testpath    | entity2   | sensor      | temperature | 21       | 23        |


  @ft-cb2sth @c2s-03 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Two consecutive and equal values of an entity attribute but with different TimeInstant metadata should be stored in STH (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value |             metadata_list                  |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     <METANAME>,<METATYPE>,<METAVALUE>      |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value |             metadata_list                  |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     <METANAME>,<METATYPE>,<METAVALUE2>      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>;<ATTVALUE>"

    Examples:
      | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |  METANAME     |  METATYPE   |       METAVALUE          |    METAVALUE2            |
      | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      |  TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z | 2016-02-10T12:05:28.841Z |
      | teststhservice | testpath    | entity2   | sensor      | temperature | 21       |  TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z | 2016-02-10T12:05:28.841Z |

  @ft-cb2sth @c2s-04 @wip @rm-entity @rm-subs @rm-sth
  Scenario Outline: A repeated value of an entity attribute (same value and same TimeInstant metadata) should be ignored in STH (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value |             metadata_list                  |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     <METANAME>,<METATYPE>,<METAVALUE>      |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value |             metadata_list                              |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     <METANAME>,<METATYPE>,<METAVALUE>; trigger,bar,foo |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |  METANAME     |  METATYPE   |       METAVALUE          |
    | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      |  TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z |
    | teststhservice | testpath    | entity2   | sensor      | temperature | 21       |  TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z |

  @ft-cb2sth @c2s-05 @wip @rm-entity @rm-subs @rm-sth
  Scenario Outline: A repeated value of an entity attribute (same value and same TimeInstant metadata) notified by a second subscription should be ignored in STH (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value |             metadata_list                  |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     <METANAME>,<METATYPE>,<METAVALUE>      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE |  METANAME     |  METATYPE   |       METAVALUE          |
    | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      |  TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z |
    | teststhservice | testpath    | entity2   | sensor      | temperature | 21       |  TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z |

  @ft-cb2sth @c2s-06 @wip @rm-entity @rm-subs @rm-sth
  Scenario Outline: A new value of an entity attribute with a repeated TimeInstant metadata should overwrite the attribute value in STH (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE>  | <ATTNAME>       | cb2sth      | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value |             metadata_list               |
      | <ATTNAME>      | attrType       | <ATTVALUE1>      |     <METANAME>,<METATYPE>,<METAVALUE>  |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value |             metadata_list               |
      | <ATTNAME>      | attrType       | <ATTVALUE2>     |     <METANAME>,<METATYPE>,<METAVALUE>   |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE2>"

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE1 | ATTVALUE2 |  METANAME    |  METATYPE   |       METAVALUE          |
    | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S       | C.F       | TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z |
    | teststhservice | testpath    | entity2   | sensor      | temperature | 21        | 15        | TimeInstant  |  ISO8601    | 2016-02-10T11:05:28.841Z |

  @ft-cb2sth @c2s-07 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Several attributes of the same entity should be stored in STH
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
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
      | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME2       | ATTVALUE2 |
      | teststhservice | testpath    | entity1   | bbutton     | op_status   | C.S      | last_operation | S         |
      | teststhservice | testpath    | entity2   | sensor      | temperature | 21       | humidity       | 30        |


  @ft-cb2sth @c2s-08 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Attributes of several entities should be stored in STH (subscription throttling must be None!)
  Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id | entity_pattern | entity_type   | attributes_name      | notify_url  | duration | notify_type | notif_cond_values    | throttling |
      | <SERVICE> | <SERVICEPATH> | .*        | true           | <ENTITY_TYPE> | <ATTNAME>;<ATTNAME2> | cb2sth      |  2       | ONCHANGE    | <ATTNAME>;<ATTNAME2> | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "<N>" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME2>     | attrType       | <ATTVALUE2>     |     None      |
    Then I check attribute "<ATTNAME>" was registered in STH for every entity created and has samples for "<ATTVALUE>"
    And I check attribute "<ATTNAME2>" was registered in STH for every entity created and has samples for "<ATTVALUE2>"

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID       | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME2       | ATTVALUE2 | N |
    | teststhservice | testpath    | entity_bbutton  | bbutton     | op_status   | C.S      | last_operation | S         | 2 |
    | teststhservice | testpath    | entity_sensor   | sensor      | temperature | 21       | humidity       | 30        | 2 |

  @ft-cb2sth @c2s-09 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Attributes of several entities with same ID but different capitalization should be stored in STH separately (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> |     .*      |     true       | <ENTITY_TYPE>  |     None        | cb2sth      |     2    | ONCHANGE    |   <ATTNAME>       | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID_2>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME_2>    | attrType       | <ATTVALUE_2>    |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"
    And I check entity with "<ENTITY_ID_2>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME_2>" registered in STH and has samples for "<ATTVALUE_2>"

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_ID_2 | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME_2      | ATTVALUE_2 |
    | teststhservice | testpath    | entity1   | ENTITY1     | bbutton     | op_status   | C.S      | last_operation | S          |
    | teststhservice | testpath    | entity2   | ENTITY2     | sensor      | temperature | 21       | humidity       | 30         |

  @ft-cb2sth @c2s-10 @rm-entity @rm-subs @rm-sth
  Scenario Outline: Attributes of several entities with same ID and type but different capitalization should be stored in STH separately (subscription throttling must be None!)
    Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
    And a service and subservice are provisioned
    And service and subservice are provisioned in ContextBroker and STH
    And a valid token with scope is retrieved for service admin user
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern |  entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> |      false     |                |      None       | cb2sth      |   2      | ONCHANGE    | <ATTNAME>         | None       |
    When I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
    And I send a context update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", and "1" entities with id "<ENTITY_ID>" and type "<ENTITY_TYPE_2>"
      | attribute_name | attribute_type | attribute_value | metadata_list |
      | <ATTNAME>      | attrType       | <ATTVALUE>      |     None      |
      | <ATTNAME_2>    | attrType       | <ATTVALUE_2>    |     None      |
    Then I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE>" has the attribute "<ATTNAME>" registered in STH and has samples for "<ATTVALUE>"
    And I check entity with "<ENTITY_ID>" and "<ENTITY_TYPE_2>" has the attribute "<ATTNAME_2>" registered in STH and has samples for "<ATTVALUE_2>"

  Examples:
    | SERVICE        | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ENTITY_TYPE_2 | ATTNAME     | ATTVALUE | ATTNAME_2      | ATTVALUE_2 |
    | teststhservice | testpath    | entity1   | bbutton     |  BBUTTON      | op_status   | C.S      | last_operation | S          |
    | teststhservice | testpath    | entity2   | sensor      |  SENSOR       | temperature | 21       | humidity       | 30         |

# TODO: define this behavior. Will this be implemented? ISSUE in CB: first notification of suscription cause problems
#  @ft-cb2sth @c2s-11 @wip @rm-entity @rm-subs @rm-sth
#  Scenario Outline: STH should not store attributes modified before creating the suscription
#  Given a Client of "<SERVICE>" and a Subservice called "<SERVICEPATH>"
#  And a service and subservice are provisioned
#  And service and subservice are provisioned in ContextBroker and STH
#  And a valid token with scope is retrieved for service admin user
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
#  | SERVICE        | SERVICEPATH | ENTITY_ID       | ENTITY_TYPE | ATTNAME     | ATTVALUE | ATTNAME2       | ATTVALUE2 | N |
#  | teststhservice | testpath    | entity_bbutton  | bbutton     | op_status   | C.S      | last_operation | S         | 2 |
#  | teststhservice | testpath    | entity_sensor   | sensor      | temperature | 21       | humidity       | 30        | 2 |
