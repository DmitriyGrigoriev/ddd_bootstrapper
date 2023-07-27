# ddd-bootstrapper
Provide utilities to generate files and code implementing tactical patterns of the Domain Driven Design.

## Patterns
- Dependency inversion through dependency injection and interface declaration
- Anticorruption layer through translators objects
- Repository
- Command Query Separation through read and write use cases with queries and commands


## Usage

`python3 launcher.py -c MyBoundedContext -ucw my_use_case_to_write_sth -a MyAggregateName -r MyRepositoryName -t MyTranslatorName -d MyDataTransferObjectName`

