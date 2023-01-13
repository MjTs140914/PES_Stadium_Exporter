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

# Select multiple object hierarchy
def SelectableObj(child):
	bpy.ops.object.select_all(action='DESELECT')

	child.select_set(True)
	for ob in bpy.data.objects[child.name].children[:1]:
		ob.select_set(True)
		if ob is not None:
			for ob2 in bpy.data.objects[ob.name].children:
				if ob2 is not None and  ob2.type == "MESH":
					ob2.select_set(True)

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
							
def Settings(self,context,fox2xml):
	LimitedRotatable_ObjectLinks(self,context,fox2xml)
	idx=0

	# We need get fullname in xml before applied value and duplicate object
	model_transform_dict2 = xmlParser(fox2xml)
	for model in model_transform_dict2.keys():
		fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
		fmdl_name = os.path.splitext(fmdl_name)
		fmdl_name = str(fmdl_name[0]).split('/')[-1]
		objlist.append(fmdl_name)

	# Applied value to each object in xml and duplicate object length in xml
	for ob in bpy.data.objects[context.scene.part_info].children:
		if ob.type == "EMPTY":
			model_transform_dict = xmlParser(fox2xml)
			if ob.name in ObjectLinksList:
				ob.scrLimitedRotatable = True
				ob.EntityObjectLinks=_linksaddr[idx]
				ob.ObjectLinksName = _linksName[_linksBaseName[idx]]
				ob.packagePathHash = str(_packagePathHash_[idx])
				ob.maxRotDegreeLeft = int(_maxRotDegreeLeft[idx])
				ob.maxRotDegreeRight = int(_maxRotDegreeRight[idx])
				ob.maxRotSpeedLeft = int(_maxRotSpeedLeft[idx])
				ob.maxRotSpeedRight = int(_maxRotSpeedRight[idx])
				idx+=1
			for model in model_transform_dict.keys():
				model_name = model.find('staticProperties').findall('property')[0].find('value').text
				fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
				if ob.name in fmdl_name:
					transformEntityPtr = model.find('staticProperties').findall('property')[3].find('value').text
					_direction = model.find('staticProperties').findall('property')[18].find('value').text
					_kind = model.find('staticProperties').findall('property')[19].find('value').text
					_demoGroup = model.find('staticProperties').findall('property')[20].find('value').text
					transform = model_transform_dict[model]

					for property in transform.find('staticProperties').findall('property'):
						addr=property.find('value').text
						if addr is not None:
							ob.scrName = model_name
							ob.scrEntityPtr= addr
							ob.scrTransformEntity = transformEntityPtr
							ob.scrDirection = int(_direction)
							ob.scrKind = int(_kind)
							ob.scrDemoGroup = int(_demoGroup)

						property_val = property.find('value')
						transform_type=property.get('name')	
						if transform_type=='transform_rotation_quat':
							qx,qy,qz,qw= property_val.get('x'), property_val.get('y'), property_val.get('z'), property_val.get('w')
							if (qx,qy,qz,qw) is not None:
								ob.rotation_mode = "QUATERNION"
								ob.rotation_quaternion.w = float(qw)
								ob.rotation_quaternion.x = float(qx)
								ob.rotation_quaternion.y = float(qz)*-1
								ob.rotation_quaternion.z = float(qy)
						if transform_type=='transform_translation':
							tx,ty,tz,tw= property_val.get('x'), property_val.get('y'), property_val.get('z'), property_val.get('w')
							if (tx,ty,tz,tw) is not None:
								ob.location.x = float(tx)
								ob.location.y = float(tz)*-1
								ob.location.z = float(ty)

					# Actually need duplicate object by length-1 of object in xml, but this no (wee fix it in last loop) 
					SelectableObj(ob)
					bpy.ops.object.duplicate()
	
	del_obj(context)
	return 1

def del_obj(context):

	# In this case we delete last object duplicate, because we no need last object
	for ob in bpy.data.objects[context.scene.part_info].children:
		if ob.type == "EMPTY":
			if '.' in ob.name:
				_obname = str(ob.name).split('.')[0]
				obLen=objlist.count(_obname)
				if len(str(obLen)) == 1:
					_obLen='.00%s'%obLen
				elif len(str(obLen)) == 2:
					_obLen='.0%s'%obLen
				else:
					_obLen='.%s'%obLen
				if ob.name == _obname+_obLen:
					print('Delete duplicate last object: "%s%s"'%(_obname,_obLen))
					SelectableObj(ob)
					bpy.ops.object.delete()


