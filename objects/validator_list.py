from argparse import Namespace
from typing import Dict

import attr

from ddd_bootstrapper.objects.validator import Validator
from ddd_bootstrapper.utils import DddObject, DDD_LOGIC_PATH, AttributeName


@attr.dataclass(slots=True, frozen=True)
class ValidatorList(DddObject):
    arg_short_name = "vl"
    arg_long_name = "validator_list"
    help_text = "Specify the ValidatorListName (in CamelCase)"
    validator: 'Validator'

    @classmethod
    def init_dependencies(
            cls,
            ddd_objects_name: str,
            namespace: 'Namespace',
    ) -> Dict['AttributeName', 'DddObject']:
        return {
            'i_repository': Validator.build_from_namespace(namespace),
        }

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/domain/validator"

    def get_filename_without_extension(self) -> str:
        return "validators_by_business_action"

    def get_python_class_code_definition(self) -> str:
        return f"""

@attr.dataclass(frozen=True, slots=True)
class {self.name}(TwoStepsMultipleBusinessExceptionListValidator):

    def get_data_contract_validators(self) -> List[BusinessValidator]:
        return []

    def get_invariants_validators(self) -> List[BusinessValidator]:
        return [
            {self.validator.name}(),
        ]
"""

    def get_python_imports(self) -> str:
        return f"""

from typing import List

import attr

from base.ddd.utils.business_validator import TwoStepsMultipleBusinessExceptionListValidator, BusinessValidator
{self.validator.get_import_statement()}
"""
