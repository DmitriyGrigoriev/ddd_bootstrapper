import argparse
import contextlib
import os
import sys
from argparse import Namespace
from typing import Set, List, Type

from ddd_bootsrapper.objects.aggregate import Aggregate
from ddd_bootsrapper.objects.business_exception import BusinessException
from ddd_bootsrapper.objects.command import Command
from ddd_bootsrapper.objects.domain_service import DomainService
from ddd_bootsrapper.objects.dto import DTO
from ddd_bootsrapper.objects.entity_identity import EntityIdentity
from ddd_bootsrapper.objects.query import Query
from ddd_bootsrapper.objects.repository import Repository
from ddd_bootsrapper.objects.repository_in_memory import RepositoryInMemory
from ddd_bootsrapper.objects.repository_interface import RepositoryInterface
from ddd_bootsrapper.objects.translator import Translator
from ddd_bootsrapper.objects.translator_in_memory import TranslatorInMemory
from ddd_bootsrapper.objects.translator_interface import TranslatorInterface
from ddd_bootsrapper.objects.use_case_read import UseCaseRead
from ddd_bootsrapper.objects.use_case_write import UseCaseWrite
from ddd_bootsrapper.utils import DddObject, create__init__py
from ddd_bootsrapper.objects.validator import Validator
from ddd_bootsrapper.objects.validator_list import ValidatorList
from ddd_bootsrapper.objects.value_object import ValueObject


CURRENT_DIR = "/".join([f for f in os.getcwd().split('/')])  # FIXME equivalent "cd .."

DDD_CLASSES = [
    Aggregate,
    BusinessException,
    Command,
    DomainService,
    DTO,
    EntityIdentity,
    Query,
    Repository,
    RepositoryInMemory,
    RepositoryInterface,
    Translator,
    TranslatorInMemory,
    TranslatorInterface,
    UseCaseRead,
    UseCaseWrite,
    Validator,
    ValidatorList,
    ValueObject,
]


def execute():
    namespace = parse_arguments()
    ddd_objects = DddObjectFactory.build(namespace)
    for ddd_object in ddd_objects:
        ddd_object.write_in_file()


def is_empty(filename: str) -> bool:
    return os.stat(filename).st_size == 0


def change_or_make_dir(path: str):
    for dir_name in path.split('/'):
        try:
            os.chdir(dir_name)
        except FileNotFoundError:
            os.mkdir(dir_name)
            os.chdir(dir_name)
            create__init__py()


def back_to_main_folder() -> None:
    os.chdir(CURRENT_DIR)


def parse_arguments() -> 'Namespace':
    parser = argparse.ArgumentParser(
        description='Creates directories, files and objects from DDD tactical patterns. '
                    'All params can be used separately or you can combine all parameters.'
    )
    parser.add_argument('-c', '--context', help="Specify the context_name (in snake_case)", type=str, required=True)
    # TODO
    parser.add_argument('-e', '--entity', help="Specify the EntityName (in CamelCase)", type=str, required=False)
    parser.add_argument('-all', '--all_packages', help="Creates all DDD python packages", action='store_true', required=False)

    for klass in DDD_CLASSES:
        with contextlib.suppress(argparse.ArgumentError): # Dans les cas ou un même arg est utilisé pour plusieurs objets DDD (ex: repository)
            parser.add_argument(f"-{klass.arg_short_name}", f"--{klass.arg_long_name}", help=f"{klass.help_text}", type=str, required=False)

    # TODO :: tests translator + test repo + test use case
    return parser.parse_args(sys.argv[1:])


class DddObjectFactory:
    @staticmethod
    def build(namespace: 'Namespace') -> Set['DddObject']:
        assert namespace.context, "Please provide a context name with -c"
        objects = []
        for klass in DDD_CLASSES:
            if getattr(namespace, klass.arg_long_name, None):
                ddd_obj = klass.build_from_namespace(namespace)
                objects.append(ddd_obj)
                objects.extend(DddObjectFactory._init_dependencies_recursively(namespace, ddd_obj))
        return set(objects)

    @staticmethod
    def _init_dependencies_recursively(namespace: 'Namespace', ddd_object: 'DddObject') -> List['DddObject']:
        result = []
        for obj in ddd_object.init_dependencies(ddd_object.name, namespace).values():
            result.append(obj)
            result.extend(DddObjectFactory._init_dependencies_recursively(namespace, obj))
        return result


execute()
