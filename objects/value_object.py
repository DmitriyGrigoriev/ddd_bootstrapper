import attr

from ddd_bootsrapper.utils import DDD_LOGIC_PATH, DddObject


@attr.dataclass(slots=True, frozen=True)
class ValueObject(DddObject):
    arg_short_name = "vo"
    arg_long_name = "value_object"
    help_text = "Specify the ValueObjectName (in CamelCase)"

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/domain/model"

    def get_filename_without_extension(self) -> str:
        filename = super().get_filename_without_extension()
        return f"_{filename}"

    def get_python_class_code_definition(self) -> str:
        return f"""

@attr.dataclass(frozen=True, slots=True)
class {self.name}(interface.ValueObject):
    pass
"""

    def get_python_imports(self) -> str:
        return f"""
import attr

from osis_common.ddd import interface
"""
