import bpy, os, PES_Stadium_Exporter
import xml.etree.ElementTree as ET
from Tools import PesFoxXML

staff_walk_list = ['gu_england2018A',
				'gu_england2018B',
				'st_flee2018A_non',
				'st_flee2018B_non',
]

result = None
objlist=[]

def del_obj(cldname):
	
	# In this case we delete last object duplicate, because we no need last object
	for ob in bpy.data.objects[cldname].children:
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

def importStaffWalk(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkfilename="%sstaff\\#Win\\staff_%s.fpk"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkfilename)
	basedir = os.path.dirname(fpkfilename)
	dirPath ="%s\\addons\\Tools\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
	for root, directories, filenames in os.walk(basedir):
		for fileName in filenames:
			filename, extension = os.path.splitext(fileName)
			if extension.lower() == '.fmdl':
				if filename in staff_walk_list:
					fmdlPath = os.path.join(root, fileName)
					filename = "walk_"+filename
					print('Importing ==> %s' % fileName)
					PES_Stadium_Exporter.importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename, dirPath, "Staff Walk")
	fpkdfilename="%sstaff\#Win\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkdfilename)
	basedird = os.path.dirname(fpkdfilename)
	fox2xmlName=str()
	for root, directories, filenames in os.walk(basedird):
		for fileName in filenames:
			filename, extension = os.path.splitext(fileName)
			if extension.lower() == '.fox2':
				if '_walk' in filename:
					fox2xmlName = os.path.join(root, fileName)

	PES_Stadium_Exporter.compileXML(fox2xmlName)
	Staff_Config(self,context,fox2xmlName+'.xml','Staff Walk')

def exportStaffWalk(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	iarraySize=0
	for ob in bpy.data.objects['Staff Walk'].children:
		if ob.type == "EMPTY":
			iarraySize+=1
	xmlpath='%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_walk.fox2.xml'%(exportPath,stid,stid,stid)
	PesFoxXML.Staff_Walk_xml(xmlpath,iarraySize)
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

def Staff_Config(self,context,fox2xml, cldname):

	# We need get fullname in xml before applied value and duplicate object
	model_transform_dict2 = xmlParser(fox2xml)
	for model in model_transform_dict2.keys():
		fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
		fmdl_name = os.path.splitext(fmdl_name)
		fmdl_name = "walk_"+str(fmdl_name[0]).split('/')[-1]
		objlist.append(fmdl_name)

	# Applied value to each object in xml and duplicate object length in xml
	for ob in bpy.data.objects[cldname].children:
		if ob.type == "EMPTY":
			model_transform_dict = xmlParser(fox2xml)

			for model in model_transform_dict.keys():
				model_name = model.find('staticProperties').findall('property')[0].find('value').text
				fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
				fmdl_name = os.path.splitext(fmdl_name)
				fmdl_name = "walk_"+str(fmdl_name[0]).split('/')[-1]
				if ob.name == fmdl_name:
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

	del_obj(cldname)

	return 1

def importBallboy(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkfilename="%sstaff\\#Win\\staff_%s.fpk"%(exportPath,stid)
	fpkdfilename="%sstaff\#Win\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkfilename)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkdfilename)
	dirPath ="%s\\addons\\Tools\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
	fox2="%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_ste_sit.fox2"%(exportPath,stid,stid,stid)
	PES_Stadium_Exporter.compileXML(fox2)
	xml="%s.xml"%fox2
	xmlTree = ET.parse(xml)
	fmdl_name,fmdlname=str(),str()
	FmdlList=[]
	for entities in xmlTree.findall('entities'):
		for entity in entities.findall('entity'):
			try:
				fmdl_name = entity.find('staticProperties').findall('property')[8].find('value').text
			except:
				pass
			if ".fmdl" in fmdl_name:
				fmdlname=os.path.basename(fmdl_name)
				fmdlPath="%sstaff\\#Win\\staff_%s_fpk\\Assets\\pes16\\model\\bg\\common\\staff\\common\\scenes\\%s"%(exportPath,stid,fmdlname)
				if fmdlPath not in FmdlList:
					FmdlList.append(fmdlPath)
	for fmdl in FmdlList:
		ballboyname = "ballboy_"+str(os.path.basename(fmdl)).split(".")[0]
		print('Importing ==> %s' % ballboyname)
		PES_Stadium_Exporter.importFmdlfile(fmdl, "Skeleton_%s" % ballboyname, ballboyname, ballboyname, dirPath, "Ballboy")	
	BallboyConfig(self,context,xml)
	return 1

ObjectLinksList=["ballboy_st_jersey_ch00_non",
				"ballboy_st_jersey_ch01_non",
				"ballboy_st_jersey_ch02_non",
				"ballboy_st_jersey_ch03_non",
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
	for ob in bpy.data.objects["Ballboy"].children:
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

def BallboyConfig(self,context,fox2xml):
	LimitedRotatable_ObjectLinks(self,context,fox2xml)
	idx=0

	# We need get fullname in xml before applied value and duplicate object
	model_transform_dict2 = xmlParser(fox2xml)
	for model in model_transform_dict2.keys():
		fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
		fmdl_name = os.path.splitext(fmdl_name)
		fmdl_name = "ballboy_"+str(fmdl_name[0]).split('/')[-1]
		objlist.append(fmdl_name)

	# Applied value to each object in xml and duplicate object length in xml
	for ob in bpy.data.objects["Ballboy"].children:
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
				fmdl_name = "ballboy_"+str(os.path.basename(fmdl_name)).split(".")[0]
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
	del_obj("Ballboy")
	return 1

def Ballboy_Assign(self,context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkd="%sstaff\\#Win\\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkd)
	fox2="%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_ste_sit.fox2"%(exportPath,stid,stid,stid)
	PES_Stadium_Exporter.compileXML(fox2)
	xml="%s.xml"%fox2
	isize=0
	lstObject, lstTotal,lstTotal2,lstTotal3=[],[],[],[]
	for ob in bpy.data.objects["Ballboy"].children:
		if ob.type == "EMPTY":
			if ob.scrLimitedRotatable:
				lstTotal.append(ob.ObjectLinksName)
				lstTotal2.append(ob.scrName)
				lstTotal3.append(ob.scrEntityPtr)
				if not ob.ObjectLinksName in lstObject:
					lstObject.append(ob.ObjectLinksName)
			isize+=1
	PesFoxXML.Ballboy_xml(xml,isize,lstTotal,lstTotal2,lstTotal3)
	PES_Stadium_Exporter.compileXML(xml)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkd+".xml")
	return 1



# CamCrew
	
def importCamCrew(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkfilename="%sstaff\\#Win\\staff_%s.fpk"%(exportPath,stid)
	fpkdfilename="%sstaff\#Win\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkfilename)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkdfilename)
	dirPath ="%s\\addons\\Tools\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
	fox2="%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_cam00.fox2"%(exportPath,stid,stid,stid)
	PES_Stadium_Exporter.compileXML(fox2)
	xml="%s.xml"%fox2
	xmlTree = ET.parse(xml)
	fmdl_name,fmdlname=str(),str()
	FmdlList=[]
	for entities in xmlTree.findall('entities'):
		for entity in entities.findall('entity'):
			try:
				fmdl_name = entity.find('staticProperties').findall('property')[8].find('value').text
			except:
				pass
			if ".fmdl" in fmdl_name:
				fmdlname=os.path.basename(fmdl_name)
				fmdlPath="%sstaff\\#Win\\staff_%s_fpk\\Assets\\pes16\\model\\bg\\common\\staff\\common\\scenes\\%s"%(exportPath,stid,fmdlname)
				if fmdlPath not in FmdlList:
					FmdlList.append(fmdlPath)
	for fmdl in FmdlList:
		fname = "camcrew_"+str(os.path.basename(fmdl)).split(".")[0]
		print('Importing ==> %s' % fname)
		PES_Stadium_Exporter.importFmdlfile(fmdl, "Skeleton_%s" % fname, fname, fname, dirPath, "Cameraman Crew")	
	CamCrewConfig(self,context,xml)
	return 1

CamCrewObjectLinksList=["camcrew_ca_blou2018_bibA_short",
						"camcrew_ca_blou2018_bibB_short",
						"camcrew_ca_flee_bibA_short",
						"camcrew_ca_flee_bibB_short",
						"camcrew_ca_parka2018_bibA_short",
						"camcrew_ca_parka2018_bibB_short",
]
# We need read any values and keys of LimitedRotatableObjectLinks
CamCrew_linksBaseName=[]
CamCrew_linksaddr=[]
CamCrew_linksName={}
CamCrew_packagePathHash_=[]
CamCrew_maxRotDegreeLeft,CamCrew_maxRotDegreeRight=[],[]
CamCrew_maxRotSpeedLeft,CamCrew_maxRotSpeedRight=[],[]
def CamCrewLimitedRotatable_ObjectLinks(self,context,fox2xml):
	xmlTree = ET.parse(fox2xml)
	for ob in bpy.data.objects["Cameraman Crew"].children:
		if ob.type == "EMPTY":
			for entities in xmlTree.findall('entities'):
				for entity in entities.findall('entity'):
					if entity.get('class') == 'LimitedRotatableObjectLinks':
						if ob.name in CamCrewObjectLinksList:
							CamCrew_modelName=entity.find('staticProperties').findall('property')[0].findtext('value')
							CamCrew_linksName_=entity.find('staticProperties').findall('property')[0].findtext('value')
							CamCrew_maxRotDegreeLeft.append(entity.find('staticProperties').findall('property')[3].findtext('value'))
							CamCrew_maxRotDegreeRight.append(entity.find('staticProperties').findall('property')[4].findtext('value'))
							CamCrew_maxRotSpeedLeft.append(entity.find('staticProperties').findall('property')[5].findtext('value'))
							CamCrew_maxRotSpeedRight.append(entity.find('staticProperties').findall('property')[6].findtext('value'))
							CamCrew_linksaddr.append(entity.get('addr'))
							
							for _property in entity.find('staticProperties').findall('property'):
								CamCrew_packagePathHash_type=_property.find('value')
								CamCrew_packagePathHash=CamCrew_packagePathHash_type.get('packagePathHash')
								if CamCrew_packagePathHash is not None:
									CamCrew_packagePathHash=CamCrew_packagePathHash_type.get('packagePathHash')
									CamCrew_packagePathHash_.append(CamCrew_packagePathHash)
							CamCrew_linksBaseName.append(CamCrew_modelName)
							CamCrew_linksName[CamCrew_modelName]=CamCrew_linksName_

def CamCrewConfig(self,context,fox2xml):
	CamCrewLimitedRotatable_ObjectLinks(self,context,fox2xml)
	idx=0

	# We need get fullname in xml before applied value and duplicate object
	model_transform_dict2 = xmlParser(fox2xml)
	for model in model_transform_dict2.keys():
		fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
		fmdl_name = os.path.splitext(fmdl_name)
		fmdl_name = "camcrew_"+str(fmdl_name[0]).split('/')[-1]
		objlist.append(fmdl_name)

	# Applied value to each object in xml and duplicate object length in xml
	for ob in bpy.data.objects["Cameraman Crew"].children:
		if ob.type == "EMPTY":
			model_transform_dict = xmlParser(fox2xml)
			if ob.name in CamCrewObjectLinksList:
				ob.scrLimitedRotatable = True
				ob.EntityObjectLinks=CamCrew_linksaddr[idx]
				ob.ObjectLinksName = CamCrew_linksName[CamCrew_linksBaseName[idx]]
				ob.packagePathHash = str(CamCrew_packagePathHash_[idx])
				ob.maxRotDegreeLeft = int(CamCrew_maxRotDegreeLeft[idx])
				ob.maxRotDegreeRight = int(CamCrew_maxRotDegreeRight[idx])
				ob.maxRotSpeedLeft = int(CamCrew_maxRotSpeedLeft[idx])
				ob.maxRotSpeedRight = int(CamCrew_maxRotSpeedRight[idx])
				idx+=1
			for model in model_transform_dict.keys():
				model_name = model.find('staticProperties').findall('property')[0].find('value').text
				fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
				fmdl_name = "camcrew_"+str(os.path.basename(fmdl_name)).split(".")[0]
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
	del_obj("Cameraman Crew")
	return 1

def CamCrew_Assign(self,context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkd="%sstaff\\#Win\\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkd)
	fox2="%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_cam00.fox2"%(exportPath,stid,stid,stid)
	PES_Stadium_Exporter.compileXML(fox2)
	xml="%s.xml"%fox2
	isize=0
	lstObject, lstTotal,lstTotal2,lstTotal3=[],[],[],[]
	for ob in bpy.data.objects["Cameraman Crew"].children:
		if ob.type == "EMPTY":
			if ob.scrLimitedRotatable:
				lstTotal.append(ob.ObjectLinksName)
				lstTotal2.append(ob.scrName)
				lstTotal3.append(ob.scrEntityPtr)
				if not ob.ObjectLinksName in lstObject:
					lstObject.append(ob.ObjectLinksName)
			isize+=1
	PesFoxXML.CamCrew_xml(xml,isize,lstTotal,lstTotal2,lstTotal3)
	PES_Stadium_Exporter.compileXML(xml)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkd+".xml")
	return 1


# Steward
	
def importSteward(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkfilename="%sstaff\\#Win\\staff_%s.fpk"%(exportPath,stid)
	fpkdfilename="%sstaff\#Win\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkfilename)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkdfilename)
	dirPath ="%s\\addons\\Tools\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
	fox2="%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_steward.fox2"%(exportPath,stid,stid,stid)
	PES_Stadium_Exporter.compileXML(fox2)
	xml="%s.xml"%fox2
	xmlTree = ET.parse(xml)
	fmdl_name,fmdlname=str(),str()
	FmdlList=[]
	for entities in xmlTree.findall('entities'):
		for entity in entities.findall('entity'):
			try:
				fmdl_name = entity.find('staticProperties').findall('property')[8].find('value').text
			except:
				pass
			if ".fmdl" in fmdl_name:
				fmdlname=os.path.basename(fmdl_name)
				fmdlPath="%sstaff\\#Win\\staff_%s_fpk\\Assets\\pes16\\model\\bg\\common\\staff\\common\\scenes\\%s"%(exportPath,stid,fmdlname)
				if fmdlPath not in FmdlList:
					FmdlList.append(fmdlPath)
	for fmdl in FmdlList:
		stname = "steward_"+str(os.path.basename(fmdl)).split(".")[0]
		print('Importing ==> %s' % stname)
		PES_Stadium_Exporter.importFmdlfile(fmdl, "Skeleton_%s" % stname, stname, stname, dirPath, "Steward")	
	StewardConfig(self,context,xml)
	return 1


def StewardConfig(self,context,fox2xml):
	idx=0

	# We need get fullname in xml before applied value and duplicate object
	model_transform_dict2 = xmlParser(fox2xml)
	for model in model_transform_dict2.keys():
		fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
		fmdl_name = os.path.splitext(fmdl_name)
		fmdl_name = "steward_"+str(fmdl_name[0]).split('/')[-1]
		objlist.append(fmdl_name)

	# Applied value to each object in xml and duplicate object length in xml
	for ob in bpy.data.objects["Steward"].children:
		if ob.type == "EMPTY":
			model_transform_dict = xmlParser(fox2xml)
			for model in model_transform_dict.keys():
				model_name = model.find('staticProperties').findall('property')[0].find('value').text
				fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
				fmdl_name = "steward_"+str(os.path.basename(fmdl_name)).split(".")[0]
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
	del_obj("Steward")
	return 1

def Steward_Assign(self,context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkd="%sstaff\\#Win\\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkd)
	fox2="%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_steward.fox2"%(exportPath,stid,stid,stid)
	PES_Stadium_Exporter.compileXML(fox2)
	xml="%s.xml"%fox2
	isize=0
	lstObject, lstTotal,lstTotal2,lstTotal3=[],[],[],[]
	for ob in bpy.data.objects["Steward"].children:
		if ob.type == "EMPTY":
			if ob.scrLimitedRotatable:
				lstTotal.append(ob.ObjectLinksName)
				lstTotal2.append(ob.scrName)
				lstTotal3.append(ob.scrEntityPtr)
				if not ob.ObjectLinksName in lstObject:
					lstObject.append(ob.ObjectLinksName)
			isize+=1
	PesFoxXML.Steward_xml(xml,isize,lstTotal,lstTotal2,lstTotal3)
	PES_Stadium_Exporter.compileXML(xml)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkd+".xml")
	return 1
