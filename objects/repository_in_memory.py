from argparse import Namespace
from typing import Dict

import attr

from ddd_bootsrapper.objects.repository_interface import RepositoryInterface
from ddd_bootsrapper.utils import DddObject, INFRASTRUCTURE_PATH, AttributeName


@attr.dataclass(slots=True, frozen=True)
class RepositoryInMemory(DddObject):
    arg_short_name = "rim"
    arg_long_name = "repository_in_memory"
    help_text = "Specify the RepositoryInMemoryName (in CamelCase)"
    i_repository: 'RepositoryInterface'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'i_repository': RepositoryInterface.build_from_namespace(namespace, default_name=ddd_objects_name),
        }

    def get_path_to_folder(self) -> str:
        return f"{INFRASTRUCTURE_PATH}/{self.context_name}/repository/in_memory"

    def get_python_class_name(self):
        return f"{self.name}InMemoryRepository"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.get_python_class_name()}(InMemoryGenericRepository, {self.i_repository.get_python_class_name()}):
 
    @classmethod
    def get_dto(cls, entity_id: '{self.i_repository.aggregate.entity_id.name}') -> '{self.i_repository.dto.name}':
        raise NotImplementedError
"""

    def get_python_imports(self) -> str:
        return f"""
from typing import Optional, List

from base.ddd.utils.in_memory_repository import InMemoryGenericRepository
{self.i_repository.aggregate.get_import_statement()}, {self.i_repository.aggregate.entity_id.get_python_class_name()}
{self.i_repository.dto.get_import_statement()}
{self.i_repository.get_import_statement()}

"""
