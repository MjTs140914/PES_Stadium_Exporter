import bpy, os
import xml.etree.ElementTree as ET

# in this case we need asset path for object static so we create list for thats
scrAsset=["/Assets/pes16/model/bg/common/static_obj/so_cam_blou_bib_a.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_cam_blou_bib_b.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_cam_coat_bib_a.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_cam_coat_bib_b.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_cam_coat_bib_c.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_cam_parka_bib_a.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_cam_parka_bib_b.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_chair_b.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Lsize_A2018_base.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Lsize_A2018_head.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Lsize_B2018_base.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Lsize_B2018_head.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Msize_A_base.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Msize_A_head.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Msize_B_base.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Msize_B_head.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Msize_C_base.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_Msize_C_head.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_crew_a.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_crew_b.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_crew_c.fmdl",
		"/Assets/pes16/model/bg/common/static_obj/so_tvcam_crew_d.fmdl",
]

result = None
objlist=[]


# Parsing xml dictionary this script created by themex, full credits for him
def xmlParser(filename):
	modelName_addr_dict = {}
	model_transform_dict = {}

	xmlTree = ET.parse(filename)

	for entities in xmlTree.findall('entities'):
		for entity in entities.findall('entity'):
			if entity.get('class') == 'StadiumModel':
				modelName_addr_dict[entity.get('addr')] = entity
			if entity.get('class') == 'TransformEntity':
				for prop in entity.find('staticProperties').findall('property'):
					if prop.get('name') == 'owner':
						model_addr = prop.find('value').text
						model_transform_dict[modelName_addr_dict[model_addr]] = entity

	return model_transform_dict
	
# This list is only object have LimitedRotatableObjectLinks
ObjectLinksList=["so_cam_blou_bib_a","so_cam_blou_bib_b","so_cam_coat_bib_a",
				"so_cam_coat_bib_b","so_cam_coat_bib_c","so_cam_parka_bib_a",
				"so_cam_parka_bib_b","so_tvcam_Lsize_A2018_head", "so_tvcam_Lsize_B2018_head",
				"so_tvcam_Msize_A_head", "so_tvcam_Msize_B_head","so_tvcam_Msize_C_head"
]

# We need read any values and keys of LimitedRotatableObjectLinks
_linksBaseName=[]
_linksaddr=[]
_linksName={}
_packagePathHash_=[]
_maxRotDegreeLeft,_maxRotDegreeRight=[],[]
_maxRotSpeedLeft,_maxRotSpeedRight=[],[]
def LimitedRotatable_ObjectLinks(self,context,fox2xml):
	xmlTree = ET.parse(fox2xml)
	for ob in bpy.data.objects[context.scene.part_info].children:
		if ob.type == "EMPTY":
			for entities in xmlTree.findall('entities'):
				for entity in entities.findall('entity'):
					if entity.get('class') == 'LimitedRotatableObjectLinks':
						if ob.name in ObjectLinksList:
							_modelName=entity.find('staticProperties').findall('property')[0].findtext('value')
							_linksName_=entity.find('staticProperties').findall('property')[0].findtext('value')
							_maxRotDegreeLeft.append(entity.find('staticProperties').findall('property')[3].findtext('value'))
							_maxRotDegreeRight.append(entity.find('staticProperties').findall('property')[4].findtext('value'))
							_maxRotSpeedLeft.append(entity.find('staticProperties').findall('property')[5].findtext('value'))
							_maxRotSpeedRight.append(entity.find('staticProperties').findall('property')[6].findtext('value'))
							_linksaddr.append(entity.get('addr'))
							
							for _property in entity.find('staticProperties').findall('property'):
								_packagePathHash_type=_property.find('value')
								_packagePathHash=_packagePathHash_type.get('packagePathHash')
								if _packagePathHash is not None:
									_packagePathHash=_packagePathHash_type.get('packagePathHash')
									_packagePathHash_.append(_packagePathHash)
							_linksBaseName.append(_modelName)
							_linksName[_modelName]=_linksName_


def duplicate_hierarchy(original_root, new_name):

	new_root = original_root.copy()
	bpy.context.collection.objects.link(new_root)
	new_root.name = new_name

	for child in original_root.children:
		new_child = child.copy()

		if child.type == "MESH":
			new_child.data = child.data.copy()

		bpy.context.collection.objects.link(new_child)
		new_child.parent = new_root
		new_child.matrix_parent_inverse = new_root.matrix_world.inverted()

		for subc in child.children:
			new_sub = subc.copy()
			if subc.type == "MESH":
				new_sub.data = subc.data.copy()

			bpy.context.collection.objects.link(new_sub)
			new_sub.parent = new_child
			new_sub.matrix_parent_inverse = new_child.matrix_world.inverted()

	return new_root


def apply_xml(ob, model, transform):

	props = model.find('staticProperties').findall('property')

	ob.scrName = props[0].find('value').text
	ob.scrTransformEntity = props[3].find('value').text
	ob.scrDirection = int(props[18].find('value').text)
	ob.scrKind      = int(props[19].find('value').text)
	ob.scrDemoGroup = int(props[20].find('value').text)

	for p in transform.find('staticProperties').findall('property'):
		addr = p.find('value').text
		if addr:
			ob.scrEntityPtr = addr

		v = p.find('value')
		t = p.get('name')

		if t == 'transform_rotation_quat':
			qx, qy, qz, qw = v.get('x'), v.get('y'), v.get('z'), v.get('w')
			if None not in (qx, qy, qz, qw):
				ob.rotation_mode = "QUATERNION"
				ob.rotation_quaternion.w = float(qw)
				ob.rotation_quaternion.x = float(qx)
				ob.rotation_quaternion.y = float(qz) * -1
				ob.rotation_quaternion.z = float(qy)

		if t == 'transform_translation':
			tx, ty, tz, tw = v.get('x'), v.get('y'), v.get('z'), v.get('w')
			if None not in (tx,ty,tz,tw):
				ob.location.x = float(tx)
				ob.location.y = float(tz) * -1
				ob.location.z = float(ty)



def Settings(self, context, fox2xml):

	LimitedRotatable_ObjectLinks(self, context, fox2xml)
	idx = 0

	model_transform_dict = xmlParser(fox2xml)

	xml_map = {}
	for model in model_transform_dict.keys():
		props = model.find('staticProperties').findall('property')
		fmdl_path = props[8].find('value').text
		fmdl_name = os.path.splitext(fmdl_path)[0].split('/')[-1]

		if fmdl_name not in xml_map:
			xml_map[fmdl_name] = []
		xml_map[fmdl_name].append(model)

	for ob in bpy.data.objects[context.scene.part_info].children:

		if ob.type != "EMPTY":
			continue

		base_name = ob.name
		if base_name not in xml_map:
			continue

		xml_list = xml_map[base_name]
		xml_count = len(xml_list)

		base_model = xml_list[0]
		base_transform = model_transform_dict[base_model]
		apply_xml(ob, base_model, base_transform)


		# LimitedRotatable
		if base_name in ObjectLinksList:
			ob.scrLimitedRotatable = True
			ob.EntityObjectLinks = _linksaddr[idx]
			ob.ObjectLinksName  = _linksName[_linksBaseName[idx]]
			ob.packagePathHash  = str(_packagePathHash_[idx])
			ob.maxRotDegreeLeft  = int(_maxRotDegreeLeft[idx])
			ob.maxRotDegreeRight = int(_maxRotDegreeRight[idx])
			ob.maxRotSpeedLeft   = int(_maxRotSpeedLeft[idx])
			ob.maxRotSpeedRight  = int(_maxRotSpeedRight[idx])
			idx += 1

		for i in range(1, xml_count):

			dup_name = f"{base_name}.{i:03}"
			new_ob = duplicate_hierarchy(ob, dup_name)

			model = xml_list[i]
			transform = model_transform_dict[model]
			apply_xml(new_ob, model, transform)

	return 1

