from xml_entity import *
import xml.etree.ElementTree as ET
import os


filenameP = 'permanent.json'
filenameV = 'variable.json'
filenameXML = 'result.xml'


# возвращает данные статического словаря по Entity.id
def get_static_entity_by_id(static, entityId) -> Entity:
    print(static.id, entityId)
    if static.id == entityId:
        return static
    else:
        for child in static.child:
            result = get_static_entity_by_id(child, entityId)
            if result is not None:
                return result
    return None


# метод формирует xml из объекта Entity
# source_xml_tag - исходный тэг XML-документа (в случае СЭМД <ClinicalDocument>)
# entity - объект с данными СЭМД
def entity_to_xml(source_xml_tag, entity: Entity):

    tree = None

    comment = ET.Comment(entity.comment)
    if entity.comment != "":
        source_xml_tag.append(comment)

    if source_xml_tag is None:
        result_xml_tag = ET.Element(entity.title, entity.attributes)
        tree = ET.ElementTree(element=result_xml_tag)
    else:
        result_xml_tag = ET.SubElement(source_xml_tag, entity.title, entity.attributes)

    result_xml_tag.text = entity.value

    for child in entity.child:
        entity_to_xml(result_xml_tag, child)

    return tree


# метод принимает два объекта Entity:
# static - константы для СЭМД
# variable - переменная часть СЭМД (данные пациента)
# формирует единый объект Entity с данными static и variable
def merge_entities(static: Entity, variable: Entity) -> Entity:
    static_e = get_static_entity_by_id(static, variable.id)

    if not static_e:
        raise ValueError(f"Объект не обнаружен {variable.id}")

    attributes = static_e.attributes.copy()
    for attrname in attributes:
        if attributes[attrname] == "*":
            attributes[attrname] = variable.attributes[attrname]

    value = static_e.value
    if value == "*":
        value = variable.value
    if value == "null":
        value = None

    child_list = []
    if isinstance(variable.child, list):
        for child in variable.child:
            merged_child = merge_entities(static_e, child)
            child_list.append(merged_child)

    merged = Entity(
        id=static_e.id,
        title=static_e.title,
        comment=static_e.comment,
        attributes=attributes,
        value=value,
        child=child_list
    )

    return merged


# функция добавляет в xml файл стартовые строки с <?xml> тэгами
# xml_temp_file - временный xml-файл, удаляется после формирования результирующего документа
# xml_file - результирующий документ
def add_xml_tag(xml_temp_file, xml_file):
    file = open(xml_file, "w", encoding="utf8")
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<?xml-stylesheet type="text/xsl" href="ПРОТОКОЛ_ПРИЖИЗНЕННОГО_ПАТОЛОГОАНАТОМИЧЕСКОГО_ИССЛЕДОВАНИЯ.xsl"?>\n')

    with file:
        with open(xml_temp_file, "r", encoding="utf8") as infile:
            for line in infile:
                    file.write(line)

    file.close()
    os.remove(xml_temp_file)


# метод предназначен для генерации xml-файла СЭМД
# описание параметров:
# file_static - файл c константными параметрами СЭМД
# file_var - файл c переменными параметрами СЭМД, приходят из Морфиса
# file_xml - итоговый файл СЭМД
def build_xml(file_static, file_var, file_xml):
    static = read_json(file_static)
    variable = read_json(file_var)

    merged = merge_entities(static, variable)
    tree = entity_to_xml(None, merged)
    if tree is None:
        raise Exception(f"Не удалось сформировать древовидную структуру документа")

    # настройки вывода xml-дерева
    ET.indent(tree, space="\t", level=0)

    # генерация временного файла
    xml_temp_file = file_xml + ".tmp"
    tree.write(xml_temp_file, encoding="UTF-8")
    add_xml_tag(xml_temp_file, file_xml)


#build_xml(filenameP, filenameV, filenameXML)

