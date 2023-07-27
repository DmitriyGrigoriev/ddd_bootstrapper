import attr

from ddd_bootstrapper.utils import DddObject, DDD_LOGIC_PATH


@attr.dataclass(slots=True, frozen=True)
class DTO(DddObject):
    arg_short_name = "d"
    arg_long_name = "dto"
    help_text = "Specify the DTOName (in CamelCase)"

    @property
    def should_append_content_to_existing_file(self) -> bool:
        return True

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/dto"

    def get_python_class_name(self):
        return f"{self.name}DTO"

    def get_python_class_code_definition(self) -> str:
        return f"""

@attr.s(frozen=True, slots=True, auto_attribs=True)
class {self.get_python_class_name()}(interface.DTO):
    integer: int
    string: str
    boolean: bool
"""

    def get_python_imports(self) -> str:
        return f"""
import attr

from osis_common.ddd import interface
"""
