import attr

from ddd_bootstrapper.utils import DDD_LOGIC_PATH, DddObject


@attr.dataclass(slots=True, frozen=True)
class Query(DddObject):
    arg_short_name = "q"
    arg_long_name = "query"
    help_text = "Specify the QueryName (in CamelCase)"

    @property
    def should_append_content_to_existing_file(self) -> bool:
        return True

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}"

    def get_filename_without_extension(self) -> str:
        return "commands"

    def get_python_class_code_definition(self) -> str:
        return f"""

@attr.dataclass(frozen=True, slots=True)
class {self.name}(interface.QueryRequest):
    integer: int
    string: str
    boolean: bool
    decim: Decimal
    liste: List
"""

    def get_python_imports(self) -> str:
        return f"""
from decimal import Decimal
from typing import Optional, List

import attr

from osis_common.ddd import interface

"""
