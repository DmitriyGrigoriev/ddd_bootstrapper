import attr

from ddd_bootsrapper.utils import DDD_LOGIC_PATH, DddObject


@attr.dataclass(slots=True, frozen=True)
class DomainService(DddObject):
    arg_short_name = "ds"
    arg_long_name = "domain_service"
    help_text = "Specify the DomainServiceName (in CamelCase)"

    def get_path_to_folder(self) -> str:
        return f"{DDD_LOGIC_PATH}/{self.context_name}/domain/service"

    def get_python_class_code_definition(self) -> str:
        return f"""

class {self.name}(interface.DomainService):
    @classmethod
    def do_something(
            cls,
    ) -> None:
        raise NotImplementedError
"""

    def get_python_imports(self) -> str:
        return f"""
from osis_common.ddd import interface
"""
