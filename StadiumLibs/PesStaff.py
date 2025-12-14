import bpy, os, PES_Stadium_Exporter
import xml.etree.ElementTree as ET
from StadiumLibs import PesFoxXML

staff_walk_list = ['gu_england2018A',
				'gu_england2018B',
				'st_flee2018A_non',
				'st_flee2018B_non',
]

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



result = None
objlist=[]

def importStaffWalk(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkfilename="%sstaff\\#Win\\staff_%s.fpk"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkfilename)
	basedir = os.path.dirname(fpkfilename)
	dirPath ="%s\\addons\\StadiumLibs\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
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

def Staff_Config(self, context, fox2xml, cldname):

    model_transform_dict = xmlParser(fox2xml)

    # Build xml map (per object name)
    xml_map = {}
    for model in model_transform_dict.keys():
        props = model.find('staticProperties').findall('property')
        fmdl_path = props[8].find('value').text
        fmdl_name = "walk_" + os.path.splitext(fmdl_path)[0].split('/')[-1]

        if fmdl_name not in xml_map:
            xml_map[fmdl_name] = []
        xml_map[fmdl_name].append(model)

    # Process objects
    for ob in bpy.data.objects[cldname].children:

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

        for i in range(1, xml_count):

            dup_name = f"{base_name}.{i:03}"
            new_ob = duplicate_hierarchy(ob, dup_name)

            model = xml_list[i]
            transform = model_transform_dict[model]
            apply_xml(new_ob, model, transform)

    return 1


def importBallboy(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkfilename="%sstaff\\#Win\\staff_%s.fpk"%(exportPath,stid)
	fpkdfilename="%sstaff\#Win\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkfilename)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkdfilename)
	dirPath ="%s\\addons\\StadiumLibs\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
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

def BallboyConfig(self, context, fox2xml):

    # collect LimitedRotatableObjectLinks
    LimitedRotatable_ObjectLinks(self, context, fox2xml)

    model_transform_dict = xmlParser(fox2xml)
    idx = 0

    xml_map = {}
    for model in model_transform_dict.keys():

        props = model.find('staticProperties').findall('property')
        fp = props[8].find('value').text

        base_name = os.path.splitext(os.path.basename(fp))[0]
        fmdl_name = "ballboy_" + base_name

        xml_map.setdefault(fmdl_name, []).append(model)

    for ob in bpy.data.objects["Ballboy"].children:

        if ob.type != "EMPTY":
            continue

        base = ob.name
        if base not in xml_map:
            continue

        xml_list = xml_map[base]

        if base in ObjectLinksList:
            ob.scrLimitedRotatable = True
            ob.EntityObjectLinks = _linksaddr[idx]
            ob.ObjectLinksName   = _linksName[_linksBaseName[idx]]
            ob.packagePathHash   = str(_packagePathHash_[idx])
            ob.maxRotDegreeLeft  = int(_maxRotDegreeLeft[idx])
            ob.maxRotDegreeRight = int(_maxRotDegreeRight[idx])
            ob.maxRotSpeedLeft   = int(_maxRotSpeedLeft[idx])
            ob.maxRotSpeedRight  = int(_maxRotSpeedRight[idx])
            idx += 1

        model0 = xml_list[0]
        transform0 = model_transform_dict[model0]
        apply_xml(ob, model0, transform0)

        for i in range(1, len(xml_list)):

            dup_name = f"{base}.{i:03}"

            new_ob = duplicate_hierarchy(ob, dup_name)

            model = xml_list[i]
            transform = model_transform_dict[model]
            apply_xml(new_ob, model, transform)

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
	dirPath ="%s\\addons\\StadiumLibs\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
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

def CamCrewConfig(self, context, fox2xml):

    CamCrewLimitedRotatable_ObjectLinks(self, context, fox2xml)
    model_transform_dict = xmlParser(fox2xml)
    idx = 0

    xml_map = {}
    for model in model_transform_dict.keys():

        props = model.find('staticProperties').findall('property')
        fmdl_path = props[8].find('value').text

        fmdl_name = "camcrew_" + os.path.splitext(os.path.basename(fmdl_path))[0]

        if fmdl_name not in xml_map:
            xml_map[fmdl_name] = []

        xml_map[fmdl_name].append(model)

    for ob in bpy.data.objects["Cameraman Crew"].children:

        if ob.type != "EMPTY":
            continue

        base_name = ob.name
        if base_name not in xml_map:
            continue

        xml_list = xml_map[base_name]

        if base_name in CamCrewObjectLinksList:
            ob.scrLimitedRotatable = True
            ob.EntityObjectLinks = CamCrew_linksaddr[idx]
            ob.ObjectLinksName   = CamCrew_linksName[CamCrew_linksBaseName[idx]]
            ob.packagePathHash   = str(CamCrew_packagePathHash_[idx])
            ob.maxRotDegreeLeft  = int(CamCrew_maxRotDegreeLeft[idx])
            ob.maxRotDegreeRight = int(CamCrew_maxRotDegreeRight[idx])
            ob.maxRotSpeedLeft   = int(CamCrew_maxRotSpeedLeft[idx])
            ob.maxRotSpeedRight  = int(CamCrew_maxRotSpeedRight[idx])
            idx += 1

        base_model = xml_list[0]
        base_transform = model_transform_dict[base_model]
        apply_xml(ob, base_model, base_transform)

        for i in range(1, len(xml_list)):

            dup_name = f"{base_name}.{i:03}"
            new_ob = duplicate_hierarchy(ob, dup_name)
            model = xml_list[i]
            transform = model_transform_dict[model]
            apply_xml(new_ob, model, transform)

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
	dirPath ="%s\\addons\\StadiumLibs\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
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


def StewardConfig(self, context, fox2xml):

    model_transform_dict = xmlParser(fox2xml)

    xml_map = {}
    for model in model_transform_dict.keys():

        props = model.find('staticProperties').findall('property')

        fmdl_path = props[8].find('value').text
        fmdl_name = "steward_" + os.path.splitext(fmdl_path)[0].split('/')[-1]

        if fmdl_name not in xml_map:
            xml_map[fmdl_name] = []
        xml_map[fmdl_name].append(model)

    for ob in bpy.data.objects["Steward"].children:

        if ob.type != "EMPTY":
            continue

        base_name = ob.name
        if base_name not in xml_map:
            continue

        xml_list = xml_map[base_name]

        base_model = xml_list[0]
        base_transform = model_transform_dict[base_model]
        apply_xml(ob, base_model, base_transform)

        for i in range(1, len(xml_list)):

            dup_name = f"{base_name}.{i:03}"

            new_ob = duplicate_hierarchy(ob, dup_name)

            model = xml_list[i]
            transform = model_transform_dict[model]
            apply_xml(new_ob, model, transform)

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
