import bpy, os, PES_Stadium_Exporter
from xml.dom.minidom import parse
from mathutils import Vector
from bpy.props import EnumProperty
import random

AlphaEnumDict ={0: 'No Alpha (One Side)',
                32: 'No Alpha (Two Side)',
                16: 'Glass (One Side)',
                48: 'Glass (Two Side)',
                17: 'Glass2 (One Side)',
                49: 'Glass2 (Two Side)',
                80: 'Decal',
                112: 'Eyelash',
                128: 'Alpha (One Side)',
                160: 'Alpha (Two Side)',
                192: 'Unknown OMBS'

}

ShadowEnumDict={0:'Shadow',
                1: 'No Shadow',
                2: 'Invisible Mesh Visible Shadow',
                4: 'Tinted Glass',
                5: 'Glass',
                36: 'Light OMBS',
                38: 'Glass OMBS',
                64: 'Shadow2',
                65: 'No Shadow2'
}

AlphaEnum = [("Custom", "Custom", "Custom")] + [
    (str(k), v, v) for k, v in AlphaEnumDict.items()
]

ShadowEnum = [("Custom", "Custom", "Custom")] + [
    (str(k), v, v) for k, v in ShadowEnumDict.items()
]

def setShader(self, context):
    try:
        domData = parse(PES_Stadium_Exporter.xml_dir + "PesFoxShader.xml")
        obj = bpy.context.active_object
        blenderMaterial = obj.active_material
        material = context.material
        nt = blenderMaterial.node_tree

        old_shader = blenderMaterial.fmdl_material_shader
        has_old_shader = old_shader not in ("", None)

        backup = {"textures": {}, "parameters": {}}

        if has_old_shader:
            for node in nt.nodes:
                if node.type == "TEX_IMAGE":
                    role = node.fmdl_texture_role
                    if role and node.image:
                        backup["textures"][role] = {
                            "image": node.image,
                            "directory": getattr(node, "fmdl_texture_directory", ""),
                            "filename": getattr(node, "fmdl_texture_filename", "")
                        }
            for p in material.fmdl_material_parameters:
                backup["parameters"][p.name] = list(p.parameters)
            blenderMaterial["_shader_backup"] = backup

        material.fmdl_material_parameters.clear()
        nt.nodes.clear()

        groups = ["TRM Subsurface", "SRM Seperator", "NRM Converter"]
        for g in groups:
            n = nt.nodes.new('ShaderNodeGroup')
            n.node_tree = bpy.data.node_groups[g]
            nt.nodes['Group'].name = g

        principled = nt.nodes.new("ShaderNodeBsdfPrincipled")
        principled.location = Vector((0, 200))
        out_node = nt.nodes.new("ShaderNodeOutputMaterial")
        out_node.location = Vector((400, 200))
        nt.links.new(principled.outputs['BSDF'], out_node.inputs['Surface'])

        TRM = nt.nodes['TRM Subsurface']
        SRM = nt.nodes['SRM Seperator']
        NRM = nt.nodes['NRM Converter']

        TRM.location = Vector((-200, 200))
        SRM.location = Vector((-200, 0))
        NRM.location = Vector((-200, -200))

        nt.links.new(TRM.outputs['Subsurface'], principled.inputs['Subsurface Scale'])
        nt.links.new(TRM.outputs['Subsurface Color'], principled.inputs['Subsurface Radius'])
        nt.links.new(SRM.outputs['Specular'], principled.inputs['Specular IOR Level'])
        nt.links.new(SRM.outputs['Roughness'], principled.inputs['Roughness'])
        nt.links.new(NRM.outputs['Normal'], principled.inputs['Normal'])

        if context.scene.part_info == "AD":
            tex_dir = "/Assets/pes16/model/bg/common/ad/sourceimages/tga/"
        else:
            tex_dir = f"/Assets/pes16/model/bg/{context.scene.STID}/sourceimages/tga/"

        fox_list = domData.getElementsByTagName("FoxShader")

        restored_texture_roles = []
        restored_texture_files = {}
        missing_texture_roles = []

        used_backup = False

        for slot in obj.material_slots:
            mat = slot.material
            preset = mat.fmdl_material_preset

            for shader in fox_list:
                if shader.getAttribute("shader") != preset:
                    continue

                technique = shader.getAttribute("technique")
                mat.fmdl_material_shader = preset
                mat.fmdl_material_technique = technique

                xml_params = shader.getElementsByTagName("Parameter")
                xml_param_names = [p.getAttribute("vector") for p in xml_params if p.getAttribute("vector")]

                for tag in xml_params:
                    textures = tag.getAttribute("textures")
                    if not textures:
                        continue

                    tex = nt.nodes.new("ShaderNodeTexImage")
                    tex.name = textures

                    if has_old_shader:
                        old_texture_dict = {r: backup["textures"][r]["image"] for r in backup["textures"]}
                        old_texture_meta = {r: backup["textures"][r] for r in backup["textures"]}

                        if textures in old_texture_dict:
                            tex.image = old_texture_dict[textures]
                            restored_texture_roles.append(textures)
                            restored_texture_files[textures] = \
                                old_texture_meta[textures]["filename"] if old_texture_meta[textures]["filename"] != "" else "[NO FILE]"
                            print(f"[RESTORE] Texture restored: {textures} ({restored_texture_files[textures]})")
                        else:
                            restored_texture_files[textures] = "[NO FILE]"
                            missing_texture_roles.append(textures)
                            print(f"[WARNING] Missing texture role: {textures}")

                        tex.fmdl_texture_role = textures
                        tex.fmdl_texture_directory = old_texture_meta[textures]["directory"] if textures in old_texture_meta else tex_dir
                        tex.fmdl_texture_filename = old_texture_meta[textures]["filename"] if textures in old_texture_meta else ""

                        used_backup = True

                    else:
                        tex.fmdl_texture_role = textures
                        tex.fmdl_texture_directory = tex_dir

                        if technique == 'pes3DFW_EyeOcclusion':
                            tex.fmdl_texture_filename = 'eye_occlusion_alp.dds'
                        elif technique == 'pes3DDC_Wet':
                            if textures == 'CubeMap_Tex_LIN':
                                tex.fmdl_texture_directory = '/Assets/pes16/model/character/common/sourceimages/'
                                tex.fmdl_texture_filename = 'head_wet_cbm.dds'
                            elif textures in ('NormalMap_Tex_NRM', 'SubNormalMap_Tex_NRM'):
                                tex.fmdl_texture_directory = '/Assets/pes16/model/character/common/sourceimages/'
                                tex.fmdl_texture_filename = 'dummy_nrm.tga'
                            elif textures == 'Mask_Tex_LIN':
                                tex.fmdl_texture_directory = '/Assets/pes16/model/character/common/sourceimages/'
                                tex.fmdl_texture_filename = 'dummy_dtm.tga'

                    if "Base_Tex_" in textures:
                        tex.location = Vector((-500, 560))
                        nt.links.new(tex.outputs['Color'], principled.inputs['Base Color'])
                        nt.links.new(tex.outputs['Color'], TRM.inputs['BSM Tex'])
                        if tex.image and tex.image.alpha_mode != 'NONE':
                            nt.links.new(tex.outputs['Alpha'], principled.inputs['Alpha'])
                    elif "NormalMap_Tex_" in textures:
                        tex.location = Vector((-500, -220))
                        nt.links.new(tex.outputs['Color'], NRM.inputs['NRM Tex'])
                        nt.links.new(tex.outputs['Alpha'], NRM.inputs['Alpha'])
                    elif "SpecularMap_Tex_" in textures:
                        tex.location = Vector((-500, 40))
                        nt.links.new(tex.outputs['Color'], SRM.inputs['SRM Tex'])
                        nt.links.new(tex.outputs['Color'], SRM.inputs['RGM Tex'])
                    elif "RoughnessMap_Tex_" in textures:
                        tex.location = Vector((-750, 40))
                        nt.links.new(tex.outputs['Color'], SRM.inputs['RGM Tex'])
                    elif "MetalnessMap_Tex_" in textures:
                        tex.location = Vector((-750, 0))
                        nt.links.new(tex.outputs['Color'], principled.inputs['Metallic'])
                    elif "Translucent_Tex_" in textures:
                        tex.location = Vector((-500, 300))
                        nt.links.new(tex.outputs['Color'], TRM.inputs['TRM Tex'])
                    else:
                        tex.location = Vector((random.randint(-500, 400), random.randint(-400, 300)))

                material.fmdl_material_parameters.clear()

                if has_old_shader:
                    for name, vals in backup["parameters"].items():
                        if name in xml_param_names:
                            p = material.fmdl_material_parameters.add()
                            p.name = name
                            p.parameters = vals
                            used_backup = True
                            print(f"[RESTORE] Parameter restored: {name}")

                    for tag in xml_params:
                        name = tag.getAttribute("vector")
                        if name and name not in backup["parameters"]:
                            p = material.fmdl_material_parameters.add()
                            p.name = name
                            p.parameters = [
                                float(tag.getAttribute("x")),
                                float(tag.getAttribute("y")),
                                float(tag.getAttribute("z")),
                                float(tag.getAttribute("w")),
                            ]
                else:
                    for tag in xml_params:
                        name = tag.getAttribute("vector")
                        if name:
                            p = material.fmdl_material_parameters.add()
                            p.name = name
                            p.parameters = [
                                float(tag.getAttribute("x")),
                                float(tag.getAttribute("y")),
                                float(tag.getAttribute("z")),
                                float(tag.getAttribute("w")),
                            ]

                domData.unlink()

        for n in nt.nodes:
            n.select = False

        if has_old_shader and used_backup:
            self.report({"INFO"}, f"Shader applied (restored) for {blenderMaterial.name}")
        else:
            self.report({"INFO"}, f"Shader has been set for {blenderMaterial.name}")

        return 1

    except Exception as msg:
        self.report({"WARNING"}, str(msg))
        return {'CANCELLED'}
