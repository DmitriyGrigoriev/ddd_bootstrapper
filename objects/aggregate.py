from argparse import Namespace
from typing import Dict

import attr

from ddd_bootstrapper.objects.entity_identity import EntityIdentity
from ddd_bootstrapper.utils import DDD_LOGIC_PATH, DddObject, DddObjectType, AttributeName


@attr.dataclass(slots=True, frozen=True)
class Aggregate(DddObject):
    arg_short_name = "a"
    arg_long_name = "aggregate"
    help_text = "Specify the AggregateName (in CamelCase)"
    entity_id: 'EntityIdentity'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'entity_id': EntityIdentity.build_from_namespace(namespace, default_name=f'Identite{ddd_objects_name}'),
        }

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/domain/model"

    def get_python_class_code_definition(self) -> str:
        return f"""

{self.entity_id.get_python_class_code_definition()}

@attr.dataclass(slots=True)
class {self.name}(interface.RootEntity):
    entity_id: '{self.entity_id.name}'
"""

    def get_python_imports(self) -> str:
        return f"""
import attr

from osis_common.ddd import interface

"""
