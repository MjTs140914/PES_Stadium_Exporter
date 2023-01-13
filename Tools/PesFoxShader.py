import bpy, PES_Stadium_Exporter
from xml.dom.minidom import parse
from mathutils import Vector
from bpy.props import EnumProperty
import random

AlphaEnum = [('Custom', 'Custom', 'Custom'),
			('0', 'No Alpha (One Side)', 'No Alpha (One Side)'),
			('32', 'No Alpha (Two Side)', 'No Alpha (Two Side)'),
			('16', 'Glass (One Side)', 'Glass (One Side)'),
			('48', 'Glass (Two Side)', 'Glass (Two Side)'),
			('17', 'Glass2 (One Side)', 'Glass2 (One Side)'),
			('49', 'Glass2 (Two Side)', 'Glass2 (Two Side)'),
			('80', 'Decal', 'Decal'),
			('112', 'Eyelash', 'Eyelash'),
			('128', 'Alpha (One Side)', 'Alpha (One Side)'),
			('160', 'Alpha (Two Side)', 'Alpha (Two Side)'),
			('192', 'Unknown OMBS', 'Unknown OMBS')
]

Alpha_EnumDict ={0: 'No Alpha (One Side)',
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
ShadowEnum = [('Custom', 'Custom', 'Custom'),
			('0', 'Shadow', 'Shadow'),
			('1', 'No Shadow', 'No Shadow'),
			('2', 'Invisible Mesh Visible Shadow', 'Invisible Mesh Visible Shadow'),
			('4', 'Tinted Glass', 'Tinted Glass'),
			('5', 'Glass', 'Glass'),
			('36', 'Light OMBS', 'Light OMBS'),
			('38', 'Glass OMBS', 'Glass OMBS'),
			('64', 'Shadow2', 'Shadow2'),
			('65', 'No Shadow2', 'No Shadow2')
]

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

def setShader(self, context):
	texture_directory = str()
	domData = parse(PES_Stadium_Exporter.xml_dir+"PesFoxShader.xml")
	material = context.material
	parameter = material.fmdl_material_parameters.clear()
	blenderMaterial = bpy.context.active_object.active_material
	blenderMaterial.node_tree.nodes.clear()
	new_group_node = blenderMaterial.node_tree.nodes.new('ShaderNodeGroup')
	new_group_node.node_tree = bpy.data.node_groups['TRM Subsurface']
	blenderMaterial.node_tree.nodes['Group'].name = 'TRM Subsurface'
	new_group_node = blenderMaterial.node_tree.nodes.new('ShaderNodeGroup')
	new_group_node.node_tree = bpy.data.node_groups['SRM Seperator']
	blenderMaterial.node_tree.nodes['Group'].name = 'SRM Seperator'
	new_group_node = blenderMaterial.node_tree.nodes.new('ShaderNodeGroup')
	new_group_node.node_tree = bpy.data.node_groups['NRM Converter']
	blenderMaterial.node_tree.nodes['Group'].name = 'NRM Converter'
	blenderOutput = blenderMaterial.node_tree.nodes.new("ShaderNodeOutputMaterial")
	blenderOutput.location = Vector((400, 200))
	blenderShader = blenderMaterial.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
	blenderShader.location = Vector((0, 200))
	principled = blenderMaterial.node_tree.nodes['Principled BSDF']
	Material_Output = blenderMaterial.node_tree.nodes['Material Output']
	Material_Output.location = Vector((300, 300))
	blenderMaterial.node_tree.links.new(blenderShader.outputs['BSDF'], Material_Output.inputs['Surface'])
	TRM_Subsurface = blenderMaterial.node_tree.nodes['TRM Subsurface']
	TRM_Subsurface.location = Vector((-200, 200))
	SRM_Seperator = blenderMaterial.node_tree.nodes['SRM Seperator']
	SRM_Seperator.location = Vector((-200, 0))
	NRM_Converter = blenderMaterial.node_tree.nodes['NRM Converter']
	NRM_Converter.location = Vector((-200, -200))
	blenderMaterial.node_tree.links.new(TRM_Subsurface.outputs['Subsurface'], principled.inputs['Subsurface'])
	blenderMaterial.node_tree.links.new(TRM_Subsurface.outputs['Subsurface Color'], principled.inputs['Subsurface Color'])
	blenderMaterial.node_tree.links.new(SRM_Seperator.outputs['Specular'], principled.inputs['Specular'])
	blenderMaterial.node_tree.links.new(SRM_Seperator.outputs['Roughness'], principled.inputs['Roughness'])
	blenderMaterial.node_tree.links.new(NRM_Converter.outputs['Normal'], principled.inputs['Normal'])

	try:
		if context.scene.part_info == "AD":
			texture_directory = "/Assets/pes16/model/bg/common/ad/sourceimages/tga/"
		else:
			texture_directory = "/Assets/pes16/model/bg/%s/sourceimages/tga/" % context.scene.STID
		ob = bpy.context.active_object
		for slot in bpy.data.objects[ob.name].material_slots:
			materials_name = slot.name
			getshader = bpy.data.materials[materials_name].fmdl_material_preset
			fox = domData.getElementsByTagName("FoxShader")
			for shader in fox:
				shaderfox = shader.getAttribute("shader")
				technique = shader.getAttribute("technique")		
				if shaderfox == getshader:
					bpy.data.materials[materials_name].fmdl_material_shader = shaderfox
					bpy.data.materials[materials_name].fmdl_material_technique = technique	
					foxshader = shader.getElementsByTagName("Parameter")
					for texture in foxshader:
						textures = texture.getAttribute("textures")
						if textures:
							rdmx = random.randint(-500, 400)
							rdmy = random.randint(-400, 300)
							blenderTexture = blenderMaterial.node_tree.nodes.new("ShaderNodeTexImage")
							blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_role = textures
							blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_directory = texture_directory

							if technique == 'pes3DFW_EyeOcclusion':
								blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_filename  = 'eye_occlusion_alp.dds'
							if technique == 'pes3DDC_Wet':
								if textures == 'CubeMap_Tex_LIN':
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_directory = '/Assets/pes16/model/character/common/sourceimages/'
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_filename = 'head_wet_cbm.dds'
								elif textures == 'NormalMap_Tex_NRM' or textures == 'SubNormalMap_Tex_NRM':
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_directory = '/Assets/pes16/model/character/common/sourceimages/'
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_filename = 'dummy_nrm.tga'
								elif textures == 'Mask_Tex_LIN':
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_directory ='/Assets/pes16/model/character/common/sourceimages/'
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_filename = 'dummy_dtm.tga'
							elif technique == 'pes3DDF_Hair2_NrmUV' or technique == 'pes3DDF_Hair2':
								if textures == 'CubeMap_Tex_LIN':
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_directory = '/Assets/pes16/model/character/common/sourceimages/'
									blenderMaterial.node_tree.nodes['Image Texture'].fmdl_texture_filename = 'haircube_cbm.dds'

							if 'pes3DDF_Skin_Face' in blenderMaterial.fmdl_material_technique:
								blenderMaterial.use_sss_translucency = True
							if 'pes3DDF_Hair' in blenderMaterial.fmdl_material_technique:
								blenderMaterial.blend_method = 'HASHED'
							elif 'pes3DDC_Adjust' in blenderMaterial.fmdl_material_technique:
								blenderMaterial.blend_method = 'CLIP'
								blenderMaterial.alpha_threshold = 1.0
							elif 'fox3DDC_Blin' in blenderMaterial.fmdl_material_technique:
								blenderMaterial.blend_method = 'BLEND'
								blenderMaterial.show_transparent_back = True
							elif 'fox3DDF_Blin_Translucent' in blenderMaterial.fmdl_material_technique:
								blenderMaterial.blend_method = 'BLEND'
								blenderMaterial.show_transparent_back = False
							else:
								blenderMaterial.blend_method = 'BLEND'
								blenderMaterial.show_transparent_back = False
								
							blenderMaterial.node_tree.nodes['Image Texture'].name = textures
							blenderTexture.select = True
							blenderMaterial.node_tree.nodes.active = blenderTexture
							textureRole = textures
							if 'Base_Tex_SRGB' in textureRole or 'Base_Tex_LIN' in textureRole:
								blenderTexture.location = Vector((-500, 560))
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], principled.inputs['Base Color'])
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], TRM_Subsurface.inputs['BSM Tex'])
								if 'pes3DDF_Hair' in blenderMaterial.fmdl_material_technique:
									blenderMaterial.node_tree.links.new(blenderTexture.outputs['Alpha'], principled.inputs['Alpha'])
							elif 'NormalMap_Tex_' in textureRole:
								blenderTexture.location = Vector((-500, -220))
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], NRM_Converter.inputs['NRM Tex'])
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Alpha'], NRM_Converter.inputs['Alpha'])
							elif 'SpecularMap_Tex_' in textureRole:
								blenderTexture.location = Vector((-500, 40))
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], SRM_Seperator.inputs['SRM Tex'])
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], SRM_Seperator.inputs['RGM Tex'])
							elif 'RoughnessMap_Tex_' in textureRole:
								blenderTexture.location = Vector((-750, 40))
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], SRM_Seperator.inputs['RGM Tex'])
							elif 'Translucent_Tex_' in textureRole:
								blenderTexture.location = Vector((-500, 300))
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], TRM_Subsurface.inputs['TRM Tex'])
							elif 'MetalnessMap_Tex_' in textureRole:
								blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], principled.inputs['Metallic'])
								blenderTexture.location = Vector((-750, 0))
							else:
								blenderTexture.location = Vector((rdmx, rdmy))

					for vector in foxshader:
						if vector.getAttribute("vector"):
							parameter = material.fmdl_material_parameters.add()
							parameter.name = vector.getAttribute("vector")
							parameter.parameters = [float(vector.getAttribute("xValue")),float(vector.getAttribute("yValue")), float(vector.getAttribute("zValue")), float(vector.getAttribute("wValue"))]
					domData.unlink()
					for nodes in blenderMaterial.node_tree.nodes:
						nodes.select = False
		
		self.report({"INFO"}, "Shader has been set!!")
	except Exception as msg:
		self.report({"WARNING"}, format(msg))
		return {'CANCELLED'}
	return 1