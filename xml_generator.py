from xml_entity import *
import itertools
import xml.etree.ElementTree as ET
from pathlib import Path
import json_parcer as jpars

filenameP = 'permanent.json'
filenameV = 'variable.json'
filenameXML = 'result.xml'
tree = None

# поиск entity.value в jsonv по entity.id с перебором вложенных сущностей
# def get_entity_value_by_id(jsonV: xe.Entity, entityId) -> str:
#
#     if jsonV.id == entityId:
#         return jsonV.value
#     else:
#         for child in jsonV.child:
#             value = get_entity_value_by_id(child, entityId)
#             if value != "":
#                 return value
#     return ""
def get_entity_value_by_id(jsonV: ListOfEntityV, entityId, index=1) -> str:
    counter = 1
    result = "NOT FOUND"
    for entity in jsonV.variables:
        if entity.id == entityId:
            if counter >= index:
                return entity.value
            else:
                counter += 1
    return result


# поиск entity.attribute в jsonv по entity.id и именем аттрибута с перебором вложенных сущностей
# def get_attribute_value_by_id(jsonV: xe.Entity, entityId, attributeName) -> str:
#     #print(f'<<<{entityId}  {attributeName}')
#     if jsonV.id == entityId:
#         for attrname in jsonV.attributes:
#             if attrname == attributeName:
#                 return jsonV.attributes[attrname]
#     else:
#         for child in jsonV.child:
#             value = get_attribute_value_by_id(child, entityId, attributeName)
#             if value != "":
#                 return value
#     return ""
def get_attribute_value_by_id(jsonV: Entity, entityId, attributeName, index=1) -> str:
    counter = 1
    result = "NOT FOUND"
    for entity in jsonV.variables:
        if entity.id == entityId:
            if counter >= index:
                for attrname in entity.attributes:
                    if attrname == attributeName:
                        return entity.attributes[attrname]
            else:
                counter += 1
    return result


# поиск количества элементов в структуре json variable с одинаковым entity id
def count_entity_with_id(jsonV: ListOfEntityV, entityId) ->int:
    counter = 0
    for entity in jsonV.variables:
        if entity.id == entityId:
            counter += 1
    return counter


# поиск количества повторений для сущности, по полю repetitions
def get_jsonv_entity_repetitions_by_id(jsonV: ListOfEntityV, entityId) ->int:
    for entity in jsonV.variables:
        if entity.id == entityId:
            return entity.repetitions
    return 1


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


def entity_to_xml_multirecord(source_xml_tag, jsonP: Entity, jsonV: Entity, index=1):
    global tree

    entity_count = get_jsonv_entity_repetitions_by_id(jsonV, jsonP.id)
    if entity_count == 0:
        entity_count = 1

    #print(jsonP.id, entity_count)

    for i in range(1, entity_count+1):

        print(jsonP.id, i)
        comment = ET.Comment(jsonP.comment)
        if jsonP.comment != "":
            source_xml_tag.append(comment)

        for attrname in jsonP.attributes:
            if jsonP.attributes[attrname] == "*":
                jsonP.attributes[attrname] = get_attribute_value_by_id(jsonV, jsonP.id, attrname, i)

        if source_xml_tag is None:
            result_xml_tag = ET.Element(jsonP.title, jsonP.attributes)
            tree = ET.ElementTree(element=result_xml_tag)
        else:
            result_xml_tag = ET.SubElement(source_xml_tag, jsonP.title, jsonP.attributes)

        text = jsonP.value
        if text == "*":
            text = get_entity_value_by_id(jsonV, jsonP.id, i)
            #print(text, i)
        if text != "null":
            result_xml_tag.text = text

        for entity in jsonP.child:
            entity_to_xml_multirecord(result_xml_tag, entity, jsonV)

    return result_xml_tag
    #return


def entity_to_xml(source_xml_tag, entity:Entity):
    global tree

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

    return result_xml_tag



def fill_patient_role(ClinicalDocument, jsonP: Entity, jsonV: Entity):

    icomment = itertools.count(1)
    comment=ET.Comment(jsonP.comment)
    ClinicalDocument.insert(next(icomment), comment)
    patientRole = ET.SubElement(ClinicalDocument, jsonP.title)
    ET.Comment("<!-- test -->")
    for entity in jsonP.child:
        comment = ET.Comment(entity.comment)
        ClinicalDocument.insert(next(icomment), comment)
        for attrname in entity.attributes:
            if entity.attributes[attrname] == "*":
                entity.attributes[attrname] = get_attribute_value_by_id(jsonV, entity.id, attrname)

        value = ET.SubElement(patientRole, entity.title, entity.attributes)
        text = entity.value
        if text == "*":
            text = get_entity_value_by_id(jsonV, entity.id)
        if text != "null":
            value.text = text



def merge_entities(static: Entity, variable: Entity) -> Entity:

    # id: str              # уникальный идентификатор тега
    # title: str           # название тега
    # comment: str = ""    # комментарий, идущий перед тегом
    # attributes: dict = field(default=dict)  # аттрибуты тега
    # value: str | None = None  # текст тега
    # child: list['Entity'] = field(default=list)

    static_e = get_static_entity_by_id(static, variable.id)

    if not static_e:
        raise ValueError(f"No entity found with ID {variable.id}")


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



def build_xml(filenameP, filenameV, filenameXML):
    static = read_json_test(filenameP)
    #jsonV = read_json_test(filenameV)
    variable = read_json_test(filenameV)

    #ClinicalDocument = ET.Element(jsonP.title)
    #tree = ET.ElementTree(element=ClinicalDocument)

    merged = merge_entities(static, variable)
    entity_to_xml(None, merged)

    #entity_to_xml(None, jsonP, jsonV)
    #fill_patient_role(ClinicalDocument, jsonP, jsonV)

    ET.indent(tree, space="\t", level=0)
    tree.write(filenameXML, encoding="UTF-8")

    #print(get_jsonv_entity_repetitions_by_id(jsonV, "CD-documentationOf-serviceEvent-performer"))
    #for child in jsonP.child:
    #    print(child.title)


build_xml(filenameP, filenameV, filenameXML)
# static = read_json_test(filenameP)
# variable = read_json_test(filenameV)

# print(static)
# result = get_static_entity_by_id(static, "CD-custodian-assignedCustodian-representedCustodianOrganization-addr")
# print(result)

# merged = merge_entities(static, variable)
# print(merged)
