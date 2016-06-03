arcplus
=======
*a few little things I think Esri's arcpy and related should have*


## Quick Start

 1. Open a [pip](https://pip.pypa.io/en/latest/installing.html) and an ArcGIS python enabled command shell, then install *[current comtypes](https://github.com/enthought/comtypes/)* and *arcplus*:
	
	    pip install https://github.com/enthought/comtypes/archive/master.zip
	    pip install https://github.com/maphew/arcplus/archive/master.zip

 2. Run python and:

    ``` 
    d:\>python
    Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import arcplus   
    
    >>> for fc in arcplus.listAllFeatureClasses(r"D:\scratch.gdb"):
    ...     print fc
    ...
    Looking in D:\scratch.gdb for "*"
    Administration_Boundaries\LI_1210009_2
    Administration_Boundaries\Yukon_Ditch_ENV080
    base_toponomy\Highway_shields
    base_toponomy\Physiographic_text
    base_toponomy\Places_text
    annotation_attrib_test
    fraser_peak_GPXtoFeatures
    ...
    ```     



#### arcplus.listAllFeatureClasses
Recursively list all Feature Classes in a geodatabase or coverage (normal listFeatureClasses method does not recurse)

See [Listing all feature classes in File Geodatabase, including within feature datasets?](http://gis.stackexchange.com/questions/5893/listing-all-feature-classes-in-file-geodatabase-including-within-feature-datase)

#### arcplus.ao
See [Use Arcobjects from Python](http://gis.stackexchange.com/questions/80/how-do-i-access-arcobjects-from-python/)

*...not working reliably yet!*

    >>> from arcplus import ao
    
    >>> ao.GetLibPath()
    u'C:\\ArcGIS\\Desktop10.3\\com\\'

    >>> dir(ao)
    ['ArcCatalog_GetSelectedTable',
     'ArcMap_AddTextElement',
     'ArcMap_GetEditWorkspace',
     'ArcMap_GetSelectedGeometry',
     'ArcMap_GetSelectedTable',
     'CLSID',
     'CType',
     'GetApp',
     'GetCurrentApp',
     'GetDesktopModules',
     'GetLibPath',
     'GetModule',
     'GetStandaloneModules',
     'InitStandalone',
     'Msg',
     'NewObj',
     'Standalone_CreateTable',
     'Standalone_OpenFileGDB',
     'Standalone_OpenSDE',
     'Standalone_QueryDBValues',
     '__builtins__',
     '__doc__',
     '__file__',
     '__name__',
     '__package__',
     '__path__',
     'ao']




## Scripts

#### clip_all_layers.py

Clip all layers in map to the specified polygon layer. Command line usage:

    clip_all_layers "path\to\Some map.mxd" path\to\data.gdb\clip_poly path\to\destination.gdb

Relative paths are interpreted relative to the mxd, not the current shell folder ([ref](http://gis.stackexchange.com/a/136826/108)).
There's an example toolbox usage in the Tests folder.

Built to support [building a map package with clippping](http://gis.stackexchange.com/questions/132352/arcgis-desktop-map-package-with-clipping).


#### GPXtoFeaturesXY.py

A small enchancement to Esri's GPXtoFeatures.py: store the original geographic coordinates as attributes.

####  metadata_batch_upgrade.py

Recursively walk through a GDB or workspace and upgrades the metadata record of any feature class found.

Regular upgrade tool can only do one FC at a time, and using the batch control is painful as you drill down into each dataset individually to drag and drop.

#### set_legend_descriptions.py
 
Set description property of Unique Value legend items from a lookup table. Enables having a legend with lengthy descriptions as well as the record values.

Adapted from [Setting symbol descriptions of ArcMap layout legends from table?](http://gis.stackexchange.com/questions/102956/setting-symbol-descriptions-of-arcmap-layout-legends-from-table/)


#### TableToCSV.py

ArcGIS doesn't have an out of the box tool for exporting a table to text. Let's fix that
[not working yet]

Inspiration: [Export table to X,Y,Z ASCII file via arcpy](http://gis.stackexchange.com/questions/17933/export-table-to-x-y-z-ascii-file-via-arcpy)


SysAdmin
--------

#### [uninstall-ALL-ArcGIS-products.bat](SysAdmin/uninstall-ALL-ArcGIS-products.md)

Uninstall ArcGIS products using the Windows Installer `msiexec`, feeding it a text file with Product IDs. Will not work for programs like ArcPad which don't use msi to install in the first place.  


## Development and testing on BC GTS

 1. Open a windows command prompt and ensure that 32 bit ArcGIS python and scripts are inlcuded in the PATH:
  ```
  set PATH="E:\sw_nt\Python27\ArcGIS10.2";"E:\sw_nt\Python27\ArcGIS10.2\Scripts";%PATH%
  ```

 2. Ensure [pip](https://pypi.python.org/pypi/pip) is installed to server, [install](https://pip.pypa.io/en/stable/installing/) if it is not.

 3. Create and enable a [virtualenv](https://virtualenv.pypa.io/en/stable) for testing/development so we don't have to worry about conflicting with system installed python packages
  ```
  pip install virtualenv # (if necessary)
  mkdir arcplus
  cd arcplus
  mkdir arcplus_env
  virtualenv arcplus_env
  arcplus_env\Scripts\activate
  ```

 4. Get the `arcplus` repository by either
 a) Open a cygwin terminal with git installed, navigate to arcplus folder and `git clone git@github.com:smnorris/arcplus.git`
 OR
 b) Manually download and unzip the repository from https://github.com/smnorris/arcplus/archive/master.zip

 5. Back at the windows command prompt
  ```
  cd arcplus
  pip install https://github.com/enthought/comtypes/archive/master.zip
  pip install -e .
  ```

 6. Ensure we can reach `arcpy` from the virtualenv (based on this [USGS guide](https://my.usgs.gov/confluence/display/cdi/Calling+arcpy+from+an+external+virtual+Python+environment)) by creating a file `Lib\site-packages\ArcGIS.pth` and including these lines (or similar, check required paths by following the guide):
  ```
  # ArcGIS.pth
  # Path to ArcGIS arcpy modules
  # Place in folder ...\<path to your virtual environment>\lib\site-packages\
  e:\\sw_nt\\arcgis\\desktop10.2\\arcpy
  C:\\Windows\\system32\\python27.zip
  E:\\sw_nt\\Python27\\ArcGIS10.2\\Lib
  E:\\sw_nt\\Python27\\ArcGIS10.2\\DLLs
  E:\\sw_nt\\Python27\\ArcGIS10.2\\Lib\\lib-tk
  E:\\sw_nt\\ArcGIS\\Desktop10.2\\Bin
  E:\\sw_nt\\Python27\\ArcGIS10.2
  E:\\sw_nt\\Python27\\ArcGIS10.2\\lib\\site-packages
  E:\\sw_nt\\ArcGIS\\EsriProductionMapping\\Desktop10.2\\Bin
  E:\\sw_nt\\ArcGIS\\EsriProductionMapping\\Desktop10.2\\arcpyproduction
  E:\\sw_nt\\ArcGIS\\Desktop10.2\\arcpy
  E:\\sw_nt\\ArcGIS\\Desktop10.2\\ArcToolbox\\Scripts
  E:\\sw_nt\\Python27\\ArcGIS10.2\\lib\\site-packages\\win32
  E:\\sw_nt\\Python27\\ArcGIS10.2\\lib\\site-packages\\win32\\lib
  E:\\sw_nt\\Python27\\ArcGIS10.2\\lib\\site-packages\\Pythonwin
  ```

 7. If required, activate the virtualenv within an ArcGIS session by issuing this command from the ArcGIS python window ([credit](https://gis.stackexchange.com/questions/7333/running-arcgis-10-0-under-virtualenv)):
  ```
  execfile(r'<path to my env>\Scripts\activate_this.py', {'__file__': r'<path to my env>\Scripts\activate_this.py'})
  import arcplus
  ```

