import xml_entity as xe
import itertools
import xml.etree.ElementTree as ET
from pathlib import Path
import json_parcer as jpars

filenameP = 'permanent.json'
filenameV = 'variable.json'
filenameXML = 'result.xml'
icomment = itertools.count(1)
itest:int = 0


# поиск entity.value в jsonv по entity.id с перебором вложенных сущностей
def get_entity_value_by_id(jsonV: xe.Entity, entityId) -> str:

    if jsonV.id == entityId:
        return jsonV.value
    else:
        for child in jsonV.child:
            value = get_entity_value_by_id(child, entityId)
            if value != "":
                return value
    return ""


# поиск entity.attribute в jsonv по entity.id и именем аттрибута с перебором вложенных сущностей
def get_attribute_value_by_id(jsonV: xe.Entity, entityId, attributeName) -> str:
    #print(f'<<<{entityId}  {attributeName}')
    if jsonV.id == entityId:
        for attrname in jsonV.attributes:
            if attrname == attributeName:
                return jsonV.attributes[attrname]
    else:
        for child in jsonV.child:
            value = get_attribute_value_by_id(child, entityId, attributeName)
            if value != "":
                return value
    return ""


def entity_to_xml(source_xml_tag, jsonP: xe.Entity, jsonV: xe.Entity):
    global itest
    comment = ET.Comment(jsonP.comment)
    itest = itest + 1
    source_xml_tag.insert(itest, comment)
    print(f'comment {itest} {jsonP.comment}')

    for attrname in jsonP.attributes:
        if jsonP.attributes[attrname] == "*":
            jsonP.attributes[attrname] = get_attribute_value_by_id(jsonV, jsonP.id, attrname)

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
    jsonV = xe.read_json_test(filenameV)

    ClinicalDocument = ET.Element(jsonP.title)
    tree = ET.ElementTree(element=ClinicalDocument)

    entity_to_xml(ClinicalDocument, jsonP, jsonV)
    #fill_patient_role(ClinicalDocument, jsonP, jsonV)

    ET.indent(tree, space="\t", level=0)
    tree.write(filenameXML, encoding="UTF-8")

    #for child in jsonP.child:
    #    print(child.title)




build_xml(filenameP,filenameV,filenameXML)