import bpy, os, bpy.utils.previews, bpy_extras, shutil, bmesh, re
from struct import pack, unpack
from bpy.props import (EnumProperty, CollectionProperty, IntProperty, StringProperty, BoolProperty, FloatProperty,
                       FloatVectorProperty)
from Tools import FmdlFile, Ftex, IO, PesFoxShader, PesFoxXML, Enlighten
from xml.dom import minidom
from xml.dom.minidom import parse

bl_info = {
    "name": "PES Stadium Exporter",
    "author": "the4chancup - MjTs-140914",
    "version": (0, 2, 0),
    "blender": (2, 80, 0),
    "api": 35853,
    "location": "Under Scene Tab",
    "description": "PES Stadium Exporter",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"
}

(major, minor, build) = bpy.app.version
icons_collections = {}
myver = "v0.2.0a"

AddonsPath = str()
AddonsPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
base_file_blend = '%s\\addons\\Tools\\Gzs\\base_file.blend' % AddonsPath
texconvTools = '"%s\\addons\\Tools\\Gzs\\texconv.exe"' % AddonsPath
FtexTools = '"%s\\addons\\Tools\\Gzs\\FtexTools.exe"' % AddonsPath
GZSPATH = '"%s\\addons\\Tools\\Gzs\\GzsTool.exe"' % AddonsPath
foxTools = '"%s\\addons\\Tools\\Gzs\\FoxTool\\FoxTool.exe"' % AddonsPath
icons_dir = '%s\\addons\\Tools\\Gzs\\icons' % AddonsPath
xml_dir = '%s\\addons\\Tools\\Gzs\\xml\\' % AddonsPath
uvDataFile = '%s\\addons\\Tools\\Gzs\\uvMapData.bin' % AddonsPath
lightFxPath = '%s\\addons\\Tools\\Gzs\\' % AddonsPath
baseStartupFile = '%s\\addons\\Tools\\Gzs\\startup.blend' % AddonsPath
startupFile = '%sconfig\\startup.blend' % AddonsPath[:-7]
EnlightenPath = "%s\\addons\\Tools\\Gzs\\EnlightenOutput\\" % AddonsPath

ob_id = None
group_list = ["MAIN", "TV", "AUDIAREA", "FLAGAREA", "STAFF", "SCARECROW", "PITCH2021", "CHEER1", "CHEER2", "LIGHTS",
              "AD"]

parent_main_list = ["MESH_back1", "MESH_back2", "MESH_back3",
                    "MESH_center1", "MESH_center2", "MESH_center3",
                    "MESH_front1", "MESH_front2", "MESH_front3",
                    "MESH_left1", "MESH_left2", "MESH_left3",
                    "MESH_right1", "MESH_right2", "MESH_right3",
                    "MESH_Pitch", "MESH_front1_demo", "MESH_front1_game",
                    "MESH_center1_snow", "MESH_center1_rain",
                    "MESH_ad_acl", "MESH_ad_cl", "MESH_ad_el", "MESH_ad_normal",
                    "MESH_ad_olc", "MESH_ad_sc",
                    ]

main_list = ["back1", "back2", "back3",
             "center1", "center2", "center3",
             "front1", "front2", "front3",
             "left1", "left2", "left3",
             "right1", "right2", "right3",
             "front1_demo", "front1_game", "center1_snow", "center1_rain",
             "MESH_CROWD", "MESH_FLAGAREA", "Pitch",
             "TV_Large_Left", "TV_Large_Right", "TV_Large_Front", "TV_Large_Back",
             "TV_Small_Left", "TV_Small_Right", "TV_Small_Front", "TV_Small_Back",
             "L_FRONT", "L_RIGHT", "L_LEFT", "L_BACK",
             "ad_acl", "ad_cl", "ad_el", "ad_normal",
             "ad_olc", "ad_sc",
             ]

part_export = [("MAIN", "MAIN", "MAIN"),
               ("SCARECROW", "SCARECROW", "SCARECROW"),
               ("TV", "TV", "TV"),
               ("PITCH2021", "PITCH2021", "PITCH2021"),
               ("STAFF", "STAFF", "STAFF"),
               ("CHEER1", "CHEER1", "CHEER1"),
               ("CHEER2", "CHEER2", "CHEER2"),
               ("FLAGAREA", "FLAGAREA", "FLAGAREA"),
               ("AUDIAREA", "AUDIAREA", "AUDIAREA"),
               ("LIGHTS", "LIGHTS", "LIGHTS"),
               ("AD", "AD", "AD"),
               ]

crowd_part = ['C_front1', 'C_front2', 'C_front3',
              "C_back1", "C_back2", "C_back3",
              "C_left1", "C_left2", "C_left3",
              "C_right1", "C_right2", "C_right3"
              ]

flags_part = ['F_front1', 'F_front2', 'F_front3',
              "F_back1", "F_back2", "F_back3",
              "F_left1", "F_left2", "F_left3",
              "F_right1", "F_right2", "F_right3"
              ]

crowd_part_type = [0x00010000, 0x00010100, 0x00010200,
                   0x00010001, 0x00010101, 0x00010201,
                   0x00010002, 0x00010102, 0x00010202,
                   0x00010003, 0x00010103, 0x00010203
                   ]

tvdatalist = [0x02D72E00, 0x02D730A0, 0x02D73340,
              0x02D73650, 0x02D73490, 0x02D72D20,
              0x02D72FC0, 0x02D73260, 0x02D73570,
              0x02D73810,
              ]

lfx_tex_list = [("tex_star_00.ftex", "00 - tex_star_00", "tex_star_00"),
                ("tex_star_01.ftex", "01 - tex_star_01", "tex_star_00"),
                ("tex_star_02.ftex", "02 - tex_star_02", "tex_star_00"),
                ("tex_star_03.ftex", "03 - tex_star_03", "tex_star_00"),
                ("tex_star_04.ftex", "04 - tex_star_04", "tex_star_00"),
                ("tex_star_05_alp.ftex", "05 - tex_star_05", "tex_star_00_alp"),
                ("tex_star_07_alp.ftex", "07 - tex_star_07", "tex_star_00_alp"),
                ("tex_star_08_alp.ftex", "08 - tex_star_08", "tex_star_00_alp")]

light_sidelist = [("L_FRONT", "FRONT SIDE", "FRONT SIDE"),
                  ("L_LEFT", "LEFT SIDE", "LEFT SIDE"),
                  ("L_RIGHT", "RIGHT SIDE", "RIGHT SIDE"),
                  ("L_BACK", "BACK SIDE", "BACK SIDE")
                  ]

timeMode = [("df", "DAY FINE", "DAY FINE"),
            ("dr", "DAY RAINY", "DAY RAINY"),
            ("nf", "NIGHT FINE", "NIGHT FINE"),
            ("nr", "NIGHT RAINY", "NIGHT RAINY")
            ]

parent_list = [('MESH_back1', 'MESH_back1', 'MESH_back1'),
               ('MESH_back2', 'MESH_back2', 'MESH_back2'),
               ('MESH_back3', 'MESH_back3', 'MESH_back3'),
               ('MESH_center1', 'MESH_center1', 'MESH_center1'),
               ('MESH_center2', 'MESH_center2', 'MESH_center2'),
               ('MESH_center3', 'MESH_center3', 'MESH_center3'),
               ('MESH_front1', 'MESH_front1', 'MESH_front1'),
               ('MESH_front2', 'MESH_front2', 'MESH_front2'),
               ('MESH_front3', 'MESH_front3', 'MESH_front3'),
               ('MESH_left1', 'MESH_left1', 'MESH_left1'),
               ('MESH_left2', 'MESH_left2', 'MESH_left2'),
               ('MESH_left3', 'MESH_left3', 'MESH_left3'),
               ('MESH_right1', 'MESH_right1', 'MESH_right1'),
               ('MESH_right2', 'MESH_right2', 'MESH_right2'),
               ('MESH_right3', 'MESH_right3', 'MESH_right3'),
               ('MESH_CROWD', 'MESH_CROWD', 'MESH_CROWD'),
               ('MESH_PITCH', 'MESH_PITCH', 'MESH_PITCH'),
               ('MESH_TV', 'MESH_TV', 'MESH_TV')]

datalist = ["back1", "back2", "back3",
            "center1", "center2", "center3",
            "front1", "front2", "front3",
            "left1", "left2", "left3",
            "right1", "right2", "right3",
            "center1_snow", "center1_rain",
            "front1_game", "front1_demo"
            ]

StadiumModel = ["StadiumModel_B1", "StadiumModel_B2", "StadiumModel_B3",
                "StadiumModel_C1", "StadiumModel_C2", "StadiumModel_C3",
                "StadiumModel_F1", "StadiumModel_F2", "StadiumModel_F3",
                "StadiumModel_L1", "StadiumModel_L2", "StadiumModel_L3",
                "StadiumModel_R1", "StadiumModel_R2", "StadiumModel_R3",
                "StadiumModel_C1_ForSnow", "StadiumModel_C1_rain",
                "StadiumModel_F1_game", "StadiumModel_F1_demo"
                ]

StadiumKind = [0, 1, 2,
               0, 1, 2,
               0, 1, 2,
               0, 1, 2,
               0, 1, 2,
               0, 0,
               14, 15
               ]

transformlist = [0x02D72C40, 0x02D72D20, 0x02D72E00,
                 0x02D72EE0, 0x02D72FC0, 0x02D730A0,
                 0x02D73180, 0x02D73260, 0x02D73340,
                 0x02D73420, 0x02D73570, 0x02D73650,
                 0x02D73730, 0x02D73810, 0x02D73490,
                 0xC11921D0, 0x03173880,
                 0x03173E30, 0x03173FF0,
                 ]

TransformEntity = [0x03172D20, 0x03172EE0, 0x03172EE2,
                   0x031730A0, 0x031730A2, 0x03173260,
                   0x03173420, 0x03173650, 0x03173750,
                   0x03173810, 0x03173960, 0x03173970,
                   0x03173B20, 0x03173CE0, 0x03173CE5,
                   0xC12714B0, 0xC12714B2,
                   0x03173EA0, 0x03174060,
                   ]

shearTransform = [0x03173F10, 0x03173D50, 0x03173D60,
                  0x03173B90, 0x03173B95, 0x031739D0,
                  0x031732CB, 0x031732D0, 0x031732D2,
                  0x03172D90, 0x03172F50, 0x03172F52,
                  0x03174140, 0x03173180, 0x03173182,
                  0x00000000, 0xB13C0250,
                  0x03173490, 0x031736C0,
                  ]

pivotTransform = [0x03173F80, 0x03173DC0, 0x03173DC2,
                  0x03173C00, 0x03173C01, 0x03173A40,
                  0x031738F0, 0x03173340, 0x03173342,
                  0x03172E00, 0x03172FC0, 0x03172FC2,
                  0x03173110, 0x03174290, 0x03174292,
                  0x00000000, 0x00000000,
                  0x03173570, 0x03173730,
                  ]

crowd_type = {'UltraHome': 0.9,
              'HardcoreHome': 0.8999,
              'HeavyHome': 0.7999,
              'PopHome': 0.6999,
              'FolkHome': 0.5999,
              'JumpHome': 5,
              'Neutral': 0.5,
              'JumpAway': 4,
              'FolkAway': 0.4999,
              'PopAway': 0.3999,
              'HeavyAway': 0.2999,
              'HardcoreAway': 0.1999,
              'UltraAway': 0.0999
              }

behavior = [('UltraHome', 'UltraHome', 'UltraHome'),
            ('HardcoreHome', 'HardcoreHome', 'HardcoreHome'),
            ('HeavyHome', 'HeavyHome', 'HeavyHome'),
            ('PopHome', 'PopHome', 'PopHome'),
            ('FolkHome', 'FolkHome', 'FolkHome'),
            ('JumpHome', 'JumpHome', 'JumpHome'),
            ('Neutral', 'Neutral', 'Neutral'),
            ('JumpAway', 'JumpAway', 'JumpAway'),
            ('FolkAway', 'FolkAway', 'FolkAway'),
            ('PopAway', 'PopAway', 'PopAway'),
            ('HeavyAway', 'HeavyAway', 'HeavyAway'),
            ('HardcoreAway', 'HardcoreAway', 'HardcoreAway'),
            ('UltraAway', 'UltraAway', 'UltraAway')]

parentlist = []
shaders = []


def makedir(DirName, isStadium):
    listDir = []
    splitDir = str(DirName).split('\\')
    for idx in enumerate(splitDir):
        listDir.append(splitDir[idx[0]])
        liststr = listDir
        liststr = str(liststr).replace(",", " ")
        liststr = str(liststr).replace("'", "")
        liststr = str(liststr).replace("[", "")
        liststr = str(liststr).replace("]", "")
        liststr = str(liststr).replace(" ", "\\")
        if isStadium:
            dirNew = os.path.join(bpy.context.scene.export_path, liststr)
        else:
            dirNew = os.path.join(bpy.context.scene.export_path[:-6], liststr)
        if not os.path.exists(dirNew):
            os.mkdir(dirNew)
    return 1


def remove_dir(dirPath):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)
    return 1


def remove_file(filePath):
    if os.path.isfile(filePath):
        os.remove(filePath)
    return 1


def compileXML(filePath):
    inp_xml = ' "' + filePath + '"'
    os.system('"' + foxTools + inp_xml + '"')
    return 1


def pack_unpack_Fpk(filePath):
    inp_xml = ' "' + filePath + '"'
    os.system('"' + GZSPATH + inp_xml + '"')
    return 1


def texconv(inPath, outPath, arguments, cm):
    File = open(inPath, 'r', encoding="cp437")
    File.seek(0x54)
    TxFormat = File.read(4)
    File.close()
    if cm:
        if TxFormat == "DX10":
            args = arguments + ' "' + inPath + '"' + ' -o "' + outPath + ''
            os.system('"' + texconvTools + args + '"')
    else:
        args = arguments + ' "' + outPath + '" "' + inPath + '"'
        os.system('"' + texconvTools + args + '"')
    return 1


def convert_ftex(ftexfilepath):
    ftexname = ' "' + ftexfilepath + '"'
    os.system('"' + FtexTools + ftexname + '"')
    return 1


def convert_dds(inPath, outPath):
    ftexname = ' -f 0 -i "{0}" -o "{1}"'.format(inPath, outPath)
    os.system('"' + FtexTools + ftexname + '"')

    return 1


def fox2xml(sourcePath, filePath):
    scn = bpy.context.scene
    fox2Read = open(xml_dir + sourcePath, 'rt').read()
    fox2Read = fox2Read.replace('stid', scn.STID)
    fox2Write = open(scn.export_path + filePath, 'wt')
    fox2Write.write(fox2Read)
    fox2Write.flush(), fox2Write.close()

    return 1


def texture_load(dirPath):
    for root, directories, filenames in os.walk(dirPath):
        for fileName in filenames:
            filename, extension = os.path.splitext(fileName)
            if extension.lower() == '.ftex':

                ddsPath = os.path.join(root, filename + '.dds')
                ftexPath = os.path.join(root, filename + extension)
                if not os.path.isfile(ddsPath) and not "lut" in ddsPath and not "LUT" in ddsPath:
                    try:
                        Ftex.ftexToDds(ftexPath, ddsPath)
                    except:
                        convert_ftex(ftexPath)
                    texconv(ddsPath, dirPath, " -y -l -f DXT5 -ft dds -srgb", True)
                    print('Converting {0} ==> {1}'.format(filename + '.ftex', filename + '.dds'))

    return root, directories, filenames


def remove_dds(dirPath):
    for root, directories, filenames in os.walk(dirPath):
        for fileName in filenames:
            filename, extension = os.path.splitext(fileName)
            if extension.lower() == '.dds' or extension.lower() == '.png' or extension.lower() == '.tga':
                ddsPath = os.path.join(root, filename + extension)
                os.remove(ddsPath)
                print('Removing texture [>{0}{1}<] succesfully'.format(filename, extension))
    return root, directories, filenames


def node_group():
    inner_path = 'NodeTree'
    for NodeTree in ('NRM Converter', 'SRM Seperator', 'TRM Subsurface'):
        if not NodeTree in bpy.data.node_groups:
            bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, NodeTree),
                              directory=os.path.join(base_file_blend, inner_path), filename=NodeTree)
    return 1


def Create_Parent_Part(self, context):
    inc_list = []
    for i in context.scene.objects:
        if i.type == "EMPTY":
            if i.name in main_list:
                inc_list.append(i.name)
            if i.name in group_list:
                inc_list.append(i.name)
            if i.name in parent_main_list:
                inc_list.append(i.name)
    for o in group_list:
        if o not in inc_list:
            bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
            ob = context.active_object
            for i in range(3):
                ob.lock_location[i] = 1
                ob.lock_rotation[i] = 1
                ob.lock_scale[i] = 1
            ob.name = o
    for o in (main_list):
        if o not in inc_list:
            bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
            ob = context.active_object
            for i in range(3):
                ob.lock_location[i] = 1
                ob.lock_rotation[i] = 1
                ob.lock_scale[i] = 1
            ob.name = o
    for o in parent_main_list:
        if o not in inc_list:
            bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
            ob = context.active_object
            for i in range(3):
                ob.lock_location[i] = 1
                ob.lock_rotation[i] = 1
                ob.lock_scale[i] = 1
            ob.name = o
    for ob in bpy.data.objects:
        if ob.type == "EMPTY":
            if ob.name in ["L_FRONT", "L_RIGHT", "L_LEFT", "L_BACK"]:
                ob.parent = bpy.data.objects['LIGHTS']
            elif ob.name == "MESH_FLAGAREA":
                ob.parent = bpy.data.objects["FLAGAREA"]
            elif ob.name == "MESH_CROWD":
                ob.parent = bpy.data.objects["AUDIAREA"]
            elif ob.name == "Pitch":
                ob.parent = bpy.data.objects["PITCH2021"]
            elif ob.name in ["TV_Large_Left", "TV_Large_Right", "TV_Large_Front", "TV_Large_Back",
                             "TV_Small_Left", "TV_Small_Right", "TV_Small_Front", "TV_Small_Back"]:
                ob.parent = bpy.data.objects["TV"]
            elif ob.name in ["ad_acl", "ad_cl", "ad_el", "ad_normal", "ad_olc", "ad_sc"]:
                ob.parent = bpy.data.objects["AD"]
            elif ob.name in datalist:
                ob.parent = bpy.data.objects["MAIN"]
            if ob.name in parent_main_list:
                for op in main_list:
                    if op in ob.name and True:
                        ob.parent = bpy.data.objects[op]
    return 1


def checkStadiumID(context, isParent):
    if isParent:
        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                for ob in bpy.data.objects[child.name].children:
                    if ob is not None:
                        for ob2 in bpy.data.objects[ob.name].children:
                            if ob2 is not None and ob2.type == "MESH":
                                blenderMaterial = bpy.data.objects[ob2.name].active_material
                                for nodes in blenderMaterial.node_tree.nodes:
                                    if nodes.type == "TEX_IMAGE":
                                        blenderTexture = blenderMaterial.node_tree.nodes[
                                            nodes.name].fmdl_texture_directory
                                        if "st" in blenderTexture:
                                            if not context.scene.STID in blenderTexture:
                                                print("\nStadium ID isn't match!!")
                                                print(
                                                    "\nSome stadium IDs do not match in the node, please check first or you can swap all stadium IDs")
                                                print(
                                                    "\nCheck out Object in Parent({0} --> {1} --> {2}) in Mesh object({3}) in node({4})"
                                                        .format(context.scene.part_info, ob.parent.name,
                                                                ob2.parent.name,
                                                                ob2.name, nodes.name))
                                                return True
                                            else:
                                                return False

    else:
        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                for ob2 in bpy.data.objects[child.name].children:
                    if ob2 is not None and ob2.type == "MESH":
                        blenderMaterial = bpy.data.objects[ob2.name].active_material
                        for nodes in blenderMaterial.node_tree.nodes:
                            if nodes.type == "TEX_IMAGE":
                                blenderTexture = blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory
                                print(blenderTexture)
                                if "st" in blenderTexture:
                                    if not context.scene.STID in blenderTexture:
                                        print("\nStadium ID isn't match!!")
                                        print(
                                            "\nSome stadium IDs do not match in the node, please check first or you can swap all stadium IDs")
                                        print(
                                            "\nCheck out Object in Parent({0} --> {1}) in Mesh object({2}) in node({3})"
                                                .format(context.scene.part_info, ob2.parent.name, ob2.name, nodes.name))
                                        return True
                                    else:
                                        return False
    pass


class FMDL_MaterialParameter(bpy.types.PropertyGroup):
    name: StringProperty(name="Parameter Name")
    parameters: FloatVectorProperty(name="Parameter Values", size=4, default=[0.0, 0.0, 0.0, 0.0])


class FMDL_UL_material_parameter_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(item, 'name', text="", emboss=False)


class FMDL_Material_Parameter_List_Add(bpy.types.Operator):
    """Add New Parameter"""
    bl_idname = "fmdl.material_parameter_add"
    bl_label = "Add Parameter"

    @classmethod
    def poll(cls, context):
        return context.material != None

    def execute(self, context):
        material = context.material
        parameter = material.fmdl_material_parameters.add()
        parameter.name = "new_parameter"
        parameter.parameters = [0.0, 0.0, 0.0, 0.0]
        material.fmdl_material_parameter_active = len(material.fmdl_material_parameters) - 1
        return {'FINISHED'}


class FMDL_Material_Parameter_List_Remove(bpy.types.Operator):
    """Remove Selected Parameter"""
    bl_idname = "fmdl.material_parameter_remove"
    bl_label = "Remove Parameter"

    @classmethod
    def poll(cls, context):
        return (context.material != None and
                0 <= context.material.fmdl_material_parameter_active < len(context.material.fmdl_material_parameters)
                )

    def execute(self, context):
        material = context.material
        material.fmdl_material_parameters.remove(material.fmdl_material_parameter_active)
        if material.fmdl_material_parameter_active >= len(material.fmdl_material_parameters):
            material.fmdl_material_parameter_active = len(material.fmdl_material_parameters) - 1
        return {'FINISHED'}


class FMDL_Material_Parameter_List_MoveUp(bpy.types.Operator):
    """Move Selected Parameter Up"""
    bl_idname = "fmdl.material_parameter_moveup"
    bl_label = "Move Parameter Up"

    @classmethod
    def poll(cls, context):
        return (context.material != None and
                1 <= context.material.fmdl_material_parameter_active
                < len(context.material.fmdl_material_parameters)
                )

    def execute(self, context):
        material = context.material
        material.fmdl_material_parameters.move(
            material.fmdl_material_parameter_active,
            material.fmdl_material_parameter_active - 1
        )
        material.fmdl_material_parameter_active -= 1
        return {'FINISHED'}


class FMDL_Material_Parameter_List_MoveDown(bpy.types.Operator):
    """Move Selected Parameter Down"""
    bl_idname = "fmdl.material_parameter_movedown"
    bl_label = "Move Parameter Down"

    @classmethod
    def poll(cls, context):
        return (context.material != None and
                0 <= context.material.fmdl_material_parameter_active < len(
                    context.material.fmdl_material_parameters) - 1
                )

    def execute(self, context):
        material = context.material
        material.fmdl_material_parameters.move(
            material.fmdl_material_parameter_active,
            material.fmdl_material_parameter_active + 1
        )
        material.fmdl_material_parameter_active += 1
        return {'FINISHED'}


class FMDL_21_PT_Material_Panel(bpy.types.Panel):
    bl_label = "FMDL Material Settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        if not (context.object.name.split(sep='_')[0] != 'C'
                and context.object.name.split(sep='_')[0] != 'F'
                and context.material != None):
            return False
        return True

    def draw(self, context):
        material = context.material
        layout = self.layout
        mainColumn = layout.column(align=True)
        box = layout.box()
        mainColumn = box.row(align=0)
        mainColumn.prop(material, "fox_shader", text="PES Fox Shader")
        mainColumn.operator("shader.operator", text="", icon="SEQ_SEQUENCER")
        mainColumn = box.row(align=0)
        mainColumn.prop(material, "fmdl_material_shader")
        mainColumn = box.row(align=0)
        mainColumn.prop(material, "fmdl_material_technique")
        mainColumn = box.row(align=0)
        mainColumn.separator()
        mainColumn.label(text="Material Parameters")
        mainColumn = box.row(align=0)
        parameterListRow = mainColumn.row()
        parameterListRow.template_list(
            FMDL_UL_material_parameter_list.__name__,
            "FMDL_Material_Parameter_Names",
            material,
            "fmdl_material_parameters",
            material,
            "fmdl_material_parameter_active"
        )

        listButtonColumn = parameterListRow.column(align=True)
        listButtonColumn.operator("fmdl.material_parameter_add", icon='ADD', text="")
        listButtonColumn.operator("fmdl.material_parameter_remove", icon='REMOVE', text="")
        listButtonColumn.separator()
        listButtonColumn.operator("fmdl.material_parameter_moveup", icon='TRIA_UP', text="")
        listButtonColumn.operator("fmdl.material_parameter_movedown", icon='TRIA_DOWN', text="")
        mainColumn = box.row(align=0)
        if 0 <= material.fmdl_material_parameter_active < len(material.fmdl_material_parameters):
            valuesColumn = mainColumn.column()
            parameter = material.fmdl_material_parameter_active
            valuesColumn.prop(
                material.fmdl_material_parameters[parameter],
                "parameters"
            )

    pass


def importFmdlfile(fileName, sklname, meshID, objName):
    context = bpy.context

    extensions_enabled = context.scene.fmdl_import_extensions_enabled

    loop_preservation = context.scene.fmdl_import_loop_preservation
    mesh_splitting = context.scene.fmdl_import_mesh_splitting
    load_textures = context.scene.fmdl_import_load_textures
    import_all_bounding_boxes = context.scene.fmdl_import_all_bounding_boxes
    fixmeshesmooth = context.scene.fixmeshesmooth

    importSettings = IO.ImportSettings()
    importSettings.enableExtensions = extensions_enabled
    importSettings.enableVertexLoopPreservation = loop_preservation
    importSettings.enableMeshSplitting = mesh_splitting
    importSettings.enableLoadTextures = load_textures
    importSettings.enableImportAllBoundingBoxes = import_all_bounding_boxes
    importSettings.fixMeshsmooth = fixmeshesmooth
    importSettings.armatureName = sklname
    importSettings.meshIdName = meshID

    fmdlFile = FmdlFile.FmdlFile()
    fmdlFile.readFile(fileName)

    rootObject = IO.importFmdl(context, fmdlFile, objName, importSettings)
    rootObject.fmdl_export_extensions_enabled = importSettings.enableExtensions
    rootObject.fmdl_export_loop_preservation = importSettings.enableVertexLoopPreservation
    rootObject.fmdl_export_mesh_splitting = importSettings.enableMeshSplitting

    return 1


class FMDL_Object_BoundingBox_Create(bpy.types.Operator):
    """Create custom bounding box"""
    bl_idname = "fmdl.boundingbox_create"
    bl_label = "Create custom bounding box"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not (
                context.mode == 'OBJECT'
                and context.object is not None
                and context.object.type == 'MESH'
        ):
            return False
        for child in context.object.children:
            if child.type == 'LATTICE':
                return False
        return True

    def execute(self, context):
        IO.createFittingBoundingBox(context, context.object)
        return {'FINISHED'}


class FMDL_Object_BoundingBox_Remove(bpy.types.Operator):
    """Remove custom bounding box"""
    bl_idname = "fmdl.boundingbox_remove"
    bl_label = "Remove custom bounding box"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not (
                context.mode == 'OBJECT'
                and context.object is not None
                and context.object.type == 'MESH'
        ):
            return False
        for child in context.object.children:
            if child.type == 'LATTICE':
                return True
        return False

    def execute(self, context):
        removeList = []
        for child in context.object.children:
            if child.type == 'LATTICE':
                removeList.append(child.name)
        for objectID in removeList:
            latticeID = bpy.data.objects[objectID].data.name
            while len(bpy.data.objects[objectID].users_scene) > 0:
                bpy.context.collection.objects.unlink(bpy.data.objects[objectID])
            if bpy.data.objects[objectID].users == 0:
                bpy.data.objects.remove(bpy.data.objects[objectID])
            if bpy.data.lattices[latticeID].users == 0:
                bpy.data.lattices.remove(bpy.data.lattices[latticeID])
        return {'FINISHED'}


class FMDL_21_PT_Object_BoundingBox_Panel(bpy.types.Panel):
    bl_label = "FMDL Bounding Box"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return (
                context.object is not None
                and context.object.type == 'MESH'
        )

    def draw(self, context):
        self.layout.operator(FMDL_Object_BoundingBox_Create.bl_idname)
        self.layout.operator(FMDL_Object_BoundingBox_Remove.bl_idname)


def light_fx(outxml):
    scn = bpy.context.scene
    hdr_file = open(lightFxPath + "extras21.dll", "rb")
    hdr_file.seek(942, 0)
    dat13 = hdr_file.read(236)
    dat14 = hdr_file.read(28)
    dat15 = hdr_file.read(68)
    hdr_file.flush(), hdr_file.close()

    cfg = lightFxPath + 'xml\\effect_config_%s.xml' % scn.time_mode

    dat16 = open(cfg, 'rt').read()
    LT = scn.l_fx_tex
    if LT in ['00', '01', '04']:
        LR = '30'
    else:
        LR = '45'
    dat16 = dat16.replace('%LT', LT)
    dat16 = dat16.replace('%LR', LR)
    dat16 = dat16.replace('stid', scn.STID)
    light_cfg = open(outxml, 'wt')
    light_cfg.write(dat16)
    light_cfg.flush(), light_cfg.close()
    dirname = "effect\\#Win\\effect_" + scn.STID + "_" + scn.time_mode + "_fpk"
    lamp_list = ["L_FRONT", "front3", "L_LEFT", "left3", "L_RIGHT", "right3", "L_BACK", "back3"]

    def lamp_side(p_name, l_count):

        i = lamp_list.index(p_name)
        if scn.time_mode == 'df':
            outpath_lightfx = '{0}{1}\\Assets\\pes16\\model\\bg\\{2}\\effect\\locator\\locstar_{3}_df.model'.format(
                scn.export_path, dirname, scn.STID, lamp_list[i + 1])
        elif scn.time_mode == 'dr':
            outpath_lightfx = '{0}{1}\\Assets\\pes16\\model\\bg\\{2}\\effect\\locator\\locstar_{3}_dr.model'.format(
                scn.export_path, dirname, scn.STID, lamp_list[i + 1])
        elif scn.time_mode == 'nf':
            outpath_lightfx = '{0}{1}\\Assets\\pes16\\model\\bg\\{2}\\effect\\locator\\locstar_{3}_nf_nr.model'.format(
                scn.export_path, dirname, scn.STID, lamp_list[i + 1])
        else:
            outpath_lightfx = '{0}{1}\\Assets\\pes16\\model\\bg\\{2}\\effect\\locator\\locstar_{3}_nf_nr.model'.format(
                scn.export_path, dirname, scn.STID, lamp_list[i + 1])

        lfx = open(outpath_lightfx, "wb")
        lfx.write(dat13)
        lfx.write(pack("4I", (48 * l_count + 40), l_count, 0x72617473, 0))
        return lfx

    for p_lamp in bpy.data.objects['LIGHTS'].children:
        if len(p_lamp.children) > 0:
            l_count = len(p_lamp.children)
            lfx = lamp_side(p_lamp.name, l_count)

            for lamp in p_lamp.children:
                l_energy = lamp.l_Energy
                lfx.write(pack("12f", l_energy, 0, 0, lamp.location.x, 0, 1, 0, lamp.location.z, 0, 1, 0,
                               (lamp.location.y * -1)))

            for i in range(l_count):
                if i == 0:
                    x = 4 * l_count
                else:
                    x += 28
                lfx.write(pack("I", x))

            for p in range(l_count):
                lfx.write(dat14)

            sz1 = lfx.tell()
            lfx.write(dat15)
            lfx.seek(64, 0)
            lfx.write(pack("I", sz1 - 24))
            lfx.close()
    return 1


class FMDL_21_PT_UIPanel(bpy.types.Panel):
    bl_label = "eFootball PES2021 Stadium Exporter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        ob = context.active_object
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.alignment = 'CENTER'
        row = box.row(align=0)
        this_icon = icons_collections["custom_icons"]["icon_1"].icon_id
        row.label(text="eFootball PES2021 Stadium Exporter", icon_value=this_icon)
        row = box.row()
        this_icon = icons_collections["custom_icons"]["icon_0"].icon_id
        row.label(text="Made by: MjTs-140914 / the4chancup", icon_value=this_icon)
        row = box.row()
        box.label(text="Blender version {0}.{1}.{2} ({3})".format(major, minor, build, myver), icon="BLENDER")
        row = box.row()
        row.operator("main_parts.operator", text="Create Main Parts", icon="EMPTY_DATA")
        row.operator("scene.operator", text="", icon="PRESET_NEW")
        if ob:
            row = layout.row()
            box = layout.box()
            row = box.row()
            row.label(text="Stadium Import Menu", icon="INFO")
            row = box.row()
            row.prop(scn, "fpk_path", text="Fpk Path")
            row = box.row()
            row.prop(scn, "texture_path")
            row = box.row()
            row.operator("import.operator", text="IMPORT", icon="IMPORT")
            row.operator("clear_temp.operator", text="", icon="TRASH").opname = "cleartemp"
            if ob and ob.type == 'MESH' and ob is not None:
                mat = bpy.data.objects[ob.name].material_slots
                box = layout.box()
                row = box.row()
                row.label(text="Parent Assigment", icon="INFO")
                row = box.row()
                row.label(text="Vertex Count : " + str(len(ob.data.vertices)), icon="VERTEXSEL")
                row.label(text="Face Count : " + str(len(ob.data.polygons)), icon="FACESEL")
                row = box.row()
                row.alignment = 'EXPAND'
                split = row.split(factor=1)
                split = split.split(factor=0.6)
                row = split.row()
                row.prop(ob, "droplist", text="Parent")
                split = split.split(factor=1)
                row = split.row()
                row.operator("refresh.operator", text="", icon="FILE_REFRESH")
                row.operator("set_parent.operator", text="SET")
                row.operator("clr.operator", text="CLR")
                row = box.row()
                split = row.split(factor=1)
                split = split.split(factor=0.57)
                row = box.row()
                if ob.parent and ob.type != 'LIGHT':
                    row.label(text="Parent : " + ob.parent.name, icon="EMPTY_DATA")
                    row.label(text="Object : " + ob.name, icon="OBJECT_DATA")
                    row = box.row()
                else:
                    box.label(text="No parent for active object, assign a parent...", icon="ERROR")
                if len(mat) == 0 and not ob.name in crowd_part and not ob.name in flags_part:
                    row.label(text="Mesh [%s] not have Materials!" % ob.name, icon="ERROR")
                elif len(mat) == 1:
                    blenderMaterial = bpy.context.active_object.active_material
                    if blenderMaterial.fmdl_material_technique == str() and not ob.name in crowd_part and not ob.name in flags_part:
                        row.label(text="Mesh [%s] not have Shader!" % ob.name, icon="ERROR")
                elif len(mat) >= 2 and not ob.name in crowd_part and not ob.name in flags_part:
                    row.label(text="Mesh [%s] too much Material Slots" % ob.name, icon="ERROR")
            box = layout.box()
            row = box.row()
            row.label(text="Stadium Export Part List", icon="INFO")
            row = box.row()
            row.prop(scn, "part_info")
            row = box.row()
            row.prop(scn, "STID")
            row.operator("newid.operator", text="", icon="CENTER_ONLY")
            row = box.row()
            row.prop(scn, "export_path")
            if scn.part_info == "MAIN":
                box = layout.box()
                row = box.row()
                row.label(text="Stadium Export", icon="INFO")
                row = box.row()
                row.operator("convert.operator", text="Export Texture", icon="NODE_TEXTURE")
                if scn.useFastConvertTexture:
                    txt = "Skip Non-Modified textures"
                else:
                    txt = "Convert All textures"
                row.prop(scn, "useFastConvertTexture", text=txt)
                # row.operator("clear_temp.operator", text="", icon="MOD_EXPLODE").opname = "cleartempdata"
                row.operator("clear_temp.operator", text="", icon="TRASH").opname = "cleartempdata"
                row = box.row()
                row.operator("export_stadium.operator", text="EXPORT STADIUM", icon="EXPORT")
            elif scn.part_info == "AUDIAREA":
                if ob is not None:
                    box = layout.box()
                    row = box.row()
                    if ob.name not in crowd_part and ob.parent and ob.parent.name == "MESH_CROWD":
                        box.label(text="Crowd Part Name is Wrong, Fix it before Export... ", icon="ERROR")
                    else:
                        row.label(text="Crowd Export", icon="INFO")
                        row = box.row()
                        row.prop(scn, "crowd_row_space", text="Row Space")
                        row = box.row()
                        row.operator("crowd.operator", text="EXPORT CROWD", icon="EXPORT")
                        row = box.row()
            elif scn.part_info == "FLAGAREA":
                if ob is not None:
                    box = layout.box()
                    row = box.row()
                    if ob.name not in flags_part and ob.parent and ob.parent.name == "MESH_FLAGAREA":
                        box.label(text="Flagarea Part Name is Wrong, Fix it before Export... ", icon="ERROR")
                    else:
                        row.label(text="Flagarea Export", icon="INFO")
                        row = box.row()
                        row.operator("flags.operator", text="EXPORT FLAG AREA", icon="EXPORT")
                        row = box.row()
            elif scn.part_info == "LIGHTS" and ob is not None:
                box = layout.box()
                row = box.row()
                row.label(text="Light FX Exporter", icon="LIGHT_SPOT")
                row = box.row()
                if ob.type == 'LIGHT':
                    if ob.parent:
                        lp = ob.parent.name
                    else:
                        lp = "Not Assigned"
                    row.label(text="Parent: " + lp)
                    row.label(text="Name: " + ob.name)
                    row.label(text="Energy: " + str(round(ob.l_Energy, 2))[:4])
                    row = box.row()

                    row.prop(scn, "l_lit_side", text="")
                    row.prop(ob, "l_Energy")
                    row.operator("lightfx.operator", text="Set Light FX", icon="FILE_TICK").opname = 'set_lfx_side'
                    row = box.row()
                else:
                    row.prop(scn, "time_mode", text="Mode")
                    row = box.row()
                    row.prop(scn, "l_fx_tex", text="")
                    row.operator("lightfx.operator", text="Export Light FX ", icon="LIGHT_DATA").opname = 'export_lfx'
                    row = box.row()
            elif scn.part_info == "TV" and ob is not None:
                box = layout.box()
                row = box.row()
                row.label(text="TV Exporter", icon="INFO")
                row = box.row()
                row.prop(scn, "tvobject", text="Type")
                row.operator("tv_object.operator", text="Add %s" % context.scene.tvobject)
                row = box.row()
                row.operator("export_tv.operator", text="EXPORT TV", icon="EXPORT")
                row = box.row()
            elif scn.part_info == "PITCH2021" and ob is not None:
                box = layout.box()
                row = box.row()
                row.label(text="Pitch Exporter", icon="INFO")
                row = box.row()
                row.operator("export_pitch.operator", text="EXPORT Pitch", icon="EXPORT")
                row = box.row()
            elif scn.part_info == "STAFF" and ob is not None:
                box = layout.box()
                row = box.row()
                row.label(text="Staff Coach Position", icon="INFO")
                row = box.row()
                row.operator("staff_pos.operator", text="Load Coach", icon="IMPORT").opname = "loadcoach"
                row.operator("staff_pos.operator", text="Assign Coach", icon="EXPORT").opname = "assigncoach"
                row = box.row()
            elif scn.part_info == "AD" and ob is not None:
                box = layout.box()
                row = box.row()
                row.label(text="Stadium AD Export", icon="INFO")
                row = box.row()
                row.operator("export_ad.operator", text="EXPORT AD STADIUM", icon="EXPORT")


class Staff_Coach_Pos(bpy.types.Operator):
    """Import / Export Staff Coach Position"""
    bl_idname = "staff_pos.operator"
    bl_label = str()
    opname: StringProperty()

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def execute(self, context):
        scn = context.scene
        stid = scn.STID
        if "STAFF" not in bpy.data.objects:
            Create_Parent_Part(self, context)
        if len(stid) == 5:
            if context.scene.export_path == str():
                self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

            if not stid in context.scene.export_path:
                self.report({"WARNING"}, "Stadium ID doesn't match!!")
                print("Stadium ID doesn't match!!")
                return {'CANCELLED'}

            if not context.scene.export_path.endswith(stid + "\\"):
                self.report({"WARNING"},
                            "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

        if self.opname == "loadcoach":
            inner_path = 'Object'
            for coach in ('coach_home', 'coach_away'):
                if not coach in bpy.data.objects:
                    bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, coach),
                                      directory=os.path.join(base_file_blend, inner_path), filename=coach)
            for ob in bpy.data.objects:
                if ob.type == "MESH":
                    if ob.name == "coach_home":
                        bpy.data.objects[ob.name].rotation_mode = "QUATERNION"
                        bpy.data.objects[ob.name].rotation_quaternion[0] = -0.007337
                        bpy.data.objects[ob.name].rotation_quaternion[3] = -0.999973
                        bpy.data.objects[ob.name].location[0] = -4.893455
                        bpy.data.objects[ob.name].location[1] = 37.3332 * -1
                    if ob.name == "coach_away":
                        bpy.data.objects[ob.name].rotation_mode = "QUATERNION"
                        bpy.data.objects[ob.name].rotation_quaternion[0] = -0.007337
                        bpy.data.objects[ob.name].rotation_quaternion[3] = -0.999973
                        bpy.data.objects[ob.name].location[0] = 5.69787
                        bpy.data.objects[ob.name].location[1] = 37.2800179 * -1
                    if ob.name in ['coach_home', 'coach_away']:
                        ob.parent = bpy.data.objects['STAFF']
            self.report({"INFO"}, "Coach loaded succesfully...")

        if self.opname == "assigncoach":

            for coach in ('coach_home', 'coach_away'):
                if not coach in bpy.data.objects:
                    self.report({"WARNING"}, "Load Coach first..")
                    return {'CANCELLED'}

            pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd".format(scn.export_path, stid))
            xmlPath = "{0}staff\\#Win\\staff_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\staff\\{3}_st2018_coach.fox2.xml".format(
                scn.export_path, stid, stid, stid)
            coachXml = open(xml_dir + "StaffCoach.xml", "rt").read()

            for ob in bpy.data.objects['STAFF'].children:
                if ob.type == "MESH":
                    if ob.name == "coach_home":
                        bpy.data.objects[ob.name].rotation_mode = "QUATERNION"
                        coachXml = coachXml.replace("q_w_home", str(bpy.data.objects[ob.name].rotation_quaternion[0]))
                        coachXml = coachXml.replace("q_y_home", str(bpy.data.objects[ob.name].rotation_quaternion[3]))
                        coachXml = coachXml.replace("r_x_home", str(bpy.data.objects[ob.name].location[0]))
                        coachXml = coachXml.replace("r_z_home", str(bpy.data.objects[ob.name].location[1] * -1))
                    if ob.name == "coach_away":
                        bpy.data.objects[ob.name].rotation_mode = "QUATERNION"
                        coachXml = coachXml.replace("q_w_away", str(bpy.data.objects[ob.name].rotation_quaternion[0]))
                        coachXml = coachXml.replace("q_y_away", str(bpy.data.objects[ob.name].rotation_quaternion[3]))
                        coachXml = coachXml.replace("r_x_away", str(bpy.data.objects[ob.name].location[0]))
                        coachXml = coachXml.replace("r_z_away", str(bpy.data.objects[ob.name].location[1] * -1))
            writecoachxml = open(xmlPath, "wt")
            writecoachxml.write(coachXml)
            writecoachxml.flush(), writecoachxml.close()
            compileXML(xmlPath)
            pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path, stid))
            remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path, stid))
            remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path, stid))
            self.report({"INFO"}, "Coach assign succesfully...")
        return {'FINISHED'}

    pass


class New_STID(bpy.types.Operator):
    """Swap old ID to new ID"""
    bl_idname = "newid.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def execute(self, context):
        Rslt = str()
        stid = context.scene.STID
        if len(stid) == 5:
            if context.scene.export_path == str():
                self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

            if not stid in context.scene.export_path:
                self.report({"WARNING"}, "Stadium ID doesn't match!!")
                print("Stadium ID doesn't match!!")
                return {'CANCELLED'}

            if not context.scene.export_path.endswith(stid + "\\"):
                self.report({"WARNING"},
                            "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}
            self.report({"INFO"}, " Light FX Exported has been Successfully... ")
        else:
            self.report({"WARNING"}, "Stadium ID isn't correct!!")
        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                for ob in bpy.data.objects[child.name].children:
                    if ob is not None:
                        for ob2 in bpy.data.objects[ob.name].children:
                            if ob2 is not None and ob2.type == "MESH":
                                blenderMaterial = bpy.data.objects[ob2.name].active_material
                                for nodes in blenderMaterial.node_tree.nodes:
                                    if nodes.type == "TEX_IMAGE":
                                        blenderTexture = blenderMaterial.node_tree.nodes[
                                            nodes.name].fmdl_texture_directory
                                        if "st" in blenderTexture:
                                            oldID = re.findall(r'\d+', blenderTexture)
                                            try:
                                                for i in range(100):
                                                    Rslt = "st" + oldID[i]
                                            except:
                                                pass
                                            print(
                                                "Swap id from ({0}) to ({1}) in object ({2}) in node ({3}) succesfully...".format(
                                                    Rslt, stid, ob2.name, nodes.name))
                                            assetDirname = blenderTexture
                                            newid = str(assetDirname).replace(assetDirname,
                                                                              "/Assets/pes16/model/bg/%s/sourceimages/tga/" % stid)
                                            blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory = newid
        self.report({"INFO"}, "Swap stadium id succesfully!")
        return {'FINISHED'}

    pass


class TV_Objects(bpy.types.Operator):
    """Add TV Objects"""
    bl_idname = "tv_object.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def execute(self, context):
        inner_path = 'Object'
        if context.scene.tvobject == "tv_large_c":
            tvObject = "TV object large"
        else:
            tvObject = "TV object small"
        bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, tvObject),
                          directory=os.path.join(base_file_blend, inner_path), filename=tvObject)
        return {'FINISHED'}

    pass


class Light_FX(bpy.types.Operator):
    """Light FX Exporter"""
    bl_idname = "lightfx.operator"
    bl_label = str()
    opname: StringProperty()

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT") and (context.active_object and context.active_object)

    def execute(self, context):
        stid = context.scene.STID
        if self.opname == "set_lfx_side":
            for l_ob in bpy.context.selected_objects:
                if l_ob.type == 'LIGHT':
                    l_ob.parent = bpy.data.objects[bpy.context.scene.l_lit_side]

            return {'FINISHED'}
        if self.opname == "export_lfx":
            if len(stid) == 5:
                if context.scene.export_path == str():
                    self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    return {'CANCELLED'}

                if not stid in context.scene.export_path:
                    self.report({"WARNING"}, "Stadium ID doesn't match!!")
                    print("Stadium ID doesn't match!!")
                    return {'CANCELLED'}

                if not context.scene.export_path.endswith(stid + "\\"):
                    self.report({"WARNING"},
                                "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    return {'CANCELLED'}
                scn = bpy.context.scene
                fpkPath = "{0}effect\\#Win\\effect_{1}_{2}.fpk".format(scn.export_path, scn.STID, scn.time_mode)
                xmlPath = "{0}effect\\#Win\\effect_{1}_{2}.fpk.xml".format(scn.export_path, scn.STID, scn.time_mode)
                xmlConfigPath = "{0}effect\\#Win\\effect_{1}_{2}_fpk\\effect_config.xml".format(scn.export_path,
                                                                                                scn.STID, scn.time_mode)
                if os.path.isfile(fpkPath):
                    print("\nStarting Light FX Export !!\n")
                    pack_unpack_Fpk(fpkPath)
                else:
                    self.report({"WARNING"}, "%s file not found!" % fpkPath)
                    print("%s file not found!" % fpkPath)
                    return {'CANCELLED'}
                try:
                    light_fx(xmlConfigPath)
                    self.report({"INFO"}, " Light FX Exported has been Successfully... ")
                except Exception as msg:
                    self.report({"WARNING"}, format(msg))
                    return {'CANCELLED'}
                pack_unpack_Fpk(xmlPath)
                remove_file(xmlPath)
                remove_dir("{0}effect\\#Win\\effect_{1}_{2}_fpk".format(scn.export_path, scn.STID, scn.time_mode))
            else:
                self.report({"WARNING"}, "Stadium ID isn't correct!!")
            return {'FINISHED'}


class Refresh_OT(bpy.types.Operator):
    """Refresh Parent List"""
    bl_idname = "refresh.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        scn = context.scene
        if scn.part_info == "AUDIAREA" or scn.part_info == "FLAGAREA" or scn.part_info == "LIGHTS" or scn.part_info == "TV":
            parentlist = [(ob.name, ob.name, ob.name) for ob in
                          (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if
                          ob.name in main_list if ob.name not in ['LIGHTS', 'L_FRONT', 'L_BACK', 'L_RIGHT', 'L_LEFT']]
            parentlist.sort(reverse=0)
        else:
            parentlist = [("MESH_" + ob.name, "MESH_" + ob.name, "MESH_" + ob.name) for ob in
                          (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if
                          ob.name in main_list if
                          ob.name not in ['LIGHTS', 'L_FRONT', 'L_BACK', 'L_RIGHT', 'L_LEFT', 'MESH_CROWD',
                                          'MESH_FLAGAREA']]
            parentlist.sort(reverse=1)
        if scn.part_info == "AD":
            parentlist.sort(reverse=0)
        bpy.types.Object.droplist = EnumProperty(name="Parent List", items=parentlist)
        for p_ob in bpy.data.objects:
            if p_ob.type == 'EMPTY' and p_ob.parent and p_ob.name in parent_main_list:
                try:
                    if scn.part_info == "AUDIAREA" or scn.part_info == "FLAGAREA" or scn.part_info == "LIGHTS" or scn.part_info == "TV":
                        self.droplist = p_ob.parent.name
                    else:
                        self.droplist = "MESH_" + p_ob.parent.name
                except:
                    pass
        self.report({"INFO"}, "Refresh parent succesfully!")
        return {'FINISHED'}

    pass


class FMDL_21_PT_Mesh_Panel(bpy.types.Panel):
    bl_label = "FMDL Mesh Settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        if not (context.object.name.split(sep='_')[0] != 'C'
                and context.object.name.split(sep='_')[0] != 'F'
                and context.mesh != None):
            return False
        return True

    def draw(self, context):
        mesh = context.mesh
        mainColumn = self.layout.column()
        mainColumn.prop(mesh, "fmdl_alpha_enum_select", text='Alpha')
        mainColumn.prop(mesh, "fmdl_shadow_enum_select", text='Shadow')
        mainColumn.prop(mesh, "fmdl_alpha_enum")
        mainColumn.prop(mesh, "fmdl_shadow_enum")


class Import_OT(bpy.types.Operator):
    """Import Stadium"""
    bl_idname = "import.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        node_group()
        filename = context.scene.fpk_path
        dirpath = context.scene.texture_path
        if not os.path.isfile(filename):
            self.report({"WARNING"}, "Fpk file doesn't select!!")
            return {'CANCELLED'}
        if not filename.endswith(".fpk"):
            self.report({"WARNING"}, "File not fpk format!!")
            return {'CANCELLED'}
        if filename == str():
            self.report({"WARNING"}, "Fpk path can't be empty!!")
            return {'CANCELLED'}
        if context.scene.fmdl_import_load_textures:
            if dirpath == str():
                self.report({"WARNING"}, "Texture path can't be empty!!")
                return {'CANCELLED'}
            texture_load(dirpath)
        fpk = ' "' + filename + '"'
        os.system('"' + GZSPATH + fpk + '"')
        dir = os.path.dirname(filename)
        for root, directories, filenames in os.walk(dir):
            for fileName in filenames:
                filename, extension = os.path.splitext(fileName)
                if extension.lower() == '.fmdl':
                    fmdlPath = os.path.join(root, fileName)
                    importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename)
                    print('Importing ==> %s' % fileName)
        print('Importing stadium succesfully...!')
        self.report({"INFO"}, "Importing stadium succesfully...!")
        return {'FINISHED'}

    pass


def makeXML(filename, files, Name, FpkType, xsitype, uselist):
    root = minidom.Document()
    archiveFile = root.createElement('ArchiveFile')
    archiveFile.setAttributeNS('xmlns', 'xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    archiveFile.setAttributeNS('xmlns', 'xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    archiveFile.setAttributeNS('xsi', 'xsi:type', xsitype)
    archiveFile.setAttribute('Name', Name)
    archiveFile.setAttribute('FpkType', FpkType)

    root.appendChild(archiveFile)
    entries = root.createElement('Entries')
    archiveFile.appendChild(entries)
    if uselist:
        for file in files:
            element = root.createElement('Entry')
            element.setAttribute('FilePath', file)
            entries.appendChild(element)
    else:
        element = root.createElement('Entry')
        element.setAttribute('FilePath', files)
        entries.appendChild(element)
    archiveFile.appendChild(root.createElement('References'))
    xml_str = root.toprettyxml(indent="\t")
    with open(filename, "w") as f:
        f.write(xml_str)
    return 1


def export_fmdl(self, context, fileName, meshID, objName):
    if context.view_layer.objects.active == None:
        obj = context.window.scene.objects[0]
        context.view_layer.objects.active = obj

    extensions_enabled = context.active_object.fmdl_export_extensions_enabled
    loop_preservation = context.active_object.fmdl_export_loop_preservation
    mesh_splitting = context.active_object.fmdl_export_mesh_splitting

    exportSettings = IO.ExportSettings()
    exportSettings.enableExtensions = extensions_enabled
    exportSettings.enableVertexLoopPreservation = loop_preservation
    exportSettings.enableMeshSplitting = mesh_splitting
    exportSettings.meshIdName = meshID
    try:
        fmdlFile = IO.exportFmdl(context, objName, exportSettings)
    except IO.FmdlExportError as error:
        print("Error exporting Fmdl:\n" + "\n".join(error.errors))
        return {'CANCELLED'}
    fmdlFile.writeFile(fileName)
    return 1


def reports(self, context):
    for child in bpy.data.objects[context.scene.part_info].children:
        for ob in bpy.data.objects[child.name].children:
            if ob.type == 'MESH' and ob.data is not None:
                uv = bpy.data.meshes[ob.data.name].uv_layers
                mat = bpy.data.objects[ob.name].material_slots
                if len(uv) == 0:
                    context.scene.isActive = True
                    context.scene.report_msg = "Mesh [%s] does not have a primary UV map set!" % ob.name
                    print("Mesh [%s] does not have a primary UV map set!" % ob.name)
                elif len(uv) >= 3:
                    context.scene.isActive = True
                    context.scene.report_msg = "Mesh [%s] too much UVMap slots, need to remove!" % ob.name
                    print("Mesh [%s] too much UVMap slots, need to remove!" % ob.name)
                elif len(uv) == 1:
                    if uv[0].name != 'UVMap':
                        context.scene.isActive = True
                        context.scene.report_msg = "Mesh [%s] UVMap name isn't correct!" % ob.name
                        print("Mesh [%s] UVMap name isn't correct!" % ob.name)
                elif len(uv) == 2:
                    if uv[1].name != 'normal_map':
                        context.scene.isActive = True
                        context.scene.report_msg = "Mesh [%s] normal_map name isn't correct!" % ob.name
                        print("Mesh [%s] normal_map name isn't correct!" % ob.name)
                if len(mat) == 0:
                    context.scene.isActive = True
                    context.scene.report_msg = "Mesh [%s] does not have an associated material!" % ob.name
                    print("Mesh [%s] does not have an associated material!" % ob.name)
                if len(mat) >= 2:
                    context.scene.isActive = True
                    context.scene.report_msg = "Mesh [%s] too much material slots need to remove!" % ob.name
                    print("Mesh [%s] too much material slots need to remove!" % ob.name)
    return 1


def uv_Data(partList, obj_part):
    if bpy.ops.object.mode_set():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.data.objects:
        if ob.parent and ob.parent.name == partList:
            ob.select_set(True)

    bpy.ops.object.transform_apply(location=1, rotation=1, scale=1)
    bpy.ops.object.select_all(action='DESELECT')

    def uv_data(obj):

        mesh = obj.data
        mesh.update(calc_edges=1, calc_edges_loose=1)
        for loop in mesh.loops:
            uv_coords = mesh.uv_layers.active.data[loop.index].uv
            uvfileWrite.write(pack("2f", float(uv_coords[0]), float(uv_coords[1])))

    uvfileWrite = open(uvDataFile, "wb")
    off_list, cr_list_temp = [], []

    for cr in bpy.data.objects[partList].children:
        cr_list_temp.append(cr.name)
    for ob in obj_part:
        if ob in cr_list_temp:
            uv_data(bpy.data.objects[ob])
        else:
            off_list.append(0)
    if bpy.ops.object.mode_set():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    uvfileWrite.flush(), uvfileWrite.close()


def crowd_exp(outpath, partList, obj_part):
    scn = bpy.context.scene

    def crowd(obj):
        print("*" * 20)
        print(obj.name)
        off1 = cr_file.tell()
        off_list.append(off1)
        cr_file.write(pack("I", crowd_part_type[obj_part.index(obj.name)]))
        cr_file.write(pack("I", off1 + 8))
        bsize = obj.bound_box[3][:], obj.bound_box[5][:]
        mesh = obj.data
        mesh.update(calc_edges=1, calc_edges_loose=1)
        ud = 0

        cr_file.write(
            pack("6f", bsize[0][0], bsize[0][2], bsize[0][1] * -1, bsize[1][0], bsize[1][2], bsize[1][1] * -1))
        cr_file.write(pack("I", len(mesh.polygons)))

        for f, face in enumerate(mesh.polygons):
            vec1, vec2, idx1, idx2, vlist = [], [], [], [], []
            v1, v2, row, g = 0, 0, float(), 0x0
            for v in enumerate(face.vertices):
                uvface = mesh.uv_layers[0].data[face.index]
                fuv = uvface.uv
                if scn.part_info == "AUDIAREA":
                    g = mesh.vertices[v[1]].groups[0]
                if mesh.vertices[v[1]].co.z > face.center.z:
                    u, w = fuv[0], fuv[1]
                    idx1.append((v[1], u, w))
                else:
                    u, w = fuv[0], fuv[1]
                    idx2.append((v[1], u, w))

                v1 = mesh.vertices[v[1]].co, fuv[0], fuv[1]
                vlist.append(v1)
            if len(idx1) == len(idx2):
                for t in range(0, len(idx1), 2):
                    vec1.append((mesh.vertices[idx1[t][0]].co + mesh.vertices[idx1[t + 1][0]].co) / 2)
                    vec2.append((mesh.vertices[idx2[t][0]].co + mesh.vertices[idx2[t + 1][0]].co) / 2)
                for x in range(0, len(idx1), 2):
                    if (mesh.vertices[idx1[x + 0][0]].co[ud]) < (vec1[x][ud]):
                        v1 = mesh.vertices[idx1[x + 0][0]].co, idx1[x + 0][1], idx1[x + 0][2]
                    else:
                        v1 = mesh.vertices[idx1[x + 1][0]].co, idx1[x + 1][1], idx1[x + 1][2]
                    if (mesh.vertices[idx2[x + 0][0]].co[ud]) < (vec2[x][ud]):
                        v2 = mesh.vertices[idx2[x + 0][0]].co, idx2[x + 0][1], idx2[x + 0][2]
                    else:
                        v2 = mesh.vertices[idx2[x + 1][0]].co, idx2[x + 1][1], idx2[x + 1][2]
                    row = round((v1[0] - v2[0]).length, 1)
            else:
                print("Bad Mesh Faces for %s Crowd Part, Fix it before export !!" % obj.name)
            if scn.part_info == "AUDIAREA":
                stancename = obj.vertex_groups[g.group].name
                ha = crowd_type[stancename]
            else:
                ha = 1
            row2 = round((row / (5.0 + scn.crowd_row_space)), 1)
            cr_file.write(pack("I", f))
            cr_file.write(pack("3f", row2, ha, ha))
            for w in vlist:
                cr_file.write(pack("3f", w[0][0], w[0][2], w[0][1] * -1))
            for w in vlist:
                uvm = unpack("2f", uvfile.read(8))
                cr_file.write(pack("2f", uvm[0], uvm[1]))

    outpath_crowd_data = outpath
    uvfile = open(uvDataFile, "rb")
    cr_file = open(outpath_crowd_data, "wb")
    cr_file.write(pack("2I48s", 1, 1, "".encode()))
    off_list, cr_list_temp = [], []

    for cr in bpy.data.objects[partList].children:
        cr_list_temp.append(cr.name)

    for ob in obj_part:
        if ob in cr_list_temp:
            crowd(bpy.data.objects[ob])
        else:
            off_list.append(0)

    cr_file.seek(8, 0)
    for o in enumerate(off_list):
        cr_file.write(pack("I", o[1]))
    cr_file.flush(), cr_file.close()
    uvfile.flush(), uvfile.close()

    if bpy.ops.object.mode_set():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    remove_file(uvDataFile)


class Crowd_OT(bpy.types.Operator):
    """Export Crowd"""
    bl_idname = "crowd.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        stid = context.scene.STID
        if len(bpy.data.objects['MESH_CROWD'].children) > 0:
            for ob in bpy.data.objects['MESH_CROWD'].children:
                if ob.name not in crowd_part:
                    self.report({"WARNING"}, "%s Crowd Part Name is Wrong, Fix it before Export... " % ob.name)
                    return {'CANCELLED'}
                if "C_" not in ob.name:
                    self.report({"WARNING"}, "Mesh [%s] name isn't correct!!" % ob.name)
                    return {'CANCELLED'}
            if len(stid) == 5:
                if context.scene.export_path == str():
                    self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    return {'CANCELLED'}

                if not stid in context.scene.export_path:
                    self.report({"WARNING"}, "Stadium ID doesn't match!!")
                    print("Stadium ID doesn't match!!")
                    return {'CANCELLED'}

                if not context.scene.export_path.endswith(stid + "\\"):
                    self.report({"WARNING"},
                                "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    return {'CANCELLED'}
            else:
                self.report({"WARNING"}, "Stadium ID isn't correct!!")
                return {'CANCELLED'}
            try:
                print("\nStarting Crowd Parts Exporting...")
                # Write uv data for audiarea
                uv_Data('MESH_CROWD', crowd_part)
                # Create fpk for audiarea
                assetDirname = "/Assets/pes16/model/bg/%s/audi/" % stid
                makeXML(context.scene.export_path + "audi\\#Win\\audiarea_%s" % stid + ".fpk.xml",
                        assetDirname + "audiarea.bin", "audiarea_%s.fpk" % stid, "Fpk", "FpkFile", False)
                assetDir = os.path.join(context.scene.export_path, "audi", "#Win", "audiarea_%s_fpk" % stid, "Assets",
                                        "pes16", "model", "bg", stid, "audi\\audiarea.bin")
                dir_to_remove = os.path.join(context.scene.export_path, "audi", "#Win", "audiarea_%s_fpk" % stid)
                makedir("audi\\#Win\\audiarea_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\audi".format(stid, stid), True)
                crowd_exp(assetDir, 'MESH_CROWD', crowd_part)
                pack_unpack_Fpk(dir_to_remove[:-4] + ".fpk.xml")
                remove_dir(dir_to_remove)
                remove_file(dir_to_remove[:-4] + ".fpk.xml")
                # Create fpkd for audiarea
                makedir("audi\\#Win\\audiarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\audi".format(stid, stid), True)
                fox2xml("Crowd.xml",
                        "audi\\#Win\\audiarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\audi\\audiarea_{2}.fox2.xml".format(
                            stid, stid, stid))
                makeXML(context.scene.export_path + "audi\\#Win\\audiarea_%s" % stid + ".fpkd.xml",
                        assetDirname + "audiarea_%s.fox2" % stid, "audiarea_%s.fpkd" % stid, "Fpk", "FpkFile", False)
                compileXML(
                    "{0}audi\\#Win\\audiarea_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\audi\\audiarea_{3}.fox2.xml".format(
                        context.scene.export_path, stid, stid, stid))
                pack_unpack_Fpk(dir_to_remove[:-4] + ".fpkd.xml")
                remove_dir(dir_to_remove + "d")
                remove_file(dir_to_remove[:-4] + ".fpkd.xml")
                self.report({"INFO"}, "Exporting Crowd succesfully...!")
                print("\nExporting Crowd succesfully...!")
            except Exception as exception:
                self.report({"WARNING"}, format(exception) + " see more info => Windows -> Toggle System Console")
                print(format(type(exception).__name__), format(exception))
                if "index 0 out of range" in format(exception):
                    print(
                        "\nInfo: Check out mesh have associate Behavior Crowd?, make sure vertex weight is fine, to check weight Go To Weight Paint mode")
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "No Crowd Objects under MESH_CROWD parent !")
            print("No Crowd Objects under MESH_CROWD parent!")
        return {'FINISHED'}

    pass


class Flags_Area_OT(bpy.types.Operator):
    """Export Flag Area"""
    bl_idname = "flags.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        stid = context.scene.STID
        if len(bpy.data.objects['MESH_FLAGAREA'].children) > 0:
            for ob in bpy.data.objects['MESH_FLAGAREA'].children:
                if ob.name not in flags_part:
                    self.report({"WARNING"}, "%s Flagarea Part Name is Wrong, Fix it before Export... " % ob.name)
                    return {'CANCELLED'}
                if "F_" not in ob.name:
                    self.report({"WARNING"}, "Mesh [%s] flag area name isn't correct!!" % ob.name)
                    return {'CANCELLED'}
            if len(stid) == 5:
                if context.scene.export_path == str():
                    self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    return {'CANCELLED'}

                if not stid in context.scene.export_path:
                    self.report({"WARNING"}, "Stadium ID doesn't match!!")
                    print("Stadium ID doesn't match!!")
                    return {'CANCELLED'}

                if not context.scene.export_path.endswith(stid + "\\"):
                    self.report({"WARNING"},
                                "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                    return {'CANCELLED'}
            else:
                self.report({"WARNING"}, "Stadium ID isn't correct!!")
                return {'CANCELLED'}
            try:
                print("\nStarting Flagarea Exporting...")
                # Write uv data for Flagarea
                uv_Data('MESH_FLAGAREA', flags_part)
                # Create fpk for Flagarea
                assetDirname = "/Assets/pes16/model/bg/%s/standsFlag/" % stid
                makeXML(context.scene.export_path + "standsFlag\\#Win\\flagarea_%s" % stid + ".fpk.xml",
                        assetDirname + "flagarea.bin", "flagarea_%s.fpk" % stid, "Fpk", "FpkFile", False)
                assetDir = os.path.join(context.scene.export_path, "standsFlag", "#Win", "flagarea_%s_fpk" % stid,
                                        "Assets", "pes16", "model", "bg", stid, "standsFlag\\flagarea.bin")
                dir_to_remove = os.path.join(context.scene.export_path, "standsFlag", "#Win", "flagarea_%s_fpk" % stid)
                makedir(
                    "standsFlag\\#Win\\flagarea_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\standsFlag".format(stid, stid),
                    True)
                crowd_exp(assetDir, 'MESH_FLAGAREA', flags_part)
                pack_unpack_Fpk(dir_to_remove[:-4] + ".fpk.xml")
                remove_dir(dir_to_remove)
                remove_file(dir_to_remove[:-4] + ".fpk.xml")
                # Create fpkd for Flagarea
                makedir(
                    "standsFlag\\#Win\\flagarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\standsFlag".format(stid, stid),
                    True)
                fox2xml("Flagarea.xml",
                        "standsFlag\\#Win\\flagarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\standsFlag\\flagarea_{2}.fox2.xml".format(
                            stid, stid, stid))
                makeXML(context.scene.export_path + "standsFlag\\#Win\\flagarea_%s" % stid + ".fpkd.xml",
                        assetDirname + "flagarea_%s.fox2" % stid, "flagarea_%s.fpkd" % stid, "Fpk", "FpkFile", False)
                compileXML(
                    "{0}standsFlag\\#Win\\flagarea_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\standsFlag\\flagarea_{3}.fox2.xml".format(
                        context.scene.export_path, stid, stid, stid))
                pack_unpack_Fpk(dir_to_remove[:-4] + ".fpkd.xml")
                remove_dir(dir_to_remove + "d")
                remove_file(dir_to_remove[:-4] + ".fpkd.xml")
                self.report({"INFO"}, "Exporting Flagarea succesfully...!")
                print("\nExporting Flagarea succesfully...!")
            except Exception as exception:
                self.report({"WARNING"}, format(exception) + " see more info => Windows -> Toggle System Console")
                print(format(type(exception).__name__), format(exception))
                if "index 0 out of range" in format(exception):
                    print(
                        "\nInfo: Check out mesh have associate Behavior Crowd?, make sure vertex weight is fine, to check weight Go To Weight Paint mode")
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "No Flagarea Objects under MESH_FLAGAREA parent !")
            print("No Flagarea Objects under MESH_FLAGAREA parent!")
        return {'FINISHED'}

    pass


class PES_21_PT_CrowdSection(bpy.types.Panel):
    bl_label = "Crowd behavior Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        if context.object.name.split(sep='_')[0] != 'C':
            return False
        return True

    def draw(self, context):
        scn = context.scene
        mainColumn = self.layout.column()
        mainColumn.label(text='Crowd Assignment', icon='GROUP_VERTEX')
        mainColumn = mainColumn.row()
        mainColumn.prop(scn, 'crowd_type_enum')
        mainColumn.operator("assign.operator", icon='PLUS')

    pass


class PES_21_OT_assign_crowd_type(bpy.types.Operator):
    """Click to assign selected vertices to the selected crowd type"""
    bl_idname = "assign.operator"
    bl_label = str()

    def execute(self, context):
        try:
            crowd_groups(context.scene.crowd_type_enum)
        except ValueError as msg:
            self.report({"WARNING"}, format(msg))
        return {'FINISHED'}

    pass


def crowd_groups(Name):
    ob = bpy.context.object
    bm = bmesh.from_edit_mesh(ob.data)
    vxlist = []
    for v in bm.verts:
        if v.select == True:
            vxlist.append(v.index)
    bm.free()
    bpy.ops.object.editmode_toggle()

    if Name not in ob.vertex_groups:
        ob.vertex_groups.new(name=Name)

    for g in ob.vertex_groups:
        if g.name == Name:
            ob.vertex_groups[Name].add(vxlist, 1, 'ADD')
        else:
            ob.vertex_groups[g.name].add(vxlist, 1, 'SUBTRACT')
    bpy.ops.object.editmode_toggle()
    return 1


class Export_OT(bpy.types.Operator):
    """Export Stadium"""
    bl_idname = "export_stadium.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):

        stid = context.scene.STID
        exportPath = context.scene.export_path

        reports(self, context)
        if context.scene.isActive:
            self.report({"WARNING"}, context.scene.report_msg)
            context.scene.report_msg = str()
            context.scene.isActive = False
            return {'CANCELLED'}

        if len(stid) == 5:
            if context.scene.export_path == str():
                self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

            if not stid in context.scene.export_path:
                self.report({"WARNING"}, "Stadium ID doesn't match!!")
                print("Stadium ID doesn't match!!")
                return {'CANCELLED'}

            if not context.scene.export_path.endswith(stid + "\\"):
                self.report({"WARNING"},
                            "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "Stadium ID isn't correct!!")
            return {'CANCELLED'}
        checks = checkStadiumID(context, True)
        if checks:
            self.report({"WARNING"}, "Stadium ID doesn't match, see more info => Windows -> Toggle System Console")
            return {'CANCELLED'}
        files, files2 = [], []
        for en in Enlighten.EnlightenAsset:
            en = en.replace("stid", stid)
            files2.append(en)
        shearTransformlist, pivotTransformlist, dataList = [], [], []
        Stadium_Model, TransformEntityList, Stadium_Kinds = [], [], []
        arraySize = 0
        print('\nStarting export object as .FMDL')
        assetDirname = "/Assets/pes16/model/bg/%s/scenes/" % stid
        assetDir = "{0}#Win\\{1}_fpk\\Assets\\pes16\\model\\bg\\{2}\\scenes\\".format(exportPath, stid, stid)
        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                for ob in bpy.data.objects[child.name].children[:1]:
                    if ob is not None:
                        for ob2 in bpy.data.objects[ob.name].children[:1]:
                            if ob2 is not None:
                                print('\n********************************')
                                arraySize += 1
                                makedir("#Win\\{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes".format(stid, stid), True)
                                makedir("#Win\\{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}".format(stid, stid), True)
                                objName = child.name
                                fmdlName = child.name
                                try:
                                    addr = str.upper(hex(transformlist[datalist.index(fmdlName)]))
                                    if len(addr) == 9:
                                        addr = addr.replace("0X", "0x0")
                                    elif len(addr) == 6:
                                        addr = addr.replace("0X", "0x0000")
                                    else:
                                        addr = addr.replace("0X", "0x")
                                    shearTransformaddr = str.upper(hex(shearTransform[datalist.index(fmdlName)]))
                                    if len(shearTransformaddr) == 9:
                                        shearTransformaddr = shearTransformaddr.replace("0X", "0x0")
                                    elif len(shearTransformaddr) == 6:
                                        shearTransformaddr = shearTransformaddr.replace("0X", "0x0000")
                                    elif len(shearTransformaddr) == 3:
                                        shearTransformaddr = shearTransformaddr.replace("0X", "0x0000000")
                                    else:
                                        shearTransformaddr = shearTransformaddr.replace("0X", "0x")
                                    pivotTransformaddr = str.upper(hex(pivotTransform[datalist.index(fmdlName)]))
                                    if len(pivotTransformaddr) == 9:
                                        pivotTransformaddr = pivotTransformaddr.replace("0X", "0x0")
                                    elif len(pivotTransformaddr) == 6:
                                        pivotTransformaddr = pivotTransformaddr.replace("0X", "0x0000")
                                    elif len(pivotTransformaddr) == 3:
                                        pivotTransformaddr = pivotTransformaddr.replace("0X", "0x0000000")
                                    else:
                                        pivotTransformaddr = pivotTransformaddr.replace("0X", "0x")
                                    Transformaddr = str.upper(hex(TransformEntity[datalist.index(fmdlName)]))
                                    if len(Transformaddr) == 9:
                                        Transformaddr = Transformaddr.replace("0X", "0x0")
                                    elif len(Transformaddr) == 6:
                                        Transformaddr = Transformaddr.replace("0X", "0x0000")
                                    elif len(Transformaddr) == 3:
                                        Transformaddr = Transformaddr.replace("0X", "0x0000000")
                                    else:
                                        Transformaddr = Transformaddr.replace("0X", "0x")
                                    Stadium_Model.append(StadiumModel[datalist.index(fmdlName)])
                                    Stadium_Kinds.append(StadiumKind[datalist.index(fmdlName)])
                                except Exception as msg:
                                    self.report({"WARNING"},
                                                format(msg) + " see more info => Windows -> Toggle System Console")
                                    print("\n\nInfo: Need to delete " + format(msg))
                                    print(
                                        "\n\nInfo: Make sure mesh object in correct parent set your mesh object to parent list: %s" % datalist)
                                    return {'CANCELLED'}
                                fileName = assetDir + fmdlName + ".fmdl"
                                meshID = str(fileName).split('..')[0].split('\\')[-1:][0]
                                print('Exporting ==> %s' % meshID)
                                print('********************************')
                                files.append(assetDirname + fmdlName + ".fmdl")
                                files2.append(assetDirname + fmdlName + ".fmdl")
                                dataList.append(addr)
                                shearTransformlist.append(shearTransformaddr)
                                pivotTransformlist.append(pivotTransformaddr)
                                TransformEntityList.append(Transformaddr)
                                export_fmdl(self, context, fileName, meshID, objName)
        makeXML(exportPath + "#Win\\" + stid + ".fpk.xml", files2, "%s.fpk" % stid, "Fpk", "FpkFile", True)
        makeXML(exportPath + "#Win\\" + stid + ".fpkd.xml",
                "/Assets/pes16/model/bg/{0}/{1}_modelset.fox2".format(stid, stid), "%s.fpkd" % stid, "Fpkd", "FpkFile",
                False)
        fox2XmlPath = "{0}#Win\\{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\{3}_modelset.fox2.xml".format(exportPath, stid,
                                                                                                       stid, stid)
        try:
            PesFoxXML.makeXMLForStadium(fox2XmlPath, dataList, arraySize, files, shearTransformlist, pivotTransformlist,
                                        Stadium_Model, TransformEntityList, Stadium_Kinds)
            compileXML(fox2XmlPath)
        except Exception as msg:
            self.report({"INFO"}, format(msg))
            return {'CANCELLED'}
        # Create Enlighten System
        EnlightenPathOut = "#Win\\{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\EnlightenOutput".format(stid, stid)
        makedir(EnlightenPathOut, True)
        for filenames in os.walk(EnlightenPath):
            for fname in filenames[2]:
                oldName = str(fname)
                newName = oldName.replace("stid", stid)
                shutil.copyfile(EnlightenPath + oldName, exportPath + EnlightenPathOut + "\\" + newName)
        pack_unpack_Fpk("{0}#Win\\{1}.fpk.xml".format(exportPath, stid))
        remove_dir("{0}#Win\\{1}_fpk".format(exportPath, stid))
        remove_file("{0}#Win\\{1}.fpk.xml".format(exportPath, stid))
        pack_unpack_Fpk("{0}#Win\\{1}.fpkd.xml".format(exportPath, stid))
        remove_dir("{0}#Win\\{1}_fpkd".format(exportPath, stid))
        remove_file("{0}#Win\\{1}.fpkd.xml".format(exportPath, stid))
        self.report({"INFO"}, "Exporting stadium succesfully...!")
        return {'FINISHED'}

    pass


class Pitch_Objects(bpy.types.Operator):
    """Export Pitch Objects"""
    bl_idname = "export_pitch.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def execute(self, context):
        stid = context.scene.STID
        exportPath = context.scene.export_path
        reports(self, context)
        if context.scene.isActive:
            self.report({"WARNING"}, context.scene.report_msg)
            context.scene.report_msg = str()
            context.scene.isActive = False
            return {'CANCELLED'}

        if len(stid) == 5:
            if context.scene.export_path == str():
                self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

            if not stid in context.scene.export_path:
                self.report({"WARNING"}, "Stadium ID doesn't match!!")
                print("Stadium ID doesn't match!!")
                return {'CANCELLED'}

            if not context.scene.export_path.endswith(stid + "\\"):
                self.report({"WARNING"},
                            "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "Stadium ID isn't correct!!")
            return {'CANCELLED'}
        checks = checkStadiumID(context, True)
        if checks:
            self.report({"WARNING"}, "Stadium ID doesn't match, see more info => Window -> Toggle System Console")
            return {'CANCELLED'}
        assetDirname = "/Assets/pes16/model/bg/{0}/scenes/pitch_{1}.fmdl".format(stid, stid)
        assetDir = "{0}pitch\\#Win\\pitch_{1}_fpk\\Assets\\pes16\\model\\bg\\{2}\\scenes\\".format(exportPath, stid,
                                                                                                   stid)
        fpkdPath = "pitch\\#Win\\pitch_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\pitch".format(stid, stid)
        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                for ob in bpy.data.objects[child.name].children[:1]:
                    if ob is not None:
                        for ob2 in bpy.data.objects[ob.name].children[:1]:
                            if ob2 is not None:
                                print('\n********************************')
                                makedir("pitch\\#Win\\pitch_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes".format(stid,
                                                                                                                   stid),
                                        True)
                                makedir(fpkdPath, True)
                                objName = child.name
                                fileName = "{0}pitch_{1}.fmdl".format(assetDir, stid)
                                meshID = str(fileName).split('..')[0].split('\\')[-1:][0]
                                print("Exporting ==> pitch_%s.fmdl" % stid)
                                print('********************************\n')
                                export_fmdl(self, context, fileName, meshID, objName)

        makeXML("{0}pitch\\#Win\\pitch_{1}.fpk.xml".format(exportPath, stid), assetDirname, "pitch_%s.fpk" % stid,
                "Fpk", "FpkFile", False)
        makeXML("{0}pitch\\#Win\\pitch_{1}.fpkd.xml".format(exportPath, stid),
                "/Assets/pes16/model/bg/{0}/pitch/pitch_{1}.fox2".format(stid, stid), "pitch_%s.fpkd" % stid, "Fpk",
                "FpkFile", False)
        pitchXML = open(xml_dir + 'Pitch.xml', 'rt').read()
        pitchXML = pitchXML.replace("stid", stid)
        writepitchXML = open("{0}{1}\\pitch_{2}.fox2.xml".format(exportPath, fpkdPath, stid), "wt")
        writepitchXML.write(pitchXML)
        writepitchXML.flush(), writepitchXML.close()

        compileXML("{0}{1}\\pitch_{2}.fox2.xml".format(exportPath, fpkdPath, stid))
        pack_unpack_Fpk("{0}pitch\\#Win\\pitch_{1}.fpk.xml".format(exportPath, stid))
        remove_dir("{0}pitch\\#Win\\pitch_{1}_fpk".format(exportPath, stid))
        remove_file("{0}pitch\\#Win\\pitch_{1}.fpk.xml".format(exportPath, stid))
        pack_unpack_Fpk("{0}pitch\\#Win\\pitch_{1}.fpkd.xml".format(exportPath, stid))
        remove_dir("{0}pitch\\#Win\\pitch_{1}_fpkd".format(exportPath, stid))
        remove_file("{0}pitch\\#Win\\pitch_{1}.fpkd.xml".format(exportPath, stid))
        self.report({"INFO"}, "Exporting Pitch succesfully...!")
        return {'FINISHED'}

    pass


class ExportStadium_AD(bpy.types.Operator):
    """Export Adboard of STadium"""
    bl_idname = "export_ad.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def execute(self, context):
        stid = context.scene.STID
        exportPath = context.scene.export_path
        reports(self, context)
        if context.scene.isActive:
            self.report({"WARNING"}, context.scene.report_msg)
            context.scene.report_msg = str()
            context.scene.isActive = False
            return {'CANCELLED'}

        if len(stid) == 5:
            if context.scene.export_path == str():
                self.report({"WARNING"}, "Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Choose path to export stadium e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

            if not stid in context.scene.export_path:
                self.report({"WARNING"}, "Stadium ID doesn't match!!")
                print("Stadium ID doesn't match!!")
                return {'CANCELLED'}

            if not context.scene.export_path.endswith(stid + "\\"):
                self.report({"WARNING"},
                            "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "Stadium ID isn't correct!!")
            return {'CANCELLED'}
        checks = checkStadiumID(context, True)
        if checks:
            self.report({"WARNING"}, "Stadium ID doesn't match, see more info => Window -> Toggle System Console")
            return {'CANCELLED'}

        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                for ob in bpy.data.objects[child.name].children[:1]:
                    if ob is not None:
                        for ob2 in bpy.data.objects[ob.name].children[:1]:
                            if ob2 is not None:
                                objName = child.name
                                adName, adType = str(objName).split('_')[0], str(objName).split('_')[1]
                                fmdlName = "{0}_{1}_{2}.fmdl".format(adName, stid, adType)
                                assetDirname = "/Assets/pes16/model/bg/common/ad/scenes/%s" % fmdlName
                                assetDirnameFox2 = "/Assets/pes16/model/bg/common/ad/ad_{0}_{1}.fox2".format(stid,
                                                                                                             adType)
                                assetDir = "{0}common\\ad\\#Win\\ad_{1}_{2}_fpk\\Assets\\pes16\\model\\bg\\common\\ad\\scenes\\".format(
                                    exportPath[:-6], stid, adType)
                                fpkPath = "common\\ad\\#Win\\ad_{0}_{1}_fpk\\Assets\\pes16\\model\\bg\\common\\ad\\scenes".format(
                                    stid, adType)
                                fpkdPath = "common\\ad\\#Win\\ad_{0}_{1}_fpkd\\Assets\\pes16\\model\\bg\\common\\ad".format(
                                    stid, adType)
                                makeXML("{0}common\\ad\\#Win\\ad_{1}_{2}.fpk.xml".format(exportPath[:-6], stid, adType),
                                        assetDirname, "ad_{0}_{1}.fpk".format(stid, adType), "Fpk", "FpkFile", False)
                                makeXML(
                                    "{0}common\\ad\\#Win\\ad_{1}_{2}.fpkd.xml".format(exportPath[:-6], stid, adType),
                                    assetDirnameFox2, "ad_{0}_{1}.fpkd".format(stid, adType), "Fpk", "FpkFile", False)
                                print('\n********************************')
                                makedir(fpkPath, False)
                                makedir(fpkdPath, False)
                                fileName = assetDir + fmdlName
                                meshID = fmdlName
                                print("Exporting ==> %s" % fmdlName)
                                print('********************************\n')
                                export_fmdl(self, context, fileName, meshID, objName)
                                pack_unpack_Fpk(
                                    "{0}common\\ad\\#Win\\ad_{1}_{2}.fpk.xml".format(exportPath[:-6], stid, adType))
                                remove_dir("{0}common\\ad\\#Win\\ad_{1}_{2}_fpk".format(exportPath[:-6], stid, adType))
                                remove_file(
                                    "{0}common\\ad\\#Win\\ad_{1}_{2}.fpk.xml".format(exportPath[:-6], stid, adType))
                                adfpkd = open(xml_dir + "StadiumAd.xml", "rt").read()
                                adfpkd = adfpkd.replace("assetPath", assetDirname)
                                adfpkd = adfpkd.replace("adType", adType)
                                Writeadfpkd = open(
                                    exportPath[:-6] + fpkdPath + "\\ad_{0}_{1}.fox2.xml".format(stid, adType), "wt")
                                Writeadfpkd.write(adfpkd)
                                Writeadfpkd.flush(), Writeadfpkd.close()
                                compileXML(exportPath[:-6] + fpkdPath + "\\ad_{0}_{1}.fox2.xml".format(stid, adType))
                                pack_unpack_Fpk(
                                    "{0}common\\ad\\#Win\\ad_{1}_{2}.fpkd.xml".format(exportPath[:-6], stid, adType))
                                remove_dir("{0}common\\ad\\#Win\\ad_{1}_{2}_fpkd".format(exportPath[:-6], stid, adType))
                                remove_file(
                                    "{0}common\\ad\\#Win\\ad_{1}_{2}.fpkd.xml".format(exportPath[:-6], stid, adType))
        self.report({"INFO"}, "Exporting Stadium ad succesfully...!")
        return {'FINISHED'}


class Export_TV(bpy.types.Operator):
    """Export TV"""
    bl_idname = "export_tv.operator"
    bl_label = str()
    opname: StringProperty()

    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def execute(self, context):
        stid = context.scene.STID
        exportPath = context.scene.export_path
        reports(self, context)
        if context.scene.isActive:
            self.report({"WARNING"}, context.scene.report_msg)
            context.scene.report_msg = str()
            context.scene.isActive = False
            return {'CANCELLED'}

        if len(stid) == 5:
            if context.scene.export_path == str():
                self.report({"WARNING"}, "Choose path to export TV e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Choose path to export TV e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

            if not stid in context.scene.export_path:
                self.report({"WARNING"}, "Stadium ID doesn't match!!")
                print("Stadium ID doesn't match!!")
                return {'CANCELLED'}

            if not context.scene.export_path.endswith(stid + "\\"):
                self.report({"WARNING"},
                            "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "Stadium ID isn't correct!!")
            return {'CANCELLED'}
        checks = checkStadiumID(context, False)
        if checks:
            self.report({"WARNING"}, "Stadium ID doesn't match, see more info => Window -> Toggle System Console")
            return {'CANCELLED'}
        TvOb, files, TvMdl, addrs = [], [], [], []
        arraySize, TvBoxSize, TvLineSize = 0, 0, 0
        tvlist = ["tv_%s_large_back.fmdl" % stid,
                  "tv_%s_large_front.fmdl" % stid,
                  "tv_%s_large_left.fmdl" % stid,
                  "tv_%s_large_right.fmdl" % stid,
                  "tv_%s_small_back.fmdl" % stid,
                  "tv_%s_small_front.fmdl" % stid,
                  "tv_%s_small_left.fmdl" % stid,
                  "tv_%s_small_right.fmdl" % stid,
                  ]
        assetDirname = "/Assets/pes16/model/bg/%s/scenes/" % stid
        assetDir = "{0}tv\\#Win\\tv_{1}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes\\".format(exportPath, stid, stid)
        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                TvOb.append(child.name)
                for ob in bpy.data.objects[child.name].children[:1]:
                    if ob is not None:
                        print('\n***************************************')
                        fmdlName = child.name
                        TvMdl.append(fmdlName)
                        arraySize += 1
                        if "_Large" in fmdlName:
                            TvBoxSize += 1
                        if "_Small" in fmdlName:
                            TvLineSize += 1
                        makedir("tv\\#Win\\tv_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes".format(stid, stid), True)
                        makedir("tv\\#Win\\tv_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\tv".format(stid, stid), True)
                        addr = str.upper(hex(tvdatalist[TvOb.index(fmdlName)]))
                        if len(addr) == 9:
                            addr = addr.replace("0X", "0x0")
                        addrs.append(addr)
                        TvName = tvlist[TvOb.index(fmdlName)]
                        fileName = assetDir + TvName
                        files.append(assetDirname + TvName)
                        meshID = str(fileName).split('..')[0].split('\\')[-1:][0]
                        print("Exporting ==> %s" % TvName)
                        print('***************************************\n')
                        export_fmdl(self, context, fileName, meshID, fmdlName)
        makeXML(exportPath + "tv\\#Win\\tv_" + stid + ".fpk.xml", files, "tv_%s.fpk" % stid, "Fpk", "FpkFile", True)
        makeXML(exportPath + "tv\\#Win\\tv_" + stid + ".fpkd.xml",
                "/Assets/pes16/model/bg/{0}/tv/tv_{1}.fox2".format(stid, stid), "tv_%s.fpkd" % stid, "Fpk", "FpkFile",
                False)
        fox2XmlPath = "{0}tv\\#Win\\tv_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\tv\\tv_{3}.fox2.xml".format(exportPath,
                                                                                                            stid, stid,
                                                                                                            stid)
        try:
            PesFoxXML.makeXMLForTv(fox2XmlPath, TvMdl, arraySize, addrs, files, TvBoxSize, TvLineSize)
            compileXML(fox2XmlPath)
        except Exception as msg:
            self.report({"WARNING"}, format(msg))
            return {'CANCELLED'}

        pack_unpack_Fpk("{0}tv\\#Win\\tv_{1}.fpk.xml".format(exportPath, stid))
        remove_dir("{0}tv\\#Win\\tv_{1}_fpk".format(exportPath, stid))
        remove_file("{0}tv\\#Win\\tv_{1}.fpk.xml".format(exportPath, stid))
        pack_unpack_Fpk("{0}tv\\#Win\\tv_{1}.fpkd.xml".format(exportPath, stid))
        remove_dir("{0}tv\\#Win\\tv_{1}_fpkd".format(exportPath, stid))
        remove_file("{0}tv\\#Win\\tv_{1}.fpkd.xml".format(exportPath, stid))
        self.report({"INFO"}, "Exporting TV succesfully...!")
        return {'FINISHED'}

    pass


import time


class Convert_OT(bpy.types.Operator):
    """Export and Convert all texture to FTEX"""
    bl_idname = "convert.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        start_time = time.time()
        stid = context.scene.STID
        reports(self, context)
        if context.scene.isActive:
            self.report({"WARNING"}, context.scene.report_msg)
            context.scene.report_msg = str()
            context.scene.isActive = False
            return {'CANCELLED'}

        if len(stid) == 5:
            if context.scene.export_path == str():
                self.report({"WARNING"}, "Choose path to export TV e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Choose path to export TV e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}

            if not stid in context.scene.export_path:
                self.report({"WARNING"}, "Stadium ID doesn't match!!")
                print("Stadium ID doesn't match!!")
                return {'CANCELLED'}

            if not context.scene.export_path.endswith(stid + "\\"):
                self.report({"WARNING"},
                            "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "Stadium ID isn't correct!!")
            return {'CANCELLED'}
        checks = checkStadiumID(context, True)
        if checks:
            self.report({"WARNING"},
                        "Stadium ID doesn't match, see more info => Window -> Toggle System Console")
            return {'CANCELLED'}
        isConvertedDict = {}
        isConvertedDict.clear()
        outpath = context.scene.export_path + "sourceimages\\tga\\#windx11"
        for child in bpy.data.objects[context.scene.part_info].children:
            if child.type == 'EMPTY' and child is not None:
                for ob in bpy.data.objects[child.name].children[:1]:
                    if ob is not None:
                        for ob2 in bpy.data.objects[ob.name].children:
                            if ob2 is not None and ob2.type == "MESH":
                                blenderMaterial = bpy.data.objects[ob2.name].active_material
                                for nodes in blenderMaterial.node_tree.nodes:
                                    if nodes.type == "TEX_IMAGE":
                                        filePath = nodes.image.filepath
                                        fileName = str(filePath).split('..')[0].split('\\')[-1:][0]
                                        ftexFile = outpath + "\\" + fileName[:-3] + "ftex"

                                        if fileName in isConvertedDict.keys():
                                            if not isConvertedDict[fileName]:
                                                isConvertedDict[fileName] = True
                                            else:
                                                continue
                                        else:
                                            isConvertedDict[fileName] = False

                                        # If using skip non-modified, it will be checked here
                                        # otherwise it will convert every texture anyway
                                        if context.scene.useFastConvertTexture:
                                            if os.path.isfile(ftexFile):
                                                # if ftex file exists and original texture was not modified, skip it
                                                if not os.path.getmtime(ftexFile) < os.path.getmtime(filePath):
                                                    continue
                                        # if you reach here it means the old ftex file is going to be replaced,
                                        # so it will get removed first
                                        try:
                                            remove_file(ftexFile)
                                        except:
                                            pass

                                        inPath = fileName
                                        dirpath = os.path.dirname(filePath)
                                        if context.scene.export_path == str():
                                            self.report({"WARNING"}, "Export path can't be empty!!")
                                            print("Export path can't be empty!!")
                                            return {'CANCELLED'}
                                        filenames, extension = os.path.splitext(fileName)
                                        if extension != str():
                                            if extension.lower() == '.png':
                                                fileName = filenames + extension
                                                PNGPath = os.path.join(dirpath, fileName)
                                                texconv(PNGPath, dirpath, " -r -y -l -f DXT5 -ft dds -srgb -o ",
                                                        False)
                                                newPath = os.path.join(dirpath, filenames + ".dds")
                                                inPath = newPath
                                            elif extension.lower() == '.tga':
                                                fileName = filenames + extension
                                                TGAPath = os.path.join(dirpath, fileName)
                                                texconv(TGAPath, dirpath, " -r -y -l -f DXT5 -ft dds -srgb -o ",
                                                        False)
                                                newPath = os.path.join(dirpath, filenames + ".dds")
                                                inPath = newPath
                                            elif extension.lower() == '.dds':
                                                inPath = filePath
                                            else:
                                                self.report({"WARNING"},
                                                            "Not supported texture format, check in Blender Console => Window -> Toggle System Console !!")
                                                print(
                                                    "\nNot supported texture format!!, Texture format must be .PNG .DDS .TGA")
                                                print("Conversion Failed !! (File Not Found or Unsupported format)")
                                                print("**" * len(filenames + extension))
                                                print(
                                                    "File (" + filenames + extension + ") isn't the right texture format!!")
                                                print("**" * len(filenames + extension))
                                                print(
                                                    "\nCheck out Object in Parent ({0} --> {1} --> {2}) in Mesh object ({3}) in node({4})"
                                                        .format(context.scene.part_info, ob.parent.name,
                                                                ob2.parent.name, ob2.name, nodes.name))
                                                return {'CANCELLED'}
                                            if os.path.isfile(inPath):
                                                convert_dds(inPath, outpath)
                                                print(
                                                    "Converting texture from object->({0}) in node->({1})-->({2}) ==> ({3}ftex) ".format(
                                                        ob2.name, nodes.name, fileName, fileName[:-3]))
                                                # if the original texture was .dds itself, no need to delete it
                                                # otherwise, it was the temp texture we made, so it will be deleted
                                                if extension.lower() != '.dds':
                                                    try:
                                                        os.remove(inPath)
                                                    except Exception as msg:
                                                        self.report({"INFO"}, format(msg))
                                                        return {'CANCELLED'}
        print("--- %s seconds ---" % (time.time() - start_time))
        self.report({"INFO"}, "Converting texture succesfully...!")
        print("Converting texture succesfully...!")
        return {'FINISHED'}

    pass


class Clear_OT(bpy.types.Operator):
    """Clear Temporary Data"""
    bl_idname = "clear_temp.operator"
    bl_label = str()
    opname: StringProperty()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        filename = context.scene.fpk_path
        if self.opname == "cleartemp":
            dirpath = context.scene.texture_path
            try:
                remove_dir(filename[:-4] + "_fpk")
                remove_file(filename + ".xml")
                remove_dds(dirpath)
                self.report({"INFO"}, "Clear temporary data succesfully!")
            except:
                self.report({"WARNING"}, "No temporary data found!")
        if self.opname == "cleartempdata":
            dirpath = context.scene.export_path + "\\sourceimages\\tga\\#windx11\\"
            try:
                remove_dds(dirpath)
                self.report({"INFO"}, "Clear temporary data succesfully!")
            except:
                self.report({"WARNING"}, "No temporary data found!")
        return {'FINISHED'}

    pass


class Parent_OT(bpy.types.Operator):
    """Assign active object to parent list"""
    bl_idname = "set_parent.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        ob = context.active_object
        try:
            ob_id = ob.droplist
            for ob_p in bpy.context.selected_objects:
                ob_p.parent = bpy.data.objects[ob_id]
                ob_p.droplist = bpy.data.objects[ob_id].name
        except:
            self.report({"WARNING"}, "Parents need to refresh!!")
        return {'FINISHED'}

    pass


class remove_OT(bpy.types.Operator):
    """Unassign active object from parent list"""
    bl_idname = "clr.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.parent_clear(type='CLEAR')
        return {'FINISHED'}

    pass


class FMDL_Shader_Set(bpy.types.Operator):
    """Set a Shader from list"""
    bl_idname = "shader.operator"
    bl_label = "Set Shader"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        try:
            node_group()
            PesFoxShader.setShader(self, context)
        except Exception as exception:
            self.report({"WARNING"}, format(exception) + " see more info => Windows -> Toggle System Console")
            if 'nodes' in format(exception):
                print("\nInfo: ", format(exception) + " see more info => Windows -> Toggle System Console")
                print("\n\nPlease check your material, does it support nodes?\n",
                      "\n1) Remove problem material",
                      "\n2) Create a new material",
                      "\n\ntry if the problem is still same please contact the maker")
            return {'CANCELLED'}
        return {'FINISHED'}

    pass


class Start_New_Scene(bpy.types.Operator):
    """Start New Scene"""
    bl_idname = "scene.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        remove_file(startupFile)
        if os.path.isfile(baseStartupFile):
            shutil.copy(baseStartupFile, startupFile)
        bpy.ops.wm.read_homefile()
        return {'FINISHED'}

    pass


class Create_Main_Parts(bpy.types.Operator):
    """Create Main Parts"""
    bl_idname = "main_parts.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        scn = context.scene
        Create_Parent_Part(self, context)

        if scn.part_info == "AUDIAREA" or scn.part_info == "FLAGAREA" or scn.part_info == "TV":
            parentlist = [(ob.name, ob.name, ob.name) for ob in
                          (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if
                          ob.name in main_list if ob.name not in ['LIGHTS', 'L_FRONT', 'L_BACK', 'L_RIGHT', 'L_LEFT']]
        else:
            parentlist = [("MESH_" + ob.name, "MESH_" + ob.name, "MESH_" + ob.name) for ob in
                          (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if
                          ob.name in main_list if
                          ob.name not in ['LIGHTS', 'L_FRONT', 'L_BACK', 'L_RIGHT', 'L_LEFT', 'MESH_CROWD',
                                          'MESH_FLAGAREA']]
        parentlist.sort(reverse=0)
        bpy.types.Object.droplist = EnumProperty(name="Parent List", items=parentlist)
        self.report({"INFO"}, "Stadium main parts (Parents) has been created...")
        return {'FINISHED'}

    pass


class FMDL_21_PT_Texture_Panel(bpy.types.Panel, bpy.types.AnyType):
    bl_label = "FMDL Texture Settings"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Item'
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        if not (
                context.mode == 'OBJECT'
                and context.object is not None
                and context.active_object
                and context.material
                and context.object.type == 'MESH'
                and context.active_node is not None
                and context.object.name.split(sep='_')[0] != 'C'
                and context.object.name.split(sep='_')[0] != 'F'
                and context.active_node.show_texture):
            return False
        return True

    def draw(self, context):
        node = context.active_node
        row = self.layout.row()
        box = self.layout.box()
        box.alignment = 'CENTER'
        row = box.row(align=0)
        row.label(text="Image File")
        row.operator(FMDL_Scene_Open_Image.bl_idname, icon="FILE_FOLDER")
        row.operator("edit.operator", text="", icon="FILE_IMAGE")
        row.operator("reload.operator", text="", icon="FILE_REFRESH")
        row = box.row(align=0)
        row.prop(node, "fmdl_texture_role", text="Role")
        row = box.row(align=0)
        row.prop(node, "fmdl_texture_filename", text="Filename")
        row = box.row(align=0)
        row.prop(node, "fmdl_texture_directory", text="Directory")


class FMDL_Scene_Open_Image(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Open a Image Texture FTEX or DDS"""
    bl_idname = "open.image"
    bl_label = "Open Image Texture"
    bl_options = {'REGISTER', 'UNDO'}

    import_label = "Open Image Texture"

    filename_ext = "DDS, PNG, TGA"
    filter_glob: StringProperty(default="*.dds;*.png;*.tga", options={'HIDDEN'})

    def execute(self, context):

        filePath = self.filepath
        fileName = str(filePath).split('..')[0].split('\\')[-1:][0]
        mat_name = context.active_object.active_material.name
        node_name = context.active_node.name
        if fileName in bpy.data.images:
            bpy.data.materials[mat_name].node_tree.nodes[node_name].image = bpy.data.images[fileName]
        else:
            image = bpy.data.images.load(filepath=filePath)
            bpy.data.materials[mat_name].node_tree.nodes[node_name].image = image
        filenames = os.path.splitext(fileName)[0]
        blenderImage = bpy.data.images[fileName]
        fileName = filenames + '.tga'
        bpy.data.materials[mat_name].node_tree.nodes[node_name].image.alpha_mode = 'NONE'
        bpy.data.materials[mat_name].node_tree.nodes[node_name].fmdl_texture_filename = fileName
        bpy.data.materials[mat_name].node_tree.nodes[node_name].label = fileName
        textureRole = bpy.data.materials[mat_name].node_tree.nodes[node_name].fmdl_texture_role
        blenderImage.colorspace_settings.name = 'Non-Color'
        if 'Base_Tex_SRGB' in textureRole or 'Base_Tex_LIN' in textureRole:
            blenderImage.colorspace_settings.name = 'sRGB'
        self.report({"INFO"}, "Add texture [%s] succesfully!" % filenames)
        print("Add texture [%s] succesfully!" % filenames)
        return {'FINISHED'}


class FMDL_Externally_Edit(bpy.types.Operator):
    """Edit texture with externally editor"""
    bl_idname = "edit.operator"
    bl_label = "Externally Editor"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        mat_name = bpy.context.active_object.active_material.name
        node_name = bpy.context.active_node.name
        texname = bpy.data.materials[mat_name].node_tree.nodes[node_name]
        imagePath = str()
        try:
            for img in bpy.data.images:
                if texname.label[:-4] in img.name:
                    imagePath = bpy.data.images[img.name].filepath
        except:
            pass
        if os.path.isfile(imagePath):
            try:
                bpy.ops.image.external_edit(filepath=imagePath)
            except Exception as msg:
                self.report({"WARNING"}, format(msg))
                return {'CANCELLED'}
        else:
            self.report({"WARNING"}, "File not found!!")
            return {'CANCELLED'}
        return {'FINISHED'}

    pass


class FMDL_Reload_Image(bpy.types.Operator):
    """Reload All Image Texture"""
    bl_idname = "reload.operator"
    bl_label = str()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        for image in bpy.data.images:
            if image.users:
                image.reload()
        self.report({"INFO"}, "All image texture reloaded!")
        return {'FINISHED'}

    pass


def update_shader_list(self, context):
    try:
        self.fox_shader = self.fmdl_material_shader
    except:
        pass


def update_alpha_list(self, context):
    try:
        self.fmdl_alpha_enum = int(self.fmdl_alpha_enum_select)
    except:
        pass


def update_alpha_enum(self, context):
    try:
        self.fmdl_alpha_enum_select = str(self.fmdl_alpha_enum)
    except:
        if not self.fmdl_alpha_enum_select == str(self.fmdl_alpha_enum):
            self.fmdl_alpha_enum_select = 'Unknown'
        pass


def update_shadow_list(self, context):
    try:
        self.fmdl_shadow_enum = int(self.fmdl_shadow_enum_select)
    except:
        pass


def update_shadow_enum(self, context):
    try:
        self.fmdl_shadow_enum_select = str(self.fmdl_shadow_enum)
    except:
        if not self.fmdl_shadow_enum_select == str(self.fmdl_shadow_enum):
            self.fmdl_shadow_enum_select = 'Unknown'
        pass


classes = [

    Import_OT,

    FMDL_21_PT_Texture_Panel,
    FMDL_Scene_Open_Image,
    FMDL_21_PT_Mesh_Panel,

    FMDL_21_PT_UIPanel,
    Create_Main_Parts,
    Refresh_OT,
    Parent_OT,
    remove_OT,
    Clear_OT,
    FMDL_Shader_Set,
    FMDL_Externally_Edit,
    FMDL_Reload_Image,

    FMDL_Object_BoundingBox_Create,
    FMDL_Object_BoundingBox_Remove,
    FMDL_21_PT_Object_BoundingBox_Panel,

    Export_OT,
    Convert_OT,
    Start_New_Scene,
    Crowd_OT,
    Flags_Area_OT,
    Light_FX,
    Export_TV,
    TV_Objects,
    Pitch_Objects,
    Staff_Coach_Pos,
    New_STID,
    ExportStadium_AD,

    PES_21_PT_CrowdSection,
    PES_21_OT_assign_crowd_type,

    FMDL_Material_Parameter_List_Add,
    FMDL_Material_Parameter_List_Remove,
    FMDL_Material_Parameter_List_MoveUp,
    FMDL_Material_Parameter_List_MoveDown,
    FMDL_UL_material_parameter_list,
    FMDL_21_PT_Material_Panel,
    FMDL_MaterialParameter,
]


def register():
    pcoll = bpy.utils.previews.new()
    pcoll.load("icon_0", os.path.join(icons_dir, "icon_0.dds"), 'IMAGE')
    pcoll.load("icon_1", os.path.join(icons_dir, "icon_1.dds"), 'IMAGE')
    icons_collections["custom_icons"] = pcoll
    for c in classes:
        bpy.utils.register_class(c)

    domData = parse(xml_dir + "PesFoxShader.xml")
    shaders = [(shader.getAttribute("shader"), shader.getAttribute("technique"),
                "Shader Type: " + shader.getAttribute("shader"))
               for shader in domData.getElementsByTagName("FoxShader") if shader.getAttribute("technique")]
    shaders.sort(reverse=0)
    bpy.types.Material.fox_shader = EnumProperty(name="Select Fox Shader", items=shaders)
    bpy.types.Material.fmdl_material_parameters = CollectionProperty(name="Material Parameters",
                                                                     type=FMDL_MaterialParameter)
    bpy.types.Material.fmdl_material_parameter_active = IntProperty(name="FMDL_Material_Parameter_Name_List index",
                                                                    default=-1, options={'SKIP_SAVE'})
    bpy.types.Material.fmdl_material_shader = StringProperty(name="Shader", update=update_shader_list)
    bpy.types.Material.fmdl_material_technique = StringProperty(name="Technique")
    bpy.types.ShaderNodeTexImage.fmdl_texture_filename = StringProperty(name="Texture Filename")
    bpy.types.ShaderNodeTexImage.fmdl_texture_directory = StringProperty(name="Texture Directory")
    bpy.types.ShaderNodeTexImage.fmdl_texture_role = StringProperty(name="Texture Role")

    bpy.types.Object.fmdl_file = BoolProperty(name="Is FMDL file", options={'SKIP_SAVE'})
    bpy.types.Object.fmdl_filename = StringProperty(name="FMDL filename", options={'SKIP_SAVE'})
    bpy.types.Mesh.fmdl_alpha_enum_select = EnumProperty(name="Alpha Enum", items=PesFoxShader.AlphaEnum, default="0",
                                                         update=update_alpha_list)
    bpy.types.Mesh.fmdl_shadow_enum_select = EnumProperty(name="Shadow Enum", items=PesFoxShader.ShadowEnum,
                                                          default="0", update=update_shadow_list)
    bpy.types.Mesh.fmdl_alpha_enum = IntProperty(name="Alpha Enum", default=0, min=0, max=255, update=update_alpha_enum)
    bpy.types.Mesh.fmdl_shadow_enum = IntProperty(name="Shadow Enum", default=0, min=0, max=255,
                                                  update=update_shadow_enum)

    bpy.types.Object.fmdl_export_extensions_enabled = BoolProperty(name="Enable PES FMDL extensions", default=True)
    bpy.types.Object.fmdl_export_loop_preservation = BoolProperty(name="Preserve split vertices", default=True)
    bpy.types.Object.fmdl_export_mesh_splitting = BoolProperty(name="Autosplit overlarge meshes", default=True)
    bpy.types.Scene.fmdl_import_extensions_enabled = BoolProperty(name="Enable PES FMDL extensions", default=True)
    bpy.types.Scene.fmdl_import_loop_preservation = BoolProperty(name="Preserve split vertices", default=True)
    bpy.types.Scene.fmdl_import_mesh_splitting = BoolProperty(name="Autosplit overlarge meshes", default=True)
    bpy.types.Scene.fmdl_import_load_textures = BoolProperty(name="Load textures", default=True)
    bpy.types.Scene.fmdl_import_all_bounding_boxes = BoolProperty(name="Import all bounding boxes", default=False)
    bpy.types.Scene.fixmeshesmooth = BoolProperty(name="FIX-Smooth Meshes", default=True)
    bpy.types.Scene.useFastConvertTexture = BoolProperty(name="Skip Non-Modified textures", default=True)

    bpy.types.Scene.crowd_row_space = FloatProperty(name=" ", step=1, subtype='FACTOR', default=5.0, min=0.0, max=10.0,
                                                    description="Set a value for vertical space of seat rows. (Default: 5.00)")
    bpy.types.Object.droplist = EnumProperty(name="Parent List", items=parentlist)

    bpy.types.Scene.texture_path = StringProperty(name="Texture Path", subtype='DIR_PATH')
    bpy.types.Scene.export_path = StringProperty(name="Export Path", subtype='DIR_PATH')
    bpy.types.Scene.fpk_path = StringProperty(name="Fpk File Path", subtype='FILE_PATH')
    bpy.types.Scene.part_info = EnumProperty(name="Part List", items=part_export)
    bpy.types.Scene.STID = StringProperty(name="ID", default="st081")

    bpy.types.Scene.isActive = BoolProperty(name=str(), default=False)
    bpy.types.Scene.report_msg = StringProperty(name=str())
    bpy.types.Scene.crowd_type_enum = EnumProperty(items=behavior, name='Type')

    bpy.types.Scene.tvobject = EnumProperty(name="TV", items=[("tv_large_c", "tv_large_c", "tv_large_c"),
                                                              ("tv_small_c", "tv_small_c", "tv_small_c")])
    bpy.types.Scene.l_lit_side = EnumProperty(name="Select Side for Lights", items=light_sidelist, default="L_FRONT")
    bpy.types.Object.l_Energy = FloatProperty(name="Energy", min=0.25, max=5.0, subtype='FACTOR', default=2.5)
    bpy.types.Scene.l_fx_tex = EnumProperty(name="Texture Type for Light FX", items=lfx_tex_list,
                                            default="tex_star_02.ftex")
    bpy.types.Scene.time_mode = EnumProperty(name="Select Time/Weather", items=timeMode, default="nf")


def unregister():
    for pcoll in icons_collections.values():
        bpy.utils.previews.remove(pcoll)
    icons_collections.clear()
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
