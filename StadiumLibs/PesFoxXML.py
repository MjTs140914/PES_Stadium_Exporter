import bpy, os, PES_Stadium_Exporter
import datetime
mydate = datetime.datetime.now()

#Create and generate XML contents by object stadium
cl=['\n\t<classes>'
	'\n\t\t<class name="Entity" super="" version="2" />'
	'\n\t\t<class name="Data" super="Entity" version="2" />'
	'\n\t\t<class name="DataSet" super="" version="0" />'
	'\n\t\t<class name="StadiumModel" super="" version="3" />'
	'\n\t\t<class name="EnlightenProbeSet" super="" version="0" />'
	'\n\t\t<class name="EnlightenSystemContainer" super="" version="0" />'
	'\n\t\t<class name="TransformEntity" super="" version="0" />'
	'\n\t\t<class name="ShearTransformEntity" super="" version="0" />'
	'\n\t\t<class name="PivotTransformEntity" super="" version="0" />'
  	'\n\t</classes>'
	'\n\t<entities>'
	'\n\t\t<entity class="DataSet" classVersion="0" addr="0x03172C40" unknown1="296" unknown2="0">'
	'\n\t\t\t<staticProperties>'
	'\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
	'\n\t\t\t\t\t<value hash="0xB8A0BF169F98" />'
	'\n\t\t\t\t</property>'
	'\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
	'\n\t\t\t\t\t<value>0x00000000</value>'
	'\n\t\t\t\t</property>'
  ]
lsRow=['\n\t\t\t</staticProperties>'
	  	'\n\t\t\t<dynamicProperties />'
		'\n\t\t</entity>'
]

foxroot=["\n\t</entities>"
		"\n</fox>"
]

def makeXMLForStadium(filename,dataList, arraySize, assetpath, shearTransformlist, pivotTransformlist, Stadium_Model,TransformEntityList,Stadium_Kinds,Stadium_Dir, enable_enlighten):
	StadiumModel=str()
	idx1,idx2,idx3=0,0,0
	stid= bpy.context.scene.STID
	with open(filename, "w", encoding="utf-8") as file:
		file.write('<?xml version="1.0" encoding="utf-8"?>')
		file.write('\n<fox formatVersion="2" fileVersion="0" originalVersion="{0}">'.format(mydate.strftime("%c")))
		for ls in cl:
			file.write(ls)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%s">'%arraySize)
		for dtlist in dataList:
			file.write('\n\t\t\t\t\t<value key="{0}">{1}</value>'.format(Stadium_Model[idx1],dtlist))
			idx1+=1
		if enable_enlighten:
			file.write('\n\t\t\t\t\t<value key="EnlightenProbeSet0000">0x00007200</value>')
			file.write('\n\t\t\t\t\t<value key="EnlightenSystemContainer0000">0x00007500</value>')
		file.write('\n\t\t\t\t</property>')
		for ls in lsRow:
			file.write(ls)
		if enable_enlighten:
			Enlighten=open(PES_Stadium_Exporter.xml_dir+'EnlightenSystem.xml','rt').read()
			Enlighten=Enlighten.replace("stid",stid)
			file.write(Enlighten)
		for dtlist in dataList:
			StadiumModel=open(PES_Stadium_Exporter.xml_dir+'StadiumModel.xml','rt').read()
			StadiumModel=StadiumModel.replace("DirName",Stadium_Model[idx2])
			StadiumModel=StadiumModel.replace("addrs",dtlist)
			StadiumModel=StadiumModel.replace("owners",dtlist)
			StadiumModel=StadiumModel.replace("assetpath",assetpath[idx2])
			StadiumModel=StadiumModel.replace("ShearTransAddr",shearTransformlist[idx2])
			StadiumModel=StadiumModel.replace("PivotTransAddr",pivotTransformlist[idx2])
			StadiumModel=StadiumModel.replace("TransformEntityListAddr",TransformEntityList[idx2])
			StadiumModel=StadiumModel.replace("kindValue","%s"%Stadium_Kinds[idx2])
			StadiumModel=StadiumModel.replace("DirValue","%s"%Stadium_Dir[idx2])
			file.write(StadiumModel)
			idx2+=1
		for shearTrans in shearTransformlist:
			shearTransform=open(PES_Stadium_Exporter.xml_dir+'StadiumEntity.xml','rt').read()
			shearTransform=shearTransform.replace("ShearTransAddr",shearTrans)
			shearTransform=shearTransform.replace("PivotTransAddr",pivotTransformlist[idx3])
			file.write(shearTransform)
			idx3+=1
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

def makeXMLForExtraStadium(filename,dataList, arraySize, assetpath, shearTransformlist, pivotTransformlist, Stadium_Model,TransformEntityList,Stadium_Kinds,Stadium_Dir):
	StadiumModel=str()
	idx1,idx2,idx3=0,0,0
	stid= bpy.context.scene.STID
	with open(filename, "w", encoding="utf-8") as file:
		file.write('<?xml version="1.0" encoding="utf-8"?>')
		file.write('\n<fox formatVersion="2" fileVersion="0" originalVersion="{0}">'.format(mydate.strftime("%c")))
		for ls in cl:
			file.write(ls)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%s">'%arraySize)
		for dtlist in dataList:
			file.write('\n\t\t\t\t\t<value key="{0}">{1}</value>'.format(Stadium_Model[idx1],dtlist))
			idx1+=1
		file.write('\n\t\t\t\t</property>')
		for ls in lsRow:
			file.write(ls)
		for dtlist in dataList:
			StadiumModel=open(PES_Stadium_Exporter.xml_dir+'StadiumModel.xml','rt').read()
			StadiumModel=StadiumModel.replace("DirName",Stadium_Model[idx2])
			StadiumModel=StadiumModel.replace("addrs",dtlist)
			StadiumModel=StadiumModel.replace("owners",dtlist)
			StadiumModel=StadiumModel.replace("assetpath",assetpath[idx2])
			StadiumModel=StadiumModel.replace("ShearTransAddr",shearTransformlist[idx2])
			StadiumModel=StadiumModel.replace("PivotTransAddr",pivotTransformlist[idx2])
			StadiumModel=StadiumModel.replace("TransformEntityListAddr",TransformEntityList[idx2])
			StadiumModel=StadiumModel.replace("kindValue","%s"%Stadium_Kinds[idx2])
			StadiumModel=StadiumModel.replace("DirValue","%s"%Stadium_Dir[idx2])
			file.write(StadiumModel)
			idx2+=1
		for shearTrans in shearTransformlist:
			shearTransform=open(PES_Stadium_Exporter.xml_dir+'StadiumEntity.xml','rt').read()
			shearTransform=shearTransform.replace("ShearTransAddr",shearTrans)
			shearTransform=shearTransform.replace("PivotTransAddr",pivotTransformlist[idx3])
			file.write(shearTransform)
			idx3+=1
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

	#Create and generate XML contents by object tv
cltv=[ 
	'\n\t<classes>'
	'\n\t\t<class name="Entity" super="" version="2" />'
	'\n\t\t<class name="Data" super="Entity" version="2" />'
	'\n\t\t<class name="DataSet" super="" version="0" />'
	'\n\t\t<class name="StadiumModel" super="" version="2" />'
	'\n\t\t<class name="TransformEntity" super="" version="0" />'
	'\n\t\t<class name="StadiumTexture" super="" version="1" />'
	'\n\t</classes>'
	'\n\t<entities>'
	'\n\t\t<entity class="DataSet" classVersion="0" addr="0x02D72D90" unknown1="296" unknown2="0">'
	'\n\t\t\t<staticProperties>'
	'\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
	'\n\t\t\t\t\t<value hash="0xB8A0BF169F98" />'
	'\n\t\t\t\t</property>'
	'\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
	'\n\t\t\t\t\t<value>0x00000000</value>'
	'\n\t\t\t\t</property>'
]

tvBox=[ 
		'\n\t\t<entity class="StadiumTexture" classVersion="1" addr="0x02D72EE0" unknown1="168" unknown2="0">'
		'\n\t\t\t<staticProperties>'
		'\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>StadiumTexture_box00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>0x02D72D90</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="textureAlias" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>TV_BOX00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="parameterNames" type="String" container="DynamicArray" arraySize="2">'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_1</value>'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_2</value>'
		'\n\t\t\t\t</property>'
 		'\n\t\t\t\t<property name="materialNames" type="String" container="DynamicArray" arraySize="1">'
		'\n\t\t\t\t\t<value>tv_large_c</value>'
		'\n\t\t\t\t</property>'
]

tvLine=[ 
		'\n\t\t<entity class="StadiumTexture" classVersion="1" addr="0xA84B0590" unknown1="168" unknown2="0">'
		'\n\t\t\t<staticProperties>'
		'\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>StadiumTexture_line00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>0x02D72D90</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="textureAlias" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>TV_LINE00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="parameterNames" type="String" container="DynamicArray" arraySize="2">'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_1</value>'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_2</value>'
		'\n\t\t\t\t</property>'
 		'\n\t\t\t\t<property name="materialNames" type="String" container="DynamicArray" arraySize="1">'
		'\n\t\t\t\t\t<value>tv_small_c</value>'
		'\n\t\t\t\t</property>'
]
tvdirection={'Front':0,
			'Back':1,
			'Left':2,
			'Right':3,
}
def makeXMLForTv(filename,TvMdl,arraySize,addrs,assetpath,TvBoxSize,TvLineSize):
	idx1,idx2,idx3=0,0,0
	with open(filename, "w", encoding="utf-8") as file:
		file.write('<?xml version="1.0" encoding="utf-8"?>')
		file.write('\n<fox formatVersion="2" fileVersion="0" originalVersion="{0}">'.format(mydate.strftime("%c")))

		for ls in cltv:
			file.write(ls)
			
		if "_Large" in str(TvMdl):
			arraySize+=1
		if "_Small" in str(TvMdl):
			arraySize+=1
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%s">'%arraySize)

		for mdl in TvMdl:
			file.write('\n\t\t\t\t\t<value key="{0}">{1}</value>'.format(mdl,addrs[idx1]))
			idx1+=1
		if "_Large" in str(TvMdl):
			file.write('\n\t\t\t\t\t<value key="StadiumTexture_box00">0x02D72EE0</value>')
		if "_Small" in str(TvMdl):
			file.write('\n\t\t\t\t\t<value key="StadiumTexture_line00">0xA84B0590</value>')

		file.write('\n\t\t\t\t</property>')
		for ls in lsRow:
			file.write(ls)

		for mdl in TvMdl:
			tvDir=tvdirection[mdl.split("_")[2]]
			Tv_Mdl=open(PES_Stadium_Exporter.xml_dir+'TvModel.xml','rt').read()
			Tv_Mdl=Tv_Mdl.replace("DirName",mdl)
			Tv_Mdl=Tv_Mdl.replace("addrs",addrs[idx2])
			Tv_Mdl=Tv_Mdl.replace("assetpath",assetpath[idx2])
			Tv_Mdl=Tv_Mdl.replace("%direction",str(tvDir))
			file.write(Tv_Mdl)
			idx2+=1
		if "_Large" in str(TvMdl):
			for tvBoxs in tvBox:
				file.write(tvBoxs)
			file.write('\n\t\t\t\t<property name="models" type="EntityPtr" container="DynamicArray" arraySize="%s">'%TvBoxSize)
		for addr in TvMdl:
			if "_Large" in addr:
				file.write('\n\t\t\t\t\t<value>%s</value>'%addrs[idx3])
				idx3+=1
		if "_Large" in str(TvMdl):
			file.write('\n\t\t\t\t</property>')
			for ls in lsRow:
				file.write(ls)

		if "_Small" in str(TvMdl):
			for tvLines in tvLine:
				file.write(tvLines)
			file.write('\n\t\t\t\t<property name="models" type="EntityPtr" container="DynamicArray" arraySize="%s">'%TvLineSize)

		for addr in TvMdl:
			if "_Small" in addr:
				file.write('\n\t\t\t\t\t<value>%s</value>'%addrs[idx3])
				idx3+=1
		if "_Small" in str(TvMdl):
			file.write('\n\t\t\t\t</property>')
			for ls in lsRow:
				file.write(ls)

		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

	#Create and generate effect XML contents by object light
Vignetting=['\n\t<setting type="Vignetting" index="0">'
			'\n\t\t<param id="texturePath" type="path" value="/Assets/pes16/model/bg/common/effect/texture/filter/filter.ftex" />'
			'\n\t\t<param id="alpha" type="uint" value="0x80" />'
  			'\n\t</setting>'
]
def lightFxXml(filename,sideName,L_Side):
	scn = bpy.context.scene
	idx1,idx2,idx3,idx4,idx5,idx6=0,0,0,0,0,0
	with open(filename, "w", encoding="utf-8") as file:
		file.write('<?xml version="1.0" encoding="UTF-8"?>')
		file.write('\n<effect version="2">')
		if scn.time_mode == "dr" or scn.time_mode == "nr":
			RainDemo=open(PES_Stadium_Exporter.xml_dir+'effect\\RainDemo.xml','rt').read()
			file.write(RainDemo)
		for sd in sideName:
			LightBillboard=open(PES_Stadium_Exporter.xml_dir+'effect\\LightBillboard.xml','rt').read()
			LightBillboard=LightBillboard.replace("iSize","%i"%idx1)
			LightBillboard=LightBillboard.replace("locstar",sd)
			LightBillboard=LightBillboard.replace("stid",scn.STID)
			LT = scn.l_fx_tex
			if LT in ['00','01','04']:
				LR = '30'
			else:
				LR = '45'
			LightBillboard=LightBillboard.replace("%LT",LT)
			LightBillboard=LightBillboard.replace("%LR",LR)
			file.write(LightBillboard)
			idx1+=1
		for LFlare in bpy.data.objects['LensFlare'].children:
			for L_ob in bpy.data.objects[LFlare.name].children:
				lx,ly,lz=L_ob.location.x,L_ob.location.y*-1,L_ob.location.z
				L_ob.rotation_mode = "QUATERNION"
				rw,rx,ry,rz=L_ob.rotation_quaternion.w,L_ob.rotation_quaternion.x*-1,L_ob.rotation_quaternion.y,L_ob.rotation_quaternion.z
				LensFlare=open(PES_Stadium_Exporter.xml_dir+'effect\\LensFlare.xml','rt').read()
				LensFlare=LensFlare.replace("%LSize","%i"%idx2)
				LensFlare=LensFlare.replace("%Ltex","%s"%scn.lensflaretex)
				LensFlare=LensFlare.replace("%tx","%f"%lx)
				LensFlare=LensFlare.replace("%ty","%f"%lz)
				LensFlare=LensFlare.replace("%tz","%f"%ly)
				LensFlare=LensFlare.replace("%qx","%f"%rx)
				LensFlare=LensFlare.replace("%qy","%f"%ry)
				LensFlare=LensFlare.replace("%qz","%f"%rz)
				LensFlare=LensFlare.replace("%qw","%f"%rw)
				file.write(LensFlare)
				idx2+=1
		for v in Vignetting:
			file.write(v)
		for Halo in bpy.data.objects['Halo'].children:
			for Halo_ob in bpy.data.objects[Halo.name].children:
				haloSide=str(Halo_ob.parent.name)
				lx,ly,lz=Halo_ob.location.x,Halo_ob.location.y*-1,Halo_ob.location.z
				Halo_ob.rotation_mode = "QUATERNION"
				tex=Halo_ob.HaloTex
				rw,rx,ry,rz=Halo_ob.rotation_quaternion.w,Halo_ob.rotation_quaternion.x,Halo_ob.rotation_quaternion.y*-1,Halo_ob.rotation_quaternion.z
				lSize,lSizeY=bpy.data.lights[Halo_ob.data.name].size,bpy.data.lights[Halo_ob.data.name].size_y
				HaloXml=open(PES_Stadium_Exporter.xml_dir+'effect\\Halo.xml','rt').read()
				HaloXml=HaloXml.replace("%hTex","%s"%tex)
				HaloXml=HaloXml.replace("%hSize","%i"%idx5)
				HaloXml=HaloXml.replace("%tx","%f"%lx)
				HaloXml=HaloXml.replace("%ty","%f"%lz)
				HaloXml=HaloXml.replace("%tz","%f"%ly)
				#Rotation of Halo
				HaloXml=HaloXml.replace("%qx","%f"%rx)
				HaloXml=HaloXml.replace("%qz","%f"%ry)
				HaloXml=HaloXml.replace("%qy","%f"%rz)
				HaloXml=HaloXml.replace("%qw","%f"%rw)
				#Size of Halo
				HaloXml=HaloXml.replace("%Sx","%f"%lSize)
				HaloXml=HaloXml.replace("%Sy","%f"%lSizeY)
				HaloXml=HaloXml.replace("%Sz","1.000000")
				#Fix Rot Y
				HaloXml=HaloXml.replace("%R","%u"%Halo_ob.rotY)
				#Pivot of Halo
				HaloXml=HaloXml.replace("%pvx","%f"%Halo_ob.Pivot.x)
				HaloXml=HaloXml.replace("%pvy","%f"%Halo_ob.Pivot.y)
				HaloXml=HaloXml.replace("%pvz","%f"%Halo_ob.Pivot.z)
				#Color of Halo
				colorOb=bpy.data.lights[Halo_ob.data.name].color
				HaloXml=HaloXml.replace("%cR","%f"%colorOb.r)
				HaloXml=HaloXml.replace("%cG","%f"%colorOb.g)
				HaloXml=HaloXml.replace("%cB","%f"%colorOb.b)
				file.write(HaloXml)
				idx5+=1
		if scn.time_mode == "dr" or scn.time_mode == "nr":
			file.write('\n\t<create type="MultiUvScrollScreen" setting="0" />')
			file.write('\n\t<create type="RainDemo" setting="0" />')
		for s in L_Side:
			file.write('\n\t<create type="LightBillboard" setting="%i" floor="upper" dir="%s" />'%(idx3,s))
			idx3+=1
		for LFlare in bpy.data.objects['LensFlare'].children:
			for L_ob in bpy.data.objects[LFlare.name].children:
				file.write('\n\t<create type="LensFlare" setting="%i" />'%idx4)
				idx4+=1
		file.write('\n\t<create type="Vignetting" setting="0" />')
		for Halo in bpy.data.objects['Halo'].children:
			for Halo_ob in bpy.data.objects[Halo.name].children:
				haloSide=str(Halo_ob.parent.name).split('_')[1]
				file.write('\n\t<create type="Halo" setting="%i" floor="upper" dir="%s" />'% (idx6,haloSide.lower()))
				idx6+=1
		file.write('\n</effect>')
		file.flush(),file.close()
	return 1

def cheerXML(filename,iSize,dataListKey,hexKey,mdltype,hexTfrm):
	idx1,idx2=0,0
	with open(filename, "w", encoding="utf-8") as file:
		classcheer=open(PES_Stadium_Exporter.xml_dir+'cheer\\class.xml','rt').read()
		file.write(classcheer)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%i">'%iSize)
		for kys in dataListKey:
			file.write('\n\t\t\t\t\t<value key="%s">%s</value>'%(kys,hexKey[idx1]))
			idx1+=1
		file.write('\n\t\t\t\t</property>')
		for ls in lsRow:
			file.write(ls)
		for kys in dataListKey:
			cheermdl=open(PES_Stadium_Exporter.xml_dir+'cheer\\cheerMdl.xml','rt').read()
			cheermdl=cheermdl.replace("addrs",hexKey[idx2])
			cheermdl=cheermdl.replace("mdldir",kys)
			cheermdl=cheermdl.replace("cheer_dirs",kys)
			cheermdl=cheermdl.replace("cheertype",mdltype)
			cheermdl=cheermdl.replace("hexTfrm",hexTfrm[idx2])
			file.write(cheermdl)
			idx2+=1
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

def scrMakeXml(filename,isize,lstTotal,lstTotal2,lstTotal3):
	stid=bpy.context.scene.STID
	isize+=2
	lstObject,lstObject2,lstObject3=[],[],[]
	idx,idx2=0,0
	with open(filename, "w", encoding="utf-8") as file:
		scrclass=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\class.xml','rt').read()
		file.write(scrclass)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%i">'%isize)
		for ob in bpy.data.objects["SCARECROW"].children:
			if ob.type == 'EMPTY' and ob is not None:
				file.write('\n\t\t\t\t\t<value key="%s">%s</value>'%(ob.scrName,ob.scrEntityPtr))
		for ob in bpy.data.objects["SCARECROW"].children:
			if ob.type == 'EMPTY' and ob is not None:
				if ob.scrLimitedRotatable:
					if not ob.ObjectLinksName in lstObject:
						lstObject.append(ob.ObjectLinksName)
						file.write('\n\t\t\t\t\t<value key="%s">%s</value>'%(ob.ObjectLinksName,ob.EntityObjectLinks))
		file.write('\n\t\t\t\t\t<value key="TexAlias_bsm00__StillCam_Bib">0x00020B00</value>')
		file.write('\n\t\t\t\t\t<value key="TexAlias_bsm03__TVCam_Bib">0x00020C00</value>')
		file.write('\n\t\t\t\t</property>')
		for ls in lsRow:
			file.write(ls)
		for ob in bpy.data.objects["SCARECROW"].children:
			if ob.type == 'EMPTY' and ob is not None:
				lx,ly,lz=ob.location.x,ob.location.y*-1,ob.location.z
				rw,rx,ry,rz=ob.rotation_quaternion.w,ob.rotation_quaternion.x,ob.rotation_quaternion.y*-1,ob.rotation_quaternion.z
				stModel=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\StadiumModel.xml','rt').read()
				if "_sc20" in ob.name:
					assets="/Assets/pes16/model/bg/%s/scarecrow/%s.fmdl"%(stid,ob.name)
				else:
					fmdlname = ob.name
					if "." in ob.name:
						fmdlname = str(ob.name).split(".")[0]
					assets="/Assets/pes16/model/bg/common/static_obj/%s.fmdl"%fmdlname

				stModel=stModel.replace("%name", ob.scrName)
				stModel=stModel.replace("%assetPath", assets)
				stModel=stModel.replace("%addr", ob.scrEntityPtr)
				stModel=stModel.replace("%transform", ob.scrTransformEntity)
				stModel=stModel.replace("%direction", str(ob.scrDirection))
				stModel=stModel.replace("%kind", str(ob.scrKind))
				stModel=stModel.replace("%demoGroup", str(ob.scrDemoGroup))

				ob.rotation_mode = "QUATERNION"
				stModel=stModel.replace("%qx", "%f"%rx)
				stModel=stModel.replace("%qy", "%f"%rz)
				stModel=stModel.replace("%qz", "%f"%ry)
				stModel=stModel.replace("%qw", "%f"%rw)


				stModel=stModel.replace("%tx", "%f"%lx)
				stModel=stModel.replace("%ty", "%f"%lz)
				stModel=stModel.replace("%tz", "%f"%ly)
				file.write(stModel)


		StadiumTexAlias=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\StadiumTexAlias.xml','rt').read()
		file.write(StadiumTexAlias)
		tr=0

		for ob in bpy.data.objects["SCARECROW"].children:
			if ob.type == 'EMPTY' and ob is not None:
				if ob.scrLimitedRotatable:
					if not ob.ObjectLinksName in lstObject2:
						lstObject2.append(ob.ObjectLinksName)
						ObjectLinks=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks.xml','rt').read()
						ObjectLinks=ObjectLinks.replace("%addr",ob.EntityObjectLinks)
						ObjectLinks=ObjectLinks.replace("%name",ob.ObjectLinksName)
						file.write(ObjectLinks)
						tr=1
					else:
						tr=0
					if ob.ObjectLinksName in lstObject2:
						idx = lstTotal.count(ob.ObjectLinksName)
					if tr==1:
						file.write('\n\t\t\t\t<property name="links" type="EntityLink" container="StringMap" arraySize="%i">'%idx)
					for ls in lstTotal2[:idx]:
						if tr==1:
							file.write('\n\t\t\t\t\t<value key="%s" packagePathHash="%s" archivePath="/Assets/pes16/model/bg/%s/scarecrow/%s_pes2020_00.fox2" nameInArchive="%s">%s</value>'
							%(lstTotal2[idx2],ob.packagePathHash,stid,stid,lstTotal2[idx2],lstTotal3[idx2]))	
							idx2+=1
					if not ob.ObjectLinksName in lstObject3:
						lstObject3.append(ob.ObjectLinksName)
						ObjectLinks2=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks2.xml','rt').read()
						ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeLeft","%i"%ob.maxRotDegreeLeft)
						ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeRight","%i"%ob.maxRotDegreeRight)
						ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedLeft","%i"%ob.maxRotSpeedLeft)
						ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedRight","%i"%ob.maxRotSpeedRight)
						file.write(ObjectLinks2)
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

ballboy_class="""<?xml version="1.0" encoding="utf-8"?>
<fox formatVersion="2" fileVersion="0" originalVersion="Fri Feb 05 20:33:05 UTC+07:00 2021">
	<classes>
		<class name="Entity" super="" version="2" />
		<class name="Data" super="Entity" version="2" />
		<class name="DataSet" super="" version="0" />
		<class name="StadiumAnime" super="" version="3" />
		<class name="StadiumModel" super="" version="3" />
		<class name="TransformEntity" super="" version="0" />
		<class name="LimitedRotatableObjectLinks" super="" version="0" />
	</classes>
	<entities>
		<entity class="DataSet" classVersion="0" addr="0x00000100" unknown1="296" unknown2="0">
			<staticProperties>
				<property name="name" type="String" container="StaticArray" arraySize="1">
					<value hash="0xB8A0BF169F98" />
				</property>
				<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">
					<value>0x00000000</value>
				</property>"""
ballboy_entity_close="""
				</property>
			</staticProperties>
			<dynamicProperties />
		</entity>"""

def Ballboy_xml(filename,isize,lstTotal,lstTotal2,lstTotal3):
	stid=bpy.context.scene.STID
	isize+=5
	lstObject,lstObject2,lstObject3=[],[],[]
	idx,idx2=0,0
	with open(filename, "w", encoding="utf-8") as file:
		file.write(ballboy_class)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%i">'%isize)
		file.write('\n\t\t\t\t\t<value key="anm_idole_sit_ballboy_A">0x00000200</value>')
		file.write('\n\t\t\t\t\t<value key="anm_idole_sit_ballboy_B">0x00000F00</value>')
		file.write('\n\t\t\t\t\t<value key="anm_idole_sitA">0x00001C00</value>')
		file.write('\n\t\t\t\t\t<value key="anm_idole_sitB">0x00004100</value>')
		
		for ob in bpy.data.objects["Ballboy"].children:
			if ob.type == "EMPTY":
				keys=ob.name
				if '.' in keys:
					keys=str(ob.name).split('.')[0]
				file.write('\n\t\t\t\t\t<value key="%s">%s</value>'%(ob.scrName,ob.scrEntityPtr))
		file.write('\n\t\t\t\t\t<value key="LimitedRotatableObjectLinks_ballboy">0x00006300</value>')
		file.write(ballboy_entity_close)
		ballboy_anime=open(PES_Stadium_Exporter.xml_dir+'staff\\ballboy\\ballboy_anime.xml','rt').read()
		file.write(ballboy_anime)
		for ob in bpy.data.objects['Ballboy'].children:
			if ob.type == "EMPTY":
				lx,ly,lz=ob.location.x,ob.location.y*-1,ob.location.z
				rw,rx,ry,rz=ob.rotation_quaternion.w,ob.rotation_quaternion.x,ob.rotation_quaternion.y*-1,ob.rotation_quaternion.z
				obname = ob.name
				if '.' in obname:
					obname=str(obname).split('.')[0]
				obname=obname.replace("ballboy_","")
				walkModel=open(PES_Stadium_Exporter.xml_dir+'staff\\walkModel.xml','rt').read()
				walkModel=walkModel.replace('%obj','%s'%obname)
				walkModel=walkModel.replace('%name','%s'%ob.scrName)
				walkModel=walkModel.replace('%addr','%s'%ob.scrEntityPtr)
				walkModel=walkModel.replace('%transform','%s'%ob.scrTransformEntity)
				walkModel=walkModel.replace("%direction", str(ob.scrDirection))
				walkModel=walkModel.replace("%kind", str(ob.scrKind))
				walkModel=walkModel.replace("%demoGroup", str(ob.scrDemoGroup))

				ob.rotation_mode = "QUATERNION"
				walkModel=walkModel.replace("%qx", "%f"%rx)
				walkModel=walkModel.replace("%qy", "%f"%rz)
				walkModel=walkModel.replace("%qz", "%f"%ry)
				walkModel=walkModel.replace("%qw", "%f"%rw)


				walkModel=walkModel.replace("%tx", "%f"%lx)
				walkModel=walkModel.replace("%ty", "%f"%lz)
				walkModel=walkModel.replace("%tz", "%f"%ly)
				file.write(walkModel)
				for ob in bpy.data.objects["Ballboy"].children:
					if ob.type == 'EMPTY' and ob is not None:
						if ob.scrLimitedRotatable:
							if not ob.ObjectLinksName in lstObject2:
								lstObject2.append(ob.ObjectLinksName)
								ObjectLinks=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks.xml','rt').read()
								ObjectLinks=ObjectLinks.replace("%addr",ob.EntityObjectLinks)
								ObjectLinks=ObjectLinks.replace("%name",ob.ObjectLinksName)
								file.write(ObjectLinks)
								tr=1
							else:
								tr=0
							if ob.ObjectLinksName in lstObject2:
								idx = lstTotal.count(ob.ObjectLinksName)
							if tr==1:
								file.write('\n\t\t\t\t<property name="links" type="EntityLink" container="StringMap" arraySize="%i">'%idx)
							for ls in lstTotal2[:idx]:
								if tr==1:
									file.write('\n\t\t\t\t\t<value key="%s" packagePathHash="%s" archivePath="/Assets/pes16/model/bg/%s/staff/%s_2018_common_ste_sit.fox2" nameInArchive="%s">%s</value>'
									%(lstTotal2[idx2],ob.packagePathHash,stid,stid,lstTotal2[idx2],lstTotal3[idx2]))	
									idx2+=1
							if not ob.ObjectLinksName in lstObject3:
								lstObject3.append(ob.ObjectLinksName)
								ObjectLinks2=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks2.xml','rt').read()
								ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeLeft","%i"%ob.maxRotDegreeLeft)
								ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeRight","%i"%ob.maxRotDegreeRight)
								ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedLeft","%i"%ob.maxRotSpeedLeft)
								ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedRight","%i"%ob.maxRotSpeedRight)
								file.write(ObjectLinks2)
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

foxClass='''<?xml version="1.0" encoding="utf-8"?>
<fox formatVersion="2" fileVersion="0" originalVersion="Thu Jan 28 19:13:40 UTC+07:00 2021">
  <classes>
	<class name="Entity" super="" version="2" />
	<class name="Data" super="Entity" version="2" />
	<class name="DataSet" super="" version="0" />
	<class name="StadiumAnime" super="" version="3" />
	<class name="StadiumModel" super="" version="3" />
	<class name="TransformEntity" super="" version="0" />
  </classes>
  <entities>
	<entity class="DataSet" classVersion="0" addr="0xB39B6B50" unknown1="296" unknown2="0">
	  <staticProperties>
		<property name="name" type="String" container="StaticArray" arraySize="1">
		  <value hash="0xB8A0BF169F98" />
		</property>
		<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">
		  <value>0x00000000</value>
		</property>'''
entityClose='''
			</property>
		</staticProperties>
		<dynamicProperties />
	</entity>'''

def Staff_Walk_xml(filename,iarraySize):
	iarraySize2=iarraySize
	iarraySize+=1
	with open(filename, "w", encoding="utf-8") as file:
		file.write(foxClass)
		file.write('\n\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%i">'%iarraySize)
		file.write('\n\t\t\t<value key="ani_walk">0xB39B6C90</value>')
		for ob in bpy.data.objects['Staff Walk'].children:
			if ob.type == "EMPTY":
				file.write('\n\t\t\t<value key="%s">%s</value>'%(ob.scrName,ob.scrEntityPtr))
		file.write(entityClose)
		StadiumAnime=open(PES_Stadium_Exporter.xml_dir+'staff\\StadiumAnime.xml','rt').read()
		file.write(StadiumAnime)
		file.write('\n\t\t\t<property name="models" type="EntityPtr" container="DynamicArray" arraySize="%i">'%iarraySize2)
		for ob in bpy.data.objects['Staff Walk'].children:
			if ob.type == "EMPTY":
				file.write('\n\t\t\t\t<value>%s</value>'%ob.scrEntityPtr)
		file.write(entityClose)
		for ob in bpy.data.objects['Staff Walk'].children:
			if ob.type == "EMPTY":
				lx,ly,lz=ob.location.x,ob.location.y*-1,ob.location.z
				rw,rx,ry,rz=ob.rotation_quaternion.w,ob.rotation_quaternion.x,ob.rotation_quaternion.y*-1,ob.rotation_quaternion.z
				obname = ob.name
				if '.' in obname:
					obname=str(obname).split('.')[0]
				obname=obname.replace("walk_","")
				walkModel=open(PES_Stadium_Exporter.xml_dir+'staff\\walkModel.xml','rt').read()
				walkModel=walkModel.replace('%obj','%s'%obname)
				walkModel=walkModel.replace('%name','%s'%ob.scrName)
				walkModel=walkModel.replace('%addr','%s'%ob.scrEntityPtr)
				walkModel=walkModel.replace('%transform','%s'%ob.scrTransformEntity)
				walkModel=walkModel.replace("%direction", str(ob.scrDirection))
				walkModel=walkModel.replace("%kind", str(ob.scrKind))
				walkModel=walkModel.replace("%demoGroup", str(ob.scrDemoGroup))

				ob.rotation_mode = "QUATERNION"
				walkModel=walkModel.replace("%qx", "%f"%rx)
				walkModel=walkModel.replace("%qy", "%f"%rz)
				walkModel=walkModel.replace("%qz", "%f"%ry)
				walkModel=walkModel.replace("%qw", "%f"%rw)


				walkModel=walkModel.replace("%tx", "%f"%lx)
				walkModel=walkModel.replace("%ty", "%f"%lz)
				walkModel=walkModel.replace("%tz", "%f"%ly)
				file.write(walkModel)
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

xmlcamcrewclass='''<?xml version="1.0" encoding="utf-8"?>
<fox formatVersion="2" fileVersion="0" originalVersion="Tue Oct 11 23:17:01 UTC+07:00 2022">
  <classes>
    <class name="Entity" super="" version="2" />
    <class name="Data" super="Entity" version="2" />
    <class name="DataSet" super="" version="0" />
    <class name="StadiumAnime" super="" version="3" />
    <class name="StadiumModel" super="" version="3" />
    <class name="TransformEntity" super="" version="0" />
    <class name="LimitedRotatableObjectLinks" super="" version="0" />
    <class name="StadiumTexture" super="" version="1" />
  </classes>
  <entities>
    <entity class="DataSet" classVersion="0" addr="0x00000100" unknown1="296" unknown2="0">
      <staticProperties>
        <property name="name" type="String" container="StaticArray" arraySize="1">
          <value hash="0xB8A0BF169F98" />
        </property>
        <property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">
          <value>0x00000000</value>
        </property>'''


camcrew_entity_close="""
				</property>
			</staticProperties>
			<dynamicProperties />
		</entity>"""

def CamCrew_xml(filename,isize,lstTotal,lstTotal2,lstTotal3):
	stid=bpy.context.scene.STID
	isize+=3
	lstObject,lstObject2,lstObject3=[],[],[]
	idx,idx2=0,0
	with open(filename, "w", encoding="utf-8") as file:
		file.write(xmlcamcrewclass)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%i">'%isize)
		file.write('\n\t\t\t\t\t<value key="ani_cam00">0x00000200</value>')
		
		for ob in bpy.data.objects["Cameraman Crew"].children:
			if ob.type == "EMPTY":
				keys=ob.name
				if '.' in keys:
					keys=str(ob.name).split('.')[0]
				file.write('\n\t\t\t\t\t<value key="%s">%s</value>'%(ob.scrName,ob.scrEntityPtr))
		file.write('\n\t\t\t\t\t<value key="Limited_steal_cam_staffA_slow">0x00003900</value>')
		file.write('\n\t\t\t\t\t<value key="StadiumTexAlias_bsm00_StillBib">0x00003A00</value>')
		file.write(camcrew_entity_close)
		camcrew_anime=open(PES_Stadium_Exporter.xml_dir+'staff\\CamCrew\\StadiumAnime.xml','rt').read()
		file.write(camcrew_anime)
		for ob in bpy.data.objects['Cameraman Crew'].children:
			if ob.type == "EMPTY":
				lx,ly,lz=ob.location.x,ob.location.y*-1,ob.location.z
				rw,rx,ry,rz=ob.rotation_quaternion.w,ob.rotation_quaternion.x,ob.rotation_quaternion.y*-1,ob.rotation_quaternion.z
				obname = ob.name
				if '.' in obname:
					obname=str(obname).split('.')[0]
				obname=obname.replace("camcrew_","")
				walkModel=open(PES_Stadium_Exporter.xml_dir+'staff\\walkModel.xml','rt').read()
				walkModel=walkModel.replace('%obj','%s'%obname)
				walkModel=walkModel.replace('%name','%s'%ob.scrName)
				walkModel=walkModel.replace('%addr','%s'%ob.scrEntityPtr)
				walkModel=walkModel.replace('%transform','%s'%ob.scrTransformEntity)
				walkModel=walkModel.replace("%direction", str(ob.scrDirection))
				walkModel=walkModel.replace("%kind", str(ob.scrKind))
				walkModel=walkModel.replace("%demoGroup", str(ob.scrDemoGroup))

				ob.rotation_mode = "QUATERNION"
				walkModel=walkModel.replace("%qx", "%f"%rx)
				walkModel=walkModel.replace("%qy", "%f"%rz)
				walkModel=walkModel.replace("%qz", "%f"%ry)
				walkModel=walkModel.replace("%qw", "%f"%rw)


				walkModel=walkModel.replace("%tx", "%f"%lx)
				walkModel=walkModel.replace("%ty", "%f"%lz)
				walkModel=walkModel.replace("%tz", "%f"%ly)
				file.write(walkModel)
				for ob in bpy.data.objects["Cameraman Crew"].children:
					if ob.type == 'EMPTY' and ob is not None:
						if ob.scrLimitedRotatable:
							if not ob.ObjectLinksName in lstObject2:
								lstObject2.append(ob.ObjectLinksName)
								ObjectLinks=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks.xml','rt').read()
								ObjectLinks=ObjectLinks.replace("%addr",ob.EntityObjectLinks)
								ObjectLinks=ObjectLinks.replace("%name",ob.ObjectLinksName)
								file.write(ObjectLinks)
								tr=1
							else:
								tr=0
							if ob.ObjectLinksName in lstObject2:
								idx = lstTotal.count(ob.ObjectLinksName)
							if tr==1:
								file.write('\n\t\t\t\t<property name="links" type="EntityLink" container="StringMap" arraySize="%i">'%idx)
							for ls in lstTotal2[:idx]:
								if tr==1:
									file.write('\n\t\t\t\t\t<value key="%s" packagePathHash="%s" archivePath="/Assets/pes16/model/bg/%s/staff/%s_2018_common_cam00.fox2" nameInArchive="%s">%s</value>'
									%(lstTotal2[idx2],ob.packagePathHash,stid,stid,lstTotal2[idx2],lstTotal3[idx2]))	
									idx2+=1
							if not ob.ObjectLinksName in lstObject3:
								lstObject3.append(ob.ObjectLinksName)
								ObjectLinks2=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks2.xml','rt').read()
								ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeLeft","%i"%ob.maxRotDegreeLeft)
								ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeRight","%i"%ob.maxRotDegreeRight)
								ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedLeft","%i"%ob.maxRotSpeedLeft)
								ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedRight","%i"%ob.maxRotSpeedRight)
								file.write(ObjectLinks2)
		camcrew_StadiumTexture=open(PES_Stadium_Exporter.xml_dir+'staff\\CamCrew\\StadiumTexture.xml','rt').read()
		file.write(camcrew_StadiumTexture)
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

xmlSteward='''<?xml version="1.0" encoding="utf-8"?>
<fox formatVersion="2" fileVersion="0" originalVersion="Thu Oct 13 22:06:51 UTC+07:00 2022">
  <classes>
    <class name="Entity" super="" version="2" />
    <class name="Data" super="Entity" version="2" />
    <class name="DataSet" super="" version="0" />
    <class name="StadiumAnime" super="" version="3" />
    <class name="StadiumModel" super="" version="3" />
    <class name="TransformEntity" super="" version="0" />
  </classes>
  <entities>
    <entity class="DataSet" classVersion="0" addr="0xCBC2B8D0" unknown1="296" unknown2="0">
      <staticProperties>
        <property name="name" type="String" container="StaticArray" arraySize="1">
          <value hash="0xB8A0BF169F98" />
        </property>
        <property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">
          <value>0x00000000</value>
        </property>'''


Steward_entity_close="""
				</property>
			</staticProperties>
			<dynamicProperties />
		</entity>"""

def Steward_xml(filename,isize,lstTotal,lstTotal2,lstTotal3):
	stid=bpy.context.scene.STID
	isize+=2
	lstObject,lstObject2,lstObject3=[],[],[]
	idx,idx2=0,0
	with open(filename, "w", encoding="utf-8") as file:
		file.write(xmlSteward)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%i">'%isize)
		file.write('\n\t\t\t\t\t<value key="anm_idole_standA">0xCBC2BA10</value>')
		file.write('\n\t\t\t\t\t<value key="anm_idole_standB">0xCBC2BB50</value>')
		
		for ob in bpy.data.objects["Steward"].children:
			if ob.type == "EMPTY":
				keys=ob.name
				if '.' in keys:
					keys=str(ob.name).split('.')[0]
				file.write('\n\t\t\t\t\t<value key="%s">%s</value>'%(ob.scrName,ob.scrEntityPtr))
		file.write(Steward_entity_close)
		Steward_animeA=open(PES_Stadium_Exporter.xml_dir+'staff\\Steward\\StadiumAnimeA.xml','rt').read()
		file.write(Steward_animeA)
		animeSizeA = 0
		for ob in bpy.data.objects["Steward"].children:
			if ob.type == "EMPTY":
				if '2018A' in ob.name:
					animeSizeA += 1
				if '2018C' in ob.name:
					animeSizeA += 1
				if 'bibA' in ob.name:
					animeSizeA += 1
		file.write('\n\t\t\t\t<property name="models" type="EntityPtr" container="DynamicArray" arraySize="%i">'%animeSizeA)
		for ob in bpy.data.objects["Steward"].children:
			if ob.type == "EMPTY":
				if '2018A' in ob.name:
					file.write('\n\t\t\t\t\t<value>%s</value>' %ob.scrEntityPtr)
				if '2018C' in ob.name:
					file.write('\n\t\t\t\t\t<value>%s</value>' %ob.scrEntityPtr)
				if 'bibA' in ob.name:
					file.write('\n\t\t\t\t\t<value>%s</value>' %ob.scrEntityPtr)
		file.write(Steward_entity_close)
		Steward_animeB=open(PES_Stadium_Exporter.xml_dir+'staff\\Steward\\StadiumAnimeB.xml','rt').read()
		file.write(Steward_animeB)
		animeSizeB = 0
		for ob in bpy.data.objects["Steward"].children:
			if ob.type == "EMPTY":
				if '2018B' in ob.name:
					animeSizeB += 1
				if 'bibB' in ob.name:
					animeSizeB += 1
		file.write('\n\t\t\t\t<property name="models" type="EntityPtr" container="DynamicArray" arraySize="%i">'%animeSizeB)
		for ob in bpy.data.objects["Steward"].children:
			if ob.type == "EMPTY":
				if '2018B' in ob.name:
					file.write('\n\t\t\t\t\t<value>%s</value>' %ob.scrEntityPtr)
				if 'bibB' in ob.name:
					file.write('\n\t\t\t\t\t<value>%s</value>' %ob.scrEntityPtr)
		file.write(Steward_entity_close)
		for ob in bpy.data.objects['Steward'].children:
			if ob.type == "EMPTY":
				lx,ly,lz=ob.location.x,ob.location.y*-1,ob.location.z
				rw,rx,ry,rz=ob.rotation_quaternion.w,ob.rotation_quaternion.x,ob.rotation_quaternion.y*-1,ob.rotation_quaternion.z
				obname = ob.name
				if '.' in obname:
					obname=str(obname).split('.')[0]
				obname=obname.replace("steward_","")
				walkModel=open(PES_Stadium_Exporter.xml_dir+'staff\\walkModel.xml','rt').read()
				walkModel=walkModel.replace('%obj','%s'%obname)
				walkModel=walkModel.replace('%name','%s'%ob.scrName)
				walkModel=walkModel.replace('%addr','%s'%ob.scrEntityPtr)
				walkModel=walkModel.replace('%transform','%s'%ob.scrTransformEntity)
				walkModel=walkModel.replace("%direction", str(ob.scrDirection))
				walkModel=walkModel.replace("%kind", str(ob.scrKind))
				walkModel=walkModel.replace("%demoGroup", str(ob.scrDemoGroup))

				ob.rotation_mode = "QUATERNION"
				walkModel=walkModel.replace("%qx", "%f"%rx)
				walkModel=walkModel.replace("%qy", "%f"%rz)
				walkModel=walkModel.replace("%qz", "%f"%ry)
				walkModel=walkModel.replace("%qw", "%f"%rw)


				walkModel=walkModel.replace("%tx", "%f"%lx)
				walkModel=walkModel.replace("%ty", "%f"%lz)
				walkModel=walkModel.replace("%tz", "%f"%ly)
				file.write(walkModel)
				for ob in bpy.data.objects["Steward"].children:
					if ob.type == 'EMPTY' and ob is not None:
						if ob.scrLimitedRotatable:
							if not ob.ObjectLinksName in lstObject2:
								lstObject2.append(ob.ObjectLinksName)
								ObjectLinks=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks.xml','rt').read()
								ObjectLinks=ObjectLinks.replace("%addr",ob.EntityObjectLinks)
								ObjectLinks=ObjectLinks.replace("%name",ob.ObjectLinksName)
								file.write(ObjectLinks)
								tr=1
							else:
								tr=0
							if ob.ObjectLinksName in lstObject2:
								idx = lstTotal.count(ob.ObjectLinksName)
							if tr==1:
								file.write('\n\t\t\t\t<property name="links" type="EntityLink" container="StringMap" arraySize="%i">'%idx)
							for ls in lstTotal2[:idx]:
								if tr==1:
									file.write('\n\t\t\t\t\t<value key="%s" packagePathHash="%s" archivePath="/Assets/pes16/model/bg/%s/staff/%s_2018_common_steward.fox2" nameInArchive="%s">%s</value>'
									%(lstTotal2[idx2],ob.packagePathHash,stid,stid,lstTotal2[idx2],lstTotal3[idx2]))	
									idx2+=1
							if not ob.ObjectLinksName in lstObject3:
								lstObject3.append(ob.ObjectLinksName)
								ObjectLinks2=open(PES_Stadium_Exporter.xml_dir+'scarecrow\\LimitedRotatableObjectLinks2.xml','rt').read()
								ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeLeft","%i"%ob.maxRotDegreeLeft)
								ObjectLinks2=ObjectLinks2.replace("%maxRotDegreeRight","%i"%ob.maxRotDegreeRight)
								ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedLeft","%i"%ob.maxRotSpeedLeft)
								ObjectLinks2=ObjectLinks2.replace("%maxRotSpeedRight","%i"%ob.maxRotSpeedRight)
								file.write(ObjectLinks2)
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1