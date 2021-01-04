# Copyright (c) 2019 - 2021 Geode-solutions
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os 

from vtk.web.protocols import vtkWebProtocol
import vtk

from wslink import register as exportRpc

from uuid import uuid4 as uuid

class GeodeProtocol(vtkWebProtocol):
    def getDataBase(self):
        return self.getSharedObject("db")

    def getRenderer(self):
        return self.getSharedObject("renderer")

    def getObject(self, id):
        return self.getDataBase()[id]
    
    def getProtocol(self, name):
        for p in self.coreServer.getLinkProtocols():
            if(type(p).__name__ == name):
                return p

    def render(self, view = -1):
        self.getProtocol("vtkWebPublishImageDelivery").imagePush({"view": view})

    def registerObjectFromFile(self, type, filename, cpp, vtk_object, vtk_light):
        print(filename)
        name = os.path.basename(filename)
        return self.registerObject(type, name, cpp, vtk_object, vtk_light)

    def bbox(self, actor):
        bounds = actor.GetBounds()
        bbox = vtk.vtkBoundingBox(bounds)
        return bbox
    
    def addVTKObject(self, vtk_object):
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        mapper.SetInputData(vtk_object)
        mapper.SetColorModeToMapScalars()
        mapper.SetResolveCoincidentTopologyLineOffsetParameters(1,-0.1)
        mapper.SetResolveCoincidentTopologyPolygonOffsetParameters(2,0)
        mapper.SetResolveCoincidentTopologyPointOffsetParameter(-2)
        actor.SetMapper(mapper)
        self.getRenderer().AddActor(actor)
        return mapper, actor

    def registerObject(self, object_type, name, cpp, vtk_object, vtk_light):
        if type(vtk_object) is dict:
            mapper = {}
            actor = {}
            bbox = vtk.vtkBoundingBox()
            for key, components in vtk_object.items():
                mapper[key] = {}
                actor[key] = {}
                for id, polydata in components.items():
                    object_mapper, object_actor = self.addVTKObject(polydata)
                    if polydata.GetNumberOfPoints() != 0:
                        bbox.AddBox(self.bbox(object_actor))
                    mapper[key][id] = object_mapper
                    actor[key][id] = object_actor
        else:
            mapper, actor = self.addVTKObject(vtk_object)
            bbox = self.bbox(actor)
        id = str(uuid())
        print(id)
        self.getDataBase()[id] = {
            "type": object_type, 
            "name": name, 
            "cpp": cpp, 
            "bbox": bbox,
            "vtk": vtk_object, 
            "actor": actor,
            "mapper": mapper
        }
        return {"id": id, "name": name, "type": object_type, "data": vtk_light}

