bl_info = {
    "name": "UII Building Tools",
    "author": "CravenWarrior",
    "version": (1, 20, 8, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh",
    "description": ("Adds common parts that conform to the UII building style."),
    "warning": "IN DEVELOPMENT",
    "category": "Add Mesh",
}

import bpy
from bpy import context
from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, IntProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def add_frame_basic(self, context):
    o = self.offset
    width = self.width/2
    height = self.height + o
    
    verts = [
        # Bottom Interior
        Vector((-width, 0.125, o)),
        Vector((-width, -0.125, o)),
        Vector((width, -0.125, o)),
        Vector((width, 0.125, o)),
        # Top Interior
        Vector((-width, 0.125, height)),
        Vector((-width, -0.125, height)),
        Vector((width, -0.125, height)),
        Vector((width, 0.125, height)),
        # Bottom Exterior
        Vector((-width - 0.5, 0.125, 0)),
        Vector((-width - 0.5, -0.125, 0)),
        Vector((width + 0.5, -0.125, 0)),
        Vector((width + 0.5, 0.125, 0)),
        # Top Exterior
        Vector((-width - 0.5, 0.125, 3)),
        Vector((-width - 0.5, -0.125, 3)),
        Vector((width + 0.5, -0.125, 3)),
        Vector((width + 0.5, 0.125, 3)),
        
        # Frame Bottom Interior
        Vector((-width + 0.05, 0.175, -0.05 + o)),
        Vector((-width + 0.05, -0.175, -0.05 + o)),
        Vector((width - 0.05, -0.175, -0.05 + o)),
        Vector((width - 0.05, 0.175, -0.05 + o)),
        # Frame Top Interior
        Vector((-width + 0.05, 0.175, height -0.05)),
        Vector((-width + 0.05, -0.175, height -0.05)),
        Vector((width - 0.05, -0.175, height -0.05)),
        Vector((width - 0.05, 0.175, height -0.05)),
        # Frame Bottom Exterior
        Vector((-width - 0.05, 0.175, -0.05 + o)),
        Vector((-width - 0.05, -0.175, -0.05 + o)),
        Vector((width + 0.05, -0.175, -0.05 + o)),
        Vector((width + 0.05, 0.175, -0.05 + o)),
        # Frame Top Exterior
        Vector((-width - 0.05, 0.175, height + 0.05)),
        Vector((-width - 0.05, -0.175, height + 0.05)),
        Vector((width + 0.05, -0.175, height + 0.05)),
        Vector((width + 0.05, 0.175, height + 0.05))]
    
    faces = [
        # Interior
        [0, 1, 2, 3],
        [7, 6, 5, 4],
        [0, 4, 5, 1],
        [2, 6, 7, 3],
        # Exterior
        [8, 12, 4, 0],
        [3, 7, 15, 11],
        [4, 12, 15, 7],
        [1, 5, 13, 9],
        [10, 14, 6, 2],
        [6, 14, 13, 5],
        # Frame Interior
        [16, 20, 21, 17],
        [18, 22, 23, 19],
        [23, 22, 21, 20],
        # Frame Exterior
        [25, 29, 28, 24],
        [27, 31, 30, 26],
        [28, 29, 30, 31],
        [24, 28, 20, 16],
        [19, 23, 31, 27],
        [20, 28, 31, 23],
        [17, 21, 29, 25],
        [26, 30, 22, 18],
        [22, 30, 29, 21]]
    
    # Frame Differentiation
    if self.frameClosed == False or self.sillHeight != 0:
        if self.frameDoor == True:
            faces.extend([
                [16, 17, 25, 24],
                [27, 26, 18, 19]])
    else:
        faces.extend([
            [16, 17, 18, 19],
            [27, 26, 25, 24],
            [24, 16, 19, 27],
            [26, 18, 17, 25]])
        verts[16] = Vector((-width + 0.05, 0.175, 0.05 + o))
        verts[17] = Vector((-width + 0.05, -0.175, 0.05 + o))
        verts[18] = Vector((width - 0.05, -0.175, 0.05 + o))
        verts[19] = Vector((width - 0.05, 0.175, 0.05 + o))
    
    if self.frameDoor == False:
        faces.extend([
            [8, 0, 3, 11],
            [10, 2, 1, 9]])
    
    return (verts, faces)

def add_stairs_basic(self, context):
    height = self.height
    width = self.width/2
    depth = self.depth
    depthOffset = -depth*height/0.25
    
    verts = []
    faces = []
    
    if self.ramp == False:
        # Create Each Step
        x = 0
        y = 0
        while x < height/0.25:
            offset = 0.25 * x
            offsetDepth = depth * x
            verts.extend([
                Vector((-width, -offsetDepth, offset)),
                Vector((-width, -offsetDepth, 0.25 + offset)),
                Vector((width, -offsetDepth, 0.25 + offset)),
                Vector((width, -offsetDepth, offset))])
            faces.extend([
                [0 + y, 3 + y, -2 + y, -3 + y],
                [0 + y, 1 + y, 2 + y, 3 + y]])
            x += 1
            y = 4*x

        # Add Top and Remove Bottom
        verts.extend([
            Vector((-width, -depth -offsetDepth, 0.25 + offset)),
            Vector((width, -depth - offsetDepth, 0.25 + offset))])
        faces.append([y + 1, y - 2, y - 3, y])
        del faces[0]
    
    else:
        verts.extend([
            Vector((-width, 0, 0)),
            Vector((-width, depthOffset, height)),
            Vector((width, depthOffset, height)),
            Vector((width, 0, 0))])
        faces.append([0, 1, 2, 3])
    
    # Add Back to Stairs
    vertCount = len(verts)
    
    verts.extend([
        Vector((-width, -0.25, 0)),
        Vector((-width, depthOffset, height - 0.25)),
        Vector((width, depthOffset, height - 0.25)),
        Vector((width, -0.25, 0))])
    faces.append([vertCount + 3, vertCount + 2, vertCount + 1, vertCount])    
    
    return (verts, faces)

def add_railing(self, context):
    height = self.height
    depth = self.depth
    depthOffset = -depth*height/0.25
    slope = height / (height/0.25 * depth)
    
    verts = [
        # Initial Face
        Vector((-0.125, depth, 0)),
        Vector((0.125, depth, 0)),
        Vector((-0.125, depth, 0.1)),
        Vector((0.125, depth, 0.1)),
        # Initial Offset
        Vector((-0.125, 0, 0)),
        Vector((0.125, 0, 0)),
        # Terminal Face 1
        Vector((-0.125, depthOffset + depth, height)),
        Vector((0.125, depthOffset + depth, height)),
        Vector((-0.125, depthOffset + depth, height + 0.1)),
        Vector((0.125, depthOffset + depth, height + 0.1)),
        # Terminal Face 2
        Vector((-0.125, depthOffset, height)),
        Vector((0.125, depthOffset, height)),
        Vector((-0.125, depthOffset, height + 0.1)),
        Vector((0.125, depthOffset, height + 0.1)),

        # Initial Face Top
        Vector((-0.125, depth, 0.8)),
        Vector((0.125, depth, 0.8)),
        Vector((-0.125, depth, 0.9)),
        Vector((0.125, depth, 0.9)), #17
        # Terminal Face 1 Top
        Vector((-0.125, depthOffset + depth, height + 0.8)),
        Vector((0.125, depthOffset + depth, height + 0.8)),
        Vector((-0.125, depthOffset + depth, height + 0.9)),
        Vector((0.125, depthOffset + depth, height + 0.9)),
        # Terminal Face 2 Top
        Vector((-0.125, depthOffset, height + 0.8)),
        Vector((0.125, depthOffset, height + 0.8)),
        Vector((-0.125, depthOffset, height + 0.9)),
        Vector((0.125, depthOffset, height + 0.9)),
        # Terminal Post
        Vector((-0.0625, depthOffset + depth/2 + 0.0625, height + 0.05)),
        Vector((0.0625, depthOffset + depth/2 + 0.0625, height + 0.05)),
        Vector((-0.0625, depthOffset + depth/2 - 0.0625, height + 0.05)),
        Vector((0.0625, depthOffset + depth/2 - 0.0625, height + 0.05)),
        Vector((-0.0625, depthOffset + depth/2 + 0.0625, height + 0.85)),
        Vector((0.0625, depthOffset + depth/2 + 0.0625, height + 0.85)),
        Vector((-0.0625, depthOffset + depth/2 - 0.0625, height + 0.85)),
        Vector((0.0625, depthOffset + depth/2 - 0.0625, height + 0.85))]

    faces = [
        # Bottom Rail
        [1, 0, 2, 3],
        [5, 1, 7, 11],
        [10, 6, 0, 4],
        [9, 7, 1, 3],
        [2, 0, 6, 8],
        [3, 2, 8, 9],
        [9, 8, 12, 13],
        [8, 6, 10, 12],
        [13, 11, 7, 9],
        [13, 12, 10, 11],

        # Top Rail
        [15, 14, 16, 17],
        [21, 19, 15, 17],
        [16, 14, 18, 20],
        [17, 16, 20, 21],
        [19, 18, 14, 15],
        [21, 20, 24, 25],
        [23, 22, 18, 19],
        [20, 18, 22, 24],
        [25, 23, 19, 21],
        [25, 24, 22, 23],
        [31, 33, 29, 27],
        [26, 28, 32, 30],
        [27, 26, 30, 31],
        [33, 32, 28, 29]]
    
    # Create Posts
    x = 0; y = 0
    postHeightOffset = 0.05
    if depth != 0.25 and depth > 0.5:
        postHeightOffset = 0.05

    while x < height/0.25:
        stepCenter = depth/2 + depth*x
        offsetLow = slope * (stepCenter - 0.0625) + postHeightOffset
        offsetHigh = slope * (stepCenter + 0.0625) + postHeightOffset
        stepCenter -= depth
        verts.extend([
            Vector((-0.0625, 0.0625 - stepCenter, offsetLow)),
            Vector((-0.0625, -0.0625 - stepCenter, offsetHigh)),
            Vector((0.0625, -0.0625 - stepCenter, offsetHigh)),
            Vector((0.0625, 0.0625 - stepCenter, offsetLow)),
            Vector((-0.0625, 0.0625 - stepCenter, 0.8 + offsetLow)),
            Vector((-0.0625, -0.0625 - stepCenter, 0.8 + offsetHigh)),
            Vector((0.0625, -0.0625 - stepCenter, 0.8 + offsetHigh)),
            Vector((0.0625, 0.0625 - stepCenter, 0.8 + offsetLow))])
        faces.extend([
            [34 + y, 38 + y, 41 + y, 37 + y],
            [36 + y, 40 + y, 39 + y, 35 + y],
            [39 + y, 38 + y, 34 + y, 35 + y],
            [41 + y, 40 + y, 36 + y, 37 + y]])
        x += 1
        y = 8*x

    return (verts, faces)

def generate_mesh(self, context, verts, faces):
    mesh = bpy.data.meshes.new(name="New Mesh")
    mesh.from_pydata(verts, [], faces)
    object_data_add(context, mesh, operator=self)

class AddDoorway(Operator, AddObjectHelper):
    bl_idname = "uii.add_doorway"
    bl_label = "Add Doorway Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    width: FloatProperty(name="Width", default=1.75, min=1.75, max=5, step=25, precision=3, unit="LENGTH")
    height: FloatProperty(name="Height", default=2.25, min=2.25, max=4, step=25, precision=3, unit="LENGTH")
    frameClosed: BoolProperty(name="Closed Frame", default=False)
    
    frameDoor = True
    sillHeight = 0
    offset = 0
    
    def execute(self, context):
        verts, faces = add_frame_basic(self, context)
        generate_mesh(self, context, verts, faces)
        
        return {'FINISHED'}

class AddWindow(Operator, AddObjectHelper):
    bl_idname = "uii.add_window"
    bl_label = "Add Window Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    width: FloatProperty(name="Width", default=1.5, min=1, max=4, step=25, precision=3, unit="LENGTH")
    height: FloatProperty(name="Height", default=1.5, min=0.5, max=1.5, step=25, precision=3, unit="LENGTH")
    sillHeight: FloatProperty(name="Sill Height", default=0.1, min=0, max=0.2, step=10, precision=2, unit="LENGTH")
    offset: FloatProperty(name="Offset", default=1, min=1, max=5, step=25, precision=3, unit="LENGTH")
    
    frameClosed = True
    frameDoor = False
    
    def execute(self, context):
        verts, faces = add_frame_basic(self, context)
        
        width = self.width/2
        sillHeight = self.sillHeight
        o = self.offset
        if sillHeight > 0.01:
            verts.extend([
                # Sill Bottom
                Vector((-width - 0.1, 0.225, 0.05 - sillHeight + o)),
                Vector((-width - 0.1, -0.225, 0.05 - sillHeight + o)),
                Vector((width + 0.1, -0.225, 0.05 - sillHeight + o)),
                Vector((width + 0.1, 0.225, 0.05 - sillHeight + o)),
                # Sill Top
                Vector((-width - 0.1, 0.225, 0.05 + o)),
                Vector((-width - 0.1, -0.225, 0.05 + o)),
                Vector((width + 0.1, -0.225, 0.05 + o)),
                Vector((width + 0.1, 0.225, 0.05 + o))])
            faces.extend([
                [35, 34, 33, 32],
                [36, 37, 38, 39],
                [32, 36, 39, 35],
                [34, 38, 37, 33],
                [32, 33, 37, 36],
                [39, 38, 34, 35]])
        
        generate_mesh(self, context, verts, faces)
        
        return {'FINISHED'}

class AddStairs(Operator, AddObjectHelper):
    bl_idname = "uii.add_stairs"
    bl_label = "Add Stairs Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    width: FloatProperty(name="Width", default=1.75, min=0.75, max=10, step=25, precision=3, unit="LENGTH")
    height: FloatProperty(name="Height", default=3.25, min=0.25, max=12, step=25, precision=3, unit="LENGTH")
    depth: FloatProperty(name="Step Depth", default=0.25, min=0.25, max=5, step=25, precision=3, unit="LENGTH")
    ramp: BoolProperty(name="Ramp", default=False)
    
    def execute(self, context):
        verts, faces = add_stairs_basic(self, context)
        generate_mesh(self, context, verts, faces)
        
        return {'FINISHED'}

class AddRailing(Operator, AddObjectHelper):
    bl_idname = "uii.add_railing"
    bl_label = "Add Railing Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    width: FloatProperty(name="Width", default=1.75, min=0.75, max=10, step=25, precision=3, unit="LENGTH")
    height: FloatProperty(name="Height", default=3.25, min=0.25, max=12, step=25, precision=3, unit="LENGTH")
    depth: FloatProperty(name="Step Depth", default=0.25, min=0.25, max=5, step=25, precision=3, unit="LENGTH")
    
    def execute(self, context):
        verts, faces = add_railing(self, context)
        generate_mesh(self, context, verts, faces)
        
        return {'FINISHED'}

def add_object_button(self, context):
    self.layout.operator(
        AddDoorway.bl_idname,
        text="Add UII Doorway",
        icon='PLUGIN')
    self.layout.operator(
        AddWindow.bl_idname,
        text="Add UII Window",
        icon='PLUGIN')
    self.layout.operator(
        AddStairs.bl_idname,
        text="Add UII Stairs",
        icon='PLUGIN')
    self.layout.operator(
        AddRailing.bl_idname,
        text="Add UII Railing",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(AddDoorway)
    bpy.utils.register_class(AddWindow)
    bpy.utils.register_class(AddRailing)
    bpy.utils.register_class(AddStairs)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)
    bpy.utils.unregister_class(AddStairs)
    bpy.utils.unregister_class(AddRailing)
    bpy.utils.unregister_class(AddWindow)
    bpy.utils.unregister_class(AddDoorway)

if __name__ == "__main__":
    register()