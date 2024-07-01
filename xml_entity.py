import json
from dataclasses import dataclass, field
from dacite import from_dict

@dataclass
class Entity:
    id: str              # уникальный идентификатор тега
    title: str           # название тега
    comment: str = ""    # комментарий, идущий перед тегом
    attributes: dict = field(default=dict)  # аттрибуты тега
    value: str | None = None  # текст тега
    child: list['Entity'] = field(default=list)

    def to_string(self) -> str:
        result = ""
        if self.value == "nullValue":
            result = f"<{self.title}"
            for attrname in self.attributes:
                result += f" {attrname}=\"{self.attributes[attrname]}\""
            result += "/>"
        return result


# датакласс для хранения данных, передаваемых из Морфиса в xml-генератор
@dataclass
class EntityV:
    id: str              # уникальный идентификатор тега
    attributes: dict = field(default=dict)  # аттрибуты тега
    value: str | None = None  # текст тега

@dataclass
class ListOfEntityV:
    variables: list[EntityV] = field(default=list)


def read_json_test(filename: str) -> Entity:
    with open(filename, encoding="utf-8") as f:
        json_data = json.load(f)
        #print(type(json_data))
        #print(f'>>>{json_data}')

    c1 = from_dict(data_class=Entity, data=json_data)
    return c1


def read_json_entity_variable(filename: str) -> ListOfEntityV:
    with open(filename, encoding="utf-8") as f:
        json_data = json.load(f)
    c1 = from_dict(data_class=ListOfEntityV, data=json_data)
    return c1


#c1 = read_json_test('variable_short.json')
c1 = read_json_entity_variable('variable_short.json')
print(c1)