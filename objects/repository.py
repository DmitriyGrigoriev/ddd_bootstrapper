from argparse import Namespace
from typing import Dict

import attr

from ddd_bootstrapper.objects.repository_in_memory import RepositoryInMemory
from ddd_bootstrapper.objects.repository_interface import RepositoryInterface
from ddd_bootstrapper.utils import INFRASTRUCTURE_PATH, DddObject, AttributeName


@attr.dataclass(slots=True, frozen=True)
class Repository(DddObject):
    arg_short_name = "r"
    arg_long_name = "repository"
    help_text = "Specify the RepositoryName (in CamelCase)"
    i_repository: 'RepositoryInterface'
    in_memory_repository: 'RepositoryInMemory'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'i_repository': RepositoryInterface.build_from_namespace(namespace, default_name=ddd_objects_name),
            'in_memory_repository': RepositoryInMemory.build_from_namespace(namespace, default_name=ddd_objects_name),
        }

    def get_path_to_folder(self) -> str:
        return f"{INFRASTRUCTURE_PATH}/{self.context_name}/repository"

    def get_python_class_name(self):
        return f"{self.name}Repository"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.get_python_class_name()}({self.i_repository.get_python_class_name()}):
    @classmethod
    def get(cls, entity_id: '{self.i_repository.aggregate.entity_id.name}') -> '{self.i_repository.aggregate.name}':
        raise NotImplementedError

    @classmethod
    def search(
        cls,
        entity_ids: Optional[List['{self.i_repository.aggregate.entity_id.name}']] = None,
        **kwargs
    ) -> List['{self.i_repository.aggregate.name}']:
        raise NotImplementedError

    @classmethod
    def delete(cls, entity_id: '{self.i_repository.aggregate.entity_id.name}', **kwargs) -> None:
        raise NotImplementedError

    @classmethod
    def save(cls, pae: '{self.i_repository.aggregate.name}') -> None:
        raise NotImplementedError

    @classmethod
    def get_dto(cls, entity_id: '{self.i_repository.aggregate.entity_id.name}') -> '{self.i_repository.dto.get_python_class_name()}':
        raise NotImplementedError
"""

    def get_python_imports(self) -> str:
        return f"""
from typing import Optional, List

{self.i_repository.aggregate.get_import_statement()}, {self.i_repository.aggregate.entity_id.get_python_class_name()}
{self.i_repository.dto.get_import_statement()}
{self.i_repository.get_import_statement()}
"""
