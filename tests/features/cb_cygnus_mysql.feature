Feature: Context Broker connection with MySQL
  In order to validate interaction with an external database
  As a Long Tail Platform backend checker
  I should validate the ability of the platform to export datasets into MySQL database

  @ft-cbcygsql @ccm-01 @ready
  Scenario Outline: Entities updated should be stored in MySQL
    Given I create a MySQL database under name "<SERVICE>" and a table under name given by "<SERVICEPATH>" and "<ENTITY_ID>"
    And I launch a cygnus connection with "MYSQL"
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern | entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE> | <ATTNAME>       | CYGNUS2comp | 2        | ONCHANGE    | <ATTNAME>         | None       |
    When I send an entity update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", entity_id "<ENTITY_ID>", entity_type "<ENTITY_TYPE>", entity_pattern "false"
      | attribute_name | attribute_type | attribute_value | metadata_list                     |
      | <ATTNAME>      | default_type   | <ATTVALUE>      | <METANAME>,<METATYPE>,<METAVALUE> |
    Then I check value "<ATTVALUE>" in column name "<ATTNAME>" of "<SERVICEPATH>" table in MySQL

    Examples:
      | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAME   | ATTVALUE | METANAME | METATYPE | METAVALUE |
      | testservice | /testpath   | entity1   | bbutton     | ccid_name | 254156   | met1     | type1    | val1      |
      | testservice | /testpath   | entity2   | bbutton     | imei_name | 8348938  | met2     | type2    | val2      |
      | testservice | /testpath   | entity3   | bbutton     | imsi_name | 291371   | met3     | type3    | val3      |


  @ft-cbcygsql @ccm-02 @no-ready
  Scenario Outline: Entities with several attributes should be stored in MySQL
    Given I create a MySQL database under name "<SERVICE>" and a table under name given by "<SERVICEPATH>" and "<ENTITY_ID>"
    And I launch a cygnus connection with "MYSQL"
    And I create a subscription in context broker
      | service   | subservice    | entity_id   | entity_pattern | entity_type   | attributes_name | notify_url  | duration | notify_type | notif_cond_values | throttling |
      | <SERVICE> | <SERVICEPATH> | <ENTITY_ID> | false          | <ENTITY_TYPE> | <ATTNAMES>      | CYGNUS2comp | 2        | ONCHANGE    | <ATTNAMES>         | None       |
    When I send an entity update to context broker with service "<SERVICE>", subservice "<SERVICEPATH>", entity_id "<ENTITY_ID>", entity_type "<ENTITY_TYPE>", entity_pattern "false"
      | attribute_name | attribute_type            | attribute_value | metadata_list                     |
      | <ATTNAMES>      | default_type;default_type | <ATTVALUES>      | <METANAME>,<METATYPE>,<METAVALUE> |
    Then I check values "<ATTVALUES>" in column names "<ATTNAMES>" of "<SERVICEPATH>" table in MySQL

    Examples:
      | SERVICE     | SERVICEPATH | ENTITY_ID | ENTITY_TYPE | ATTNAMES            | ATTVALUES  | METANAME | METATYPE | METAVALUE |
      | testservice | /testpath   | entity4   | bbutton     | ccid_name;imei_name | 84324;2832 | met1     | type1    | val1      |


