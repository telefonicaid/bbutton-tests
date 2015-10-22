Feature: Context Broker connection with MySQL
  In order to validate interaction with an external database
  As a Long Tail Platform backend checker
  I should validate the ability of the platform to export datasets into MySQL database

  @ft-cbcygsql @ccm-01
  Scenario Outline: Entities updated should be stored in MySQL
    Given I create a MySQL database under name "<SERVICE>" and a table under name given by "<SERVICEPATH>" and "<ENTITY_ID>"
    And I launch a cygnus connection with "MYSQL"
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern | entity_type   | attributes_name | notify_url   | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE> | <ATTNAME>       | CYGNUS2comp | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send an entity update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", entity_id "<ENTITY_ID>", entity_type "<ENTITY_TYPE>", entity_pattern "false"
      | attribute_name | attribute_type | attribute_value | metadata_list                     |
      | <ATTNAME>      | <ATTTYPE>      | <ATTVALUE>      | <METANAME>,<METATYPE>,<METAVALUE> |
    Then I check value "<ATTVALUE>" in column name "<ATTNAME>" of "<SERVICEPATH>" table in MySQL

    Examples:
      | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME  | ATTTYPE | ATTVALUE | METANAME | METATYPE | METAVALUE |
      | testservice | /testpath   | entity1   | type1       | att_ccid | type1   | val1     | met1     | type1    | val1      |
