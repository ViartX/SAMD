import xml_entity as xe
import itertools
import xml.etree.ElementTree as ET
from pathlib import Path
import json_parcer as jpars

filenameP = 'permanent.json'
filenameV = 'variable_short.json'
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
def get_entity_value_by_id(jsonV: xe.ListOfEntityV, entityId, index=1) -> str:
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
def get_attribute_value_by_id(jsonV: xe.Entity, entityId, attributeName, index=1) -> str:
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
def count_entity_with_id(jsonV: xe.ListOfEntityV, entityId) ->int:
    counter = 0
    for entity in jsonV.variables:
        if entity.id == entityId:
            counter += 1
    return counter


def entity_to_xml(source_xml_tag, jsonP: xe.Entity, jsonV: xe.Entity):
    global tree
    comment = ET.Comment(jsonP.comment)
    if jsonP.comment != "":
        source_xml_tag.append(comment)

    for attrname in jsonP.attributes:
        if jsonP.attributes[attrname] == "*":
            jsonP.attributes[attrname] = get_attribute_value_by_id(jsonV, jsonP.id, attrname)

    if source_xml_tag is None:
        result_xml_tag = ET.Element(jsonP.title, jsonP.attributes)
        tree = ET.ElementTree(element=result_xml_tag)
    else:
        result_xml_tag = ET.SubElement(source_xml_tag, jsonP.title, jsonP.attributes)

    text = jsonP.value
    if text == "*":
        text = get_entity_value_by_id(jsonV, jsonP.id)
    if text != "null":
        result_xml_tag.text = text

    for entity in jsonP.child:
        entity_to_xml(result_xml_tag, entity, jsonV)


    return result_xml_tag



def fill_patient_role(ClinicalDocument, jsonP: xe.Entity, jsonV: xe.Entity):

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



def build_xml(filenameP, filenameV, filenameXML):
    jsonP = xe.read_json_test(filenameP)
    #jsonV = xe.read_json_test(filenameV)
    jsonV = xe.read_json_entity_variable(filenameV)

    #ClinicalDocument = ET.Element(jsonP.title)
    #tree = ET.ElementTree(element=ClinicalDocument)

    entity_to_xml(None, jsonP, jsonV)
    #fill_patient_role(ClinicalDocument, jsonP, jsonV)

    ET.indent(tree, space="\t", level=0)
    tree.write(filenameXML, encoding="UTF-8")

    #for child in jsonP.child:
    #    print(child.title)


build_xml(filenameP,filenameV,filenameXML)

