# PROJETO AT4QA

**Implementação de um sistema de Autonomous Generic Behaviour Driven Development (AGBDD) como Trabalho de Conclusão de Curso**

# Introdução
## BDD

Este repositório contém uma implementação do processo de automação de testes *Autonomous Generic Behaviour Driven Development* (AGBDD), neste caso focado no desenvolvimento de Web APIs.

Na nossa implementação, os testes são implementados em 3 partes principais características do Gherkin, são elas:

  > **`Feature Files`**

  > **`Step Definitions`**

  > **`Classes`**

Temos também 2 elementos específicos do AGBDD, são eles:

  > **`Feature Masks`**

  > **`Statement Dictionaries`**

## Feature Files

Os Feature Files são os arquivos que descrevem, em linguagem natural, o comportamento que um sistema deve ter em casos de teste.

Estes casos de teste são definidos com `Scenarios`, no nosso caso, utilizaremos exclusivamente os `Scenarios Outline` do Gherkin, que nos permite introduzir parâmetros nos *statements*.

Gherkin utiliza de 4 palavras reservadas para descrever um cenário, são elas:

- **`Given`**: Descreve a situação inicial, ou seja, o estado do ambiente antes que a API ou sistema que está sendo testado é executado.

- **`When`**: Descreve a maneira e o momento que o sistema que está sendo testado será executado.

- **`Then`**: Descreve o comportamento que o sistema deve ter após ter sido executado no ambiente descrito anteriormente.

- **`And`**: Atribui a um statement a última palavra chave diferente de si.

Os nossos Feature Files estão presentes na pasta:

  > **`/generic_api_testing/features`**

## Classes

As Classes do projeto são os arquivos que contém o código que irá realizar a execução dos comportamentos esperados.

No nosso caso, as classes contém os comportamentos gerais esperados de testes de Web APIs, tais como a realização de requisições, avaliação de valores retornados, entre outros.

Todas as classes estão dentro da pasta:

 > **`/generic_api_testing/test_classes`**

## Step Definitions

Os Step Definitions são os arquivos que irão realizar a conexão entre os *statements* descritos em um Feature File e as classes que irão realizar as chamadas para as APIs.

Ou seja, eles irão pegar os *statements* e ligá-los a um método implementado que execute o comportamento que foi descrito por tal *statement*.

Os nossos Step Definitions estão presentes na pasta:

  > **`/generic_api_testing/step_defs`**

## Pytest.ini

O arquivo pytest.ini na raiz do projeto é utilizado para estabelecer configurações gerais da execução dos testes, nele estão contidas os arugmentos de linha de comando implícitos, o local da pasta *features* para que a customização de feature files seja possível, todas as *tags* do projeto, etc.

## Conftest.py

O arquivo conftest.py irá conter as configurações do ambiente de execução de testes, nele estarão as definições de possíveis atributos que podem ser passados por linha de comando, configuração do ambiente que será executado antes de todos os testes (que inclui a criação da conexão do banco de dados e atribuição das varíaveis de ambiente), e o fechamento da conexão com o banco de dados.

# Instalação
## UTILIZE O VIRTUALENV

- Antes de executar, crie uma pasta **`venv`** na raiz do projeto e escreva no terminal o seguinte comando:

    > \> `python3 -m venv /path/to/new/virtual/environment`

    Entre no arquivo **`pyvenv.cfg`** localizado na pasta **`venv`** e modifique o `'home'` para o caminho do *Python* na sua máquina. Caso não saiba, abra o *cmd* e digite:

    > \> `where python`

    Feito isso, execute no terminal da sua *IDE* o seguinte comando para ativar o `venv`:

    > \> `.\venv\Scripts\activate`

## ANTES DE EXECUTAR

- Instale as dependências necessárias, presentes no arquivo **`requirements.txt`**. Basta abrir o terminal e digitar o comando:

    > \> `pip install -r requirements.txt`
 
## TESTES

- Para a execução dos testes de um feature file, basta executar o seguinte comando:

    > \> `pytest .\generic_api_testing\step_defs\custom\test_Custom.py -m "<tag>"`

    O argumento **`-m "<tag>"`** se refere a quais cenários de teste ou feature files serão executados (que possuem uma tag ou uma combinação delas).

- Caso queira executar todos os testes, basta não especificar uma tags, como a seguir:
  
    > \> `pytest .\generic_api_testing\step_defs\custom\test_Custom.py`

## FEATURE FILES GENÉRICOS

O elemento característico do AGBDD é o uso de *statements* genéricos para descrever os comportamentos macro da área sendo testada, no nosso caso, os *statements* genéricos serão específicos para o teste de Web APIs.

Um glossário com os *statements* genéricos, bem como explicação e exemplos de uso dos mesmos pode ser conferido [aqui](./glossario_stepdefs.md).

## FEATURE MASKS

Além da criação de feature files, também é possível criar máscaras para feature files.

Estas máscaras são essencialmente feature files resumidos, em que parâmetros que possuem valores repetidos em todos os examples de seu cenário podem ter seus valores inseridos diretamente no statement, e onde é possível utilizar statements customizados que serão traduzidos por um dicionário (que será apresentado na próxima seção).

Desta maneira podemos criar tabelas de examples menores e mais legíveis, além de utilizar os statements customizados para recuperar o elemento da linguagem natural aos testes automatizados genéricos.

Se uma feature mask não possui statements customizados e apenas valores inseridos diretamente no statement, não é necessário enviar um dicionário junto.

A sintaxe de uma feature mask é a mesma de um arquivo Gherkin, ou seja, seguirá o padrão:

  > - Feature: `(nome_da_feature)`:
    >   -  Scenario Mask: `(nome_do_scenario)`
      >       - `(statements)`
      >       - Examples:
        >            - `(nomes_dos_parametros)`
        >            - `(valores_dos_parametros)`


Além disto, agora os statements podem receber valores diretamente neles, caso este valor seja igual para todos os examples daquele parâmetro, ou seja, se houver um parâmetro de um statement que não muda em todo o cenário, é possível inseri-lo diretamente no statement para diminuir o tamanho da tabela de examples que será analisada, isso pode ser feito com a seguinte sintaxe:

  > - Parâmetros normais que serão atribuidos na tabela de examples: `"<nome_do_parâmetro>"`
  > - Parâmetros com valores repetidos em um mesmo cenário: `"<nome_na_tabela=valor_do_parâmetro>"`

Onde `nome_na_tabela` é o nome que este parâmetro repetido deve receber na tabela de examples final, evitando conflitos de nomes entre parâmetros e evitando que parâmetros com valores distintos sejam confundidos.

Caso dois parâmetros na máscara tenham o mesmo nome, eles irão compartilhar uma coluna da tabela de examples, assim como nos feature files normais.

Um exemplo pode ser visto [aqui](./generic_api_testing/translator/examples/use_cases/dogFacts.mask).

Para desenvolvedores, também temos um exemplo da estrutura de dados que será construída a partir desta mesma máscara para facilitar alterações futuras [aqui](./generic_api_testing/translator/examples/data_structures/mask.json).

## DICTIONARIES

Como dito na seção anterior, temos que um statement customizado pode ser criado em uma feature mask, e este será traduzido por um dicionário.

Tais dicionários são arquivos .dict que deverão ser enviados em conjunto com uma máscara que contenha statements customizados, estes dicionários devem conter a definição do statement customizado e os parâmetros que este statement deve receber, além dos parâmetros que seus statements equivalentes recebem.

Além disso, os parâmetros passados no statement customizado podem ser inseridos nos valores dos statements equivalentes, ao colocar o nome do parâmetro customizado entre `@`.

A sintaxe de um dicionário é similar a de um arquivo Gherkin, porém, seguirá o padrão:

  > - Feature Dictionary: `(nome_do_dicionário)`:
    >   -  Statement: `(statement_customizado)`
      >       - `(statements_equivalentes)`
      >       - Statement Params:
        >            - `(nomes_dos_parametros)`
        >            - `(valores_dos_parametros)`

Além disto, os valores parametrizados no statement customizado podem ser injetados como valores de seus statements equivalentes, por exemplo:

  > - Statement Customizado: Tenho `"<quantidade_de_mangas>"` mangas
  > - Statement Equivalente: Comprei `"<quantidade_comprada>"` e comi `"<quantidade_comida>"`
  > - Nome dos Parâmetros:    |  quantidade_comprada     |  quantidade_comida  |
  > - Valores dos Parâmetros: |  @quantidade_de_mangas@  |  0                  |

Desta maneira, o valor parametrizado na máscara chamado `<quantidade_de_mangas>` será injetado no parâmetro `<quantidade_comprada>` de um de seus statements equivalentes.

Valores repetidos podem ser inseridos dentro do statement customizado e também podem ser injetados, e a injeção pode ser feita em diversas instâncias.

Um exemplo desta sintaxe pode ser visto [aqui](./generic_api_testing/translator/examples/use_cases/dictionary.dict).

Temos também um exemplo de um feature file final traduzido [aqui](./generic_api_testing/translator/examples/use_cases/translatedFeature.feature).

Para desenvolvedores, também temos um exemplo da estrutura de dados que será construída a partir do dicionário acima, para facilitar alterações futuras, [aqui](./generic_api_testing/translator/examples/data_structures/mask.json) e tambem do feature file traduzido [aqui](./generic_api_testing/translator/examples/data_structures/translatedMask.json).

## Copyright

Copyright © 2024 Opus Software

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
