from argparse import Namespace
from typing import Dict

import attr

from ddd_bootstrapper.objects.translator_interface import TranslatorInterface
from ddd_bootstrapper.utils import DddObject, INFRASTRUCTURE_PATH, AttributeName


@attr.dataclass(slots=True, frozen=True)
class TranslatorInMemory(DddObject):
    arg_short_name = "tim"
    arg_long_name = "translator_in_memory"
    help_text = "Specify the TranslatorName (in CamelCase)"
    i_translator: 'TranslatorInterface'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'i_translator': TranslatorInterface.build_from_namespace(namespace, default_name=ddd_objects_name),
        }

    def get_path_to_folder(self) -> str:
        return f"{INFRASTRUCTURE_PATH}/{self.context_name}/domain/service/in_memory"

    def get_python_class_name(self):
        return f"{self.name}InMemoryTranslator"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.name}({self.i_translator.get_python_class_name()}):
    @classmethod
    def get(
        cls,
    ) -> '{self.i_translator.value_object.name}':
        raise NotImplementedError    

    @classmethod
    def search(
        cls,
    ) -> List['{self.i_translator.value_object.name}']:
        raise NotImplementedError
"""

    def get_python_imports(self) -> str:
        return f"""
from typing import List

{self.i_translator.get_import_statement()}
{self.i_translator.value_object.get_import_statement()}
"""
