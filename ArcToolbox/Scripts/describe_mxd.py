'''
Given an mxd, read all layers and dump to a human (and machine) readable list:
Symbolization details such as colour are not accessible via arcpy.
'''

import arcpy
import csv
#from arcplus import ao

# introspection of the arcpy layer object doesn't work that well,
# just hard code a list of properties to inspect via arcpy.mapping
PROPERTIES = ["name",
              "longName",
              "workspacePath",
              "datasetName",
              "dataSource",
              "description",
              "visible",
              "isBroken",
              "definitionQuery",
              "maxScale",
              "minScale",
              "labelClasses",
              "showLabels",
              "isGroupLayer",
              "isFeatureLayer",
              "isRasterLayer",
              "isServiceLayer",
              "isNetworkAnalystLayer",
              "isRasterizingLayer",
              "symbologyType",
              "transparency",
              "brightness",
              "contrast",
              "credits"]
              #"serviceProperties",
              #"symbology",
              #"time"]

# again, hard code which properties need to be checked if they are supported,
# it isn't easy to get what we want from introspection
CHECK_SUPPORTED = ["brightness", "contrast", "datasetname",
                   "datasource", "definitionquery", "description",
                   "labelclasses", "serviceproperties", "showlabels",
                   "symbology", "symbologytype", "transparency", "visible",
                   "workspacepath"]


class MapDoc:
    """
    Avoid the del statement
    - http://sgillies.net/blog/1067/get-with-it/
    - http://sgillies.net/blog/2013/12/17/teaching-python-gis-users-to-be-more-rational.html
    """
    def __init__(self, mapDoc):
        self.mapDoc = mapDoc

    def __enter__(self):
        return self.mapDoc

    def __exit__(self, type, value, traceback):
        # self.mapDoc.close() is not available
        del self.mapDoc


def layer_dict(lyr):
    pr = {}
    pr["labelclasses"] = ""
    for prop in PROPERTIES:
        if prop.lower() in CHECK_SUPPORTED:
            if lyr.supports(prop):
                # label classes return a label class group
                if prop != 'labelClasses':
                    value = getattr(lyr, prop)
                    pr[prop.lower()] = value
                else:
                    for i, label_class in enumerate(lyr.labelClasses, 1):
                        if label_class.showClassLabels:
                            labelinfo = [label_class.className,
                                         label_class.expression,
                                         label_class.SQLQuery]
                            pr["labelclasses"] = ",".join(labelinfo)+";"

            else:
                pr[prop.lower()] = None
        else:
            value = getattr(lyr, prop)
            pr[prop.lower()] = value
    return pr


def ArcMap_DescribeMXD(outfile="arcmap_describe.txt", bStandalone=False):
    '''
    Describe all layers in an mxd, dump to text file
    '''
    in_file = r"../Tests/describe_mxd/test.mxd"
    with MapDoc(arcpy.mapping.MapDocument(in_file)) as mxd:
        layers = []
        for df in arcpy.mapping.ListDataFrames(mxd):
            for layer in arcpy.mapping.ListLayers(mxd, "", df):
                layers.append(layer_dict(layer))
    # write to csv
    with open('test.csv', 'wb') as csvfile:
        columns = [p.lower() for p in PROPERTIES if p != "isgrouplayer"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for row in layers:
            # don't write group layers
            if not row["isgrouplayer"]:
                writer.writerow(row)

if __name__ == "__main__":
    mxd = r"../Tests/describe_mxd/test.mxd"
    ArcMap_DescribeMXD("test.txt", True)
