import abc
import datetime
import os
import re
import typing
from argparse import Namespace
from enum import Enum

import attr

from ddd_bootstrapper.osis_license import get_osis_license

DDD_LOGIC_PATH = "ddd/logic"
INFRASTRUCTURE_PATH = "infrastructure"
TODAY = datetime.date.today()

AttributeName = str


class DddObjectType(Enum):
    AGGREGATE = 'aggregate'
    BUSINESS_EXCEPTION = 'business_exception'
    COMMAND = 'command'
    DOMAIN_SERVICE = 'domain_service'
    DTO = 'dto'
    ENTITY_ID = 'entity_id'
    QUERY = 'query'
    REPOSITORY = 'repository'
    REPOSITORY_INTERFACE = 'repository_interface'
    REPOSITORY_IN_MEMORY = 'repository_in_memory'
    USE_CASE_READ = 'use_case_read'
    USE_CASE_WRITE = 'use_case_write'
    VALIDATOR = 'validator'
    VALIDATOR_LIST = 'validator_list'
    VALUE_OBJECT = 'value_object'


@attr.dataclass(slots=True, frozen=True)
class DddobjectsFactory(abc.ABC):
    """Identifie les DddObjects à créer sur base du namespace"""

    @staticmethod
    def identify(namespace) -> typing.List['DddObject']:
        from ddd_bootstrapper.objects.aggregate import Aggregate
        ddd_objects_classes = [
            Aggregate,
        ]
        aggregate_name = getattr(namespace, Aggregate.arg_long_name, None)
        if aggregate_name:
            pass


@attr.dataclass(slots=True, frozen=True)
class DddObject(abc.ABC):
    type: typing.ClassVar[DddObjectType]
    context_name: str
    name: str
    arg_short_name: typing.ClassVar[str]  # TODO à déplacer dans Mixin séparé ?
    arg_long_name: typing.ClassVar[str]
    help_text: typing.ClassVar[str]

    @classmethod
    def build_from_namespace(cls, namespace: 'Namespace', default_name: str = None) -> typing.Optional['DddObject']:
        ddd_object_name = getattr(namespace, cls.arg_long_name, None) or default_name
        if not ddd_object_name:
            raise AttributeError(f'Please provide a {cls.__name__} name')
        dependencies = cls.init_dependencies(ddd_object_name, namespace)
        return cls(context_name=namespace.context, name=ddd_object_name, **dependencies)

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> typing.Dict['AttributeName', 'DddObject']:
        """
        If the DddObject depends on other DddObject, this method must return the args add to the instanciation
        of the objects.
        :param namespace: The namespace of the cmd line
        :return: A dictionary mapping the name of the DddObject attribute with its DddObject instance.
        """
        return {}

    @property
    def file_extension(self):
        return "py"

    @property
    def should_append_content_to_existing_file(self) -> bool:
        """
        False by default.
        :return: True if this DddObject should be appended at the end of non-empty file.
        """
        return False

    def get_filename_with_extension(self) -> str:
        """
        :return: The python filename (in snake case) of the DddObject (including extension)
        """
        return f"{self.get_filename_without_extension()}.{self.file_extension}"

    @abc.abstractmethod
    def get_path_to_folder(self) -> str:
        """
        :return: The path to the DddObject in the folder tree"
        """""
        pass

    @abc.abstractmethod
    def get_python_class_code_definition(self, **kwargs: 'DddObject') -> str:
        """
        :param kwargs: the required DddObjects used to generate the class code of this DddObject.
        :return: The python code definition of the class that represent this DddObject
        """
        pass

    @abc.abstractmethod
    def get_python_imports(self, **kwargs: 'DddObject') -> str:
        """
        :param kwargs: the required DddObjects used to generate pertinent imports
        used in the python class code definition
        :return: The code of the python imports
        """
        pass

    def get_filename_without_extension(self) -> str:
        """
        :return: The filename of this DddObject (excluding extension)
        """
        return convert_camel_case_to_snake_case(self.name)

    def get_import_statement(self) -> str:
        """
        :return: The code of the python import of this DddObject
        """
        path_to_folder = self.get_path_to_folder().replace('/', '.')
        return f"from {path_to_folder}.{self.get_filename_without_extension()} import {self.get_python_class_name()}"

    def get_python_class_name(self) -> str:
        """
        :return: The python class name in the code of this DddObject.
        """
        return self.name

    def write_in_file(self) -> None:
        change_or_make_dir(self.get_path_to_folder())
        with open(self.get_filename_with_extension(), "a+") as f:
            if is_empty(self.get_filename_with_extension()):
                f.write(get_osis_license())
                f.write(self.get_python_imports())
                f.write(self.get_python_class_code_definition())  # TODO :: DddObject.prerequisites -> Dict[str, DddObject] ou DddObjectInvokation ?
            elif self.should_append_content_to_existing_file:
                current_position = f.tell()
                f.seek(0)
                if f"class {self.name}" not in str(f.read()):  # évite les doublons
                    f.seek(current_position)
                    f.write(self.get_python_class_code_definition())
        back_to_main_folder()


def convert_camel_case_to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def create__init__py():
    filename = "__init__.py"
    with open(filename, "a+") as f:
        pass


def change_or_make_dir(path: str):
    for dir_name in path.split('/'):
        try:
            os.chdir(dir_name)
        except FileNotFoundError:
            os.mkdir(dir_name)
            os.chdir(dir_name)
            create__init__py()


def is_empty(filename: str) -> bool:
    return os.stat(filename).st_size == 0


def back_to_main_folder() -> None:
    from ddd_bootstrapper.launcher import CURRENT_DIR
    os.chdir(CURRENT_DIR)
