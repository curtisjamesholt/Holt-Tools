#region INFORMATION
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
bl_info = {
    "name" : "Holt Tools",
    "author" : "Curtis Holt",
    "description" : "Just some workflow tools I put together.",
    "blender" : (4, 5, 0),
    "version" : (6, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}
#endregion
#region IMPORTS
import bpy
from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)
from . easybpy import *
from random import uniform
#endregion
#region PROPERTIES
class HTProperties(PropertyGroup):
    #region PROPERTIES - CLEANUP
    cleanup_mode : EnumProperty(
        name = "Cleanup Mode",
        description = "The mode of cleanup",
        items=[
            ('OUTLINER', "Outliner", ""),
            ('OBJECT', "Object", ""),
            ('MATERIALS', "Materials", ""),
        ],
        default = "OUTLINER"
    )
    autosmooth_angle : IntProperty(
        name = "Autosmooth Angle",
        description = "The angle for autosmoothing",
        default = 60,
        min = 0,
        max = 180
    )
    material_name : StringProperty(
        name = "Material Name",
        description = "The material to perform cleanup operations on",
        default = "Material Name"
    )
    #endregion
    #region PROPERTIES - SELECTION
    selection_mode : EnumProperty(
        name = "Selection Mode",
        description = "The mode of selection",
        items=[
            ('SELECT_ALL_INCLUDING',"Select All Including",""),
            ('SELECT_ALL_TYPE',"Select By Type",""),
            ('SELECT_BY_VERTEX',"Select By Vertex Count","")
        ],
        default = "SELECT_ALL_INCLUDING"
    )
    select_string : StringProperty(
        name = "Select Similar String",
        description = "Used for finding objects that include this in their name",
        default = "Cube"
    )
    is_scene_only : BoolProperty(
        name = "Is Scene Only",
        description = "Toggles whether to only search in the active scene",
        default = False
    )
    is_case_sensitive : BoolProperty(
        name = "Is Case Sensitive",
        description = "Toggles whether to consider case when comparing names",
        default = True
    )
    select_types : EnumProperty(
        name = "Select Types",
        description = "Different types of object to select",
        items=[
            ('ARMATURES',"Armatures",""),
            ('CAMERAS',"Cameras",""),
            ('CURVES',"Curves",""),
            ('EMPTIES',"Empties",""),
            ('GREASE_PENCILS',"Grease Pencils",""),
            ('HAIR',"Hair",""),
            ('LATTICES',"Lattices",""),
            ('LIGHTS',"Lights",""),
            ('LIGHT PROBES',"Light Probes",""),
            ('MESHES',"Meshes",""),
            ('METAS',"Metas",""),
            ('POINT_CLOUDS',"Point Clouds",""),
            ('SURFACES',"Surfaces",""),
            ('TEXT',"Text",""),
            ('VOLUMES',"Volumes",""),
        ],
        default = "MESHES"
    )
    tag_string : StringProperty(
        name = "Tag String",
        description = "Tag to be added as a prefix or suffix",
        default = "Tag"
    )
    delimiter_string : StringProperty(
        name = "Delimiter String",
        description = "Delimiter to use for prefixes and suffixes",
        default = "_"
    )
    vertex_count : IntProperty(
        name = "Vertex Count",
        description = "Vertex count for comparing objects to choose selection",
        default = 10000
    )
    comparison_mode : EnumProperty(
        name = "Comparison Mode",
        description = "Mode to compare the vertex count",
        items = [
            ('GREATER', "Greater Than", ""),
            ('LESS', "Less Than", ""),
            ('EQUAL', "Equal To", "")
        ],
        default = "GREATER"
    )
    #endregion
    #region PROPERTIES - LIGHTING
    light_add_global : FloatProperty(
        name = "Light Add Global",
        description = "Value to add to all lights globally",
        default = 5.0
    )
    light_multiply_global : FloatProperty(
        name = "Light Multiply Global",
        description = "Value to multiply light sources by",
        default = 1.5
    )
    light_mode : EnumProperty(
        name = "Light Mode",
        description = "The mode for modifying light strength",
        items=[
            ('ADDITIVE',"Additive",""),
            ('MULTIPLICATIVE', "Multiplicative", "")
        ],
        default = "ADDITIVE"
    )
    light_target : EnumProperty(
        name = "Light Target",
        description = "The target for lighting changes",
        items=[
            ('LIGHT_OBJECTS', "Light Objects", ""),
            ('EMISSIVE_MATERIALS',"Emissive Materials",""),
            ('BOTH', "Both", "")
        ],
        default = "LIGHT_OBJECTS"
    )
    light_mat_includes : StringProperty(
        name = "Material Name Includes",
        description = "A string that must be included in a material name",
        default = "Emis_"
    )
    light_node_includes : StringProperty(
        name = "Node Name Includes",
        description = "A string that must be included in a node name",
        default = "Light_"
    )
    color : FloatVectorProperty(
        subtype="COLOR",
        min=0,
        max = 1,
        default = [1.0,1.0,1.0]
    )
    color_selected_only : BoolProperty(
        name = "Selected Only",
        description = "Only change color of selected light objects",
        default = True
    )
    #endregion
    #region PROPERTIES - OPTIMIZATION
    decimate_rate : FloatProperty(
        name = "Decimate Rate",
        description = "The rate to quickly decimate selected object",
        default = 0.1,
        min = 0.0,
        max = 1.0
    )
    #endregion
#endregion
#region OPERATORS - CLEANUP - OUTLINER
class HTOOLS_OT_OrganizeOutliner(bpy.types.Operator):
    # Calling Organize Outliner
    bl_idname = "outliner.organize_outliner"
    bl_label = "Organize Outliner"
    bl_description = "Organizes the outliner into categories"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        organize_outliner()
        return {'FINISHED'}
class HTOOLS_OT_ConvertSuffixes(bpy.types.Operator):
    # Calling Convert Suffixes
    bl_idname = "object.convert_suffixes"
    bl_label = "Convert Suffixes"
    bl_description = "Convert .001 suffixes to _1"
    bl_options = {'REGISTER','UNDO'}
    def execute(self, context):
        convert_suffixes()
        return {'FINISHED'}
class HTOOLS_OT_PurgeUnwantedData(bpy.types.Operator):
    bl_idname = "object.purge_unwanted_data"
    bl_label = "Purge Unwanted Data"
    bl_description = "Remove all data that isn't being used"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        clear_unwanted_data()
        return {'FINISHED'}
class HTOOLS_OT_DeepClean(bpy.types.Operator):
    # Doing a deep-clean
    bl_idname = "outliner.deep_clean"
    bl_label = "Deep Clean"
    bl_description = "Just clean the blend file me, will ya?"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        organize_outliner()
        convert_suffixes()
        return {'FINISHED'}
#endregion
#region OPERATORS - CLEANUP - OBJECT
class HTOOLS_OT_SetAutoSmooth(bpy.types.Operator):
    bl_idname = "object.set_auto_smooth"
    bl_label = "Set Auto Smooth"
    bl_description = "Sets auto smooth true and gives angle"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        ht_tool = context.scene.ht_tool
        for o in so():
            set_smooth_angle(o, ht_tool.autosmooth_angle)
        return {'FINISHED'}
class HTOOLS_OT_SyncMeshName(bpy.types.Operator):
    bl_idname = "object.sync_mesh_name"
    bl_label = "Set Auto Smooth"
    bl_description = "Sets auto smooth true and gives angle"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        ht_tool = context.scene.ht_tool
        for o in so():
            if o.data.name != o.name:
                o.data.name = o.name
        return {'FINISHED'}
class HTOOLS_OT_ShiftToWorldOrigin(bpy.types.Operator):
    bl_idname = "object.shift_to_world_origin"
    bl_label = "Shift to World Origin"
    bl_description = "Takes the selected point and uses this to shift the object to the world origin"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        ht_tool = context.scene.ht_tool
        bpy.ops.view3d.snap_cursor_to_selected()
        object_mode(ao())
        set_origin_to_cursor(ao())
        location(ao(), [0,0,0])
        return {'FINISHED'}
#endregion
#region OPERATORS - CLEANUP - MATERIALS
class HTOOLS_OT_RemoveUnusedSlots(bpy.types.Operator):
    bl_idname = "object.remove_unused_slots"
    bl_label = "Remove Unused Slots"
    bl_description = "Removes unused material slots from selected object"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        remove_unused_material_slots()
        return {'FINISHED'}
class HTOOLS_OT_FixDuplicateNodeGroups(bpy.types.Operator):
    bl_idname = "object.fix_duplicate_node_groups"
    bl_label = "Fix Duplicate Node Groups"
    bl_description = "Removes duplicate node groups and replaced with original"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        fix_duplicate_nodes()
        return {'FINISHED'}
class HTOOLS_OT_SetNodeGroupDefaults(bpy.types.Operator):
    bl_idname = "object.set_node_group_defaults"
    bl_label = "Set Defaults"
    bl_description = "Sets the current values to be the default values for selected node groups"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool

        # Set Material Shader Nodes
        for m in bpy.data.materials:
            matnodes = m.node_tree.nodes
            i = 0
            while i < len(matnodes):
                if matnodes[i].select:
                    if matnodes[i].type == 'GROUP':
                        node_group = matnodes[i].node_tree
                        j = 0
                        while j < len(matnodes[i].inputs):
                            x = 0
                            while x < len(node_group.interface.items_tree):
                                if node_group.interface.items_tree[x].in_out == 'INPUT':
                                    if node_group.interface.items_tree[x].name == matnodes[i].inputs[j].name:
                                        node_group.interface.items_tree[x].default_value = matnodes[i].inputs[j].default_value
                                x += 1
                            j += 1
                i += 1
        
        # Set World Shader Nodes
        for w in bpy.data.worlds:
            worldnodes = w.node_tree.nodes
            i = 0
            while i < len(worldnodes):
                if worldnodes[i].select:
                    if worldnodes[i].type == 'GROUP':
                        node_group = worldnodes[i].node_tree
                        j = 0
                        while j < len(worldnodes[i].inputs):
                            x = 0
                            while x < len(node_group.interface.items_tree):
                                if node_group.interface.items_tree[x].in_out == 'INPUT':
                                    if node_group.interface.items_tree[x].name == worldnodes[i].inputs[j].name:
                                        node_group.interface.items_tree[x].default_value = worldnodes[i].inputs[j].default_value
                                x += 1
                            j += 1
                i += 1
        
        # Set Geometry Nodes
        for n in bpy.data.node_groups:
            geonodes = n.nodes
            i = 0
            while i < len(geonodes):
                if geonodes[i].select:
                    if geonodes[i].type == 'GROUP':
                        node_group = geonodes[i].node_tree
                        j = 0
                        while j < len(geonodes[i].inputs):
                            x = 0
                            while x < len(node_group.interface.items_tree):
                                if node_group.interface.items_tree[x].in_out == 'INPUT':
                                    if node_group.interface.items_tree[x].name == geonodes[i].inputs[j].name:
                                        node_group.interface.items_tree[x].default_value = geonodes[i].inputs[j].default_value
                                x += 1
                            j += 1
                i += 1

        return {'FINISHED'}
class HTOOLS_OT_GetNodeGroupDefaults(bpy.types.Operator):
    bl_idname = "object.get_node_group_defaults"
    bl_label = "Get Defaults"
    bl_description = "Gets the current values to be the default values for selected node groups"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---

        # Get Material Shader Nodes
        for m in bpy.data.materials:
            matnodes = m.node_tree.nodes
            i = 0
            while i < len(matnodes):
                if matnodes[i].select:
                    if matnodes[i].type == 'GROUP':
                        node_group = matnodes[i].node_tree
                        j = 0
                        while j < len(matnodes[i].inputs):
                            x = 0
                            while x < len(node_group.interface.items_tree):
                                if node_group.interface.items_tree[x].in_out == 'INPUT':
                                    if node_group.interface.items_tree[x].name == matnodes[i].inputs[j].name:
                                        matnodes[i].inputs[j].default_value = node_group.interface.items_tree[x].default_value
                                x += 1
                            j += 1
                i += 1
        
        # Get World Shader Nodes
        for w in bpy.data.worlds:
            worldnodes = w.node_tree.nodes
            i = 0
            while i < len(worldnodes):
                if worldnodes[i].select:
                    if worldnodes[i].type == 'GROUP':
                        node_group = worldnodes[i].node_tree
                        j = 0
                        while j < len(worldnodes[i].inputs):
                            x = 0
                            while x < len(node_group.interface.items_tree):
                                if node_group.interface.items_tree[x].in_out == 'INPUT':
                                    if node_group.interface.items_tree[x].name == worldnodes[i].inputs[j].name:
                                         worldnodes[i].inputs[j].default_value = node_group.interface.items_tree[x].default_value
                                x += 1
                            j += 1
                i += 1

        # Get Geometry Nodes
        for n in bpy.data.node_groups:
            geonodes = n.nodes
            i = 0
            while i < len(geonodes):
                if geonodes[i].select:
                    if geonodes[i].type == 'GROUP':
                        node_group = geonodes[i].node_tree
                        j = 0
                        while j < len(geonodes[i].inputs):
                            x = 0
                            while x < len(node_group.interface.items_tree):
                                if node_group.interface.items_tree[x].in_out == 'INPUT':
                                    if node_group.interface.items_tree[x].name == geonodes[i].inputs[j].name:
                                        geonodes[i].inputs[j].default_value = node_group.interface.items_tree[x].default_value
                                x += 1
                            j += 1
                i += 1

        return {'FINISHED'}
#endregion
#region OPERATORS - SELECTION
class HTOOLS_OT_SelectAllIncluding(bpy.types.Operator):
    # Calling Select All Including
    bl_idname = "object.select_all_including"
    bl_label = "Select All Including"
    bl_description = "Selects all objects including ht_tools.select_type"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        if ht_tool.is_case_sensitive:
            select_objects_including(ht_tool.select_string, True)
        else:
            select_objects_including(ht_tool.select_string, False)
        return {'FINISHED'}
class HTOOLS_OT_FormCollectionString(bpy.types.Operator):
    bl_idname = "object.form_collection_string"
    bl_label = "Form Collection"
    bl_description = "Form a collection with the found objects"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        col = []
        if collection_exists(ht_tool.select_string):
            col = get_collection(ht_tool.select_string)
        else:
            col = create_collection(ht_tool.select_string)
        obj_list = []
        if ht_tool.is_case_sensitive:
            obj_list = get_objects_including(ht_tool.select_string, True)
        else:
            obj_list = get_objects_including(ht_tool.select_string, False)
        move_objects_to_collection(obj_list, col)
        return {'FINISHED'}
class HTOOLS_OT_SelectAllType(bpy.types.Operator):
    # Calling Select All Type
    bl_idname = "object.select_all_type"
    bl_label = "Select All Type"
    bl_description = "Selects all objects of ht_tools.select_string"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        if ht_tool.select_types == "MESHES":
            select_all_meshes()
        if ht_tool.select_types == "CURVES":
            select_all_curves()
        if ht_tool.select_types == "SURFACES":
            select_all_surfaces()
        if ht_tool.select_types == "METAS":
            select_all_metas()
        if ht_tool.select_types == "TEXT":
            select_all_text()
        if ht_tool.select_types == "HAIR":
            select_all_hair()
        if ht_tool.select_types == "POINT_CLOUDS":
            select_all_point_clouds()
        if ht_tool.select_types == "VOLUMES":
            select_all_volumes()
        if ht_tool.select_types == "ARMATURES":
            select_all_armatures()
        if ht_tool.select_types == "LATTICES":
            select_all_lattices()
        if ht_tool.select_types == "EMPTIES":
            select_all_empties()
        if ht_tool.select_types == "GREASE_PENCILS":
            select_all_grease_pencils()
        if ht_tool.select_types == "CAMERAS":
            select_all_cameras()
        if ht_tool.select_types == "LIGHTS":
            select_all_lights()
        if ht_tool.select_types == "LIGHT PROBES":
            select_all_light_probes()
        return {'FINISHED'}
class HTOOLS_OT_FormCollectionType(bpy.types.Operator):
    bl_idname = "object.form_collection_type"
    bl_label = "Form Collection"
    bl_description = "Form a collection with the found objects of a type"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        col = None
        if ht_tool.select_types == "MESHES":
            select_all_meshes()
            if collection_exists("Meshes"):
                col = get_collection("Meshes")
            else:
                col = create_collection("Meshes")

        if ht_tool.select_types == "CURVES":
            select_all_curves()
            if collection_exists("Curves"):
                col = get_collection("Curves")
            else:
                col = create_collection("Curves")

        if ht_tool.select_types == "SURFACES":
            select_all_surfaces()
            if collection_exists("Surfaces"):
                col = get_collection("Surfaces")
            else:
                col = create_collection("Surfaces")

        if ht_tool.select_types == "METAS":
            select_all_metas()
            if collection_exists("Metas"):
                col = get_collection("Metas")
            else:
                col = create_collection("Metas")

        if ht_tool.select_types == "TEXT":
            select_all_text()
            if collection_exists("Text"):
                col = get_collection("Text")
            else:
                col = create_collection("Text")

        if ht_tool.select_types == "HAIR":
            select_all_hair()
            if collection_exists("Hair"):
                col = get_collection("Hair")
            else:
                col = create_collection("Hair")

        if ht_tool.select_types == "POINT_CLOUDS":
            select_all_point_clouds()
            if collection_exists("Point Clouds"):
                col = get_collection("Point Clouds")
            else:
                col = create_collection("Point Clouds")

        if ht_tool.select_types == "VOLUMES":
            select_all_volumes()
            if collection_exists("Volumes"):
                col = get_collection("Volumes")
            else:
                col = create_collection("Volumes")

        if ht_tool.select_types == "ARMATURES":
            select_all_armatures()
            if collection_exists("Armatures"):
                col = get_collection("Armatures")
            else:
                col = create_collection("Armatures")

        if ht_tool.select_types == "LATTICES":
            select_all_lattices()
            if collection_exists("Lattices"):
                col = get_collection("Lattices")
            else:
                col = create_collection("Lattices")

        if ht_tool.select_types == "EMPTIES":
            select_all_empties()
            if collection_exists("Empties"):
                col = get_collection("Empties")
            else:
                col = create_collection("Empties")

        if ht_tool.select_types == "GREASE_PENCILS":
            select_all_grease_pencils()
            if collection_exists("Grease Pencils"):
                col = get_collection("Grease Pencils")
            else:
                col = create_collection("Grease Pencils")

        if ht_tool.select_types == "CAMERAS":
            select_all_cameras()
            if collection_exists("Cameras"):
                col = get_collection("Cameras")
            else:
                col = create_collection("Cameras")

        if ht_tool.select_types == "LIGHTS":
            select_all_lights()
            if collection_exists("Lights"):
                col = get_collection("Lights")
            else:
                col = create_collection("Lights")

        if ht_tool.select_types == "LIGHT PROBES":
            select_all_light_probes()
            if collection_exists("Light Probes"):
                col = get_collection("Light Probes")
            else:
                col = create_collection("Light Probes")

        move_objects_to_collection(so(), col)
        return {'FINISHED'}
class HTOOLS_OT_NameAddPrefix(bpy.types.Operator):
    bl_idname = "object.name_add_prefix"
    bl_label = "Name Add Prefix"
    bl_description = "Adds the tag string as a prefix"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        add_prefix_to_name(so(), ht_tool.tag_string, ht_tool.delimiter_string)
        return {'FINISHED'}
class HTOOLS_OT_NameAddSuffix(bpy.types.Operator):
    bl_idname = "object.name_add_suffix"
    bl_label = "Name Add Suffix"
    bl_description = "Adds the tag string as a suffix"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        add_suffix_to_name(so(), ht_tool.tag_string, ht_tool.delimiter_string)
        return {'FINISHED'}
class HTOOLS_OT_SelectByVertexCount(bpy.types.Operator):
    bl_idname = "object.select_by_vertex_count"
    bl_label = "Select By Vertex Count"
    bl_description = "Selects objects by comparing given vertex count"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        select_objects_by_vertex(ht_tool.vertex_count, ht_tool.comparison_mode)
        return {'FINISHED'}
class HTOOLS_OT_FormCollectionVertices(bpy.types.Operator):
    bl_idname = "object.form_collection_vertices"
    bl_label = "Form Collection"
    bl_description = "Form a collection with the found objects depending on vertex count"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        col = None
        colname = ""
        cmode = ht_tool.comparison_mode.upper()
        if cmode == "EQUAL" or cmode == "SAME":
            colname = "Equal to " + str(ht_tool.vertex_count)
            
        if cmode == "GREATER" or cmode == "MORE":
            colname = "Greater than " + str(ht_tool.vertex_count)
            pass
        if cmode == "LESS" or cmode == "FEWER":
            colname = "Less than " + str(ht_tool.vertex_count)
        
        if collection_exists(colname):
            col = get_collection(colname)
        else:
            col = create_collection(colname)

        select_objects_by_vertex(ht_tool.vertex_count, ht_tool.comparison_mode)
        move_objects_to_collection(so(), col)
        return {'FINISHED'}
#endregion
#region OPERATORS - LIGHTING
class HTOOLS_OT_AddLightIntensityGlobal(bpy.types.Operator):
    # Add Light Intensity Global
    bl_idname = "object.add_light_intensity_global"
    bl_label = "Add Light Intensity Global"
    bl_description = "Adds intensity to all lights in the scene"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        if ht_tool.light_target == "LIGHT_OBJECTS" or ht_tool.light_target == "BOTH":
            select_all_lights()
            light_power_add(ht_tool.light_add_global)
        if ht_tool.light_target == "EMISSIVE_MATERIALS" or ht_tool.light_target == "BOTH":
            mats = get_all_materials()
            for m in mats:
                if ht_tool.light_mat_includes in m.name:
                    nodes = get_nodes(m)
                    for n in nodes:
                        if n.type == 'EMISSION':
                            if ht_tool.light_node_includes in n.name:
                                if ht_tool.light_node_includes in n.name:
                                    n.inputs[1].default_value += ht_tool.light_add_global
                        if n.type == 'BSDF_PRINCIPLED':
                            if ht_tool.light_node_includes in n.name:
                                s_index = get_index_of_input(n, "Emission Strength")
                                n.inputs[s_index].default_value += ht_tool.light_add_global #20
        return {'FINISHED'}
class HTOOLS_OT_SubtractLightIntensityGlobal(bpy.types.Operator):
    # Add Light Intensity Global
    bl_idname = "object.subtract_light_intensity_global"
    bl_label = "Subtract Light Intensity Global"
    bl_description = "Subtracts intensity to all lights in the scene"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        if ht_tool.light_target == "LIGHT_OBJECTS" or ht_tool.light_target == "BOTH":
            select_all_lights()
            light_power_add(-ht_tool.light_add_global)
        if ht_tool.light_target == "EMISSIVE_MATERIALS" or ht_tool.light_target == "BOTH":
            mats = get_all_materials()
            for m in mats:
                if ht_tool.light_mat_includes in m.name:
                    nodes = get_nodes(m)
                    for n in nodes:
                        if n.type == 'EMISSION':
                            if ht_tool.light_node_includes in n.name:
                                n.inputs[1].default_value -= ht_tool.light_add_global
                        if n.type == 'BSDF_PRINCIPLED':
                            if ht_tool.light_node_includes in n.name:
                                s_index = get_index_of_input(n, "Emission Strength")
                                n.inputs[s_index].default_value -= ht_tool.light_add_global #20
        return {'FINISHED'}
class HTOOLS_OT_MultiplyLightIntensityGlobal(bpy.types.Operator):
    # Multiply Light Intensity Global
    bl_idname = "object.multiply_light_intensity_global"
    bl_label = "Multiply Light Intensity Global"
    bl_description = "Multiplies intensity of all lights in the scene"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        if ht_tool.light_target == "LIGHT_OBJECTS" or ht_tool.light_target == "BOTH":
            select_all_lights()
            light_power_multiply(ht_tool.light_multiply_global)
        if ht_tool.light_target == "EMISSIVE_MATERIALS" or ht_tool.light_target == "BOTH":
            mats = get_all_materials()
            for m in mats:
                if ht_tool.light_mat_includes in m.name:
                    nodes = get_nodes(m)
                    for n in nodes:
                        if n.type == 'EMISSION':
                            if ht_tool.light_node_includes in n.name:
                                n.inputs[1].default_value *= ht_tool.light_multiply_global
                        if n.type == 'BSDF_PRINCIPLED':
                            if ht_tool.light_node_includes in n.name:
                                s_index = get_index_of_input(n, "Emission Strength")
                                n.inputs[s_index].default_value *= ht_tool.light_multiply_global #20
        return{'FINISHED'}
class HTOOLS_OT_SetLightColor(bpy.types.Operator):
    bl_idname = "object.set_light_color"
    bl_label = "Set Light Color"
    bl_description = "Sets the color of selected lights to the RGB property"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        if ht_tool.color_selected_only == True:
            for o in so():
                if o.type == "LIGHT":
                    o.data.color = ht_tool.color
        else:
            for l in bpy.data.lights:
                l.color = ht_tool.color
        
        return {'FINISHED'}
class HTOOLS_OT_RandomizeLightColor(bpy.types.Operator):
    bl_idname = "object.randomize_light_color"
    bl_label = "Randomize Light Color"
    bl_description = "Randomizes the light color for selected light objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        if ht_tool.color_selected_only == True:
            for o in so():
                if o.type == "LIGHT":
                    o.data.color.r = uniform(0,1)
                    o.data.color.g = uniform(0,1)
                    o.data.color.b = uniform(0,1)
        else:
            for l in bpy.data.lights:
                l.color.r = uniform(0,1)
                l.color.g = uniform(0,1)
                l.color.b = uniform(0,1)
        return {'FINISHED'}
#endregion
#region OPERATORS - OPTIMIZATION
class HTOOLS_OT_QuickDecimate(bpy.types.Operator):
    # Quick Decimate
    bl_idname = "object.quick_decimate"
    bl_label = "Quick Decimate"
    bl_description = "Quickly decimates object based on ht_tool.decimate_rate"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        objs = so()
        for o in objs:
            mod = add_decimate(o)
            mod.ratio = ht_tool.decimate_rate
            apply_all_modifiers(o)
        return {'FINISHED'}
#endregion
#region OPERATORS - WORLD
class HTOOLS_OT_ToggleWorldVolume(bpy.types.Operator):
    bl_idname = "object.toggle_world_volume"
    bl_label = "Toggle World Volume"
    bl_description = "Toggles volume shaders in the world nodes"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        wnodes = get_world_nodes()
        for n in wnodes:
            if n.type == "PRINCIPLED_VOLUME" or n.type == "VOLUME_SCATTER":
                if n.mute == True:
                    n.mute = False
                else:
                    n.mute = True
        return {'FINISHED'}
#endregion
#region PANELS - CLEANUP
class HTOOLS_PT_Cleanup_Panel(Panel):
    bl_idname = "HTOOLS_PT_Cleanup_Panel"
    bl_label = "Cleanup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    #bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text = "", icon = "BRUSH_DATA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
class HTOOLS_PT_Cleanup_Outliner(Panel):
    bl_idname = "HTOOLS_PT_Cleanup_Outliner"
    bl_label = "Outliner"
    bl_parent_id = "HTOOLS_PT_Cleanup_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
            self.layout.label(text = "", icon = "OUTLINER")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.operator("outliner.organize_outliner")
        row = col.row(align=True)
        row.operator("object.convert_suffixes")
        row = col.row(align=True)
        row.operator("object.purge_unwanted_data")
        row = col.row(align=True)
        row.operator("outliner.deep_clean", text = "^ Deep Clean ^")
        row = col.row(align=True)
class HTOOLS_PT_Cleanup_Objects(Panel):
    bl_idname = "HTOOLS_PT_Cleanup_Objects"
    bl_label = "Objects"
    bl_parent_id = "HTOOLS_PT_Cleanup_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text = "", icon = "OBJECT_DATA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        box = layout.box()
        col = box.column()
        if context.active_object != None:
            if context.active_object.mode == 'EDIT':
                row = col.row()
                row.separator()
                row = col.row()
                row.operator("mesh.normals_make_consistent", text="Recalculate Normals")
                row = col.row()
                row.operator("mesh.remove_doubles", text="Merge By Distance")
                row = col.row()
                row.operator("object.shift_to_world_origin", text = "Shift to World Origin")
                row = col.row()
                row.separator()
        if context.active_object != None:
            if context.active_object.mode == 'OBJECT':
                row = col.label(text="( more in edit mode )")
        row = col.row()
        row.operator("mesh.customdata_custom_splitnormals_clear", text="Clean Custom Split Normals")
        row = col.row()
        row.operator("anim.keyframe_clear_v3d", text="Clear Keyframes")

        row = col.row()
        row.label(text="Auto Smooth")
        row = col.row()
        row.prop(ht_tool, "autosmooth_angle", text="")
        row = col.row()
        row.operator("object.set_auto_smooth", text="^ Set Auto Smooth ^")
        row = col.row()
        row.label(text="Other Operations")
        row = col.row()
        row.operator("object.sync_mesh_name", text="Sync Mesh Name")
        row = col.row()
        row.operator("object.transform_apply", text="Apply Transforms")
class HTOOLS_PT_Cleanup_Materials(Panel):
    bl_idname = "HTOOLS_PT_Cleanup_Materials"
    bl_label = "Materials"
    bl_parent_id = "HTOOLS_PT_Cleanup_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text = "", icon = "MATERIAL")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        box = layout.box()
        col = box.column()
        row = col.row()
        row.operator("object.remove_unused_slots", text="Remove Unused Slots")
        row = col.row()
        row.operator("object.fix_duplicate_node_groups", text="Fix Duplicate Node Groups")

        box2 = layout.box()
        col = box2.column()
        row = col.row()
        #row.prop(ht_tool, "material_name", text = "")
        #row = col.row()
        row.label(text="( select node groups )")
        row = col.row()
        row.operator("object.set_node_group_defaults", text = "Set Defaults")
        row = col.row()
        row.operator("object.get_node_group_defaults", text = "Get Defaults")
#endregion
#region PANELS - SELECTION
class HTOOLS_PT_Selection_Panel(Panel):
    bl_idname = "HTOOLS_PT_Selection_Panel"
    bl_label = "Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"

    def draw_header(self, context):
            self.layout.label(text = "", icon = "RESTRICT_SELECT_OFF")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
class HTOOLS_PT_Selection_AllIncluding(Panel):
    bl_idname = "HTOOLS_PT_Selection_AllIncluding"
    bl_label = "Select All Including"
    bl_parent_id = "HTOOLS_PT_Selection_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
            self.layout.label(text = "", icon = "FONT_DATA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        # Select all including
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.label(text="Select all objects including:")
        row = col.row(align=True)
        row.prop(ht_tool, "select_string", text = "")
        row = col.row(align=True)
        row.prop(ht_tool, "is_case_sensitive", text="Case Sensitive")
        row = col.row(align=True)
        row.operator("object.select_all_including", text="^ Select All Including ^")
        row = col.row(align=True)
        row.operator("object.form_collection_string", text = "Form Collection")

        # Tagging objects
        box2 = box.box()
        col = box2.column()
        row = col.row(align=True)
        row.label(text="Tag Objects")
        row = col.row(align=True)
        row.prop(ht_tool, "tag_string", text="")
        row.scale_x=-20
        row.prop(ht_tool, "delimiter_string", text="")
        row = col.row(align=True)
        row.operator("object.name_add_prefix", text="Prefix")
        row.operator("object.name_add_suffix", text="Suffix")
class HTOOLS_PT_Selection_ByType(Panel):
    bl_idname = "HTOOLS_PT_Selection_ByType"
    bl_label = "Select By Type"
    bl_parent_id = "HTOOLS_PT_Selection_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
            self.layout.label(text = "", icon = "MESH_DATA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.label(text="Select all objects of this type:")
        row = col.row(align=True)
        row.prop(ht_tool, "select_types", text="")
        row = col.row(align=True)
        row.separator()
        row = col.row(align=True)
        row.operator("object.select_all_type", text="^ Select All Type ^")
        row = col.row(align=True)
        row.operator("object.form_collection_type", text = "Form Collection")
class HTOOLS_PT_Selection_ByVertexCount(Panel):
    bl_idname = "HTOOLS_PT_Selection_ByVertexCount"
    bl_label = "Select By Vertex Count"
    bl_parent_id = "HTOOLS_PT_Selection_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
            self.layout.label(text = "", icon = "SNAP_VERTEX")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.label(text="Comparison:")
        row = col.row(align=True)
        row.prop(ht_tool, "comparison_mode", text="")
        row = col.row(align=True)
        row.label(text="Vertex Count:")
        row = col.row(align=True)
        row.prop(ht_tool, "vertex_count", text="")
        row = col.row(align=True)
        row.separator()
        row = col.row(align=True)
        row.operator("object.select_by_vertex_count", text="^ Select ^")
        row = col.row(align=True)
        row.operator("object.form_collection_vertices", text = "Form Collection")
#endregion
#region PANELS - LIGHTING
class HTOOLS_PT_Lighting_Panel(Panel):
    bl_idname = "HTOOLS_PT_Lighting_Panel"
    bl_label = "Lighting"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"

    def draw_header(self, context):
            self.layout.label(text = "", icon = "LIGHT")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
class HTOOLS_PT_Lighting_Power(Panel):
    bl_idname = "HTOOLS_PT_Lighting_Power"
    bl_label = "Power"
    bl_parent_id = "HTOOLS_PT_Lighting_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
            self.layout.label(text = "", icon = "LIGHT_SUN")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---

        box = layout.box()
        #box.label(text="Global Lighting Mode")
        col = box.column()
        row = col.row(align=True)
        row.label(text="Global Lighting Mode")
        row = col.row(align=True)
        row.prop(ht_tool, "light_mode", text="")
        row = col.row(align=True)
        row.label(text="Target")
        row = col.row(align=True)
        row.prop(ht_tool, "light_target", text="")
        row = col.row(align=True)

        if ht_tool.light_target == "EMISSIVE_MATERIALS" or ht_tool.light_target == "BOTH":
            row.label(text="Material Name Includes:")
            row = col.row(align=True)
            row.prop(ht_tool, "light_mat_includes", text="")
            row = col.row(align=True)
            row.label(text="Node Name Includes:")
            row = col.row(align=True)
            row.prop(ht_tool, "light_node_includes", text="")

        row = col.row(align=True)
        row.separator()
        if ht_tool.light_mode == "ADDITIVE":
            row = col.row(align=True)
            row.prop(ht_tool, "light_add_global", text="")
            row = col.row(align=True)
            row.operator("object.subtract_light_intensity_global", text="-")
            row.operator("object.add_light_intensity_global", text="+")

        if ht_tool.light_mode == "MULTIPLICATIVE":
            row = col.row(align=True)
            row.scale_x = 20
            row.prop(ht_tool, "light_multiply_global", text="")
            row.scale_x = 0
            row.operator("object.multiply_light_intensity_global", text="X")
class HTOOLS_PT_Lighting_Color(Panel):
    bl_idname = "HTOOLS_PT_Lighting_Color"
    bl_label = "Color"
    bl_parent_id = "HTOOLS_PT_Lighting_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
            self.layout.label(text = "", icon = "COLOR")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.prop(ht_tool, "color", text="")
        row = col.row(align=True)
        row.prop(ht_tool, "color_selected_only", text = "Selected Only")
        row = col.row(align=True)
        row.operator("object.set_light_color", text = "Set Light Color")
        row = col.row(align=True)
        row.operator("object.randomize_light_color", text = "Randomize Light Color")
#endregion
#region PANELS - OPTIMIZATION
class HTOOLS_PT_Optimization_Panel(Panel):
    bl_idname = "HTOOLS_PT_Optimization_Panel"
    bl_label = "Optimization"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"

    def draw_header(self, context):
        self.layout.label(text = "", icon = "MOD_DECIM")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
class HTOOLS_PT_Optimization_Mesh(Panel):
    bl_idname = "HTOOLS_PT_Optimization_Mesh"
    bl_label = "Mesh"
    bl_parent_id = "HTOOLS_PT_Optimization_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text = "", icon = "MESH_DATA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        b = layout.box()
        b.label(text="Quick Decimation")
        column = b.column()

        row = column.row()
        row.prop(ht_tool, "decimate_rate", text="")
        row = column.row()
        row.operator("object.quick_decimate", text="Quick Decimate")
#endregion
#region PANELS - INTERFACE
class HTOOLS_PT_Interface_Panel(Panel):
    bl_idname = "HTOOLS_PT_Interface_Panel"
    bl_label = "Interface"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"

    def draw_header(self, context):
        self.layout.label(text = "", icon = "PROPERTIES")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
class HTOOLS_PT_Interface_Theme(Panel):
    bl_idname = "HTOOLS_PT_Interface_Theme"
    bl_label = "Theme"
    bl_parent_id = "HTOOLS_PT_Interface_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text = "", icon = "PRESET")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        b = layout.box()
        #b.label(text="Change the theme.")
        column = b.column()
        row = column.row()
        row.menu("USERPREF_MT_interface_theme_presets")
#endregion
#region PANELS - WORLD
class HTOOLS_PT_World_Panel(Panel):
    bl_idname = "HTOOLS_PT_World_Panel"
    bl_label = "World"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"

    def draw_header(self, context):
        self.layout.label(text = "", icon = "WORLD")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
class HTOOLS_PT_World_Volume(Panel):
    bl_idname = "HTOOLS_PT_World_Volume"
    bl_label = "Volume"
    bl_parent_id = "HTOOLS_PT_World_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text = "", icon = "VOLUME_DATA")
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        b = layout.box()
        column = b.column()
        row = column.row()
        row.operator("object.toggle_world_volume", text = "Toggle World Volume")
#endregion
#region PANELS - INFO
class HTOOLS_PT_HoltToolsInfo(Panel):
    bl_idname = "OBJECT_PT_HoltToolsInfo"
    bl_label = "Information"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"

    def draw_header(self, context):
        self.layout.label(text = "", icon = "INFO")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---

        #Operations Layout
        box = layout.box()
        column = box.column()
        column.label(text = "Created by Curtis Holt")
        column.label(text="Enhanced with EasyBPY")
        #---------- Box - Support
        b = box.box()
        b.label(text="Support")
        column = b.column()

        row = column.row()
        row.scale_y = 1.2
        row.operator("wm.url_open", text = "Donate", icon='WORLD').url = "https://www.curtisholt.online/donate"
        #----------

        #---------- Box - Social
        b = box.box()
        b.label(text="Social")
        column = b.column()

        row = column.row()
        row.scale_y = 1.2
        row.operator("wm.url_open", text="YouTube", icon='FILE_MOVIE').url = "https://www.youtube.com/CurtisHolt"
        row.operator("wm.url_open", text="Twitter", icon='COMMUNITY').url = "https://www.twitter.com/curtisjamesholt"
        
        row = column.row()
        row.scale_y = 1.2
        row.operator("wm.url_open", text="Website", icon='WORLD').url = "https://www.curtisholt.online"
        row.operator("wm.url_open", text="Instagram", icon='COMMUNITY').url = "https://www.instagram.com/curtisjamesholt"
#endregion
#region REGISTRATION
classes = (
    HTProperties,
    # Cleanup
    HTOOLS_OT_OrganizeOutliner,
    HTOOLS_OT_ConvertSuffixes,
    HTOOLS_OT_DeepClean,
    HTOOLS_OT_PurgeUnwantedData,
    HTOOLS_OT_SetAutoSmooth,
    HTOOLS_OT_SyncMeshName,
    HTOOLS_OT_ShiftToWorldOrigin,
    HTOOLS_OT_RemoveUnusedSlots,
    HTOOLS_OT_FixDuplicateNodeGroups,
    HTOOLS_OT_SetNodeGroupDefaults,
    HTOOLS_OT_GetNodeGroupDefaults,
    # Selection
    HTOOLS_OT_SelectAllIncluding,
    HTOOLS_OT_FormCollectionString,
    HTOOLS_OT_SelectAllType,
    HTOOLS_OT_FormCollectionType,
    HTOOLS_OT_NameAddPrefix,
    HTOOLS_OT_NameAddSuffix,
    HTOOLS_OT_SelectByVertexCount,
    HTOOLS_OT_FormCollectionVertices,
    # Lighting
    HTOOLS_OT_AddLightIntensityGlobal,
    HTOOLS_OT_SubtractLightIntensityGlobal,
    HTOOLS_OT_MultiplyLightIntensityGlobal,
    HTOOLS_OT_SetLightColor,
    HTOOLS_OT_RandomizeLightColor,
    # Optimization
    HTOOLS_OT_QuickDecimate,
    # World
    HTOOLS_OT_ToggleWorldVolume,
    # Panels
    # Cleanup
    HTOOLS_PT_Cleanup_Panel,
    HTOOLS_PT_Cleanup_Outliner,
    HTOOLS_PT_Cleanup_Objects,
    HTOOLS_PT_Cleanup_Materials,
    # Selection
    HTOOLS_PT_Selection_Panel,
    HTOOLS_PT_Selection_AllIncluding,
    HTOOLS_PT_Selection_ByType,
    HTOOLS_PT_Selection_ByVertexCount,
    # Lighting
    HTOOLS_PT_Lighting_Panel,
    HTOOLS_PT_Lighting_Power,
    HTOOLS_PT_Lighting_Color,
    # Optimization
    HTOOLS_PT_Optimization_Panel,
    HTOOLS_PT_Optimization_Mesh,
    # Interface
    HTOOLS_PT_Interface_Panel,
    HTOOLS_PT_Interface_Theme,
    # World
    HTOOLS_PT_World_Panel,
    HTOOLS_PT_World_Volume,
    # Information
    HTOOLS_PT_HoltToolsInfo
)
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.ht_tool = PointerProperty(type=HTProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.ht_tool

if __name__ == "__main__":
    register()
#endregion