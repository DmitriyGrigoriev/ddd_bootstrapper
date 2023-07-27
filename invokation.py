from typing import Type, List

import attr

from ddd_bootstrapper.objects.aggregate import Aggregate
from ddd_bootstrapper.objects.business_exception import BusinessException
from ddd_bootstrapper.objects.command import Command
from ddd_bootstrapper.objects.domain_service import DomainService
from ddd_bootstrapper.objects.dto import DTO
from ddd_bootstrapper.objects.query import Query
from ddd_bootstrapper.objects.repository import Repository
from ddd_bootstrapper.objects.repository_in_memory import RepositoryInMemory
from ddd_bootstrapper.objects.repository_interface import RepositoryInterface
from ddd_bootstrapper.objects.translator import Translator
from ddd_bootstrapper.objects.translator_in_memory import TranslatorInMemory
from ddd_bootstrapper.objects.translator_interface import TranslatorInterface
from ddd_bootstrapper.objects.use_case_read import UseCaseRead
from ddd_bootstrapper.objects.use_case_write import UseCaseWrite
from ddd_bootstrapper.objects.validator import Validator
from ddd_bootstrapper.objects.validator_list import ValidatorList
from ddd_bootstrapper.objects.value_object import ValueObject
from ddd_bootstrapper.utils import DddObject


DddObjectClass: Type[DddObject]


@attr.dataclass(slots=True, frozen=True)
class DddObjectInvokation:
    short_name: str
    long_name: str
    description: str
    ddd_object_class: List[DddObjectClass]


commands = [
    DddObjectInvokation(
        short_name='-a',
        long_name='--aggregate',
        description="Specify the AggregateName (in CamelCase)",
        ddd_object_class=[Aggregate]
    ),
    DddObjectInvokation(
        short_name='-be',
        long_name='--business_exception',
        description="Specify the BusinessExceptionName (in CamelCase)",
        ddd_object_class=[BusinessException]
    ),
    DddObjectInvokation(
        short_name='-cmd',
        long_name='--command',
        description="Specify the CommandName (in CamelCase)",
        ddd_object_class=[Command]
    ),
    DddObjectInvokation(
        short_name='-ds',
        long_name='--domain_service',
        description="Specify the DomainServiceName (in CamelCase)",
        ddd_object_class=[DomainService]
    ),
    DddObjectInvokation(
        short_name='-d',
        long_name='--dto',
        description="Specify the DTOName (in CamelCase)",
        ddd_object_class=[DTO]
    ),
    DddObjectInvokation(
        short_name='-q',
        long_name='--query',
        description="Specify the QueryName (in CamelCase)",
        ddd_object_class=[Query]
    ),
    DddObjectInvokation(
        short_name='-r',
        long_name='--repository',
        description="Specify the RepositoryName (in CamelCase)",
        ddd_object_class=[Repository, RepositoryInterface, RepositoryInMemory]
    ),
    DddObjectInvokation(
        short_name='-t',
        long_name='--translator',
        description="Specify the TranslatorName (in CamelCase)",
        ddd_object_class=[Translator, TranslatorInterface, TranslatorInMemory]
    ),
    DddObjectInvokation(
        short_name='-ucr',
        long_name='--use_case_read',
        description="Specify the read use_case_name (in snake_case)",
        ddd_object_class=[UseCaseRead]
    ),
    DddObjectInvokation(
        short_name='-ucw',
        long_name='--use_case_write',
        description="Specify the write use_case_name (in snake_case)",
        ddd_object_class=[UseCaseWrite]
    ),
    DddObjectInvokation(
        short_name='-v',
        long_name='--validator',
        description="Specify the ValidatorName (in CamelCase)",
        ddd_object_class=[Validator]
    ),
    DddObjectInvokation(
        short_name='-vl',
        long_name='--validator_list',
        description="Specify the ValidatorListName (in CamelCase)",
        ddd_object_class=[ValidatorList]
    ),
    DddObjectInvokation(
        short_name='-vo',
        long_name='--value_object',
        description="Specify the ValueObjectName (in CamelCase)",
        ddd_object_class=[ValueObject()]
    ),
    # DddObjectInvokation(
    # short_name='-e',
    # long_name='--entity',
    # description="Specify the EntityName (in CamelCase)"),  TODO
    # DddObjectInvokation(
    # short_name='-c',
    # long_name='--context',
    # description="Specify the context_name (in snake_case)"),  TODO
    # DddObjectInvokation(
    # short_name='-all',
    # long_name='--all_packages',
    # description="Creates all DDD python packages"),  TODO
]
