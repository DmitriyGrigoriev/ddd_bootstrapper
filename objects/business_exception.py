import attr

from ddd_bootsrapper.utils import DddObject, DDD_LOGIC_PATH


@attr.dataclass(slots=True, frozen=True)
class BusinessException(DddObject):
    arg_short_name = "be"
    arg_long_name = "business_exception"
    help_text = "Specify the BusinessExceptionName (in CamelCase)"

    @property
    def should_append_content_to_existing_file(self) -> bool:
        return True

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/domain/validator"

    def get_filename_without_extension(self) -> str:
        return "exceptions"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.name}(interface.BusinessException):
    def __init__(self, *args, **kwargs):
        message = _("{self.name}")
        super().__init__(message, **kwargs)
"""

    def get_python_imports(self) -> str:
        return f"""

from osis_common.ddd import interface
from django.utils.translation import gettext_lazy as _
"""
