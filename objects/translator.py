from argparse import Namespace
from typing import Dict

import attr

from ddd_bootstrapper.objects.translator_in_memory import TranslatorInMemory
from ddd_bootstrapper.objects.translator_interface import TranslatorInterface
from ddd_bootstrapper.utils import DddObject, INFRASTRUCTURE_PATH, AttributeName


@attr.dataclass(slots=True, frozen=True)
class Translator(DddObject):
    arg_short_name = "t"
    arg_long_name = "translator"
    help_text = "Specify the TranslatorName (in CamelCase)"
    i_translator: 'TranslatorInterface'
    translator_in_memory: 'TranslatorInMemory'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'i_translator': TranslatorInterface.build_from_namespace(namespace, default_name=ddd_objects_name),
            'translator_in_memory': TranslatorInMemory.build_from_namespace(namespace, default_name=ddd_objects_name),
        }

    def get_path_to_folder(self) -> str:
        return f"{INFRASTRUCTURE_PATH}/{self.context_name}/domain/service"

    def get_python_class_name(self):
        return f"{self.name}Translator"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.get_python_class_name()}({self.i_translator.get_python_class_name()}):
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
