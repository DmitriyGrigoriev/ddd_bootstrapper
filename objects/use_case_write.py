from argparse import Namespace
from typing import Dict

import attr

from ddd_bootsrapper.objects.command import Command
from ddd_bootsrapper.objects.repository_interface import RepositoryInterface
from ddd_bootsrapper.utils import DddObject, DDD_LOGIC_PATH, convert_camel_case_to_snake_case, AttributeName


@attr.dataclass(slots=True, frozen=True)
class UseCaseWrite(DddObject):
    arg_short_name = "ucw"
    arg_long_name = "use_case_write"
    help_text = "Specify the write use_case_name (in snake_case)"
    cmd: 'Command'
    i_repository: 'RepositoryInterface'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'cmd': Command.build_from_namespace(namespace, default_name=ddd_objects_name),
            'i_repository': RepositoryInterface.build_from_namespace(namespace),
        }

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/use_case/write"

    def get_filename_without_extension(self) -> str:
        filename = super().get_filename_without_extension()
        return f"{filename}_service"

    def get_python_class_code_definition(self) -> str:
        return f"""

def {convert_camel_case_to_snake_case(self.name)}(
        cmd: '{self.cmd.name}',
        repository: '{self.i_repository.get_python_class_name()}',
) -> '{self.i_repository.aggregate.name}':
    # GIVEN
    identite = {self.i_repository.aggregate.entity_id.name}(cmd)
    {convert_camel_case_to_snake_case(self.i_repository.aggregate.name)} = repository.get(identite) 
    
    # WHEN
    {convert_camel_case_to_snake_case(self.i_repository.aggregate.name)}.do_something()
    
    # THEN
    repository.save()
    
    return {convert_camel_case_to_snake_case(self.i_repository.aggregate.name)}.entity_id
"""

    def get_python_imports(self) -> str:
        return f"""

{self.cmd.get_import_statement()}
{self.i_repository.get_import_statement()}
{self.i_repository.aggregate.get_import_statement()}
{self.i_repository.aggregate.entity_id.get_import_statement()}
"""
