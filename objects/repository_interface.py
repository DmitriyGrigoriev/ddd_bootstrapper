from argparse import Namespace
from typing import Dict

import attr

from ddd_bootsrapper.objects.aggregate import Aggregate
from ddd_bootsrapper.objects.dto import DTO
from ddd_bootsrapper.objects.entity_identity import EntityIdentity
from ddd_bootsrapper.utils import DDD_LOGIC_PATH, DddObject, AttributeName


@attr.dataclass(slots=True, frozen=True)
class RepositoryInterface(DddObject):
    arg_short_name = "r"
    arg_long_name = "repository"
    help_text = "Specify the RepositoryName (in CamelCase)"
    aggregate: 'Aggregate'
    dto: 'DTO'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'aggregate': Aggregate.build_from_namespace(namespace, default_name=ddd_objects_name),
            'dto': DTO.build_from_namespace(namespace, default_name=ddd_objects_name),
        }

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/repository"

    def get_filename_without_extension(self) -> str:
        filename = super().get_filename_without_extension()
        return f"i_{filename}"

    def get_python_class_name(self):
        return f"I{self.name}Repository"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.get_python_class_name()}(interface.AbstractRepository):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: '{self.aggregate.entity_id.name}') -> '{self.aggregate.name}':
        pass

    @classmethod
    @abc.abstractmethod
    def search(
        cls,
        entity_ids: Optional[List['{self.aggregate.entity_id.name}']] = None,
        **kwargs
    ) -> List['{self.aggregate.name}']:
        pass

    @classmethod
    @abc.abstractmethod
    def delete(cls, entity_id: '{self.aggregate.entity_id.name}', **kwargs) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def save(cls, pae: '{self.aggregate.name}') -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def get_dto(cls, entity_id: '{self.aggregate.entity_id.name}') -> '{self.dto.name}':
        pass
"""

    def get_python_imports(self) -> str:
        return f"""
import abc
from typing import Optional, List

{self.aggregate.get_import_statement()}
{self.aggregate.entity_id.get_import_statement()}
{self.dto.get_import_statement()}
from osis_common.ddd import interface

"""
