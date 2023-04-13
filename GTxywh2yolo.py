import os
from xml.dom import minidom
import xml.etree.cElementTree as ET
from PIL import Image
import cv2

ANNOTATIONS_DIR_PREFIX = "/data/aicity2023/track5/images"

DESTINATION_DIR = "/data/aicity2023/track5/images"

CLASS_MAPPING = {
    '0': 'motorbike', '1': 'DHelmet', '2': 'DNoHelmet', '3': 'P1Helmet', '4': 'P1NoHelmet', '5': 'P2Helmet', '6': 'P2NoHelmet'
}

def formatter(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def create_root(file_prefix, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "difficult").text = "0"
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_xml_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    with open("{}/{}.xml".format(DESTINATION_DIR, file_prefix), "w") as f:

            f.write(formatter(root))
            f.close()


def read_file(file_path):
    width = 1920
    height = 1080
    subDIR = '' 
    i = 0
    pre_frame = ''
    with open(file_path, 'r') as infile:
        lines = infile.readlines()

        data = lines[i].split(",")
        video_id = int(data[0])
       
        if len(data[0]) == 1:
            subDIR = '00' + data[0]
        elif len(data[0]) == 2:
            subDIR = '0' + data[0]
        else:
            subDIR = data[0]
        #print(subDIR)

        pre_frame = int(data[1])
        path = os.path.join('train/labels/', subDIR)
        if not os.path.exists(path):
            os.mkdir(path)
        filename = "train/labels/{}/{}.txt".format(subDIR, data[1])
        print('pre filename: ', filename)
        f = open(filename, "w")    
            
        track_id = int(data[2])
        #print('i=%d, pre_frame=%d' %(i, pre_frame))
        x = float(data[3])
        y = float(data[4])
        bw = float(data[5])
        bh = float(data[6]) 
        label = int(data[7])

        # Find the center point coordinates
        xc, yc = (x + bw*0.5, y + bh*0.5)
        # Normalized 
        x_rel, y_rel = (xc / width, yc / height)
        w_rel, h_rel = (bw / width, bh / height)

        print('%d %f %f %f %f' %(label-1, x_rel, y_rel, w_rel, h_rel))
        f.write('%d %.6f %.6f %.6f %.6f\n' %(label-1, x_rel, y_rel, w_rel, h_rel))

        i = i + 1
        while (i < 65664):
            data1 = lines[i].split(",")
            video_id1 = int(data1[0])
            if len(data1[0]) == 1:
                subDIR1 = '00' + data1[0]
            elif len(data1[0]) == 2:
                subDIR1 = '0' + data1[0]
            else:
                subDIR1 = data1[0]
            #print(subDIR1)

            cur_frame = int(data1[1])
            track_id1 = int(data1[2])
            #print('i=%d, cur_frame=%d' %(i, cur_frame))
            x1 = float(data1[3])
            y1 = float(data1[4])
            bw1 = float(data1[5])
            bh1 = float(data1[6]) 
            label1 = int(data1[7])

            # Find the center point coordinates
            xc1, yc1 = (x1 + bw1*0.5, y1 + bh1*0.5)
            # Normalized 
            x_rel1, y_rel1 = (xc1 / width, yc1 / height)
            w_rel1, h_rel1 = (bw1 / width, bh1 / height)

            if (cur_frame != pre_frame):
                f.close()
                
                path = os.path.join('train/labels/', subDIR1)
                if not os.path.exists(path):
                    os.mkdir(path)
                filename1 = "train/labels/{}/{}.txt".format(subDIR1, data1[1])
                print('new filename: ', filename1)
                f = open(filename1, "w")
            else:
                filename = filename1
                #print('old filename: ', filename)
                #
            print('%d %f %f %f %f' %(label1-1, x_rel1, y_rel1, w_rel1, h_rel1))
            f.write('%d %.6f %.6f %.6f %.6f\n' %(label1-1, x_rel1, y_rel1, w_rel1, h_rel1))

            pre_frame = cur_frame
            i = i + 1
            if cv2.waitKey() & 0xFF == ord('q'):
                break
        f.close()
    infile.close()
    
def start():
    read_file('gt.txt')


if __name__ == "__main__":
    start()
