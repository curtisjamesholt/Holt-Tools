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
    "blender" : (2, 90, 3),
    "version" : (0, 0, 3),
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
    light_add_global : IntProperty(
        name = "Light Add Global",
        description = "Value to add to all lights globally",
        default = 5
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
            ('EMISSIVE_MATERIALS',"Emissive Materials","")
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
class HOLTTOOLS_OT_OrganizeOutliner(bpy.types.Operator):
    # Calling Organize Outliner
    bl_idname = "outliner.organize_outliner"
    bl_label = "Organize Outliner"
    bl_description = "Organizes the outliner into categories"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        organize_outliner()
        return {'FINISHED'}
class HOLTTOOLS_OT_ConvertSuffixes(bpy.types.Operator):
    # Calling Convert Suffixes
    bl_idname = "object.convert_suffixes"
    bl_label = "Convert Suffixes"
    bl_description = "Convert .001 suffixes to _1"
    bl_options = {'REGISTER','UNDO'}
    def execute(self, context):
        convert_suffixes()
        return {'FINISHED'}
class HOLTTOOLS_OT_PurgeUnwantedData(bpy.types.Operator):
    bl_idname = "object.purge_unwanted_data"
    bl_label = "Purge Unwanted Data"
    bl_description = "Remove all data that isn't being used"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        clear_unwanted_data()
        return {'FINISHED'}
class HOLTTOOLS_OT_DeepClean(bpy.types.Operator):
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
class HOLTTOOLS_OT_SetAutoSmooth(bpy.types.Operator):
    bl_idname = "object.set_auto_smooth"
    bl_label = "Set Auto Smooth"
    bl_description = "Sets auto smooth true and gives angle"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        ht_tool = context.scene.ht_tool
        set_smooth_angle(ao(), ht_tool.autosmooth_angle)
        return {'FINISHED'}
#endregion
#region OPERATORS - CLEANUP - MATERIALS
class HOLTTOOLS_OT_RemoveUnusedSlots(bpy.types.Operator):
    bl_idname = "object.remove_unused_slots"
    bl_label = "Remove Unused Slots"
    bl_description = "Removes unused material slots from selected object"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        remove_unused_material_slots()
        return {'FINISHED'}
class HOLTTOOLS_OT_FixDuplicateNodeGroups(bpy.types.Operator):
    bl_idname = "object.fix_duplicate_node_groups"
    bl_label = "Fix Duplicate Node Groups"
    bl_description = "Removes duplicate node groups and replaced with original"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        fix_duplicate_nodes()
        return {'FINISHED'}
#endregion
#region OPERATORS - SELECTION
class HOLTTOOLS_OT_SelectAllIncluding(bpy.types.Operator):
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
class HOLTTOOLS_OT_SelectAllType(bpy.types.Operator):
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
class HOLTTOOLS_OT_NameAddPrefix(bpy.types.Operator):
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
class HOLTTOOLS_OT_NameAddSuffix(bpy.types.Operator):
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
class HOLTTOOLS_OT_SelectByVertexCount(bpy.types.Operator):
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
#endregion
#region OPERATORS - LIGHTING
class HOLTTOOLS_OT_AddLightIntensityGlobal(bpy.types.Operator):
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
        if ht_tool.light_target == "LIGHT_OBJECTS":
            select_all_lights()
            light_power_add(ht_tool.light_add_global)
        if ht_tool.light_target == "EMISSIVE_MATERIALS":
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
                                n.inputs[18].default_value += ht_tool.light_add_global
        return {'FINISHED'}
class HOLTTOOLS_OT_SubtractLightIntensityGlobal(bpy.types.Operator):
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
        if ht_tool.light_target == "LIGHT_OBJECTS":
            select_all_lights()
            light_power_add(-ht_tool.light_add_global)
        if ht_tool.light_target == "EMISSIVE_MATERIALS":
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
                                n.inputs[18].default_value -= ht_tool.light_add_global
        return {'FINISHED'}
class HOLTTOOLS_OT_MultiplyLightIntensityGlobal(bpy.types.Operator):
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
        if ht_tool.light_target == "LIGHT_OBJECTS":
            select_all_lights()
            light_power_multiply(ht_tool.light_multiply_global)
        if ht_tool.light_target == "EMISSIVE_MATERIALS":
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
                                n.inputs[18].default_value *= ht_tool.light_multiply_global
        return{'FINISHED'}
#endregion
#region OPERATORS - OPTIMIZATION
class HOLTTOOLS_OT_QuickDecimate(bpy.types.Operator):
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
#region PANELS
class OBJECT_PT_HoltToolsCleanup(Panel):
    bl_idname = "OBJECT_PT_HoltToolsCleanup"
    bl_label = "Holt Tools - Cleanup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---
        box = layout.box()
        box.label(text="Cleanup Mode")
        col = box.column()
        row = col.prop(ht_tool, "cleanup_mode", text="")
        row = col.row(align=True)

        if ht_tool.cleanup_mode == 'OUTLINER':
            row.operator("outliner.organize_outliner")
            row = col.row(align=True)
            row.operator("object.convert_suffixes")
            row = col.row(align=True)
            row.operator("object.purge_unwanted_data")
            row = col.row(align=True)
            row.operator("outliner.deep_clean", text = "^ Deep Clean ^")
            row = col.row(align=True)
        if ht_tool.cleanup_mode == "OBJECT":
            if context.active_object != None:
                if context.active_object.mode == 'EDIT':
                    row = col.row()
                    row.separator()
                    row = col.row()
                    row.operator("mesh.normals_make_consistent", text="Recalculate Normals")
                    row = col.row()
                    row.operator("mesh.remove_doubles", text="Merge By Distance")
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
            pass
        if ht_tool.cleanup_mode == "MATERIALS":
            row = col.row()
            row.operator("object.remove_unused_slots", text="Remove Unused Slots")
            row = col.row()
            row.operator("object.fix_duplicate_node_groups", text="Fix Duplicate Node Groups")
            pass
class OBJECT_PT_HoltToolsSelection(Panel):
    bl_idname = "OBJECT_PT_HoltToolsSelection"
    bl_label = "Holt Tools - Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool

        #---
        box = layout.box()
        box.label(text="Selection Modes")

        col = box.column()
        row = col.row(align=True)
        row.prop(ht_tool,"selection_mode", text="")
        row = col.row(align=True)

        if ht_tool.selection_mode == 'SELECT_ALL_INCLUDING':
            # Select all including
            box2 = box.box()
            col = box2.column()
            row = col.row(align=True)
            row.label(text="Select all objects including:")
            row = col.row(align=True)
            row.prop(ht_tool, "select_string", text = "")
            row = col.row(align=True)
            row.prop(ht_tool, "is_case_sensitive", text="Case Sensitive")
            row = col.row(align=True)
            row.operator("object.select_all_including", text="^ Select All Including ^")
            row = col.row(align=True)

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

        if ht_tool.selection_mode == 'SELECT_ALL_TYPE':
            # Select all by type
            row.label(text="Select all objects of this type:")
            row = col.row(align=True)
            row.prop(ht_tool, "select_types", text="")
            row = col.row(align=True)
            row.separator()
            row = col.row(align=True)
            row.operator("object.select_all_type", text="^ Select All Type ^")

        if ht_tool.selection_mode == "SELECT_BY_VERTEX":
            # Select by vertex
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
class OBJECT_PT_HoltToolsLighting(Panel):
    bl_idname = "OBJECT_PT_HoltToolsLighting"
    bl_label = "Holt Tools - Lighting"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
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

        if ht_tool.light_target == "EMISSIVE_MATERIALS":
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
class OBJECT_PT_HoltToolsOptimization(Panel):
    bl_idname = "OBJECT_PT_HoltToolsOptimization"
    bl_label = "Holt Tools - Optimization"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"
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
class OBJECT_PT_HoltToolsInfo(Panel):
    bl_idname = "OBJECT_PT_HoltToolsInfo"
    bl_label = "Holt Tools - Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Holt Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ht_tool = scene.ht_tool
        #---

        #Operations Layout
        box = layout.box()
        box.label(text = "Created by Curtis Holt")
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
    HOLTTOOLS_OT_OrganizeOutliner,
    HOLTTOOLS_OT_ConvertSuffixes,
    HOLTTOOLS_OT_DeepClean,
    HOLTTOOLS_OT_PurgeUnwantedData,
    HOLTTOOLS_OT_SetAutoSmooth,
    HOLTTOOLS_OT_RemoveUnusedSlots,
    HOLTTOOLS_OT_FixDuplicateNodeGroups,
    # Selection
    HOLTTOOLS_OT_SelectAllIncluding,
    HOLTTOOLS_OT_SelectAllType,
    HOLTTOOLS_OT_NameAddPrefix,
    HOLTTOOLS_OT_NameAddSuffix,
    HOLTTOOLS_OT_SelectByVertexCount,
    # Lighting
    HOLTTOOLS_OT_AddLightIntensityGlobal,
    HOLTTOOLS_OT_SubtractLightIntensityGlobal,
    HOLTTOOLS_OT_MultiplyLightIntensityGlobal,
    # Optimization
    HOLTTOOLS_OT_QuickDecimate,
    # Panels
    OBJECT_PT_HoltToolsCleanup,
    OBJECT_PT_HoltToolsSelection,
    OBJECT_PT_HoltToolsLighting,
    OBJECT_PT_HoltToolsOptimization,
    OBJECT_PT_HoltToolsInfo
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