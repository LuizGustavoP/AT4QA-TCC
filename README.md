# AT4QA Project

**Implementing Autonomous Generic Testing for Behaviour Driven Development (AGBDD) for Web APIs as a Capstone Project**

# Introduction

## BDD

This repository contains the implementation of an Autonomous Generic Behaviour Driven Development system, in this case focused on Web API development.

In this implementation, we have devided our elements in 3 main types that are inherent to Gherkin based BDD, they are:

  > **`Feature Files`**

  > **`Step Definitions`**

  > **`Classes`**

We also have 2 new definitions specific to AGBDD, which are:

  > **`Feature Masks`**

  > **`Statement Dictionaries`**

## Feature Files

Feature Files contain the test cases that are to be executed, described using natural language.

These test cases are defined as `Scenarios`, in our case, we will be using exclusively `Scenario Outlines`, which are a subset of Gherkin scenarios which allow us to introduce parameters in the statements. 

Gherkin utilizes 4 main key words to define the order

- **`Given`**: Describes the environment in which a test subject must find itself before being tested.

- **`When`**: Describes the way in which a subject must be tested.

- **`Then`**: Describes the behaviours we expect to arise as a consequence of executing the subject.

- **`And`**: Ascribes to its statement the same key word as the last statement defined with a different key word.

Our feature files will be located in the following directory:

  > **`/generic_api_testing/features`**

## Classes

Classes are the files that contain code implementation of a specific behaviour.

In our case, they are the files which will contain generic overall behaviours expected from Web API Testing, such as making requests, evaluating returned values, and so on.

All classes will be located in the following directory:

 > **`/generic_api_testing/test_classes`**

## Step Definitions

Step Definitions are the files which will link a statement contained in a given feature file, to its respective programmed behaviour in a class.

Therefore, they will be the ones connecting our programmed behaviours to the natural language contained in feature files.

Our Step Definitions will be located in the following directory:

  > **`/generic_api_testing/step_defs`**

## Pytest.ini

The pytest.ini file contains general settings of the pytest library, such as the location of the feature file directory, test markes, addopted default command line parameters and so on.

## Conftest.py

The conftest.py file will contain hooks and expected environmental settings that must be present in every test, with specific hooks to define what we want to be done before all tests, and after all tests.

It also contains the definitions of custom command line parameters.

# INSTALLATION
## USING A VIRTUAL ENVIRONMENT

- Before executing the tests, create a directory name `venv`, and run the following command on your terminal:

    > \> `python3 -m venv /path/to/new/virtual/environment`

    Open **`pyvenv.cfg`** located in **`venv`** and modify `'home'` to the *Python* base path in your system. If you don't know where it is, open your command prompt and run:

    > \> `where python`

    With that, you can run the following command to activate your virtual environment:

    > \> `.\venv\Scripts\activate`

## BEFORE EXECUTING

- Install the necessary dependencies, located in the file **`requirements.txt`**. To do so, run the following command:

    > \> `pip install -r requirements.txt`

## TESTS

- To run a test for a given feature file, run the following command:

    > \> `pytest .\generic_api_testing\step_defs\custom\test_Custom.py -m "<tag>"`

    The argument **`-m "<tag>"`** refers to the tags contained in the feature file, which have to be defined in order to determined which test cases are to be executed.

- If you want to run all tests, use the following command:
  
    > \> `pytest .\generic_api_testing\step_defs\custom\test_Custom.py`

## GENERIC FEATURE FILES

The defining feature of AGBDD is the use of generic statements that define the macro behaviours of our test area, in this case, the macro behaviours relevant to Web API testing.

A glossary containing all of our generic statements, as well as examples and use cases, can be found [here](./generic_statement_glossary.md).

## FEATURE MASKS

Aside from the creation of Feature Files, another main aspect of AGBDD is the use of Feature Masks.

Feature Masks are summarizations of generic feature files, which allows testers to focus on the relevant aspects of their current testing subjects, and to return to a natural language environment which is inherent to traditional BDD, by allowing the use of custom statements.

It does this by working in tandem with another element of AGBDD, Statement Dictionaries, which will be discussed in the next section.

A feature mask's syntax is similar to a feature file's, being defined as such:

  > - Feature: `(feature_name)`:
    >   -  Scenario Mask: `(scenario_name)`
      >       - `(statements)`
      >       - Examples:
        >            - | `(parameter_names)`  |
        >            - | `(parameter_values)` |

In a feature mask, parameters that have a repeated value in all examples of its scenario can be inserted directly in the statement:

  > - Normal parêmters with values on the Examples table: `"<parameter_name>"`
  > - Parameters with repeating values in the entire scenario: `"<parameter_name=parameter_value>"`

Where `parameter_name` will be the name of the parameter's column in the Examples table.

If two parameters have the same name, they will share the column, just like in a Feature File.

An example of a Feature Mask can be found in [here](./generic_api_testing/translator/examples/use_cases/dogFacts.mask).

We also have examples of the data structures used in the translation process [here](./generic_api_testing/translator/examples/data_structures/mask.json).

## DICTIONARIES

As was introduced in the previous section, it is possible to create custom statements through the use of Feature Masks and Statement Dictionaries.

These dicitionaries are .dict files that contain the definitions for custom statements, which includes their generic counterparts, and their respective values

A dictionary's syntax is similar to a Gherkin file, being defined as:

  > - Feature Dictionary: `(dictionary_name)`:
    >   -  Statement: `(custom_statement)`
      >       - `(equivalent_statement)`
      >       - Statement Params:
        >            - `(parameter_names)`
        >            - `(parameter_values)`

Parameters can also be passed through custom statements, and can be inserted into their generic counterparts by putting their names into the examples table between `@`, such as the following example:

  > - Custom Statement: I have `"<potion_amount>"` potions
  > - Equivalent Statement: I bought `"<amount_bought>"` and used `"<amount_used>"`
  > - Parameter Names:    |  amount_bought   | amount_used |
  > - Parameter Values:   |  @potion_amount@ |  0          |

With this, the parametized value in the mask `<potion_amount>` will be injected in the parameter `<amount_bought>` of one of its equivalent statements.

Repeated values can be injected in the same way, and the injection can be used on multiple equivalent statements at the same time.

An example of this syntax can be found [here](./generic_api_testing/translator/examples/use_cases/dictionary.dict).

We also have an example of a translated product of a mask and a dictionary [here](./generic_api_testing/translator/examples/use_cases/dogFacts.feature).

There is also an example of the data structure used in the construction of dictionaries [here](./generic_api_testing/translator/examples/data_structures/dict.json) and of a translated feature file [here](./generic_api_testing/translator/examples/data_structures/translatedFeature.json).

## Copyright

Copyright © 2024 Opus Software

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
