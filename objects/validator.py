from argparse import Namespace
from typing import Dict

import attr

from ddd_bootstrapper.objects.business_exception import BusinessException
from ddd_bootstrapper.utils import DddObject, DDD_LOGIC_PATH, AttributeName


@attr.dataclass(slots=True, frozen=True)
class Validator(DddObject):
    arg_short_name = "v"
    arg_long_name = "validator"
    help_text = "Specify the ValidatorName (in CamelCase)"
    exc: 'BusinessException'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'exc': Validator.build_from_namespace(namespace),
        }

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/domain/validator"

    def get_python_class_code_definition(self) -> str:
        return f"""

@attr.dataclass(frozen=True, slots=True)
class {self.name}(BusinessValidator):

    def validate(self, *args, **kwargs):
        raise {self.exc.name}()
"""

    def get_python_imports(self) -> str:
        return f"""

import attr

from base.ddd.utils.business_validator import BusinessValidator
{self.exc.get_import_statement()}
"""
