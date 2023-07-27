from argparse import Namespace
from typing import Dict

import attr

from ddd_bootsrapper.objects.value_object import ValueObject
from ddd_bootsrapper.utils import DddObject, DDD_LOGIC_PATH, AttributeName


@attr.dataclass(slots=True, frozen=True)
class TranslatorInterface(DddObject):
    arg_short_name = "ti"
    arg_long_name = "translator_interface"
    help_text = "Specify the TranslatorInterfaceName (in CamelCase)"
    value_object: 'ValueObject'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'value_object': ValueObject.build_from_namespace(namespace),
        }

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/domain/service"

    def get_filename_without_extension(self) -> str:
        filename = super().get_filename_without_extension()
        return f"i_{filename}"

    def get_python_class_name(self):
        return f"I{self.name}Translator"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.get_python_class_name()}(interface.DomainService):
    @classmethod
    @abc.abstractmethod
    def get(
        cls,
    ) -> '{self.value_object.name}':
        pass    

    @classmethod
    @abc.abstractmethod
    def search(
        cls,
    ) -> List['{self.value_object.name}']:
        pass
"""

    def get_python_imports(self) -> str:
        return f"""
import abc
from typing import List

{self.value_object.get_import_statement()}
from osis_common.ddd import interface
"""
