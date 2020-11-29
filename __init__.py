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
    "blender" : (2, 90, 1),
    "version" : (0, 0, 1),
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
    select_string : StringProperty(
        name = "Select Similar String",
        description = "Used for finding objects that include this in their name",
        default = "Cube"
    )
    select_types : EnumProperty(
        name = "Select Types",
        description = "Different types of object to select",
        items=[
            ('MESHES',"Meshes",""),
            ('CURVES',"Curves",""),
            ('SURFACES',"Surfaces",""),
            ('METAS',"Metas",""),
            ('TEXT',"Text",""),
            ('HAIR',"Hair",""),
            ('POINT_CLOUDS',"Point Clouds",""),
            ('VOLUMES',"Volumes",""),
            ('ARMATURES',"Armatures",""),
            ('LATTICES',"Lattices",""),
            ('EMPTIES',"Empties",""),
            ('GREASE_PENCILS',"Grease Pencils",""),
            ('CAMERAS',"Cameras",""),
            ('LIGHTS',"Lights",""),
            ('LIGHT PROBES',"Light Probes","")
        ],
        default = "MESHES"
    )
    light_add_global : IntProperty(
        name = "Light Add Global",
        description = "Value to add to all lights globally",
        default = 5
    )
    decimate_rate : FloatProperty(
        name = "Decimate Rate",
        description = "The rate to quickly decimate selected object",
        default = 0.1,
        min = 0.0,
        max = 1.0
    )
#endregion
#region OPERATORS - CLEANUP
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
        select_objects_including(ht_tool.select_string)
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
        select_all_lights()
        light_power_add(ht_tool.light_add_global)
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
        select_all_lights()
        light_power_add(-ht_tool.light_add_global)
        return {'FINISHED'}
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
        obj = ao()
        mod = add_decimate()
        mod.ratio = ht_tool.decimate_rate
        apply_all_modifiers()
        return {'FINISHED'}
#endregion
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
        box = layout.box()
        box.label(text="Cleanup Operations")
        col = box.column()
        colrow = col.row(align=True)
        colrow.operator("outliner.organize_outliner")
        colrow = col.row(align=True)
        colrow.operator("object.convert_suffixes")
        colrow = col.row(align=True)
        colrow.operator("object.purge_unwanted_data")
        colrow = col.row(align=True)
        colrow.operator("outliner.deep_clean", text = "^ Deep Clean ^")
        colrow = col.row(align=True)
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
        box = layout.box()
        box.label(text="Select All Including")
        col = box.column()
        colrow = col.row(align=True)
        colrow.prop(ht_tool, "select_string", text = "")
        colrow = col.row(align=True)
        colrow.operator("object.select_all_including", text="^ Select All Including ^")
        colrow = col.row(align=True)
        colrow.separator()
        #-- New Box
        box = layout.box()
        box.label(text="Select All By Type")
        col = box.column()
        colrow = col.row(align=True)
        colrow.prop(ht_tool, "select_types", text="")
        colrow = col.row(align=True)
        colrow.operator("object.select_all_type", text="^ Select All Type ^")
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

        b = layout.box()
        b.label(text="Global Lighting")
        column = b.column()

        row = column.row()
        row.prop(ht_tool, "light_add_global", text="")
        row = column.row()
        row.operator("object.subtract_light_intensity_global", text="-")
        row.operator("object.add_light_intensity_global", text="+")
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
        bytool = scene.by_tool

        #Operations Layout
        box = layout.box()
        box.label(text = "Created by Curtis Holt")
        #---------- Box - Support
        b = box.box()
        b.label(text="Support")
        column = b.column()

        row = column.row()
        row.scale_y = 1.2
        row.operator("wm.url_open", text = "Gumroad", icon='WORLD').url = "https://gumroad.com/l/BY-GEN"
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
    # Selection
    HOLTTOOLS_OT_SelectAllIncluding,
    HOLTTOOLS_OT_SelectAllType,
    # Lighting
    HOLTTOOLS_OT_AddLightIntensityGlobal,
    HOLTTOOLS_OT_SubtractLightIntensityGlobal,
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