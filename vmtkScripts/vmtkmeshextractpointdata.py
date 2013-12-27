#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkmeshextractpointdata.py,v $
## Language:  Python
## Date:      $Date: 2005/09/14 09:49:59 $
## Version:   $Revision: 1.6 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


from vmtk import vtkvmtk
import vtk
import sys

import pypes
import vmtkmeshvectorfromcomponents

vmtkmeshextractpointdata = 'vmtkMeshExtractPointData'

class vmtkMeshExtractPointData(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)

        self.Mesh = None
        self.PointId = None
        self.ArrayName = None
        self.ComponentsArrayNames = None
        self.SetScriptName('vmtkmeshextractpointdata')
        self.SetScriptDoc('extract the magnitude value of an array for a point id')
        self.SetInputMembers([
            ['Mesh','i','vtkUnstructuredGrid',1,'','the input mesh','vmtkmeshreader'],    
            ['PointId','pointid','int',1,'','the id of the cell'],
            ['ComponentsArrayNames','components','str',-1,'',''],
            ['ArrayName','array','str',1,'',''],
            ])
        self.SetOutputMembers([
            ])

    def Execute(self):

        if (self.Mesh == None):
            self.PrintError('Error: no Mesh.')
            
        if (self.PointId == None):
            self.PrintError('Error: no PointId.')
        
        if (self.ArrayName == None):
            self.PrintError('Error: no ArrayName.')
            
        vectorFromComponents = vmtkmeshvectorfromcomponents.vmtkMeshVectorFromComponents()
        vectorFromComponents.Mesh = self.Mesh
        vectorFromComponents.VectorArrayName = self.ArrayName
        vectorFromComponents.ComponentsArrayNames = self.ComponentsArrayNames
        vectorFromComponents.RemoveComponentArrays = True
        vectorFromComponents.Execute()
        dataArray = self.Mesh.GetPointData().GetArray(self.ArrayName)
        dataValue = vtk.vtkMath.Norm((dataArray.GetTuple(self.PointId)[0],dataArray.GetTuple(self.PointId)[1],dataArray.GetTuple(self.PointId)[2]))
        
        self.PrintLog('')
        
        logLine = 'PointId: %d\n' % self.PointId
        logLine += '  Array: %s\n' % self.ArrayName
        logLine += '  Value: %f\n' % dataValue
        
        self.PrintLog(logLine)
        
if __name__=='__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()