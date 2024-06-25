import json
from dataclasses import dataclass

from dacite import from_dict


# from dataclasses_json import dataclass_json, LetterCase
# import msgspec


# @dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PatientIdentityDocV:
    IdentitySeries: str  # Серия документа, должен
    IdentityNumber: str  # Номер документа, обязан
    IdentityIssueOrgName: str  # Наименование организации, выдавшей документ, должен
    IdentityIssueOrgCode: str  # Код подразделения организации, выдавшей документ, должен
    IdentityIssueDate: str  # Дата выдачи документа, обязан


# @dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PatientInsurancePolicyV:
    Series: str  # Серия полиса ОМС, не обязан
    Number: str  # Номер полиса ОМС, обязан


# @dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PatientRoleV:
    PatientId: str  # Уникальный идентификатор пациента в МИС, обязан
    SnilsId: str  # СНИЛС пациента, обязан
    IdentityDoc: PatientIdentityDocV  # Документ, удостоверяющий личность пациента, серия, номер, кем выдан, должен
    InsurancePolicy: PatientInsurancePolicyV  # Полис ОМС, обязан


def read_json_v() -> PatientRoleV:
    with open('variable.json') as f:
        json_data = json.load(f)
        print(type(json_data))
        print(f'>>>{json_data}')

        # c1 = PatientIdentityDocV.from_json(json.dumps(json_data))
    c1 = from_dict(data_class=PatientRoleV, data=json_data)
    print(type(c1))

    # c1 = PatientIdentityDocV
    # c1 = PatientIdentityDocV.from_json(json_data)
    print(c1)
    return c1
