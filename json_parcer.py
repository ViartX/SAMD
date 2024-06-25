import json
from dataclasses import dataclass, field

import json_variable as jv
import json_permanent as jp


def read_json():
    json_p = jp.read_json_p()
    json_v = jv.read_json_v()
    '''
    data = XmlInputData(
        a=1,
        b='123',
        c=[
            Cassette(
                a=1,
                b='123',
                d=None
            )
        ]
    )
    '''
#read_json()


#result_xml = xml_generator(data=data)