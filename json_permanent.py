import json
from dataclasses import dataclass, field
from dacite import from_dict


@dataclass
class PatientRoleP:
    IdentityCardType: str       # тип документа удостоверяющего личность, обязан
    InsurancePolicyType: str    # Тип полиса ОМС, обязан


def read_json_p() -> PatientRoleP:
    with open('permanent.json') as f:
        json_data = json.load(f)
        print(type(json_data))
        print(f'>>>{json_data}')

        c1 = from_dict(data_class=PatientRoleP, data=json_data)
        print(c1)

        #obj = json.loads(c1.InsurancePolicyType)
        #print(obj)

        return c1