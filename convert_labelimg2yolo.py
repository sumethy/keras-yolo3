import xml.etree.ElementTree as ET
import numpy as np
import os

LABEL_DIR = 'data\labels'

class_dict = dict()
with open('train_classes.txt', 'r') as f:
    lines = f.readlines()
    for i,line in enumerate(lines):
        if line[-1] == '\n':
            line = line[:-1]
        class_dict[line] = i

print('classes:', class_dict)

def parseAnnotation(filename):
    root = ET.parse(filename).getroot()
    filename_linux = filename.replace('\\','/')
    line = filename_linux[:-3] # strip off the 'xml' file extension at the end
    line += root[1].text[-3:] # append the correct file extension
    line = line.replace('labels', 'images') 
    for lv1 in root:
        if lv1.tag == 'object':
            for lv2 in lv1:
                if lv2.tag == 'bndbox':
                    line += ' ' + lv2[0].text + \
                        ',' + lv2[1].text + ',' + lv2[2].text + \
                        ',' + lv2[3].text + ','
                    line += str(class_dict[lv1[0].text])
    
    return line

xml_files = os.listdir(LABEL_DIR)
with open('train_labels.txt', 'w') as f:
    for xml_file in xml_files:
        path = LABEL_DIR + '\\' + xml_file
        line = parseAnnotation(path)
        f.write(line + '\n')
