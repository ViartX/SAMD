# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import xml.etree.ElementTree as ET
from pathlib import Path
import json_parcer as jpars

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    d1 = {"a":"1"}
    d1["b"] = "3"

    d2 = {"c1":34, "c2":54, "c3":d1}
    d1["n"] = d2
    print(d1)

    #raise Exception(d1)
    print(d1["n"]["c3"]["a"])





def ClinicalDocument_header(ClinicalDocument):

    # R [1..1] Область применения документа (Страна)
    realmCode = ET.SubElement(ClinicalDocument, "realmCode", code="RU")

    # R [1..1] Указатель на использование CDA R2
    typeId = ET.SubElement(ClinicalDocument, "typeId", root="2.16.840.1.113883.1.3", extension="POCD_MT000040")

    # R [1..1] Идентификатор документа "Руководство по реализации CDA (Release 2) уровень 3 Протокол прижизненного патологоанатомического исследования Редакция 2"
    templateId = ET.SubElement(ClinicalDocument, 'templateId', root="1.2.643.5.1.13.13.14.12.9.2")

    # R[1..1] Уникальный идентификатор документа
    id = ET.SubElement(ClinicalDocument, 'id', root="1.2.643.5.1.13.13.12.2.77.9638.100.1.1.51", extension="987654321") # номер приходит извне

    # R [1..1] Тип документа
    code = ET.SubElement(ClinicalDocument, 'code', code="12", codeSystem="1.2.643.5.1.13.13.11.1522", codeSystemVersion="4.13", \
    codeSystemName="Виды медицинской документации", displayName="Протокол прижизненного патологоанатомического исследования")

    # R [1..1] Заголовок документа
    ET.SubElement(ClinicalDocument, "title", name="title").text = "Протокол прижизненного патологоанатомического исследования"

    # R [1..1] Дата создания документа
    effectiveTime = ET.SubElement(ClinicalDocument, 'effectiveTime', value="202105261835+0300")  # вставить функцию для времени

    # R [1..1] Уровень конфиденциальности документа
    confidentialityCode = ET.SubElement(ClinicalDocument, 'confidentialityCode', code="N", codeSystem="1.2.643.5.1.13.13.99.2.285", \
    codeSystemVersion="1.1", codeSystemName="Уровень конфиденциальности медицинского документа", displayName="обычный")

    # R [1..1] Язык документа
    languageCode = ET.SubElement(ClinicalDocument, 'languageCode', value="ru-RU")

    #  R [1..1] Уникальный идентификатор набора версий документа
    setId = ET.SubElement(ClinicalDocument, 'setId', root="1.2.643.5.1.13.13.12.2.77.9638.100.1.1.50", extension="987654321") # присваивать номер документа

    # R [1..1] Номер версии данного документа
    versionNumber = ET.SubElement(ClinicalDocument, 'versionNumber', value="1")


def PatientInfo(ClinicalDocument, json_p, json_v):

    # R [1..1] ДАННЫЕ О ПАЦИЕНТЕ
    recordTarget = ET.SubElement(ClinicalDocument, 'recordTarget')
    # R [1..1] ПАЦИЕНТ (роль)
    patientRole = ET.SubElement(recordTarget, 'patientRole')
    # R [1..1] Уникальный идентификатор пациента в МИС
    ET.SubElement(patientRole, 'id', root="1.2.643.5.1.13.13.12.2.77.9638.100.1.1.10", extension=json_v.PatientId)
    #  R [1..1] СНИЛС пациента
    ET.SubElement(patientRole, 'id', root="1.2.643.100.3", extension=json_v.SnilsId)
    # [1..1] Документ, удостоверяющий личность пациента, серия, номер, кем выдан.
    ET.SubElement(patientRole, 'identity:IdentityDoc', nullFlavor="NA")
    # R [1..1] Полис ОМС
    polis = ET.SubElement(patientRole, 'identity:InsurancePolicy')
    # R [1..1] Тип полиса ОМС
    ET.SubElement(polis, 'identity:InsurancePolicyType', json_p.InsurancePolicyType)

#def fill_header(root):
    # <?xml version="1.0" encoding="UTF-8"?>
    #header = ET.(root, encoding='UTF-8', xml_declaration=True)

def xml_creator():

    filename = Path('C:/ARTEM/ECO-MED-IS/Morfis/Demo/filename.xml')
    filename_tmp  = Path('C:/ARTEM/ECO-MED-IS/Morfis/Demo/filename_temp.xml')

    json_p = jpars.jp.read_json_p()
    json_v = jpars.jv.read_json_v()

    key_dictionary = {
        "xmlns":"urn:hl7-org:v3",
        "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
        "xmlns:fias":"urn:hl7-ru:fias",
        "xmlns:identity":"urn:hl7-ru:identity",
        "xmlns:address":"urn:hl7-ru:address",
        "xmlns:medService":"urn:hl7-ru:medService"
    }

    ClinicalDocument = ET.Element("ClinicalDocument", **key_dictionary)

    tree = ET.ElementTree(element=ClinicalDocument)

    ClinicalDocument_header(ClinicalDocument)
    PatientInfo(ClinicalDocument, json_p, json_v)

    '''
    root = tree.getroot()
    #root = ET.Element("root")

    doc = ET.SubElement(root, "doc")
    #fill_header(root)
    ET.SubElement(doc, "field1", name="blah").text = "some value1"
    ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
    '''
    #tree = ET.ElementTree(ClinicalDocument)
    #tree.write("C:\\ARTEM\\ECO-MED-IS\\Morfis\\Demo\\filename.xml", encoding='UTF-8', xml_declaration=True)

    ET.indent(tree, space="\t", level=0)
    tree.write(filename_tmp, encoding="UTF-8")

    file = open(filename, "w", encoding="utf8")
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<?xml-stylesheet type="text/xsl" href="ПРОТОКОЛ_ПРИЖИЗНЕННОГО_ПАТОЛОГОАНАТОМИЧЕСКОГО_ИССЛЕДОВАНИЯ.xsl"?>\n')

    with file:
        with open(filename_tmp, "r", encoding="utf8") as infile:
            for line in infile:
                    file.write(line)

    file.close()

    #os.remove(filename_tmp)

    #Pathlib


def test01():
    document = ET.Element('outer')
    node = ET.SubElement(document, 'inner')
    node.text = '1'
    res = ET.tostring(document, encoding='utf8', method='xml').decode()
    print(res)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    #xml_creator()
    #test01()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


