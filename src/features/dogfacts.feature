@dogFacts
Feature: Dog Facts!

  @dogFacts @success
  Scenario Outline: Learning some dog breeds!

    When the API with method "<method>" is called on the endpoint "<url>" with headers "<headers>", parameters "<params>" and payload "<payload_api>"
    Then the API will return "<status_code>"
    And the field(s) "<api_returned_field>" is(are) "<field_situation>" in the "<api_return_origin>" of the API response

    Examples:
      | method | url                              | headers | params  | payload_api | status_code | api_returned_field | field_situation | api_return_origin |
      | GET    | https://dogapi.dog/api/v2/breeds | omitted | omitted | omitted     | 200         | data               | presente        | body              |

  @dogFacts @failure
  Scenario Outline: Failing the API call

    When the API with method "<method>" is called on the endpoint "<url>" with headers "<headers>", parameters "<params>" and payload "<payload_api>"
    Then the API will return "<status_code>"

    Examples:
      | method | url                              | headers | params  | payload_api | status_code |
      | GET    | https://dogapi.dog/api/v2/breevs | omitted | omitted | omitted     | 404         |