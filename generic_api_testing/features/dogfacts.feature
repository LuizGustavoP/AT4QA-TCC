@dogFacts
Feature: Dog Facts!

  @dogFacts
  Scenario Outline: Learning some dog breeds!

    When a API com o verbo "<verbo>" for chamada no endpoint "<caminho>" com os headers "<headers>", parâmetros "<params>" e payload "<payload_api>"
    Then a API retornará "<status_code>"
    And o(s) campo(s) "<campos_retorno_api>" está(ão) "<situacao_campos>" no "<origem_retorno_api>" da resposta da API

    Examples:
      | verbo | caminho                          | headers | params  | payload_api | status_code | campos_retorno_api | situacao_campos | origem_retorno_api |
      | GET   | https://dogapi.dog/api/v2/breeds | omitido | omitido | omitido     | 200         | data               | presente        | body               |