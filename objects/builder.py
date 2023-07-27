# TODO
# import attr
#
# from ddd_bootstrapper.utils import DDD_LOGIC_PATH, DddObject
#
#
# @attr.dataclass(slots=True, frozen=True)
# class Builder(DddObject):
#     arg_short_name = "b"
#     arg_long_name = "builder"
#     help_text = "Specify the Builder class name (in CamelCase)"
#
#     def get_path_to_folder(self) -> str:
#         return f"{DDD_LOGIC_PATH}/{self.context_name}/builder"
#
#     def get_python_class_code_definition(self) -> str:
#         return f"""
#
# class {self.name}(interface.RootEntityBuilder):
#     @classmethod
#     def build_from_command(cls, cmd: 'CommandRequest') -> 'ActivitesAideALaReussite':
#         pass
#
#     @classmethod
#     def build_from_repository_dto(cls, dto_object: 'ActivitesAideALaReussiteDTO') -> 'ActivitesAideALaReussite':
#         return cls.build(
#             noma=dto_object.noma,
#             annee=dto_object.annee,
#             code_programme=dto_object.code_programme,
#             suivies_par_etudiant=dto_object.inscription_completee_par_des_aar,
#             demandees_par_etudiant=dto_object.demande_faite_par_etudiant
#         )
# """
#
#     def get_python_imports(self) -> str:
#         return f"""
# from osis_common.ddd import interface
# """
