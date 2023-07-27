from argparse import Namespace
from typing import Dict

import attr

from ddd_bootstrapper.objects.query import Query
from ddd_bootstrapper.objects.repository_interface import RepositoryInterface
from ddd_bootstrapper.utils import DddObject, DDD_LOGIC_PATH, convert_camel_case_to_snake_case, AttributeName


@attr.dataclass(slots=True, frozen=True)
class UseCaseRead(DddObject):
    arg_short_name = "ucr"
    arg_long_name = "use_case_read"
    help_text = "Specify the read use_case_name (in snake_case)"
    query: 'Query'
    i_repository: 'RepositoryInterface'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'query': Query.build_from_namespace(namespace),
            'i_repository': RepositoryInterface.build_from_namespace(namespace),
        }

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/use_case/read"

    def get_filename_without_extension(self) -> str:
        filename = super().get_filename_without_extension()
        return f"{filename}_service"

    def get_python_class_code_definition(self) -> str:
        return f"""

def {convert_camel_case_to_snake_case(self.name)}(
        query: '{self.query.name}',
        repository: '{self.i_repository.name}',
) -> '{self.i_repository.dto.name}':
    return repository.get_dto()
"""

    def get_python_imports(self) -> str:
        return f"""

{self.query.get_import_statement()}
{self.i_repository.get_import_statement()}
{self.i_repository.dto.get_import_statement()}
"""
