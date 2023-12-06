#
# MIT License

# Copyright (c) 2021 MjTs-140914

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# '''
# Thanks to the following people who have contributed to this project:

#     leus
#     MjTs140914
#     the4chancup
#     Atvaark
#     Suat Cadgas/sxsxsx
#     themex
#     zlac
# '''

import bpy, os, bpy.utils.previews, bpy_extras, shutil, bmesh, re, math
from struct import pack,unpack
from bpy.props import (EnumProperty, CollectionProperty, IntProperty, StringProperty, BoolProperty, FloatProperty, FloatVectorProperty)
from Tools import FmdlFile, Ftex, IO, PesFoxShader, PesFoxXML, PesEnlighten, PesScarecrow, PesStaff
from xml.dom import minidom
from mathutils import Vector
from re import search

bl_info = {
	"name": "PES Stadium Exporter",
	"description": "eFootbal PES2021 PES Stadium Exporter",
	"author": "MjTs-140914 || the4chancup",
	"version": (0, 7, 1),
	"blender": (2, 90, 0),
	"location": "Under Scene Tab",
	# "warning": "This addon is still in development.",
	"wiki_url": "https://github.com/MjTs140914/PES_Stadium_Exporter/wiki",
	"tracker_url": "https://github.com/MjTs140914/PES_Stadium_Exporter/issues",
	"category": "System" 
}

(major, minor, build) = bpy.app.version
icons_collections = {}
version="v0.7.1b"

AddonsPath = str()
AddonsPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
base_file_blend = '%s\\addons\\Tools\\Gzs\\base_file.blend' % AddonsPath
texconvTools = '"%s\\addons\\Tools\\Gzs\\texconv.exe"' % AddonsPath 
FtexTools ='"%s\\addons\\Tools\\Gzs\\FtexTools.exe"' % AddonsPath 
GZSPATH = '"%s\\addons\\Tools\\Gzs\\GzsTool.exe"' % AddonsPath 
foxTools = '"%s\\addons\\Tools\\Gzs\\FoxTool\\FoxTool.exe"' % AddonsPath 
icons_dir = '%s\\addons\\Tools\\Gzs\\icons' % AddonsPath
xml_dir = '%s\\addons\\Tools\\Gzs\\xml\\' % AddonsPath
lightFxPath = '%s\\addons\\Tools\\Gzs\\' % AddonsPath
baseStartupFile = '%s\\addons\\Tools\\Gzs\\startup.blend' % AddonsPath
startupFile = '%sconfig\\startup.blend'%AddonsPath[:-7]
EnlightenPath="%s\\addons\\Tools\\Gzs\\EnlightenOutput\\" % AddonsPath 
commonfile = "%s\\addons\\Tools\\Gzs\\xml\\scarecrow\\common" % AddonsPath 
csvPath = "%s\\addons\\Tools\\Gzs\\xml\\Path.csv" % AddonsPath 

ob_id = None
group_list=["MAIN", "TV", "AUDIAREA", "FLAGAREA", "STAFF", "SCARECROW", "PITCH2021", "CHEER1", "CHEER2", "LIGHTS", "AD", "EXTRA"]

parent_main_list=["MESH_back1","MESH_back2","MESH_back3",
				 "MESH_center1","MESH_center2","MESH_center3",
				 "MESH_front1", "MESH_front2","MESH_front3",
				 "MESH_left1","MESH_left2","MESH_left3",
				 "MESH_right1","MESH_right2","MESH_right3",
				 "MESH_Pitch","MESH_front1_demo","MESH_front1_game",
				 "MESH_center1_snow","MESH_center1_rain","MESH_center1_tifo",			 
				 "MESH_ad_acl","MESH_ad_cl","MESH_ad_el","MESH_ad_normal",			 
				 "MESH_ad_olc","MESH_ad_sc",
				 "MESH_cheer_back1_h_a1","MESH_cheer_front1_h_a1", "MESH_cheer_left1_h_a1", "MESH_cheer_right1_h_a1",
				 "MESH_cheer_back1_h_a2","MESH_cheer_front1_h_a2", "MESH_cheer_left1_h_a2", "MESH_cheer_right1_h_a2",
				 "MESH_back1_df","MESH_back2_df","MESH_back3_df",
				 "MESH_center1_df","MESH_center2_df","MESH_center3_df",
				 "MESH_front1_df", "MESH_front2_df","MESH_front3_df",
				 "MESH_left1_df","MESH_left2_df","MESH_left3_df",
				 "MESH_right1_df","MESH_right2_df","MESH_right3_df",
				 "MESH_back1_dr","MESH_back2_dr","MESH_back3_dr",
				 "MESH_center1_dr","MESH_center2_dr","MESH_center3_dr",
				 "MESH_front1_dr", "MESH_front2_dr","MESH_front3_dr",
				 "MESH_left1_dr","MESH_left2_dr","MESH_left3_dr",
				 "MESH_right1_dr","MESH_right2_dr","MESH_right3_dr",
				 "MESH_back1_nf","MESH_back2_nf","MESH_back3_nf",
				 "MESH_center1_nf","MESH_center2_nf","MESH_center3_nf",
				 "MESH_front1_nf", "MESH_front2_nf","MESH_front3_nf",
				 "MESH_left1_nf","MESH_left2_nf","MESH_left3_nf",
				 "MESH_right1_nf","MESH_right2_nf","MESH_right3_nf",
				 "MESH_back1_nr","MESH_back2_nr","MESH_back3_nr",
				 "MESH_center1_nr","MESH_center2_nr","MESH_center3_nr",
				 "MESH_front1_nr", "MESH_front2_nr","MESH_front3_nr",
				 "MESH_left1_nr","MESH_left2_nr","MESH_left3_nr",
				 "MESH_right1_nr","MESH_right2_nr","MESH_right3_nr",
]

main_list=["back1","back2","back3",
			"center1","center2","center3",
			"front1", "front2","front3",
			"left1","left2","left3",
			"right1","right2","right3",
			"front1_demo","front1_game","center1_snow","center1_rain","center1_tifo",
			"MESH_CROWD","MESH_FLAGAREA","Pitch",
			"TV_Large_Left","TV_Large_Right","TV_Large_Front","TV_Large_Back",
			"TV_Small_Left","TV_Small_Right","TV_Small_Front","TV_Small_Back",
			"L_FRONT","L_RIGHT","L_LEFT","L_BACK",
			"H_FRONT","H_RIGHT","H_LEFT","H_BACK",
			"F_FRONT","F_RIGHT","F_LEFT","F_BACK",
			"ad_acl","ad_cl","ad_el","ad_normal", 
			"ad_olc","ad_sc", "LightBillboard", "LensFlare", "Halo",
			"cheer_back1_h_a1","cheer_front1_h_a1", "cheer_left1_h_a1", "cheer_right1_h_a1",
			"cheer_back1_h_a2","cheer_front1_h_a2", "cheer_left1_h_a2", "cheer_right1_h_a2",
			"Staff Coach","Steward", "Staff Walk","Ballboy","Cameraman Crew",
			"back1_df","back2_df","back3_df",
			"center1_df","center2_df","center3_df",
			"front1_df","front2_df","front3_df",
			"left1_df","left2_df","left3_df",
			"right1_df","right2_df","right3_df",
			"back1_dr","back2_dr","back3_dr",
			"center1_dr","center2_dr","center3_dr",
			"front1_dr","front2_dr","front3_dr",
			"left1_dr","left2_dr","left3_dr",
			"right1_dr","right2_dr","right3_dr",
			"back1_nf","back2_nf","back3_nf",
			"center1_nf","center2_nf","center3_nf",
			"front1_nf","front2_nf","front3_nf",
			"left1_nf","left2_nf","left3_nf",
			"right1_nf","right2_nf","right3_nf",
			"back1_nr","back2_nr","back3_nr",
			"center1_nr","center2_nr","center3_nr",
			"front1_nr","front2_nr","front3_nr",
			"left1_nr","left2_nr","left3_nr",
			"right1_nr","right2_nr","right3_nr",
]

part_export=[("MAIN","MAIN","MAIN"),
			("EXTRA","EXTRA","EXTRA"),
			("SCARECROW","SCARECROW","SCARECROW"),
			("TV","TV","TV"),
			("PITCH2021","PITCH2021","PITCH2021"),
			("STAFF","STAFF","STAFF"),
			("CHEER1","CHEER1","CHEER1"),
			("CHEER2","CHEER2","CHEER2"),
			("FLAGAREA","FLAGAREA","FLAGAREA"),
			("AUDIAREA","AUDIAREA","AUDIAREA"),
			("LIGHTS","LIGHTS","LIGHTS"),
			("AD","AD","AD"),
]

crowd_part=['C_front1','C_front2','C_front3',
		"C_back1","C_back2","C_back3",
		"C_left1","C_left2","C_left3",
		"C_right1","C_right2","C_right3"
]

crowd_side={0: 'C_front',
			1: 'C_back',
			2: 'C_left',
			3: 'C_right',
}

flags_part=['F_front1','F_front2','F_front3',
		"F_back1","F_back2","F_back3",
		"F_left1","F_left2","F_left3",
		"F_right1","F_right2","F_right3"
]

crowd_part_type=[0x00010000,0x00010100,0x00010200,
				0x00010001,0x00010101,0x00010201,
				0x00010002,0x00010102,0x00010202,
				0x00010003,0x00010103,0x00010203
]

tvdatalist=[0x02D72E00,0x02D730A0,0x02D73340,
			0x02D73650,0x02D73490,0x02D72D20,
			0x02D72FC0,0x02D73260,0x02D73570,
			0x02D73810,
]

light_sidelist=[]

timeMode=[("df","DAY FINE","DAY FINE"),
		("dr","DAY RAINY","DAY RAINY"),
		("nf","NIGHT FINE","NIGHT FINE"),
		("nr","NIGHT RAINY","NIGHT RAINY")
]

parent_list=[('MESH_back1','MESH_back1','MESH_back1'),
		   ('MESH_back2','MESH_back2','MESH_back2'),
		   ('MESH_back3','MESH_back3','MESH_back3'),
		   ('MESH_center1','MESH_center1','MESH_center1'),
		   ('MESH_center2','MESH_center2','MESH_center2'),
		   ('MESH_center3','MESH_center3','MESH_center3'),
		   ('MESH_front1','MESH_front1','MESH_front1'),
		   ('MESH_front2','MESH_front2','MESH_front2'),
		   ('MESH_front3','MESH_front3','MESH_front3'),
		   ('MESH_left1','MESH_left1','MESH_left1'),
		   ('MESH_left2','MESH_left2','MESH_left2'),
		   ('MESH_left3','MESH_left3','MESH_left3'),
		   ('MESH_right1','MESH_right1','MESH_right1'),
		   ('MESH_right2','MESH_right2','MESH_right2'),
		   ('MESH_right3','MESH_right3','MESH_right3'),
		   ('MESH_CROWD','MESH_CROWD','MESH_CROWD'),
		   ('MESH_PITCH','MESH_PITCH','MESH_PITCH'),
		   ('MESH_TV','MESH_TV','MESH_TV')
]

datalist=["back1","back2","back3",
			"center1","center2","center3",
			"front1","front2","front3",
			"left1","left2","left3",
			"right1","right2","right3",
			"center1_snow", "center1_rain", "center1_tifo",
			"front1_game","front1_demo"
]


StadiumModel=["StadiumModel_B1","StadiumModel_B2","StadiumModel_B3",
			"StadiumModel_C1","StadiumModel_C2","StadiumModel_C3",
			"StadiumModel_F1","StadiumModel_F2","StadiumModel_F3",
			"StadiumModel_L1","StadiumModel_L2","StadiumModel_L3",
			"StadiumModel_R1","StadiumModel_R2","StadiumModel_R3",
			"StadiumModel_C1_ForSnow", "StadiumModel_C1_rain", "StadiumModel_C1_tifo",
			"StadiumModel_F1_game","StadiumModel_F1_demo",
]

StadiumKind=[0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,0,2,
			14,15
]
StadiumDir=[1,1,1,
			4,4,0,
			0,0,0,
			2,2,2,
			3,3,3,
			4,4,0,
			4,4
]

transformlist=[0x02D72C40,0x02D72D20,0x02D72E00,
				0x02D72EE0,0x02D72FC0,0x02D730A0,
				0x02D73180,0x02D73260,0x02D73340,
				0x02D73420,0x02D73570,0x02D73650,
				0x02D73730,0x02D73810,0x02D73490,
				0xC11921D0,0x03173880,0x031738E4, 
				0x03173E30,0x03173FF0,
]

TransformEntity=[0x03172D20,0x03172EE0,0x03172EE2,
				0x031730A0,0x031730A2,0x03173260,
				0x03173420,0x03173650,0x03173750,
				0x03173810,0x03173960,0x03173970,
				0x03173B20,0x03173CE0,0x03173CE5,
				0xC12714B0,0xC12714B2,0x03173B3A,
				0x03173EA0,0x03174060,
]

shearTransform=[0x03173F10,0x03173D50,0x03173D60,
				0x03173B90,0x03173B95,0x031739D0,
				0x031732CB,0x031732D0,0x031732D2,
				0x03172D90,0x03172F50,0x03172F52,
				0x03174140,0x03173180,0x03173182,
				0x00000000,0xB13C0250,0x03173D90,
				0x03173490,0x031736C0,
]

pivotTransform=[0x03173F80,0x03173DC0,0x03173DC2,
				0x03173C00,0x03173C01,0x03173A40,
				0x031738F0,0x03173340,0x03173342,
				0x03172E00,0x03172FC0,0x03172FC2,
				0x03173110,0x03174290,0x03174292,
				0x00000000,0x00000000,0x03173FE6,
				0x03173570,0x03173730,
]

cheerhexKey=[0x00000200,0x00000400,0x00000600,0x00000800
]

cheerhextfrm=[0x00000300,0x00000500,0x00000700,0x00000900
]

#ExtraStadium
StadiumModel2=["StadiumModel_B1","StadiumModel_B2","StadiumModel_B3",
			"StadiumModel_C1","StadiumModel_C2","StadiumModel_C3",
			"StadiumModel_F1","StadiumModel_F2","StadiumModel_F3",
			"StadiumModel_L1","StadiumModel_L2","StadiumModel_L3",
			"StadiumModel_R1","StadiumModel_R2","StadiumModel_R3",
			"StadiumModel_B1","StadiumModel_B2","StadiumModel_B3",
			"StadiumModel_C1","StadiumModel_C2","StadiumModel_C3",
			"StadiumModel_F1","StadiumModel_F2","StadiumModel_F3",
			"StadiumModel_L1","StadiumModel_L2","StadiumModel_L3",
			"StadiumModel_R1","StadiumModel_R2","StadiumModel_R3",
			"StadiumModel_B1","StadiumModel_B2","StadiumModel_B3",
			"StadiumModel_C1","StadiumModel_C2","StadiumModel_C3",
			"StadiumModel_F1","StadiumModel_F2","StadiumModel_F3",
			"StadiumModel_L1","StadiumModel_L2","StadiumModel_L3",
			"StadiumModel_R1","StadiumModel_R2","StadiumModel_R3",
			"StadiumModel_B1","StadiumModel_B2","StadiumModel_B3",
			"StadiumModel_C1","StadiumModel_C2","StadiumModel_C3",
			"StadiumModel_F1","StadiumModel_F2","StadiumModel_F3",
			"StadiumModel_L1","StadiumModel_L2","StadiumModel_L3",
			"StadiumModel_R1","StadiumModel_R2","StadiumModel_R3",
]
datalist2=["back1_df","back2_df","back3_df",
			"center1_df","center2_df","center3_df",
			"front1_df","front2_df","front3_df",
			"left1_df","left2_df","left3_df",
			"right1_df","right2_df","right3_df",
			"back1_dr","back2_dr","back3_dr",
			"center1_dr","center2_dr","center3_dr",
			"front1_dr","front2_dr","front3_dr",
			"left1_dr","left2_dr","left3_dr",
			"right1_dr","right2_dr","right3_dr",
			"back1_nf","back2_nf","back3_nf",
			"center1_nf","center2_nf","center3_nf",
			"front1_nf","front2_nf","front3_nf",
			"left1_nf","left2_nf","left3_nf",
			"right1_nf","right2_nf","right3_nf",
			"back1_nr","back2_nr","back3_nr",
			"center1_nr","center2_nr","center3_nr",
			"front1_nr","front2_nr","front3_nr",
			"left1_nr","left2_nr","left3_nr",
			"right1_nr","right2_nr","right3_nr",
]

StadiumKind2=[0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
			0,1,2,
]
StadiumDir2=[1,1,1,
			4,4,0,
			0,0,0,
			2,2,2,
			3,3,3,
			1,1,1,
			4,4,0,
			0,0,0,
			2,2,2,
			3,3,3,
			1,1,1,
			4,4,0,
			0,0,0,
			2,2,2,
			3,3,3,
			1,1,1,
			4,4,0,
			0,0,0,
			2,2,2,
			3,3,3,
]

transformlist2=[0x02D72C40,0x02D72D20,0x02D72E00,
				0x02D72EE0,0x02D72FC0,0x02D730A0,
				0x02D73180,0x02D73260,0x02D73340,
				0x02D73420,0x02D73570,0x02D73650,
				0x02D73730,0x02D73810,0x02D73490,
				0x02D72C40,0x02D72D20,0x02D72E00,
				0x02D72EE0,0x02D72FC0,0x02D730A0,
				0x02D73180,0x02D73260,0x02D73340,
				0x02D73420,0x02D73570,0x02D73650,
				0x02D73730,0x02D73810,0x02D73490,
				0x02D72C40,0x02D72D20,0x02D72E00,
				0x02D72EE0,0x02D72FC0,0x02D730A0,
				0x02D73180,0x02D73260,0x02D73340,
				0x02D73420,0x02D73570,0x02D73650,
				0x02D73730,0x02D73810,0x02D73490,
				0x02D72C40,0x02D72D20,0x02D72E00,
				0x02D72EE0,0x02D72FC0,0x02D730A0,
				0x02D73180,0x02D73260,0x02D73340,
				0x02D73420,0x02D73570,0x02D73650,
				0x02D73730,0x02D73810,0x02D73490,
]

TransformEntity2=[0x03172D20,0x03172EE0,0x03172EE2,
				0x031730A0,0x031730A2,0x03173260,
				0x03173420,0x03173650,0x03173750,
				0x03173810,0x03173960,0x03173970,
				0x03173B20,0x03173CE0,0x03173CE5,
				0x03172D20,0x03172EE0,0x03172EE2,
				0x031730A0,0x031730A2,0x03173260,
				0x03173420,0x03173650,0x03173750,
				0x03173810,0x03173960,0x03173970,
				0x03173B20,0x03173CE0,0x03173CE5,
				0x03172D20,0x03172EE0,0x03172EE2,
				0x031730A0,0x031730A2,0x03173260,
				0x03173420,0x03173650,0x03173750,
				0x03173810,0x03173960,0x03173970,
				0x03173B20,0x03173CE0,0x03173CE5,
				0x03172D20,0x03172EE0,0x03172EE2,
				0x031730A0,0x031730A2,0x03173260,
				0x03173420,0x03173650,0x03173750,
				0x03173810,0x03173960,0x03173970,
				0x03173B20,0x03173CE0,0x03173CE5,
]

shearTransform2=[0x03173F10,0x03173D50,0x03173D60,
				0x03173B90,0x03173B95,0x031739D0,
				0x031732CB,0x031732D0,0x031732D2,
				0x03172D90,0x03172F50,0x03172F52,
				0x03174140,0x03173180,0x03173182,
				0x03173F10,0x03173D50,0x03173D60,
				0x03173B90,0x03173B95,0x031739D0,
				0x031732CB,0x031732D0,0x031732D2,
				0x03172D90,0x03172F50,0x03172F52,
				0x03174140,0x03173180,0x03173182,
				0x03173F10,0x03173D50,0x03173D60,
				0x03173B90,0x03173B95,0x031739D0,
				0x031732CB,0x031732D0,0x031732D2,
				0x03172D90,0x03172F50,0x03172F52,
				0x03174140,0x03173180,0x03173182,
				0x03173F10,0x03173D50,0x03173D60,
				0x03173B90,0x03173B95,0x031739D0,
				0x031732CB,0x031732D0,0x031732D2,
				0x03172D90,0x03172F50,0x03172F52,
				0x03174140,0x03173180,0x03173182,
]

pivotTransform2=[0x03173F80,0x03173DC0,0x03173DC2,
				0x03173C00,0x03173C01,0x03173A40,
				0x031738F0,0x03173340,0x03173342,
				0x03172E00,0x03172FC0,0x03172FC2,
				0x03173110,0x03174290,0x03174292,
				0x03173F80,0x03173DC0,0x03173DC2,
				0x03173C00,0x03173C01,0x03173A40,
				0x031738F0,0x03173340,0x03173342,
				0x03172E00,0x03172FC0,0x03172FC2,
				0x03173110,0x03174290,0x03174292,
				0x03173F80,0x03173DC0,0x03173DC2,
				0x03173C00,0x03173C01,0x03173A40,
				0x031738F0,0x03173340,0x03173342,
				0x03172E00,0x03172FC0,0x03172FC2,
				0x03173110,0x03174290,0x03174292,
				0x03173F80,0x03173DC0,0x03173DC2,
				0x03173C00,0x03173C01,0x03173A40,
				0x031738F0,0x03173340,0x03173342,
				0x03172E00,0x03172FC0,0x03172FC2,
				0x03173110,0x03174290,0x03174292,
]


crowd_type = {'C1-UltraHome':0.9999, 'C2-UltraHome':2.9999, 'C3-UltraHome':4.9999,
			  'C1-HardcoreHome':0.8999, 'C2-HardcoreHome':2.8999, 'C3-HardcoreHome':4.8999,
			  'C1-HeavyHome':0.8599, 'C2-HeavyHome':2.8599, 'C3-HeavyHome':4.8599,
			  'C1-PopHome':0.7999, 'C2-PopHome':2.7999, 'C3-PopHome':4.7999,
			  'C1-FolkHome':0.6999, 'C2-FolkHome':2.6999, 'C3-FolkHome':4.6999,
			  'C1-Neutral':0.5, 'C2-Neutral':2.5, 'C3-Neutral':4.5,
			  'C1-FolkAway':0.4999, 'C2-FolkAway':2.4999, 'C3-FolkAway':4.4999,
			  'C1-PopAway':0.3999,'C2-PopAway':2.3999,'C3-PopAway':4.3999,
			  'C1-HeavyAway':0.2999, 'C2-HeavyAway':2.2999, 'C3-HeavyAway':4.2999,
			  'C1-HardcoreAway':0.1999, 'C2-HardcoreAway':2.1999, 'C3-HardcoreAway':4.1999,
			  'C1-UltraAway':0.0999, 'C2-UltraAway':2.0999, 'C3-UltraAway':4.0999
}

crowd_typedict={0:'C1-UltraHome', 11:'C2-UltraHome', 22:'C3-UltraHome',
				1:'C1-HardcoreHome', 12:'C2-HardcoreHome', 23:'C3-HardcoreHome',
				2:'C1-HeavyHome', 13:'C2-HeavyHome', 24:'C3-HeavyHome',
				3:'C1-PopHome', 14:'C2-PopHome', 25:'C3-PopHome',
				4:'C1-FolkHome', 15:'C2-FolkHome', 26:'C3-FolkHome',
				5:'C1-Neutral', 16:'C2-Neutral', 27:'C3-Neutral',
				6:'C1-FolkAway', 17:'C2-FolkAway', 28:'C3-FolkAway',
				7:'C1-PopAway', 18:'C2-PopAway', 29:'C3-PopAway',
				8:'C1-HeavyAway', 19:'C2-HeavyAway', 30:'C3-HeavyAway',
				9:'C1-HardcoreAway', 20:'C2-HardcoreAway', 31:'C3-HardcoreAway',
				10:'C1-UltraAway', 21:'C2-UltraAway', 32:'C3-UltraAway'
}

behavior0=[('C1-UltraHome', 'C1-UltraHome', 'Stance Type : Normal'),
		   ('C1-HardcoreHome', 'C1-HardcoreHome', 'Stance Type : Normal'),
		   ('C1-HeavyHome', 'C1-HeavyHome', 'Stance Type : Normal'),
		   ('C1-PopHome', 'C1-PopHome', 'Stance Type : Normal'),
		   ('C1-FolkHome', 'C1-FolkHome', 'Stance Type : Normal'),
		   ('C1-Neutral', 'C1-Neutral', 'Stance Type : Normal'),
		   ('C1-FolkAway', 'C1-FolkAway', 'Stance Type : Normal'),
		   ('C1-PopAway', 'C1-PopAway', 'Stance Type : Normal'),
		   ('C1-HeavyAway', 'C1-HeavyAway', 'Stance Type : Normal'),
		   ('C1-HardcoreAway', 'C1-HardcoreAway', 'Stance Type : Normal'),
		   ('C1-UltraAway', 'C1-UltraAway', 'Stance Type : Normal'),
]
behavior1=[('C2-UltraHome', 'C2-UltraHome', 'Stance Type : Standing Non-chair'),
		   ('C2-HardcoreHome', 'C2-HardcoreHome', 'Stance Type : Standing Non-chair'),
		   ('C2-HeavyHome', 'C2-HeavyHome', 'Stance Type : Standing Non-chair'),
		   ('C2-PopHome', 'C2-PopHome', 'Stance Type : Standing Non-chair'),
		   ('C2-FolkHome', 'C2-FolkHome', 'Stance Type : Standing Non-chair'),
		   ('C2-Neutral', 'C2-Neutral', 'Stance Type : Standing Non-chair'),
		   ('C2-FolkAway', 'C2-FolkAway', 'Stance Type : Standing Non-chair'),
		   ('C2-PopAway', 'C2-PopAway', 'Stance Type : Standing Non-chair'),
		   ('C2-HeavyAway', 'C2-HeavyAway', 'Stance Type : Standing Non-chair'),
		   ('C2-HardcoreAway', 'C2-HardcoreAway', 'Stance Type : Standing Non-chair'),
		   ('C2-UltraAway', 'C2-UltraAway', 'Stance Type : Standing Non-chair'),
]
behavior2=[('C3-UltraHome', 'C3-UltraHome', 'Stance Type : Standing with Chair'),
		   ('C3-HardcoreHome', 'C3-HardcoreHome', 'Stance Type : Standing with Chair'),
		   ('C3-HeavyHome', 'C3-HeavyHome', 'Stance Type : Standing with Chair'),
		   ('C3-PopHome', 'C3-PopHome', 'Stance Type : Standing with Chair'),
		   ('C3-FolkHome', 'C3-FolkHome', 'Stance Type : Standing with Chair'),
		   ('C3-Neutral', 'C3-Neutral', 'Stance Type : Standing with Chair'),
		   ('C3-FolkAway', 'C3-FolkAway', 'Stance Type : Standing with Chair'),
		   ('C3-PopAway', 'C3-PopAway', 'Stance Type : Standing with Chair'),
		   ('C3-HeavyAway', 'C3-HeavyAway', 'Stance Type : Standing with Chair'),
		   ('C3-HardcoreAway', 'C3-HardcoreAway', 'Stance Type : Standing with Chair'),
		   ('C3-UltraAway', 'C3-UltraAway', 'Stance Type : Standing with Chair')
]
parentlist, shaders=[],[]

L_Side=["back","front","left","right"
]

L_P_List=["L_BACK",
			"L_FRONT",
			"L_LEFT",
			"L_RIGHT"
]

lfx_tex_list=[("tex_star_00.ftex","00 - tex_star_00","tex_star_00"),
			  ("tex_star_01.ftex","01 - tex_star_01","tex_star_01"),
			  ("tex_star_02.ftex","02 - tex_star_02","tex_star_02"),
			  ("tex_star_03.ftex","03 - tex_star_03","tex_star_03"),
			  ("tex_star_04.ftex","04 - tex_star_04","tex_star_04"),
			  ("tex_star_05_alp.ftex","05 - tex_star_05","tex_star_05_alp"),
			  ("tex_star_07_alp.ftex","07 - tex_star_07","tex_star_07_alp"),
			  ("tex_star_08_alp.ftex","08 - tex_star_08","tex_star_08_alp"),
			  ("tex_star_20.ftex","20 - tex_star_20","tex_star_20"),
			  ("tex_star_21.ftex","21 - tex_star_21","tex_star_21"),
			  ("tex_star_22.ftex","22 - tex_star_22","tex_star_22"),
			  ("tex_star_23.ftex","23 - tex_star_23","tex_star_23"),
			  ("tex_star_24.ftex","24 - tex_star_24","tex_star_24"),
			  ("tex_star_25.ftex","25 - tex_star_25","tex_star_25"),
			  ("tex_star_26.ftex","26 - tex_star_26","tex_star_26"),
			  ("tex_star_27.ftex","27 - tex_star_27","tex_star_27"),
			  ("tex_star_28.ftex","28 - tex_star_28","tex_star_28"),
]

LensFlareTexList=[("tex_ghost_00.ftex","00 - tex_ghost_00","tex_ghost_00.ftex"),
				("tex_ghost_01.ftex","01 - tex_ghost_01","tex_ghost_01.ftex"),
				("tex_ghost_02.ftex","02 - tex_ghost_02","tex_ghost_02.ftex"),
				("tex_ghost_03.ftex","03 - tex_ghost_03","tex_ghost_03.ftex"),
				("tex_ghost_04.ftex","04 - tex_ghost_04","tex_ghost_04.ftex"),
				("tex_ghost_05.ftex","05 - tex_ghost_05","tex_ghost_05.ftex"),
				("tex_ghost_06.ftex","06 - tex_ghost_06","tex_ghost_06.ftex")

]

HaloTexList=[("tex_halo_D00.ftex","D00 - tex_halo_D00","tex_halo_D00.ftex"),
			("tex_halo_D01.ftex","D01 - tex_halo_D01","tex_halo_D01.ftex"),
			("tex_halo_D02.ftex","D02 - tex_halo_D02","tex_halo_D02.ftex"),
			("tex_halo_N00.ftex","N00 - tex_halo_N00","tex_halo_N00.ftex"),
			("tex_halo_N01.ftex","N01 - tex_halo_N01","tex_halo_N01.ftex"),
			("tex_halo_N02.ftex","N02 - tex_halo_N02","tex_halo_N02.ftex"),
			("tex_halo_N03.ftex","N03 - tex_halo_N03","tex_halo_N03.ftex"),
			("tex_halo_N04.ftex","N04 - tex_halo_N04","tex_halo_N04.ftex"),
			("tex_halo_N05.ftex","N05 - tex_halo_N05","tex_halo_N05.ftex"),
			("tex_halo_N06.ftex","N06 - tex_halo_N06","tex_halo_N06.ftex"),
			("tex_halo_N07.ftex","N07 - tex_halo_N07","tex_halo_N07.ftex"),
			("tex_halo_N08.ftex","N08 - tex_halo_N08","tex_halo_N08.ftex"),
			("tex_halo_N09.ftex","N09 - tex_halo_N09","tex_halo_N09.ftex"),
			("tex_halo_S00.ftex","S00 - tex_halo_S00","tex_halo_S00.ftex"),
			("tex_halo_S01.ftex","S01 - tex_halo_S01","tex_halo_S01.ftex"),
			("tex_halo_S02.ftex","S02 - tex_halo_S02","tex_halo_S02.ftex")
]
				
def makedir(DirName, isStadium):
	if isStadium:
		dirNew = os.path.join(bpy.context.scene.export_path,DirName)
	else:
		dirNew = os.path.join(bpy.context.scene.export_path[:-6],DirName)
	if not os.path.exists(dirNew):
		os.makedirs(dirNew, exist_ok=True)
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

def hxd(val, count):
	given_int = val
	given_len = count

	hex_result = hex(given_int)[2:].upper()
	num_hex_chars = len(hex_result)
	extra_zeros = '0' * (given_len - num_hex_chars)

	return ('0x' + hex_result if num_hex_chars == given_len else
			'?' * given_len if num_hex_chars > given_len else
			'0x' + extra_zeros + hex_result if num_hex_chars < given_len else
			None)
			
def texconv(inPath, outPath, arguments, cm):
	if os.path.isfile(inPath):
		File = open(inPath, 'r', encoding="cp437")
		File.seek(0x54)
		TxFormat = File.read(4)
		File.close()
		if cm:
			if TxFormat == "DX10":
				args = arguments + ' "' + inPath + '"' + ' -o "' + outPath+''
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
	fox2Read=open(xml_dir+sourcePath,'rt').read()
	fox2Read=fox2Read.replace('stid',scn.STID)
	fox2Write=open(scn.export_path+filePath,'wt')
	fox2Write.write(fox2Read)
	fox2Write.flush(),fox2Write.close()

	return 1

def findDirectory(dirPath):
	path = str()
	listDir=[]
	for root in os.walk(dirPath):
		if "#Win" in root[0]:
			path = root[0].replace("\\",",")
			lists = path.split(',')
			if "#Win" in lists:
				for p in lists:
					listDir.append(p)
					if p == "#Win":	
						path = f"{listDir[0]}\\{os.path.join(*listDir).split(':')[1]}"
						return path[:-4]
					
def findTextureDirectory(dirPath):
	for root in os.walk(dirPath):
		if "#windx11" in root[0]:
			return root[0]

def getDirPath(dirPath):
	for root, directories, filenames in os.walk(dirPath):
		for fileName in filenames:
			filename, extension = os.path.splitext(fileName)
			return os.path.dirname(os.path.join(root, filename+extension))

def textureLoad(dirPath):
	for root, directories, filenames in os.walk(dirPath):
		for fileName in filenames:
			filename, extension = os.path.splitext(fileName)
			if extension.lower() == '.ftex':
				
				ddsPath = os.path.join(root, filename + '.dds')
				ftexPath = os.path.join(root, filename + extension)
				if not os.path.isfile(ddsPath):
					# if search("lut", ddsPath.lower()):
					# 	continue
					try:
						Ftex.ftexToDds(ftexPath, ddsPath)
					except:
						convert_ftex(ftexPath)
					texconv(ddsPath, dirPath, " -y -l -f DXT5 -ft dds -srgb", True)
					print('Converting {0} ==> {1}'.format(filename+'.ftex', filename+'.dds'))
					
	return 1

def remove_dds(dirPath):
	for root, directories, filenames in os.walk(dirPath):
		for fileName in filenames:
			filename, extension = os.path.splitext(fileName)
			if extension.lower() == '.dds' or extension.lower() == '.png' or extension.lower() == '.tga':
				ddsPath = os.path.join(root, filename + extension)
				os.remove(ddsPath)
				print('Removing texture [>{0}{1}<] succesfully'.format(filename, extension))
	return 1

def node_group():
	inner_path = 'NodeTree'
	for NodeTree in ('NRM Converter', 'SRM Seperator', 'TRM Subsurface'):
		if not NodeTree in bpy.data.node_groups:
			bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, NodeTree),directory=os.path.join(base_file_blend, inner_path),filename=NodeTree)
	return 1

def Create_Parent_Part(self, context):

	inc_list=[]
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
			bpy.ops.object.add(type='EMPTY',location=(0,0,0))
			ob = context.active_object
			for i in range(3):
				ob.lock_location[i]=1
				ob.lock_rotation[i]=1
				ob.lock_scale[i]=1
			ob.name = o
	for o in (main_list):
		if o not in inc_list:
			bpy.ops.object.add(type='EMPTY',location=(0,0,0))
			ob = context.active_object
			for i in range(3):
				ob.lock_location[i]=1
				ob.lock_rotation[i]=1
				ob.lock_scale[i]=1
			ob.name = o
	for o in parent_main_list:
		if o not in inc_list:
			bpy.ops.object.add(type='EMPTY',location=(0,0,0))
			ob = context.active_object
			for i in range(3):
				ob.lock_location[i]=1
				ob.lock_rotation[i]=1
				ob.lock_scale[i]=1
			ob.name = o
	for ob in bpy.data.objects:
		if ob.type=="EMPTY":
			if ob.name in ["L_FRONT","L_RIGHT","L_LEFT","L_BACK"]:
				ob.parent = bpy.data.objects['LightBillboard']
			elif ob.name in ["H_FRONT","H_RIGHT","H_LEFT","H_BACK"]:
				ob.parent = bpy.data.objects['Halo']
			elif ob.name in ["F_FRONT","F_RIGHT","F_LEFT","F_BACK"]:
				ob.parent = bpy.data.objects['LensFlare']
			elif ob.name in ["LightBillboard", "LensFlare", "Halo"]:
				ob.parent = bpy.data.objects["LIGHTS"]
			elif ob.name in ["cheer_back1_h_a1","cheer_front1_h_a1", "cheer_left1_h_a1", "cheer_right1_h_a1"]:
				ob.parent = bpy.data.objects["CHEER1"]
			elif ob.name in ["cheer_back1_h_a2","cheer_front1_h_a2", "cheer_left1_h_a2", "cheer_right1_h_a2"]:
				ob.parent = bpy.data.objects["CHEER2"]
			elif ob.name in ["Staff Coach","Steward", "Staff Walk","Ballboy","Cameraman Crew"]:
				ob.parent = bpy.data.objects["STAFF"]				
			elif ob.name == "MESH_FLAGAREA":
				ob.parent = bpy.data.objects["FLAGAREA"]
			elif ob.name == "MESH_CROWD":
				ob.parent = bpy.data.objects["AUDIAREA"]
			elif ob.name == "Pitch":
				ob.parent = bpy.data.objects["PITCH2021"]
			elif ob.name in ["TV_Large_Left","TV_Large_Right","TV_Large_Front","TV_Large_Back",
							"TV_Small_Left","TV_Small_Right","TV_Small_Front","TV_Small_Back"]:
				ob.parent = bpy.data.objects["TV"]
			elif ob.name in ["ad_acl","ad_cl","ad_el","ad_normal","ad_olc","ad_sc"]:
				ob.parent = bpy.data.objects["AD"]
			elif ob.name in datalist2:
				ob.parent = bpy.data.objects["EXTRA"]	
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
							if ob2 is not None and  ob2.type == "MESH":
								blenderMaterial = bpy.data.objects[ob2.name].active_material
								for nodes in blenderMaterial.node_tree.nodes:
									if nodes.type == "TEX_IMAGE":
										blenderTexture = blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory
										if "st" in blenderTexture:
											if not context.scene.STID in blenderTexture:
												print("\nStadium ID isn't match!!")
												print("\nSome stadium IDs do not match in the node, please check first or you can swap all stadium IDs")
												print("\nCheck out Object in Parent({0} --> {1} --> {2}) in Mesh object({3}) in node({4})"
												.format(context.scene.part_info, ob.parent.name, ob2.parent.name, ob2.name, nodes.name))
												return True
											else:
												return False

	else:
		for child in bpy.data.objects[context.scene.part_info].children:
			if child.type == 'EMPTY' and child is not None:
				for ob2 in bpy.data.objects[child.name].children:
					if ob2 is not None and  ob2.type == "MESH":
						blenderMaterial = bpy.data.objects[ob2.name].active_material
						for nodes in blenderMaterial.node_tree.nodes:
							if nodes.type == "TEX_IMAGE":
								blenderTexture = blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory
								if "st" in blenderTexture:
									if not context.scene.STID in blenderTexture:
										print("\nStadium ID isn't match!!")
										print("\nSome stadium IDs do not match in the node, please check first or you can swap all stadium IDs")
										print("\nCheck out Object in Parent({0} --> {1}) in Mesh object({2}) in node({3})"
										.format(context.scene.part_info, ob2.parent.name, ob2.name, nodes.name))
										return True
									else:
										return False
	pass


class FMDL_MaterialParameter(bpy.types.PropertyGroup):
	name : StringProperty(name="Parameter Name")
	parameters : FloatVectorProperty(name="Parameter Values", size=4, default=[0.0, 0.0, 0.0, 0.0])

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
		mainColumn = self.layout.column(align=True)
		mainColumn=mainColumn.row()
		mainColumn.prop(material, "fmdl_material_preset", text="Preset")
		mainColumn.operator("shader.operator", text="", icon="SEQ_SEQUENCER")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(material, "fmdl_material_shader")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(material, "fmdl_material_technique")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.label(text="Material Parameters")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
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
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		if 0 <= material.fmdl_material_parameter_active < len(material.fmdl_material_parameters):
			valuesColumn = mainColumn.column()
			parameter = material.fmdl_material_parameter_active
			valuesColumn.prop(
				material.fmdl_material_parameters[parameter],
				"parameters"
			)
	pass


def importFmdlfile(fileName, sklname, meshID, objName, texturePath, parent):

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
	importSettings.texture_path = texturePath
	importSettings.parents = parent

	fmdlFile = FmdlFile.FmdlFile()
	fmdlFile.readFile(fileName)

	rootObject = IO.importFmdl(context, fmdlFile, objName, importSettings)
	rootObject.fmdl_export_extensions_enabled = importSettings.enableExtensions
	rootObject.fmdl_export_loop_preservation = importSettings.enableVertexLoopPreservation
	rootObject.fmdl_export_mesh_splitting = importSettings.enableMeshSplitting

	return True
	
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
		if bpy.app.version >= (2, 90, 0):
			this_icon = icons_collections["custom_icons"]["icon_1"].icon_id
			row.label(text="eFootball PES2021 Stadium Exporter", icon_value=this_icon)
			row = box.row()
			this_icon = icons_collections["custom_icons"]["icon_0"].icon_id
			row.label(text="Made by: MjTs-140914 || the4chancup", icon_value=this_icon)
			row = box.row()
			box.label(text="Blender version {0}.{1}.{2} ({3})".format(major, minor, build, version) , icon="BLENDER")
			row = box.row()
			row.operator("main_parts.operator", text="Create Stadium Parts", icon="EMPTY_DATA")
			row.operator("scene.operator", text="", icon="PRESET_NEW")
			if ob and ob is not None:
				blenderMaterial = context.active_object.active_material
				if ob.name == "MAIN":
					row = layout.row()
					box = layout.box()
					row = box.row()
					row.label(text="Stadium Import Menu", icon="INFO")
					row = box.row()
					row.operator(FDMDL_OT_Import_Main_Stadium.bl_idname, text="Import Main Stadium", icon="IMPORT")
					row.operator("clear_temp.operator", text="", icon="TRASH").opname = "cleartemp"
				if ob.name == "EXTRA":
					row = layout.row()
					box = layout.box()
					row = box.row()
					row.label(text="Stadium Import Menu", icon="INFO")
					row = box.row()
					row.operator(FDMDL_OT_Import_Extra_Stadium.bl_idname, text="Import Extra Stadium", icon="IMPORT")
					row.operator("clear_temp.operator", text="", icon="TRASH").opname = "cleartemp"
				if ob and ob.type == 'MESH' and ob is not None:
					mat = bpy.data.objects[ob.name].material_slots
					box = layout.box()
					row = box.row()
					row.label(text="Parent Assigment", icon="INFO")
					row = box.row()
					row.label(text="Vertex Count : " +str(len(ob.data.vertices)), icon="VERTEXSEL")
					row.label(text="Face Count : " +str(len(ob.data.polygons)), icon="FACESEL")
					row = box.row()
					row.alignment = 'EXPAND'
					split = row.split(factor=1)
					split = split.split(factor=0.6)
					row = split.row()
					row.prop(ob, "droplist", text="Parent")
					split = split.split(factor=1)
					row = split.row()
					row.operator("refresh.operator",text="",icon="FILE_REFRESH")
					row.operator("set_parent.operator",text="SET")
					row.operator("clr.operator",text="CLR")
					row = box.row()
					split = row.split(factor=1)
					split = split.split(factor=0.57)
					row = box.row()
					if ob.parent and ob.type != 'LIGHT':
						pn=ob.parent.name
						pn=pn.replace("MESH_","")
						row.label(text="Parent : " +pn, icon="EMPTY_DATA")
						row.label(text="Object : " +ob.name, icon="OBJECT_DATA")
						row = box.row()
						if blenderMaterial is not None and ob.name not in crowd_part and ob.name not in flags_part:
							box = layout.box()
							row = box.row()
							row.label(text="Shader : %s" % blenderMaterial.fmdl_material_shader, icon="MATSHADERBALL")
							row = box.row()
							row.label(text="Technique : %s" % blenderMaterial.fmdl_material_technique, icon="MATSHADERBALL")
							row = box.row()
							if '3DDF' in blenderMaterial.fmdl_material_technique:
								row.label(text="Shader Type : Deferred Shaders", icon="MATSHADERBALL")
							if '3DFW' in blenderMaterial.fmdl_material_technique:
								row.label(text="Shader Type : Forward Shaders", icon="MATSHADERBALL")	
							if '3DDC' in blenderMaterial.fmdl_material_technique:
								row.label(text="Shader Type : Deferred Decal Shaders", icon="MATSHADERBALL")		
							row = box.row()
							row = box.row()
							if ob.data.fmdl_alpha_enum_select != "Custom":
								row.label(text="Alpha Type : %s" % PesFoxShader.Alpha_EnumDict[int(ob.data.fmdl_alpha_enum_select)], icon="TEXTURE_DATA")
							else:
								row.label(text="Alpha Type : Custom", icon="TEXTURE_DATA")
							row = box.row()
							if ob.data.fmdl_shadow_enum_select != "Custom":
								row.label(text="Shadow Type : %s" % PesFoxShader.ShadowEnumDict[int(ob.data.fmdl_shadow_enum_select)], icon="TEXTURE_DATA")
							else:
								row.label(text="Shadow Type : Custom", icon="TEXTURE_DATA")
							row = box.row()
					else:
						box.label(text="No parent for active object, assign a parent...", icon="ERROR")
					if len(mat) == 0 and not ob.name in crowd_part and not ob.name in flags_part:
						row.label(text="Mesh [%s] not have Materials!" % ob.name, icon="ERROR")
					elif len(mat) == 1:
						if blenderMaterial.fmdl_material_technique == str()	and not ob.name in crowd_part and not ob.name in flags_part:
							row.label(text="Mesh [%s] not have Shader!" % ob.name, icon="ERROR")
					elif len(mat) >= 2	and not ob.name in crowd_part and not ob.name in flags_part:
						row.label(text="Mesh [%s] too much Material Slots" % ob.name, icon="ERROR")
						
				box = layout.box()
				row = box.row()
				row.label(text="Stadium Export Part List", icon="INFO")
				row = box.row()
				row.prop(scn,"part_info")
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
					row.operator("clear_temp.operator", text="", icon="TRASH").opname = "cleartempdata"
					row = box.row()
					row.operator("export_stadium.operator", text="Export Main Stadium", icon="EXPORT").opname = "mainstadium"
				elif scn.part_info == "EXTRA":
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
					row.operator("clear_temp.operator", text="", icon="TRASH").opname = "cleartempdata"
					row = box.row()
					row.operator("export_stadium.operator", text="Export Extra Stadium", icon="EXPORT").opname = "extrastadium"
				elif scn.part_info == "AUDIAREA":
					if ob is not None:
						if ob.name == "AUDIAREA":
							box = layout.box()
							row = box.row()
							row.label(text="Crowd Import", icon="INFO")
							row = box.row()
							row.operator("crowd_import.operator", text="Import Stadium Audiarea", icon="IMPORT")
							row = box.row()
						else:
							box = layout.box()
							row = box.row()
							if ob.name not in crowd_part and ob.parent and ob.parent.name == "MESH_CROWD":
								box.label(text="Crowd Part Name is Wrong, Fix it before Export... ",icon="ERROR")
							else:
								row.label(text="Crowd Export", icon="INFO")
								row = box.row()
								row.prop(scn,"crowd_row_space",text="Row Space")
								row = box.row()
								row.operator("crowd.operator", text="Export Stadium Audiarea", icon="EXPORT")
								row = box.row()
				elif scn.part_info == "FLAGAREA":
					if ob is not None:
						box = layout.box()
						row = box.row()
						if ob.name not in flags_part and ob.parent and ob.parent.name == "MESH_FLAGAREA":
							box.label(text="Flagarea Part Name is Wrong, Fix it before Export... ",icon="ERROR")
						else:
							row.label(text="Flagarea Export", icon="INFO")
							row = box.row()
							row.operator("flags.operator", text="Export Stadium Flagarea", icon="EXPORT")
							row = box.row()
				elif scn.part_info == "LIGHTS" and ob is not None:
					if ob.name == "LIGHTS":
						box = layout.box()
						row = box.row()
						row.label(text="Light FX Importer", icon="LIGHT_SPOT")
						row = box.row()
						row.operator("ligtfx_importer.operator", text="Import Light FX", icon="IMPORT")
						row = box.row()
					else:
						box = layout.box()
						row = box.row()
						row.label(text="Light FX Exporter", icon="LIGHT_SPOT")
						row = box.row()
						if str(ob.name).startswith("L_") and ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type == 'POINT':
							if ob.parent:
								lp=ob.parent.name
							else:
								lp="Not Assigned"
							row.label(text="Parent: " +lp)
							row.label(text="Name: " +ob.name)
							row.label(text="Energy: " +str(round(ob.l_Energy,2))[:4])
							row = box.row()	
							row.prop(scn,"l_lit_side",text="")
							row.operator("lights_side.operator",text="",icon="FILE_REFRESH")
							row.prop(scn,"l_fxe")
							row.operator("lightfx.operator",text="Set Light FX",icon="FILE_TICK").opname='set_lfx_side'
							row = box.row()
						elif str(ob.name).startswith("H_") and ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type == 'AREA':
							if ob.parent:
								lp=ob.parent.name
							else:
								lp="Not Assigned"
							row.label(text="Parent: " +lp)
							row.label(text="Name: " +ob.name)
							row = box.row()
							row.prop(ob,"HaloTex", text="Texture")
							row.prop(ob,"rotY", text="Fix-Rot-Y")
							row = box.row()
							row.prop(ob,"Pivot")
							row = box.row()
							row.prop(scn,"l_lit_side",text="")
							row.operator("lights_side.operator",text="",icon="FILE_REFRESH")
							row.operator("lightfx.operator",text="Set Light FX",icon="FILE_TICK").opname='set_lfx_side'
							row = box.row()
						elif str(ob.name).startswith("F_") and ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type == 'AREA':
							if ob.parent:
								lp=ob.parent.name
							else:
								lp="Not Assigned"
							row.label(text="Parent: " +lp)
							row.label(text="Name: " +ob.name)
							row = box.row()
							row.prop(scn,"l_lit_side",text="")
							row.operator("lights_side.operator",text="",icon="FILE_REFRESH")
							row.operator("lightfx.operator",text="Set Light FX",icon="FILE_TICK").opname='set_lfx_side'
							row = box.row()
						elif ob.type=='MESH' or ob.type=='EMPTY':
							row.prop(scn,"time_mode",text="Mode")
							row = box.row()
							row.prop(scn,"lensflaretex",text="Lens Flare")
							row = box.row()
							row.prop(scn,"l_fx_tex",text="")		
							row.operator("lightfx.operator", text="Export Light FX ", icon="LIGHT_DATA").opname='export_lfx'
							row = box.row()
						else:
							if str(ob.name).startswith("H_") and ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type != 'AREA':
								row = box.row()
								row.label(text="Light object %s type isn't Area"%ob.name, icon="ERROR")
								row = box.row()
							elif str(ob.name).startswith("F_") and ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type != 'AREA':
								row = box.row()
								row.label(text="Light object %s type isn't Area"%ob.name, icon="ERROR")
								row = box.row()
							elif str(ob.name).startswith("L_") and ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type != 'POINT':
								row = box.row()
								row.label(text="Light object %s type isn't POINT"%ob.name, icon="ERROR")
								row = box.row()
							else:
								row = box.row()
								row.label(text="Light object %s name isn't correct"%ob.name, icon="ERROR")
								row = box.row()
								row.label(text="Light object name must startswith:", icon="ERROR")
								row = box.row()
								row.label(text="(L_) for LightBillboard -> Lights type (Point)", icon="ERROR")
								row = box.row()
								row.label(text="(F_) for LensFlare -> Lights type (Area)", icon="ERROR")
								row = box.row()
								row.label(text="(H_) for Halo -> Lights type (Area)", icon="ERROR")
								row = box.row()
				elif scn.part_info == "TV" and ob is not None:
					box = layout.box()
					row = box.row()
					row.label(text="TV Exporter", icon="INFO")
					row = box.row()
					row.prop(scn,"tvobject",text="Type")
					row.operator("tv_object.operator", text="Add %s"%context.scene.tvobject)
					row = box.row()
					row.operator("export_tv.operator", text="Export Stadium Tv", icon="EXPORT")
					row = box.row()
				elif scn.part_info == "PITCH2021" and ob is not None:
					if ob.name == "PITCH2021":
						box = layout.box()
						row = box.row()
						row.label(text="Load Stadium Pitch", icon="INFO")
						row = box.row()
						row.operator("export_pitch.operator", text="Load Stadium Pitch", icon="IMPORT").opname = "pitch_import"
						row = box.row()
					else:
						box = layout.box()
						row = box.row()
						row.label(text="Pitch Exporter", icon="INFO")
						row = box.row()
						row.operator("export_pitch.operator", text="Export Stadium Pitch", icon="EXPORT").opname = "pitch_export"
						row = box.row()
				elif scn.part_info == "STAFF" and ob is not None:
					if ob.name =="Staff Coach":
						box = layout.box()
						row = box.row()
						row.label(text="Staff Coach Position", icon="INFO")
						row = box.row()
						row.operator("staff_pos.operator", text="Import", icon="IMPORT").opname = "loadcoach"
						row.operator("staff_pos.operator", text="Export", icon="EXPORT").opname = "assigncoach"
						row = box.row()
					if ob.name =="Staff Walk":
						box = layout.box()
						row = box.row()
						row.label(text="Staff Walk Position", icon="INFO")
						row = box.row()
						row.operator("staff_pos.operator", text="Import", icon="IMPORT").opname = "loadwalk"
						row.operator("staff_pos.operator", text="Export", icon="EXPORT").opname = "assignwalk"
						row = box.row()
					else:
						if ob is not None and ob.parent is not None:
							if ob.parent.name == "Staff Walk" and ob.type == "EMPTY":
								box = layout.box()
								row = box.row()
								row.label(text="Staff Walk Position", icon="INFO")
								row = box.row()
								row = box.row()
								row = box.row()
								row.prop(ob,"scrName")
								row = box.row()
								row.prop(ob,"scrEntityPtr")
								row = box.row()
								row.prop(ob,"scrTransformEntity")
								row = box.row()
								row.prop(ob,"scrDirection")
								row.prop(ob,"scrKind")
								row.prop(ob,"scrDemoGroup")	
								row = box.row()
					if ob.name =="Ballboy":
						box = layout.box()
						row = box.row()
						row.label(text="Ballboy Position", icon="INFO")
						row = box.row()
						row.operator("staff_pos.operator", text="Import", icon="IMPORT").opname = "loadballboy"
						row.operator("staff_pos.operator", text="Export", icon="EXPORT").opname = "assignballboy"
						row = box.row()
					else:
						if ob is not None and ob.parent is not None:
							if ob.parent.name == "Ballboy" and ob.type == "EMPTY":
								box = layout.box()
								row = box.row()
								row.label(text="Ballboy Position", icon="INFO")
								row = box.row()
								row = box.row()
								row = box.row()
								row.prop(ob,"scrName")
								row = box.row()
								row.prop(ob,"scrEntityPtr")
								row = box.row()
								row.prop(ob,"scrTransformEntity")
								row = box.row()
								row = box.row()
								row.prop(ob,"scrLimitedRotatable")
								if ob.scrLimitedRotatable:
									row = box.row()
									row.prop(ob,"ObjectLinksName")
									row = box.row()
									row.prop(ob,"EntityObjectLinks")
									row = box.row()
									row.prop(ob,"packagePathHash")
									row = box.row()
									row.prop(ob,"maxRotDegreeLeft")
									row.prop(ob,"maxRotDegreeRight")
									row = box.row()
									row.prop(ob,"maxRotSpeedLeft")
									row.prop(ob,"maxRotSpeedRight")
									row = box.row()
								row = box.row()
								row.prop(ob,"scrDirection")
								row.prop(ob,"scrKind")
								row.prop(ob,"scrDemoGroup")	
								row = box.row()
					if ob.name =="Cameraman Crew":
						box = layout.box()
						row = box.row()
						row.label(text="Cameraman Crew Position", icon="INFO")
						row = box.row()
						row.operator("staff_pos.operator", text="Import", icon="IMPORT").opname = "loadcamcrew"
						row.operator("staff_pos.operator", text="Export", icon="EXPORT").opname = "assigncamcrew"
						row = box.row()
					else:
						if ob is not None and ob.parent is not None:
							if ob.parent.name == "Cameraman Crew" and ob.type == "EMPTY":
								box = layout.box()
								row = box.row()
								row.label(text="Cameraman Crew Position", icon="INFO")
								row = box.row()
								row = box.row()
								row = box.row()
								row.prop(ob,"scrName")
								row = box.row()
								row.prop(ob,"scrEntityPtr")
								row = box.row()
								row.prop(ob,"scrTransformEntity")
								row = box.row()
								row = box.row()
								row.prop(ob,"scrLimitedRotatable")
								if ob.scrLimitedRotatable:
									row = box.row()
									row.prop(ob,"ObjectLinksName")
									row = box.row()
									row.prop(ob,"EntityObjectLinks")
									row = box.row()
									row.prop(ob,"packagePathHash")
									row = box.row()
									row.prop(ob,"maxRotDegreeLeft")
									row.prop(ob,"maxRotDegreeRight")
									row = box.row()
									row.prop(ob,"maxRotSpeedLeft")
									row.prop(ob,"maxRotSpeedRight")
									row = box.row()
								row = box.row()
								row.prop(ob,"scrDirection")
								row.prop(ob,"scrKind")
								row.prop(ob,"scrDemoGroup")	
								row = box.row()
					if ob.name =="Steward":
						box = layout.box()
						row = box.row()
						row.label(text="Steward Position", icon="INFO")
						row = box.row()
						row.operator("staff_pos.operator", text="Import", icon="IMPORT").opname = "loadSteward"
						row.operator("staff_pos.operator", text="Export", icon="EXPORT").opname = "assignSteward"
						row = box.row()
					else:
						if ob is not None and ob.parent is not None:
							if ob.parent.name == "Steward" and ob.type == "EMPTY":
								box = layout.box()
								row = box.row()
								row.label(text="Steward Position", icon="INFO")
								row = box.row()
								row = box.row()
								row = box.row()
								row.prop(ob,"scrName")
								row = box.row()
								row.prop(ob,"scrEntityPtr")
								row = box.row()
								row.prop(ob,"scrTransformEntity")
								row = box.row()
								row = box.row()
								row.prop(ob,"scrLimitedRotatable")
								if ob.scrLimitedRotatable:
									row = box.row()
									row.prop(ob,"ObjectLinksName")
									row = box.row()
									row.prop(ob,"EntityObjectLinks")
									row = box.row()
									row.prop(ob,"packagePathHash")
									row = box.row()
									row.prop(ob,"maxRotDegreeLeft")
									row.prop(ob,"maxRotDegreeRight")
									row = box.row()
									row.prop(ob,"maxRotSpeedLeft")
									row.prop(ob,"maxRotSpeedRight")
									row = box.row()
								row = box.row()
								row.prop(ob,"scrDirection")
								row.prop(ob,"scrKind")
								row.prop(ob,"scrDemoGroup")	
								row = box.row()
				elif scn.part_info == "AD" and ob is not None:
					box = layout.box()
					row = box.row()
					row.label(text="Stadium AD Export", icon="INFO")
					row = box.row()
					row.operator("convert.operator", text="Export Ads Texture", icon="NODE_TEXTURE")
					if scn.useFastConvertTexture:
						txt = "Skip Non-Modified textures"
					else:
						txt = "Convert All textures"
					row.prop(scn, "useFastConvertTexture", text=txt)
					row = box.row()
					row.operator("export_ad.operator", text="Export Stadium Ads", icon="EXPORT")
				elif scn.part_info == "CHEER1" and ob is not None:
					box = layout.box()
					row = box.row()
					row.label(text="Stadium Banner Import/Export (H1)", icon="INFO")
					row = box.row()
					row.operator("stadium_banner.operator", text="Import Banner", icon="IMPORT").opname = "import_cheer1"
					row.operator("stadium_banner.operator", text="Export Banner", icon="EXPORT").opname = "export_cheer1"
				elif scn.part_info == "CHEER2" and ob is not None:
					box = layout.box()
					row = box.row()
					row.label(text="Stadium Banner Import/Export (H2)", icon="INFO")
					row = box.row()
					row.operator("stadium_banner.operator", text="Import Banner", icon="IMPORT").opname = "import_cheer2"
					row.operator("stadium_banner.operator", text="Export Banner", icon="EXPORT").opname = "export_cheer2"
				elif scn.part_info == "SCARECROW" and ob is not None:
					box = layout.box()
					row = box.row()
					row.label(text="Stadium Scarecrow Import/Export", icon="INFO")
					row = box.row()
					if ob is not None and ob.parent is not None:
						if ob.parent.name == "SCARECROW" and ob.type == "EMPTY":
							row = box.row()
							row.prop(ob,"scrName")
							row = box.row()
							row.prop(ob,"scrEntityPtr")
							row = box.row()
							row.prop(ob,"scrTransformEntity")
							row = box.row()
							row.prop(ob,"scrLimitedRotatable")
							if ob.scrLimitedRotatable:
								row = box.row()
								row.prop(ob,"ObjectLinksName")
								row = box.row()
								row.prop(ob,"EntityObjectLinks")
								row = box.row()
								row.prop(ob,"packagePathHash")
								row = box.row()
								row.prop(ob,"maxRotDegreeLeft")
								row.prop(ob,"maxRotDegreeRight")
								row = box.row()
								row.prop(ob,"maxRotSpeedLeft")
								row.prop(ob,"maxRotSpeedRight")
								row = box.row()
							row = box.row()
							row.prop(ob,"scrDirection")
							row.prop(ob,"scrKind")
							row.prop(ob,"scrDemoGroup")	
					row = box.row()
					row.prop(scn,"scrGenerateFpkd")
					row = box.row()
					row.operator("stadium_scarecrow.operator", text="Import Scarecrow", icon="IMPORT").opname = "import"
					row.operator("stadium_scarecrow.operator", text="Export Scarecrow", icon="EXPORT").opname = "export"
			if ob is not None:
				if ob.type == "EMPTY" and ob.name == "MAIN" or ob.name == "EXTRA" and not ob.parent:
					box = layout.box()
					row = box.row()
					row.label(text="Visit Link For Full Tutorial", icon="URL")
					row = box.row()
					this_icon = icons_collections["custom_icons"]["icon_3"].icon_id
					row.operator("wm.url_open", text='Evo-Web', icon_value=this_icon).url = 'https://evo-web.co.uk/threads/efootbal-pes2021-pes-stadium-exporter-v0-6-1b.85432/post-3644019'
					this_icon = icons_collections["custom_icons"]["icon_2"].icon_id
					row.operator("wm.url_open", text='Implying-Rigged', icon_value=this_icon).url = 'https://implyingrigged.info/wiki/User:Mjts140914'
					this_icon = icons_collections["custom_icons"]["icon_5"].icon_id
					row.operator("wm.url_open", text='Wiki', icon_value=this_icon).url = 'https://github.com/MjTs140914/PES_Stadium_Exporter/wiki'
					this_icon = icons_collections["custom_icons"]["icon_4"].icon_id
					row.operator("wm.url_open", text='', icon_value=this_icon).url = 'https://www.paypal.com/paypalme/mjts140914'
		else:
			row = box.row()
			row.label(text="Not support Blender version!", icon="ERROR")
			row = box.row()

def copytree(src, dst, symlinks=False, ignore=None):
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

class Stadium_Scarecrow(bpy.types.Operator):
	"""Stadium Scarecrow"""
	bl_idname = "stadium_scarecrow.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT")
	
	def execute(self, context):
		scn=context.scene
		stid=scn.STID
		exportPath=scn.export_path
		fpkdir="%sscarecrow\\#Win\\scarecrow_%s_fpk"% (exportPath,stid)
		fpkddir="%sscarecrow\\#Win\\scarecrow_%s_fpkd"% (exportPath,stid)
		Xmlfile="%sscarecrow\\#Win\\scarecrow_%s.fpk.xml"% (exportPath,stid)
		Xmlfile2="%sscarecrow\\#Win\\scarecrow_%s.fpkd.xml"% (exportPath,stid)
		if self.opname == "import":
			Create_Parent_Part(self, context)
			if len(stid) == 5:
				if context.scene.export_path == str():
					self.report({"WARNING"}, "Choose path to import %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					print("Choose path to import %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					return {'CANCELLED'}

				if not stid in context.scene.export_path:
					self.report({"WARNING"}, "Stadium ID doesn't match!!")
					print("Stadium ID doesn't match!!")
					return {'CANCELLED'}

				if not context.scene.export_path.endswith(stid+"\\"):
					self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					return {'CANCELLED'}
			else:
				self.report({"WARNING"}, "Stadium ID isn't correct!!")
				return {'CANCELLED'}
			checks=checkStadiumID(context, True)
			if checks:
				self.report({"WARNING"}, "Stadium ID isn't match, more info see => System Console (^_^)")
				return {'CANCELLED'}
				
			for ob in bpy.data.objects["SCARECROW"].children:
				if ob.type == "EMPTY":
					if "so_" in ob.name or "_sc2" in ob.name:
						self.report({"WARNING"}, "Scarecrow already imported !!")
						return {'CANCELLED'}

			fpkfilename="%sscarecrow\\#Win\\scarecrow_%s.fpk"%(exportPath,stid)
			pack_unpack_Fpk(fpkfilename)
			basedir = os.path.dirname(fpkfilename)
			dirPath ="%s\\addons\\Tools\\Gzs\\xml\\scarecrow\\textures\\"%AddonsPath
			for root, directories, filenames in os.walk(basedir):
				for fileName in filenames:
					filename, extension = os.path.splitext(fileName)
					if extension.lower() == '.fmdl':
						fmdlPath = os.path.join(root, fileName)
						print('Importing ==> %s' % fileName)
						importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename, dirPath, "SCARECROW")
			fpkdfilename="%sscarecrow\\#Win\\scarecrow_%s.fpkd"%(exportPath,stid)
			pack_unpack_Fpk(fpkdfilename)
			basedird = os.path.dirname(fpkdfilename)
			fox2xmlName=str()
			for root, directories, filenames in os.walk(basedird):
				for fileName in filenames:
					filename, extension = os.path.splitext(fileName)
					if extension.lower() == '.fox2':
						fox2xmlName = os.path.join(root, fileName)

			compileXML(fox2xmlName)
			PesScarecrow.Settings(self,context,fox2xmlName+'.xml')
			self.report({"INFO"}, "Importing scarecrow succesfully...")

			remove_dir(fpkdir)
			remove_file(Xmlfile)
			remove_dir(fpkddir)
			remove_file(Xmlfile2)
			return {'FINISHED'}
		if self.opname == "export":

			if len(bpy.data.objects[context.scene.part_info].children) == 0:
				self.report({"WARNING"}, "No object under '%s' parent !!"%context.scene.part_info)
				print("No object under '%s' parent !!"%context.scene.part_info)
				return {'CANCELLED'}
			fpkname,xmlPath=str(),str()
			Asset,lstObject, lstTotal,lstTotal2,lstTotal3=[],[],[],[],[]
			keyInfo=[]
			isize,exSize=0,0
			
			for ltm in PesScarecrow.scrAsset:
				Asset.append(ltm)
			for child in bpy.data.objects[context.scene.part_info].children:
				if child.type == 'EMPTY' and child is not None:
					isize+=1
					if child.scrName == str():
						self.report({"WARNING"}, "Object key is empty !!, more info see System Console (^_^)")
						print("Check out object: '%s' key: can't be empty !!"%child.name)
						return {'CANCELLED'}
					if child.scrEntityPtr == str():
						self.report({"WARNING"}, "Object value is empty !!, more info see System Console (^_^)")
						print("Check out object: '%s' value: can't be empty !!"%child.name)
						return {'CANCELLED'}
					if child.scrTransformEntity == str():
						self.report({"WARNING"}, "Object value is empty !!, more info see System Console (^_^)")
						print("Check out object: '%s' value: can't be empty !!"%child.name)
						return {'CANCELLED'}

					if child.scrName not in keyInfo:
						keyInfo.append(child.scrName)
					else:
						self.report({"WARNING"}, "Object same key already added !!, more info see System Console (^_^)")
						print("Check out object: '%s' key: '%s' already added !! (Tips: don't use same key)"%(child.name,child.scrName))
						return {'CANCELLED'}
					if child.scrEntityPtr not in keyInfo:
						keyInfo.append(child.scrEntityPtr)
					else:
						self.report({"WARNING"}, "Object same value already added !!, more info see System Console (^_^)")
						print("Check out object: '%s' value: '%s' already added !! (Tips: don't use same value)"%(child.name,child.scrEntityPtr))
						return {'CANCELLED'}
					if child.scrTransformEntity not in keyInfo:
						keyInfo.append(child.scrTransformEntity)
					else:
						self.report({"WARNING"}, "Object same value already added !!, more info see System Console (^_^)")
						print("Check out object: '%s' value: '%s' already added !! (Tips: don't use same value)"%(child.name,child.scrTransformEntity))
						return {'CANCELLED'}
					if child.scrLimitedRotatable:
						lstTotal.append(child.ObjectLinksName)
						lstTotal2.append(child.scrName)
						lstTotal3.append(child.scrEntityPtr)
						if not child.ObjectLinksName in lstObject:
							lstObject.append(child.ObjectLinksName)
							exSize+=1

					for ob in bpy.data.objects[child.name].children[:1]:
						if ob.type == 'EMPTY' and ob is not None:
							if "_sc20" in ob.name:
								makedir("scarecrow\\#Win\\scarecrow_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\scarecrow"%(stid,stid),True)
								if not scn.scrGenerateFpkd:

									fpkname="scarecrow_%s.fpk"%stid
									xmlPath="%sscarecrow\\#Win\\scarecrow_%s.fpk.xml"% (exportPath,stid)
									assets="/Assets/pes16/model/bg/%s/scarecrow/"%stid
									makedir("scarecrow\\#Win\\scarecrow_%s_fpk\\Assets\\pes16\\model\\bg\\%s\\scarecrow"%(stid,stid),True)
									assetDir="%sscarecrow\\#Win\\scarecrow_%s_fpk\\Assets\\pes16\\model\\bg\\%s\\scarecrow" % (exportPath,stid,stid)
									print('\n********************************')								
									objName = child.name
									fileName = "%s\\%s.fmdl"% (assetDir,objName)
									meshID = str(fileName).split('..')[0].split('\\')[-1:][0]	
									Asset.append(assets+meshID)	
									print('Exporting ==> %s' % meshID)
									print('********************************')
									export_fmdl(self, context, fileName, meshID, objName)
			try:
				if not scn.scrGenerateFpkd:
					copytree(commonfile,"%sscarecrow\\#Win\\scarecrow_%s_fpk\\Assets\\pes16\\model\\bg"%(exportPath,stid), False,None)
			except:
				pass
			isize+=exSize
			fox2xmlName="%sscarecrow\\#Win\\scarecrow_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\scarecrow\\%s_pes2020_00.fox2.xml" % (exportPath,stid,stid,stid)
			PesFoxXML.scrMakeXml(fox2xmlName,isize,lstTotal,lstTotal2,lstTotal3)
			if not scn.scrGenerateFpkd:
				makeXML(xmlPath, Asset, fpkname,"Fpk","FpkFile", True)
			makeXML("%sscarecrow\\#Win\\scarecrow_%s.fpkd.xml"%(exportPath,stid),"/Assets/pes16/model/bg/%s/scarecrow/%s_pes2020_00.fox2"%(stid,stid), "scarecrow_%s.fpkd"%stid,"Fpk","FpkFile", False)
			compileXML(fox2xmlName)
			self.report({"INFO"}, "Exporting scarecrow succesfully...")
			print("Exporting scarecrow succesfully...")
			if not scn.scrGenerateFpkd:
				pack_unpack_Fpk(Xmlfile)
			pack_unpack_Fpk(Xmlfile2)
			remove_dir(fpkdir)
			remove_file(Xmlfile)
			remove_dir(fpkddir)
			remove_file(Xmlfile2)
			return {'FINISHED'}
	pass

class Stadium_Banner(bpy.types.Operator):
	"""Stadium Banner"""
	bl_idname = "stadium_banner.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT")
	
	def execute(self, context):
		scn=context.scene
		stid=scn.STID
		exportPath=scn.export_path
		iSize=0
		dataListKey,hexTfrm,hexKey,kysName,files2=[],[],[],[],[]
		dirPath=str()
		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to import/export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				print( "Choose path to import/export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium id isn't correct!!")
			print("Stadium id isn't correct!!")
			return {'CANCELLED'}	
		if self.opname == "import_cheer1":
			node_group()
			Create_Parent_Part(self,context)
			for ob in bpy.data.objects:
				if ob is not None and ob.type == "MESH" and "_h_a1_" in ob.name:
					self.report({"WARNING"}, "Banner already imported !!")
					print("Banner already imported !!")
					return {'CANCELLED'}
			fpkfilename="%scheer\\#Win\\cheer_%s_h_a1.fpk" % (exportPath,stid)
			dirRemove="%scheer\\#Win\\cheer_%s_h_a1_fpk"% (exportPath,stid)
			fileRemove="%scheer\\#Win\\cheer_%s_h_a1.fpk.xml"% (exportPath,stid)

			
			if context.scene.fmdl_import_load_textures:	
				for texname in ["banner_dumy_bsm.ftex","banner_lbm.ftex","banner_lym.ftex","banner_nrm.ftex",
								"banner_srm.ftex","banner2_dumy_bsm.ftex","banner2_lym.ftex","banner2_nrm.ftex"]:
					ftexPath = "%ssourceimages\\tga\\#windx11\\%s" % (exportPath,texname)
					dirPath = "%ssourceimages\\tga\\#windx11\\" % exportPath
					ddsPath = ftexPath[:-4]+"dds"
					if os.path.isfile(ftexPath):
						try:
							Ftex.ftexToDds(ftexPath , ddsPath)
						except:
							convert_ftex(ftexPath)
						texconv(ddsPath, dirPath, " -y -l -f DXT5 -ft dds -srgb", True)
			if os.path.isfile(fpkfilename):
				pack_unpack_Fpk(fpkfilename)
				dir = os.path.dirname(fpkfilename)
				for root, directories, filenames in os.walk(dir):
					for fileName in filenames:
						filename, extension = os.path.splitext(fileName)
						if extension.lower() == '.fmdl':
							fmdlPath = os.path.join(root, fileName)
							importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename, dirPath, "CHEER1")
							print('Importing ==> %s' % fileName)
				self.report({"INFO"}, "Import banner succesfully...")
				remove_dir(dirRemove)
				remove_file(fileRemove)
		if self.opname == "import_cheer2":
			node_group()
			Create_Parent_Part(self,context)
			for ob in bpy.data.objects:
				if ob is not None and ob.type == "MESH" and "_h_a2_" in ob.name:
					self.report({"WARNING"}, "Banner already imported !!")
					print("Banner already imported !!")
					return {'CANCELLED'}
			fpkfilename="%scheer\\#Win\\cheer_%s_h_a2.fpk" % (exportPath,stid)
			dirRemove="%scheer\\#Win\\cheer_%s_h_a2_fpk"% (exportPath,stid)
			fileRemove="%scheer\\#Win\\cheer_%s_h_a2.fpk.xml"% (exportPath,stid)

			if context.scene.fmdl_import_load_textures:	
				for texname in ["banner_dumy_bsm.ftex","banner_lbm.ftex","banner_lym.ftex","banner_nrm.ftex",
								"banner_srm.ftex","banner2_dumy_bsm.ftex","banner2_lym.ftex","banner2_nrm.ftex"]:
					ftexPath = "%ssourceimages\\tga\\#windx11\\%s" % (exportPath,texname)
					dirPath = "%ssourceimages\\tga\\#windx11\\" % exportPath
					ddsPath = ftexPath[:-4]+"dds"
					print("")
					if os.path.isfile(ftexPath):
						try:
							Ftex.ftexToDds(ftexPath , ddsPath)
						except:
							convert_ftex(ftexPath)
						texconv(ddsPath, dirPath, " -y -l -f DXT5 -ft dds -srgb", True)
			if os.path.isfile(fpkfilename):
				pack_unpack_Fpk(fpkfilename)
				dir = os.path.dirname(fpkfilename)
				for root, directories, filenames in os.walk(dir):
					for fileName in filenames:
						filename, extension = os.path.splitext(fileName)
						if extension.lower() == '.fmdl':
							fmdlPath = os.path.join(root, fileName)
							importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename, dirPath, "CHEER2")
							print('Importing ==> %s' % fileName)
				self.report({"INFO"}, "Import banner succesfully...")
				remove_dir(dirRemove)
				remove_file(fileRemove)
		if self.opname == "export_cheer1":
			for child in bpy.data.objects[context.scene.part_info].children:
				if child.type == 'EMPTY' and child is not None:
					for ob in bpy.data.objects[child.name].children:
						if ob is not None:
							for ob2 in bpy.data.objects[ob.name].children:
								if ob2 is not None and  ob2.type == "MESH":
									blenderMaterial = bpy.data.objects[ob2.name].active_material
									if blenderMaterial.name != "banner_shader" and blenderMaterial.name != "banner_shader2":
										self.report({"WARNING"}, "Object %s material name isn't correct!"%ob2.name)
										print("Object %s material name isn't correct!"%ob2.name)
										return {'CANCELLED'}
			c1,c2 = len(bpy.data.objects["MESH_cheer_back1_h_a1"].children), len(bpy.data.objects["MESH_cheer_front1_h_a1"].children)
			c3,c4 = len(bpy.data.objects["MESH_cheer_left1_h_a1"].children), len(bpy.data.objects["MESH_cheer_right1_h_a1"].children)
			if c1==0 and c2==0 and c3==0 and c4==0:
				self.report({"WARNING"}, "Cannot export %s empty or no object!"%context.scene.part_info)
				print("Cannot export %s empty or no object!"%context.scene.part_info)
				return {'CANCELLED'}
			assetDir="%scheer\\#Win\\cheer_%s_h_a1_fpk\\Assets\\pes16\\model\\bg\\%s\\scenes" % (exportPath,stid,stid)
			assetDirFpkd="%scheer\\#Win\\cheer_%s_h_a1_fpkd\\Assets\\pes16\\model\\bg\\%s\\cheer" % (exportPath,stid,stid)
			assetDirname = "/Assets/pes16/model/bg/%s/scenes/" % stid
			xmlPath="%scheer\\#Win\\cheer_%s_h_a1.fpk.xml" % (exportPath,stid)
			xmldPath="%scheer\\#Win\\cheer_%s_h_a1.fpkd.xml" % (exportPath,stid)
			fpkname= "cheer_%s_h_a1.fpk" % stid
			fpkdname= "cheer_%s_h_a1.fpkd" % stid
			dirRemove="%scheer\\#Win\\cheer_%s_h_a1_fpk"% (exportPath,stid)
			fileRemove="%scheer\\#Win\\cheer_%s_h_a1.fpk.xml"% (exportPath,stid)
			dirdRemove="%scheer\\#Win\\cheer_%s_h_a1_fpkd"% (exportPath,stid)
			filedRemove="%scheer\\#Win\\cheer_%s_h_a1.fpkd.xml"% (exportPath,stid)
			foxxmlName="%s\\cheer_%s_h_a1.fox2.xml"%(assetDirFpkd,stid)
			kysName=["cheer_back1_h_a1","cheer_front1_h_a1","cheer_left1_h_a1","cheer_right1_h_a1"]
			mdltype="h_a1"
			fox2asset="/Assets/pes16/model/bg/%s/cheer/cheer_%s_h_a1.fox2" % (stid,stid)
			for child in bpy.data.objects[context.scene.part_info].children:
				if child.type == 'EMPTY' and child is not None:
					for ob in bpy.data.objects[child.name].children[:1]:
						if ob is not None:
							for ob2 in bpy.data.objects[ob.name].children[:1]:
								if ob2 is not None:
									print('\n********************************')
									makedir("cheer\\#Win\\cheer_%s_h_a1_fpk\\Assets\\pes16\\model\\bg\\%s\\scenes"%(stid,stid),True)
									makedir("cheer\\#Win\\cheer_%s_h_a1_fpkd\\Assets\\pes16\\model\\bg\\%s\\cheer"%(stid,stid),True)
									
									objName = child.name
									fmdlName = child.name
									iSize+=1
									files2.append(assetDirname +fmdlName+".fmdl")
									fileName = "%s\\%s.fmdl"% (assetDir,fmdlName)
									meshID = str(fileName).split('..')[0].split('\\')[-1:][0]
									dtlskey="%s_%s"%(str(fmdlName).split("_")[0],str(fmdlName).split("_")[1])	
									hexKey.append(hxd(cheerhexKey[kysName.index(fmdlName)],8))
									hexTfrm.append(hxd(cheerhextfrm[kysName.index(fmdlName)],8))
									dataListKey.append(dtlskey)						
									print('Exporting ==> %s' % meshID)
									print('********************************')
									export_fmdl(self, context, fileName, meshID, objName)
			makeXML(xmlPath, files2, fpkname,"Fpk","FpkFile", True)
			pack_unpack_Fpk(xmlPath)
			remove_dir(dirRemove)
			remove_file(fileRemove)
			PesFoxXML.cheerXML(foxxmlName,iSize,dataListKey,hexKey,mdltype,hexTfrm)
			compileXML(foxxmlName)
			makeXML(xmldPath, fox2asset, fpkdname,"Fpk","FpkFile", False)
			pack_unpack_Fpk(xmldPath)
			remove_dir(dirdRemove)
			remove_file(filedRemove)
			self.report({"INFO"}, "Export banner succesfully...")
		if self.opname == "export_cheer2":
			for child in bpy.data.objects[context.scene.part_info].children:
				if child.type == 'EMPTY' and child is not None:
					for ob in bpy.data.objects[child.name].children:
						if ob is not None:
							for ob2 in bpy.data.objects[ob.name].children:
								if ob2 is not None and  ob2.type == "MESH":
									blenderMaterial = bpy.data.objects[ob2.name].active_material
									if blenderMaterial.name != "banner_shader" and blenderMaterial.name != "banner_shader2":
										self.report({"WARNING"}, "Object %s material name isn't correct!"%ob2.name)
										print("Object %s material name isn't correct!"%ob2.name)
										return {'CANCELLED'}
			c1,c2 = len(bpy.data.objects["MESH_cheer_back1_h_a2"].children), len(bpy.data.objects["MESH_cheer_front1_h_a2"].children)
			c3,c4 = len(bpy.data.objects["MESH_cheer_left1_h_a2"].children), len(bpy.data.objects["MESH_cheer_right1_h_a2"].children)
			if c1==0 and c2==0 and c3==0 and c4==0:
				self.report({"WARNING"}, "Cannot export %s empty or no object!"%context.scene.part_info)
				print("Cannot export %s empty or no object!"%context.scene.part_info)
				return {'CANCELLED'}
			assetDir="%scheer\\#Win\\cheer_%s_h_a2_fpk\\Assets\\pes16\\model\\bg\\%s\\scenes" % (exportPath,stid,stid)
			assetDirFpkd="%scheer\\#Win\\cheer_%s_h_a2_fpkd\\Assets\\pes16\\model\\bg\\%s\\cheer" % (exportPath,stid,stid)
			assetDirname = "/Assets/pes16/model/bg/%s/scenes/" % stid
			xmlPath="%scheer\\#Win\\cheer_%s_h_a2.fpk.xml" % (exportPath,stid)
			xmldPath="%scheer\\#Win\\cheer_%s_h_a2.fpkd.xml" % (exportPath,stid)
			fpkname= "cheer_%s_h_a2.fpk" % stid
			fpkdname= "cheer_%s_h_a2.fpkd" % stid
			dirRemove="%scheer\\#Win\\cheer_%s_h_a2_fpk"% (exportPath,stid)
			fileRemove="%scheer\\#Win\\cheer_%s_h_a2.fpk.xml"% (exportPath,stid)
			dirdRemove="%scheer\\#Win\\cheer_%s_h_a2_fpkd"% (exportPath,stid)
			filedRemove="%scheer\\#Win\\cheer_%s_h_a2.fpkd.xml"% (exportPath,stid)
			foxxmlName="%s\\cheer_%s_h_a2.fox2.xml"%(assetDirFpkd,stid)
			kysName=["cheer_back1_h_a2","cheer_front1_h_a2","cheer_left1_h_a2","cheer_right1_h_a2"]
			mdltype="h_a2"
			fox2asset="/Assets/pes16/model/bg/%s/cheer/cheer_%s_h_a2.fox2" % (stid,stid)
			for child in bpy.data.objects[context.scene.part_info].children:
				if child.type == 'EMPTY' and child is not None:
					for ob in bpy.data.objects[child.name].children[:1]:
						if ob is not None:
							for ob2 in bpy.data.objects[ob.name].children[:1]:
								if ob2 is not None:
									print('\n********************************')
									makedir("cheer\\#Win\\cheer_%s_h_a2_fpk\\Assets\\pes16\\model\\bg\\%s\\scenes"%(stid,stid),True)
									makedir("cheer\\#Win\\cheer_%s_h_a2_fpkd\\Assets\\pes16\\model\\bg\\%s\\cheer"%(stid,stid),True)
									
									objName = child.name
									fmdlName = child.name
									iSize+=1
									files2.append(assetDirname +fmdlName+".fmdl")
									fileName = "%s\\%s.fmdl"% (assetDir,fmdlName)
									meshID = str(fileName).split('..')[0].split('\\')[-1:][0]
									dtlskey="%s_%s"%(str(fmdlName).split("_")[0],str(fmdlName).split("_")[1])	
									hexKey.append(hxd(cheerhexKey[kysName.index(fmdlName)],8))
									hexTfrm.append(hxd(cheerhextfrm[kysName.index(fmdlName)],8))
									dataListKey.append(dtlskey)						
									print('Exporting ==> %s' % meshID)
									print('********************************')
									export_fmdl(self, context, fileName, meshID, objName)
			makeXML(xmlPath, files2, fpkname,"Fpk","FpkFile", True)
			pack_unpack_Fpk(xmlPath)
			remove_dir(dirRemove)
			remove_file(fileRemove)
			PesFoxXML.cheerXML(foxxmlName,iSize,dataListKey,hexKey,mdltype,hexTfrm)
			compileXML(foxxmlName)
			makeXML(xmldPath, fox2asset, fpkdname,"Fpk","FpkFile", False)
			pack_unpack_Fpk(xmldPath)
			remove_dir(dirdRemove)
			remove_file(filedRemove)
			self.report({"INFO"}, "Export banner succesfully...")
		return {'FINISHED'}
	pass

class Staff_Coach_Pos(bpy.types.Operator):
	"""Load / Assign Staff Position"""
	bl_idname = "staff_pos.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT")
	
	def execute(self, context):
		scn=context.scene
		stid=scn.STID
		if "STAFF" not in bpy.data.objects:
			Create_Parent_Part(self, context)
		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to load/assign %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				print("Choose path to load/assign %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
	# Staff Coach
		if self.opname == "loadcoach":
			inner_path = 'Object'
			for coach in ('coach_home', 'coach_away'):
				if not coach in bpy.data.objects:
					bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, coach),directory=os.path.join(base_file_blend, inner_path),filename=coach)
					for ob in bpy.data.objects:
						if ob.type == "MESH":
							if ob.name == "coach_home":
								ob.rotation_mode = "QUATERNION"
								ob.rotation_quaternion.w = -0.007337
								ob.rotation_quaternion.z= -0.999973
								ob.location.x= -4.893455
								ob.location.y = 37.3332*-1
							if ob.name == "coach_away":
								ob.rotation_mode = "QUATERNION"
								ob.rotation_quaternion.w = -0.007337
								ob.rotation_quaternion.z = -0.999973
								ob.location.x = 5.69787
								ob.location.y = 37.2800179*-1
							if ob.name in ['coach_home', 'coach_away']:
								ob.parent = bpy.data.objects['Staff Coach']
					self.report({"INFO"}, "Coach loaded succesfully...")
				else:
					self.report({"WARNING"}, "Coach already loaded !!")
			return {'FINISHED'}
		if self.opname == "assigncoach":

			for coach in ('coach_home', 'coach_away'):
				if not coach in bpy.data.objects:
					self.report({"WARNING"}, "Load Coach first..")
					return {'CANCELLED'}	

			pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd".format(scn.export_path,stid))
			xmlPath="{0}staff\\#Win\\staff_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\staff\\{3}_2018_common_coach.fox2.xml".format(scn.export_path,stid,stid,stid)
			coachXml=open(xml_dir+"StaffCoach.xml", "rt").read()

			for ob in bpy.data.objects['Staff Coach'].children:
				if ob.type == "MESH":
					if ob.name == "coach_home":
						bpy.data.objects[ob.name].rotation_mode = "QUATERNION"
						coachXml=coachXml.replace("q_w_home","{0}".format(ob.rotation_quaternion[0]))
						coachXml=coachXml.replace("q_y_home","{0}".format(ob.rotation_quaternion[3]))
						coachXml=coachXml.replace("r_x_home","{0}".format(ob.location[0]))
						coachXml=coachXml.replace("r_z_home","{0}".format(ob.location[1]*-1))
					if ob.name == "coach_away":
						bpy.data.objects[ob.name].rotation_mode = "QUATERNION"
						coachXml=coachXml.replace("q_w_away","{0}".format(ob.rotation_quaternion[0]))
						coachXml=coachXml.replace("q_y_away","{0}".format(ob.rotation_quaternion[3]))
						coachXml=coachXml.replace("r_x_away","{0}".format(ob.location[0]))
						coachXml=coachXml.replace("r_z_away","{0}".format(ob.location[1]*-1))	

			writecoachxml=open(xmlPath, "wt")
			writecoachxml.write(coachXml)
			writecoachxml.flush(),writecoachxml.close()
			compileXML(xmlPath)
			pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			self.report({"INFO"}, "Coach assign succesfully...")
			return {'FINISHED'}
	# Staff Walk
		if self.opname == "loadwalk":
			for child in bpy.data.objects[context.scene.part_info].children:
				for ob in bpy.data.objects[child.name].children:
					if ob.type == "EMPTY":
						if ob.name in PesStaff.staff_walk_list:
							if 'gu_' in ob.name or 'st_' in ob.name:
								self.report({"WARNING"}, "Staff Walk already loaded !!")
								return {'CANCELLED'}

			self.report({"INFO"}, "Load Staff Walk succesfully...")
			PesStaff.importStaffWalk(self, context)
			remove_dir("{0}staff\\#Win\\staff_{1}_fpk".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpk.xml".format(scn.export_path,stid))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			return {'FINISHED'}
		if self.opname == "assignwalk":
			pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd".format(scn.export_path,stid))
			PesStaff.exportStaffWalk(self, context)
			self.report({"INFO"}, "Assign Staff Walk succesfully...")
			xmlPath="{0}staff\\#Win\\staff_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\staff\\{3}_2018_common_walk.fox2.xml".format(scn.export_path,stid,stid,stid)
			compileXML(xmlPath)
			pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			return {'FINISHED'}


		if self.opname == "loadballboy":
			try:
				PesStaff.importBallboy(self, context)
				self.report({"INFO"}, "Load Ballboy succesfully...")
			except Exception as e:
				self.report({"WARNING"}, format(e))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpk".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpk.xml".format(scn.export_path,stid))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			return {'FINISHED'}
		if self.opname == "assignballboy":
			try:
				PesStaff.Ballboy_Assign(self,context)
				self.report({"INFO"}, "Assign Ballboy succesfully...")
			except Exception as e:
				self.report({"WARNING"}, format(e))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			return {'FINISHED'}

		if self.opname == "loadcamcrew":
			try:
				PesStaff.importCamCrew(self, context)
				self.report({"INFO"}, "Load Cam Crew succesfully...")
			except Exception as e:
				self.report({"WARNING"}, format(e))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpk".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpk.xml".format(scn.export_path,stid))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			return {'FINISHED'}

		if self.opname == "assigncamcrew":
			pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd".format(scn.export_path,stid))
			try:
				PesStaff.CamCrew_Assign(self,context)
				self.report({"INFO"}, "Assign Cam Crew succesfully...")
			except Exception as e:
				self.report({"WARNING"}, format(e))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			return {'FINISHED'}

		if self.opname == "loadSteward":
			try:
				PesStaff.importSteward(self, context)
				self.report({"INFO"}, "Load Steward succesfully...")
			except Exception as e:
				self.report({"WARNING"}, format(e))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpk".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpk.xml".format(scn.export_path,stid))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
			return {'FINISHED'}

		if self.opname == "assignSteward":
			pack_unpack_Fpk("{0}staff\\#Win\\staff_{1}.fpkd".format(scn.export_path,stid))
			try:
				PesStaff.Steward_Assign(self,context)
				self.report({"INFO"}, "Assign Steward succesfully...")
			except Exception as e:
				self.report({"WARNING"}, format(e))
			remove_dir("{0}staff\\#Win\\staff_{1}_fpkd".format(scn.export_path,stid))
			remove_file("{0}staff\\#Win\\staff_{1}.fpkd.xml".format(scn.export_path,stid))
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
		Rslt=str()
		stid=context.scene.STID
		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to swap id e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Choose path to swap id e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}
		for child in bpy.data.objects[context.scene.part_info].children:
			if child.type == 'EMPTY' and child is not None:
				for ob in bpy.data.objects[child.name].children:
					if ob is not None:
						for ob2 in bpy.data.objects[ob.name].children:
							if ob2 is not None and  ob2.type == "MESH":
								blenderMaterial = bpy.data.objects[ob2.name].active_material
								for nodes in blenderMaterial.node_tree.nodes:
									if nodes.type == "TEX_IMAGE":
										blenderTexture = blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory
										if "st" in blenderTexture:
											oldID=re.findall(r'\d+', blenderTexture)
											try:
												for i in range(100):
													Rslt="st"+oldID[i] 
											except:
												pass
											print("Swap id from ({0}) to ({1}) in object ({2}) in node ({3}) succesfully...".format(Rslt,stid,ob2.name,nodes.name))
											assetDirname = blenderTexture
											newid=str(assetDirname).replace(assetDirname,"/Assets/pes16/model/bg/%s/sourceimages/tga/"%stid)
											blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory=newid
		self.report( {"INFO"}, "Swap stadium id succesfully!" )
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
		bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, tvObject),directory=os.path.join(base_file_blend, inner_path),filename=tvObject)
		return {'FINISHED'}
	pass

def r_side(context):
	ob = context.active_object
	if str(ob.name).startswith("L_"):
		if ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type == 'POINT':
			light_sidelist=[("L_FRONT","FRONT SIDE","FRONT SIDE for LightBillboard"),
							("L_LEFT","LEFT SIDE","LEFT SIDE for LightBillboard"),
							("L_RIGHT","RIGHT SIDE","RIGHT SIDE for LightBillboard"),
							("L_BACK","BACK SIDE","BACK SIDE for LightBillboard")]
			bpy.types.Scene.l_lit_side = EnumProperty(name="Select Side for Lights",items=light_sidelist)
	elif str(ob.name).startswith("H_"):
		if ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type == 'AREA':
			light_sidelist=[("H_FRONT","FRONT SIDE","FRONT SIDE for Halo"),
							("H_LEFT","LEFT SIDE","LEFT SIDE for Halo"),
							("H_RIGHT","RIGHT SIDE","RIGHT SIDE for Halo"),
							("H_BACK","BACK SIDE","BACK SIDE for Halo")]
			bpy.types.Scene.l_lit_side = EnumProperty(name="Select Side for Lights",items=light_sidelist)
	elif str(ob.name).startswith("F_"):
		if ob.type=='LIGHT' and bpy.data.lights[ob.data.name].type == 'AREA':
			light_sidelist=[("F_FRONT","FRONT SIDE","FRONT SIDE for LensFlare"),
							("F_LEFT","LEFT SIDE","LEFT SIDE for LensFlare"),
							("F_RIGHT","RIGHT SIDE","RIGHT SIDE for LensFlare"),
							("F_BACK","BACK SIDE","BACK SIDE for LensFlare")]
			bpy.types.Scene.l_lit_side = EnumProperty(name="Select Side for Lights",items=light_sidelist)
	else:
		return True

class Refresh_Light_Side(bpy.types.Operator):
	"""Refresh Lights Side"""
	bl_idname = "lights_side.operator"
	bl_label = str()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT")
	
	def execute(self, context):
		side_refresh = r_side(context)
		if side_refresh:
			self.report( {"WARNING"}, "Light object name isn't correct!,more info see System Console (^_^)")
			print("\nLight object name must startswith: \n(L_) for LightBillboard -> object type (Point). \n(H_) for Halo -> object type (Area). \n(F_) for LensFlare -> object type (Area).")
			return {'CANCELLED'}
		return {'FINISHED'}
	pass


class Light_FX(bpy.types.Operator):
	"""Light FX Exporter"""
	bl_idname = "lightfx.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT") and (context.active_object and context.active_object)
	
	def execute(self, context):
		stid = context.scene.STID
		x=int()
		if self.opname == "set_lfx_side":
			side_refresh = r_side(context)
			if side_refresh:
				self.report( {"WARNING"}, "Light object name isn't correct!,more info see System Console (^_^)")
				print("\nLight object name must startswith: \n(L_) for LightBillboard -> object type (Point). \n(H_) for Halo -> object type (Area). \n(F_) for LensFlare -> object type (Area).")
				return {'CANCELLED'}
			try:
				for l_ob in bpy.context.selected_objects:
					if l_ob.type == 'LIGHT':
						l_ob.parent = bpy.data.objects[bpy.context.scene.l_lit_side]
						l_ob.l_Energy = context.scene.l_fxe
			except Exception as exception:
				self.report({"WARNING"},format(exception))
				print(format(exception))
				return {'CANCELLED'}


			return {'FINISHED'}
		if self.opname == "export_lfx":
			scn = bpy.context.scene
			sideName,LSide=[],[]
			
			if len(stid) == 5:
				if context.scene.export_path == str():
					self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					return {'CANCELLED'}

				if not stid in context.scene.export_path:
					self.report({"WARNING"}, "Stadium ID doesn't match!!")
					print("Stadium ID doesn't match!!")
					return {'CANCELLED'}

				if not context.scene.export_path.endswith(stid+"\\"):
					self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					return {'CANCELLED'}

				l1,l2 = len(bpy.data.objects["L_BACK"].children), len(bpy.data.objects["L_FRONT"].children)
				l3,l4 = len(bpy.data.objects["L_LEFT"].children), len(bpy.data.objects["L_RIGHT"].children)
				if l1==0 and l2==0 and l3==0 and l4==0:
					self.report({"WARNING"}, "Cannot export LightBillboard empty or no object!")
					print("Cannot export LightBillboard empty or no object!")
					return {'CANCELLED'}

				f1,f2 = len(bpy.data.objects["F_BACK"].children), len(bpy.data.objects["F_FRONT"].children)
				f3,f4 = len(bpy.data.objects["F_LEFT"].children), len(bpy.data.objects["F_RIGHT"].children)
				if f1==0 and f2==0 and f3==0 and f4==0:
					self.report({"WARNING"}, "Cannot export LensFlare empty or no object!")
					print("Cannot export LensFlare empty or no object!")
					return {'CANCELLED'}

				for child in bpy.data.objects["LightBillboard"].children:	
					if child.type == "EMPTY":
						for ob in bpy.data.objects[child.name].children:
							if ob.type == "LIGHT":
								ol = bpy.data.lights[ob.data.name]
								if ol.type != "POINT":
									self.report({"WARNING"}, "Object %s type isn't POINT!"%ob.name)
									print("Object %s type isn't POINT!, Checkout object in %s -> %s -> %s"%(ob.name,child.parent.name,ob.parent.name, ob.name))
									return {'CANCELLED'}
								if ol.type == "POINT" and not "L_" in ob.name:
									self.report({"WARNING"}, "Object (%s) name isn't correct!"%ob.name)
									print("Object (%s) name isn't correct!, Checkout object in %s -> %s -> %s"%(ob.name,child.parent.name,ob.parent.name, ob.name))
									return {'CANCELLED'}
				for child in bpy.data.objects["LensFlare"].children:
					if child.type == "EMPTY":
						for ob in bpy.data.objects[child.name].children:
							if ob.type == "LIGHT":
								ol = bpy.data.lights[ob.data.name]
								if ol.type != "AREA":
									self.report({"WARNING"}, "Object %s type isn't AREA!"%ob.name)
									print("Object %s type isn't AREA!, Checkout object in %s -> %s -> %s"%(ob.name,child.parent.name,ob.parent.name, ob.name))
									return {'CANCELLED'}
								if ol.type == "AREA" and not "F_" in ob.name:
									self.report({"WARNING"}, "Object (%s) name isn't correct!"%ob.name)
									print("Object (%s) name isn't correct!, Checkout object in %s -> %s -> %s"%(ob.name,child.parent.name,ob.parent.name, ob.name))
									return {'CANCELLED'}
				for child in bpy.data.objects["Halo"].children:
					if child.type == "EMPTY":
						for ob in bpy.data.objects[child.name].children:
							if ob.type == "LIGHT":
								ol = bpy.data.lights[ob.data.name]
								if ol.type != "AREA":
									self.report({"WARNING"}, "Object %s type isn't AREA!"%ob.name)
									print("Object %s type isn't AREA!, Checkout object in %s -> %s -> %s"%(ob.name,child.parent.name,ob.parent.name, ob.name))
									return {'CANCELLED'}
								if ol.type == "AREA" and not "H_" in ob.name:
									self.report({"WARNING"}, "Object (%s) name isn't correct!"%ob.name)
									print("Object (%s) name isn't correct!, Checkout object in %s -> %s -> %s"%(ob.name,child.parent.name,ob.parent.name, ob.name))
									return {'CANCELLED'}
				
				makedir("effect\\#Win\\effect_{0}_{1}_fpk\\Assets\\pes16\\model\\bg\\{2}\\effect\\locator".format(scn.STID,scn.time_mode,scn.STID), True)
				xmlPath="{0}effect\\#Win\\effect_{1}_{2}.fpk.xml".format(scn.export_path, scn.STID,scn.time_mode)
				xmlConfigPath= "{0}effect\\#Win\\effect_{1}_{2}_fpk\\effect_config.xml".format(scn.export_path, scn.STID,scn.time_mode)
				
				p_Ass=[]
				print("\nStarting Light FX Export !!\n")
				try:
					hdr_file=open(lightFxPath+"extras21.dll","rb")
					hdr_file.seek(942,0)
					dat13=hdr_file.read(236)
					dat14=hdr_file.read(28)
					dat15=hdr_file.read(68)
					hdr_file.flush(),hdr_file.close()

					dirname="effect\\#Win\\effect_"+scn.STID+"_"+scn.time_mode+"_fpk"
					lamp_list=["L_FRONT","front3","L_LEFT","left3","L_RIGHT","right3","L_BACK","back3"]

					def lamp_side(p_name,l_count):
						
						i=lamp_list.index(p_name)
						outpath_lightfx = '{0}{1}\\Assets\\pes16\\model\\bg\\{2}\\effect\\locator\\locstar_{3}_{4}.model'.format(scn.export_path,dirname,scn.STID,lamp_list[i+1],scn.time_mode)
							
						lfx=open(outpath_lightfx,"wb")
						lfx.write(dat13)
						lfx.write(pack("4I",(48*l_count+40),l_count,0x72617473,0))
						return lfx
					for p_lamp in bpy.data.objects['LightBillboard'].children:
						sideList=["locstar_back3_%s"%scn.time_mode,
									"locstar_front3_%s"%scn.time_mode,
									"locstar_left3_%s"%scn.time_mode,
									"locstar_right3_%s"%scn.time_mode
						]
						
						if len(p_lamp.children) > 0:

							sideName.append(sideList[L_P_List.index(p_lamp.name)])
							LSide.append(L_Side[L_P_List.index(p_lamp.name)])
							assetName="/Assets/pes16/model/bg/{0}/effect/locator/locstar_{1}3_{2}.model".format(scn.STID,L_Side[L_P_List.index(p_lamp.name)],scn.time_mode)
							p_Ass.append(assetName)
							l_count=len(p_lamp.children)
							lfx=lamp_side(p_lamp.name,l_count)
							
							for lamp in p_lamp.children:
								l_energy=lamp.l_Energy
								lfx.write(pack("12f",l_energy,0,0,lamp.location.x,0,1,0,lamp.location.z,0,1,0,(lamp.location.y*-1)))
							
							for i in range(l_count):
								if i == 0:
									x=4*l_count
								else:
									x+=28
								lfx.write(pack("I",x))
						
							for p in range(l_count):
								lfx.write(dat14)
							
							sz1=lfx.tell()
							lfx.write(dat15)
							lfx.seek(64,0)
							lfx.write(pack("I",sz1-24))
							lfx.close()	
					PesFoxXML.lightFxXml(xmlConfigPath,sideName, L_Side)
					p_Ass.append('effect_config.xml')
					makeXML(context.scene.export_path+"effect\\#Win\\effect_{0}_{1}.fpk.xml".format(stid,scn.time_mode), p_Ass, "effect_{0}_{1}.fpk".format(stid,scn.time_mode),"Fpk","FpkFile", True)
					self.report( {"INFO"}, " Light FX Exported has been Successfully... ")
				except Exception as msg:
					self.report( {"WARNING"}, format(msg))
					return {'CANCELLED'}
					
				pack_unpack_Fpk(xmlPath)
				remove_file(xmlPath)
				remove_dir("{0}effect\\#Win\\effect_{1}_{2}_fpk".format(scn.export_path, scn.STID,scn.time_mode))
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
			parentlist = [(ob.name,ob.name,ob.name) for ob in (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if ob.name in main_list 
			if ob.name not in ['LIGHTS','L_FRONT','L_BACK','L_RIGHT','L_LEFT','LightBillboard','LensFlare','Halo','Staff Coach','Steward', 'Staff Walk','Ballboy','Cameraman Crew']]
			parentlist.sort(reverse=0)
		else:
			parentlist = [("MESH_"+ob.name,"MESH_"+ob.name,"MESH_"+ob.name) for ob in (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if ob.name in main_list
			if ob.name not in ['LIGHTS','L_FRONT','L_BACK','L_RIGHT','L_LEFT', 'MESH_CROWD', 'MESH_FLAGAREA','Staff Coach','Steward', 'Staff Walk','Ballboy','Cameraman Crew']]
			parentlist.sort(reverse=1)
		if scn.part_info == "AD":
			parentlist.sort(reverse=0)
		bpy.types.Object.droplist = EnumProperty(name="Parent List", items=parentlist)
		for p_ob in bpy.data.objects:
			if p_ob.type == 'EMPTY' and p_ob.parent and p_ob.name in parent_main_list :
				try:
					if scn.part_info == "AUDIAREA" or scn.part_info == "FLAGAREA" or scn.part_info == "LIGHTS" or scn.part_info == "TV":
						self.droplist = p_ob.parent.name
					else:
						self.droplist = "MESH_"+p_ob.parent.name
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
		mainColumn=mainColumn.row()
		mainColumn.prop(mesh, "fmdl_alpha_enum_select", text='Alpha')
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(mesh, "fmdl_shadow_enum_select", text='Shadow')
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(mesh, "TwoSided")
		mainColumn.prop(mesh, "Transparent")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(mesh, "fmdl_flags_castshadow")
		mainColumn.prop(mesh, "fmdl_flags_invisible")
		if mesh.fmdl_alpha_enum_select == "Custom":
			mainColumn = self.layout.column()
			mainColumn=mainColumn.row()
			mainColumn.prop(mesh, "fmdl_alpha_enum")
		if mesh.fmdl_shadow_enum_select == "Custom":
			mainColumn = self.layout.column()
			mainColumn=mainColumn.row()
			mainColumn.prop(mesh, "fmdl_shadow_enum")

class FDMDL_OT_Import_Main_Stadium(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	"""Import Main Stadium"""
	bl_idname = "importmain.operator"
	bl_label = "Import Main Stadium"
	
	import_label = "PES FMDL (.fpk)"
	
	filename_ext = ".fpk"
	filter_glob : bpy.props.StringProperty(default="*.fpk", options={'HIDDEN'})

	def execute(self, context):
		node_group()
		fpkfilename = self.filepath
		with open(csvPath, "w") as f:
			f.write(fpkfilename)
		fpkdir = os.path.dirname(fpkfilename)
		stid=context.scene.STID
		fn = os.path.basename(fpkfilename)
		if "_" in fn:
			self.report({"WARNING"}, "Fpk file is not main stadium!!")
			return {'CANCELLED'}
		if not os.path.isfile(fpkfilename):
			self.report({"WARNING"}, "Fpk file doesn't select!!")
			return {'CANCELLED'}
		if not fpkfilename.endswith(".fpk"):
			self.report({"WARNING"}, "File not fpk format!!")
			return {'CANCELLED'}
		if fpkfilename == str():
			self.report({"WARNING"}, "Fpk path can't be empty!!")
			return {'CANCELLED'}
		if len(stid) == 5:
			if not stid in fpkfilename:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}

		getTextureDir = str()
		if context.scene.fmdl_import_load_textures:
			textureDir = f"{findDirectory(fpkdir)}"
			win11Dir = findTextureDirectory(textureDir)
			if os.path.exists(win11Dir):
				getTextureDir = getDirPath(win11Dir)
			if os.path.exists(getTextureDir):
				textureLoad(getTextureDir)
		try:
			fpk = ' "' + fpkfilename + '"'
			os.system('"' + GZSPATH + fpk + '"')
			dir = os.path.dirname(fpkfilename)
			for root, directories, filenames in os.walk(dir):
				for fileName in filenames:
					filename, extension = os.path.splitext(fileName)
					if extension.lower() == '.fmdl':
						fmdlPath = os.path.join(root, fileName)
						importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename, getTextureDir, "MAIN")
						print('Importing ==> %s' % fileName)
			remove_dir("%s\\%s_fpk"%(fpkdir,stid))
			remove_file("%s\\%s.fpk.xml"%(fpkdir,stid))
			print('Importing stadium succesfully...!')
			self.report({"INFO"}, "Importing main stadium succesfully...!")
		except Exception as e:
			self.report({"WARNING"}, "Error: FMDL format doesn't support !!")
			print("Error: FMDL format doesn't support !!,", format(e))
			return {'CANCELLED'}
		return {'FINISHED'}

class FDMDL_OT_Import_Extra_Stadium(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	"""Import Extra Stadium"""
	bl_idname = "importextra.operator"
	bl_label = "Import Extra Stadium"
	
	import_label = "PES FMDL (.fpk)"
	
	filename_ext = ".fpk"
	filter_glob : bpy.props.StringProperty(default="*.fpk", options={'HIDDEN'})

	def execute(self, context):
		node_group()
		fpkfilename = self.filepath
		with open(csvPath, "w") as f:
			f.write(fpkfilename)
		fpkdir = os.path.dirname(fpkfilename)
		stid=context.scene.STID
		fn = os.path.basename(fpkfilename)
		if "_" not in fn:
			self.report({"WARNING"}, "Fpk file is not extra stadium!!")
			return {'CANCELLED'}
		if not os.path.isfile(fpkfilename):
			self.report({"WARNING"}, "Fpk file doesn't select!!")
			return {'CANCELLED'}
		if not fpkfilename.endswith(".fpk"):
			self.report({"WARNING"}, "File not fpk format!!")
			return {'CANCELLED'}
		if fpkfilename == str():
			self.report({"WARNING"}, "Fpk path can't be empty!!")
			return {'CANCELLED'}
		if len(stid) == 5:
			if not stid in fpkfilename:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}

		getTextureDir = str()
		if context.scene.fmdl_import_load_textures:
			textureDir = f"{findDirectory(fpkdir)}"
			win11Dir = findTextureDirectory(textureDir)
			if os.path.exists(win11Dir):
				getTextureDir = getDirPath(win11Dir)
			if os.path.exists(getTextureDir):
				textureLoad(getTextureDir)
		try:
			fpk = ' "' + fpkfilename + '"'
			os.system('"' + GZSPATH + fpk + '"')
			dir = os.path.dirname(fpkfilename)
			for root, directories, filenames in os.walk(dir):
				for fileName in filenames:
					filename, extension = os.path.splitext(fileName)
					if extension.lower() == '.fmdl':
						fmdlPath = os.path.join(root, fileName)
						importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename, getTextureDir, "EXTRA")
						print('Importing ==> %s' % fileName)
			remove_dir("%s\\%s_df_fpk"%(fpkdir,stid))
			remove_dir("%s\\%s_dr_fpk"%(fpkdir,stid))
			remove_dir("%s\\%s_nf_fpk"%(fpkdir,stid))
			remove_dir("%s\\%s_nr_fpk"%(fpkdir,stid))
			remove_file("%s\\%s_df.fpk.xml"%(fpkdir,stid))
			remove_file("%s\\%s_dr.fpk.xml"%(fpkdir,stid))
			remove_file("%s\\%s_nf.fpk.xml"%(fpkdir,stid))
			remove_file("%s\\%s_nr.fpk.xml"%(fpkdir,stid))
			print('Importing stadium succesfully...!')
			self.report({"INFO"}, "Importing extra stadium succesfully...!")
		except Exception as e:
			self.report({"WARNING"}, "Error: FMDL format doesn't support !!")
			print("Error: FMDL format doesn't support !!,", format(e))
			return {'CANCELLED'}
		return {'FINISHED'}

def makeXML(filename, files, Name,FpkType, xsitype, uselist):

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
	xml_str = root.toprettyxml(indent = "\t")
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

def Crowd_Import(filename, c_par):

	side_pointers = []
	audifile=open(filename, 'rb')
	audifile.seek(0x08, 0)  #skip first 8 bytes in header ... unknown? i.e. jump to offset 0x08 in file
	#let's read all 12 pointers for 12 sides in total
	for i in range(12):
		side_group_ptr = unpack('<I', audifile.read(4))[0]  # 32-bit int at offset 8 in header
		side_pointers.append(side_group_ptr)
	
	for side_group_ptr in side_pointers:
		audifile.seek(side_group_ptr, 0)  # 0 at 2nd param means absolute offset, from file start, not relative to current position
		side = unpack('B', audifile.read(1))[0] # audiarea side
		level = unpack('B', audifile.read(1))[0] # audiarea levels, mean level of side
	   
		group_len = unpack('H', audifile.read(2))[0] # unsigned short len of group
		if group_len > 0:
			# read the address of the 1st group:
			groups_start = unpack('<I', audifile.read(4))[0]  # 1st pointer - 32-bit int at offset 4 bytes after group_len
			# jump where 1st pointer tells you
			audifile.seek(groups_start, 0)  # again, absolute offset, from the start of the file
			
			verts=[]
			uvmap=[]
			faces=[]
			num = 0
			c_typeVlist = []
			crowd_name=crowd_side[side]+str(level+1)
			crowd_type=0
			crowd_type_name='UltraHome'
			for g in range(group_len):
				# skip the initial 0x18 bytes in group (0x18 bytes before "Len of mesh (faces)"
				audifile.seek(0x18, 1)  # very important - 2nd param for seek is 1 - this jump is RELATIVE to the old position in file!
				mesh_len =  unpack('<2H', audifile.read(4))[0] # unsigned short len of faces
				
				for u in range(mesh_len):
					unk0_float =  unpack('<1f', audifile.read(4))[0] # float
					unk0_uint = unpack('<I', audifile.read(4))[0] # unsigned int
					c_type =  unpack('<2f', audifile.read(8))[0] # float Crowd type
					crowd_type=c_type	
					
					face = []
					for w in range(4): # data of vertices
						ver = unpack('<3f', audifile.read(12))
						verts.append(ver)
						face.append(num)
						num += 1
					for m in range(4): # data of uvs
						uvs = unpack('<2f', audifile.read(8))
						uvmap.append(uvs)
					faces.append(face)

					# get audiarea type standing normal
					if crowd_type <= 1.0 and crowd_type >= 0.90:
						c_typeVlist.append((crowd_typedict[0], face))
					elif crowd_type <= 0.90 and crowd_type >= 0.86:
						c_typeVlist.append((crowd_typedict[1], face))
					elif c_type <= 0.86 and crowd_type >= 0.80:
						c_typeVlist.append((crowd_typedict[2], face))
					elif c_type <= 0.80 and crowd_type >= 0.70:
						c_typeVlist.append((crowd_typedict[3], face))
					elif c_type <= 0.70 and crowd_type >= 0.60:
						c_typeVlist.append((crowd_typedict[4], face))
					elif c_type <= 0.60 and crowd_type >= 0.50:
						c_typeVlist.append((crowd_typedict[5], face))
					elif c_type <= 0.50 and crowd_type >= 0.40:
						c_typeVlist.append((crowd_typedict[6], face))
					elif c_type <= 0.40 and crowd_type >= 0.30:
						c_typeVlist.append((crowd_typedict[7], face))
					elif c_type <= 0.30 and crowd_type >= 0.20:
						c_typeVlist.append((crowd_typedict[8], face))
					elif c_type <= 0.20 and crowd_type >= 0.10:
						c_typeVlist.append((crowd_typedict[9], face))
					elif c_type <= 0.10 and crowd_type >= 0.00:
						c_typeVlist.append((crowd_typedict[10], face))
					# get audiarea type standing non-chair
					elif crowd_type <= 3.0 and crowd_type >= 2.90:
						c_typeVlist.append((crowd_typedict[11], face))
					elif crowd_type <= 2.90 and crowd_type >= 2.86:
						c_typeVlist.append((crowd_typedict[12], face))
					elif c_type <= 2.86 and crowd_type >= 2.80:
						c_typeVlist.append((crowd_typedict[13], face))
					elif c_type <= 2.80 and crowd_type >= 2.70:
						c_typeVlist.append((crowd_typedict[14], face))
					elif c_type <= 2.70 and crowd_type >= 2.60:
						c_typeVlist.append((crowd_typedict[15], face))
					elif c_type <= 2.60 and crowd_type >= 2.50:
						c_typeVlist.append((crowd_typedict[16], face))
					elif c_type <= 2.50 and crowd_type >= 2.40:
						c_typeVlist.append((crowd_typedict[17], face))
					elif c_type <= 2.40 and crowd_type >= 2.30:
						c_typeVlist.append((crowd_typedict[18], face))
					elif c_type <= 2.30 and crowd_type >= 2.20:
						c_typeVlist.append((crowd_typedict[19], face))
					elif c_type <= 2.20 and crowd_type >= 2.10:
						c_typeVlist.append((crowd_typedict[20], face))
					elif c_type <= 2.10 and crowd_type >= 2.00:
						c_typeVlist.append((crowd_typedict[21], face))
					# get audiarea type standing with chair
					elif crowd_type <= 5.0 and crowd_type >= 4.90:
						c_typeVlist.append((crowd_typedict[22], face))
					elif crowd_type <= 4.90 and crowd_type >= 4.86:
						c_typeVlist.append((crowd_typedict[23], face))
					elif c_type <= 4.86 and crowd_type >= 4.80:
						c_typeVlist.append((crowd_typedict[24], face))
					elif c_type <= 4.80 and crowd_type >= 4.70:
						c_typeVlist.append((crowd_typedict[25], face))
					elif c_type <= 4.70 and crowd_type >= 4.60:
						c_typeVlist.append((crowd_typedict[26], face))
					elif c_type <= 4.60 and crowd_type >= 4.50:
						c_typeVlist.append((crowd_typedict[27], face))
					elif c_type <= 4.50 and crowd_type >= 4.40:
						c_typeVlist.append((crowd_typedict[28], face))
					elif c_type <= 4.40 and crowd_type >= 4.30:
						c_typeVlist.append((crowd_typedict[29], face))
					elif c_type <= 4.30 and crowd_type >= 4.20:
						c_typeVlist.append((crowd_typedict[30], face))
					elif c_type <= 4.20 and crowd_type >= 4.10:
						c_typeVlist.append((crowd_typedict[31], face))
					elif c_type <= 4.10 and crowd_type >= 4.00:
						c_typeVlist.append((crowd_typedict[32], face))

			print("\n")
			print("***"*20)
			print("Audiarea Side:",crowd_name)
			mesh = bpy.data.meshes.new(crowd_name)
			mesh.from_pydata(verts, [], faces)
			mesh.update()
			mesh.uv_layers.new(name='audi_seat_map')
			bm = bmesh.new()
			bm.from_mesh(mesh)
			uvlayers = bm.loops.layers.uv['audi_seat_map']
			for face in bm.faces:
				for uvlayer in face.loops:
					uvlayer[uvlayers].uv.x = uvmap[uvlayer.vert.index][0]
					uvlayer[uvlayers].uv.y = uvmap[uvlayer.vert.index][1]
			bm.to_mesh(mesh)
			bm.free()
			object = bpy.data.objects.new(crowd_name, mesh)

			object.location = Vector((0,0,0))
			object.rotation_euler[0] = math.radians(90) # in order vertices is wrong position from Y to Z, so need to rotate object to correct vertices direction
			
			col = bpy.data.collections.get("Collection")
			col.objects.link(object)
			# assign audiarea type to each mesh specific faces where the type audiarea placed
			vg=object.vertex_groups
			for crowd_num_type in c_typeVlist:
				crowd_type_name=crowd_num_type[0]
				if crowd_type_name not in vg:
					vg.new(name=crowd_type_name)
					if "C1" in crowd_type_name:
						print("Audiarea Type: %s -> Stance Type: Normal"%crowd_type_name)
					elif "C2" in crowd_type_name:
						print("Audiarea Type: %s -> Stance Type: Standing Non-chair"%crowd_type_name)
					else:
						print("Audiarea Type: %s -> Stance Type: Standing with Chair"%crowd_type_name)
				vg[crowd_type_name].add(crowd_num_type[1], 1.0, 'ADD')
			print("***"*20)
				
			# move objects to crowd parent
			parent = bpy.data.objects.get(c_par)
			child = bpy.data.objects.get(crowd_name)
			child.parent = parent

	# apply objects transform
	if bpy.ops.object.mode_set():
		bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	for ob in bpy.data.objects:
		if ob.name in crowd_part:
			ob.select_set(True)
	bpy.ops.object.transform_apply(location=1,rotation=1,scale=1)
	bpy.ops.object.select_all(action='DESELECT')

class Import_Crowd_OT(bpy.types.Operator):
	"""Import Crowd Audiarea"""
	bl_idname = "crowd_import.operator"
	bl_label = str()


	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		stid=context.scene.STID
		exportpath=context.scene.export_path
		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path Import Crowd Audiarea e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Choose path to Import Crowd Audiarea e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")

		audiareafpkpath="%saudi\\#Win\\audiarea_%s.fpk"%(exportpath,stid)
		audiareabinpath="%saudi\\#Win\\audiarea_%s_fpk\\Assets\\pes16\\model\\bg\\%s\\audi\\audiarea.bin"%(exportpath,stid,stid)

		# check audiarea in children
		if len(bpy.data.objects['MESH_CROWD'].children) != 0:
			self.report( {"WARNING"}, "The crowd already in parent, delete first before import !!" )
			return {'CANCELLED'}
		pack_unpack_Fpk(audiareafpkpath)
		try:
			Crowd_Import(audiareabinpath, "MESH_CROWD")
		except Exception as e:
			self.report( {"INFO"}, format(e))
			return {'CANCELLED'}
		self.report( {"INFO"}, "Importing Crowd Audiarea has been Successfully... " )
		remove_dir("%saudi\\#Win\\audiarea_%s_fpk"%(exportpath,stid))
		remove_file("%saudi\\#Win\\audiarea_%s.fpk.xml"%(exportpath,stid))
		texture_path="%saudi\\sourceimages\\au_seat.png"%exportpath

		# assign texture seat to audiarea objects
		for ob in bpy.data.objects["MESH_CROWD"].children:
			if str(ob.name).startswith("C_"):
				blenderMaterial = bpy.data.materials.get("audi_seat_mat")
				if blenderMaterial is None:
					blenderMaterial = bpy.data.materials.new(name="audi_seat_mat")
				ob.active_material = blenderMaterial
				blenderMaterial.use_nodes = True
				try:
					blenderTexture = blenderMaterial.node_tree.nodes["Image Texture"]
				except:
					blenderTexture = blenderMaterial.node_tree.nodes.new("ShaderNodeTexImage")
				blenderTexture.location = Vector((-500, 560))
				blenderTexture.select = True
				blenderMaterial.node_tree.nodes.active = blenderTexture

				if "au_seat.png" in bpy.data.images:
					blenderImage = bpy.data.images["au_seat.png"]
				else:
					blenderImage = bpy.data.images.new("au_seat.png", width=0, height=0)
				if os.path.isfile(texture_path):
					blenderImage.filepath = texture_path
				blenderImage.source = 'FILE'
				blenderTexture.image = blenderImage
				principled = blenderMaterial.node_tree.nodes['Principled BSDF']
				blenderMaterial.node_tree.links.new(blenderTexture.outputs['Color'], principled.inputs['Base Color'])
				for nodes in blenderMaterial.node_tree.nodes:
					nodes.select = False 
		return {'FINISHED'}
	pass

def Crowd_Export(outpath, partList, obj_part):
	scn = bpy.context.scene

	if bpy.ops.object.mode_set():
		bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	for ob in bpy.data.objects:
		if ob.parent and ob.parent.name == partList:
			ob.select_set(True)
	bpy.ops.object.transform_apply(location=1,rotation=1,scale=1)
	bpy.ops.object.select_all(action='DESELECT')

	def crowd(obj):
		print("\n")
		print("***"*20)
		print("Audiarea Side:",obj.name)
		off1=audifile.tell()
		off_list.append(off1)
		audifile.write(pack("I",crowd_part_type[obj_part.index(obj.name)]))
		audifile.write(pack("I",off1+8))
		bsize=obj.bound_box[3][:],obj.bound_box[5][:]
		mesh=obj.data
		mesh.update(calc_edges=1, calc_edges_loose=1)	
		ud=0
		num=0
		if str(obj.name).split("_")[1][:1] in ["l","r"]:
			ud=1
		audifile.write(pack("6f",bsize[0][0],bsize[0][2],bsize[0][1]*-1,bsize[1][0],bsize[1][2],bsize[1][1]*-1))
		audifile.write(pack("I",len(mesh.polygons)))
		for f, face in enumerate(mesh.polygons):
			vec1,vec2,idx1,idx2,vlist=[],[],[],[],[]
			row,g=float(),0x0
			v1,v2,v3,v4=0,0,0,0
			for v in enumerate(face.vertices):
				fuv=mesh.uv_layers.active.data[num].uv
				num+=1
				if scn.part_info == "AUDIAREA":
					g = mesh.vertices[v[1]].groups[0]
				if mesh.vertices[v[1]].co.z > face.center.z:
					u,w=fuv[0],fuv[1]
					idx1.append((v[1],u,w))
				else:
					u,w=fuv[0],fuv[1]
					idx2.append((v[1],u,w))
				
			if len(idx1)==len(idx2):
				for t in range(0,len(idx1),2):
					vec1.append((mesh.vertices[idx1[t][0]].co+mesh.vertices[idx1[t+1][0]].co)/2)
					vec1.append((mesh.vertices[idx1[t][0]].co+mesh.vertices[idx1[t+1][0]].co)/2)
					vec2.append((mesh.vertices[idx2[t][0]].co+mesh.vertices[idx2[t+1][0]].co)/2)
					vec2.append((mesh.vertices[idx2[t][0]].co+mesh.vertices[idx2[t+1][0]].co)/2)

				for x in range(0,len(idx1),2):
					if (mesh.vertices[idx1[x+0][0]].co[ud]) < (vec1[x][ud]):
						v1=mesh.vertices[idx1[x+0][0]].co,idx1[x+0][1],idx1[x+0][2]
					else:
						v1=mesh.vertices[idx1[x+1][0]].co,idx1[x+1][1],idx1[x+1][2]
					if (mesh.vertices[idx1[x+0][0]].co[ud]) > (vec1[x][ud]):
						v2=mesh.vertices[idx1[x+0][0]].co,idx1[x+0][1],idx1[x+0][2]
					else:
						v2=mesh.vertices[idx1[x+1][0]].co,idx1[x+1][1],idx1[x+1][2]
					if (mesh.vertices[idx2[x+0][0]].co[ud]) < (vec2[x][ud]):
						v3=mesh.vertices[idx2[x+0][0]].co,idx2[x+0][1],idx2[x+0][2]
					else:
						v3=mesh.vertices[idx2[x+1][0]].co,idx2[x+1][1],idx2[x+1][2]
					if (mesh.vertices[idx2[x+0][0]].co[ud]) > (vec2[x][ud]):
						v4=mesh.vertices[idx2[x+0][0]].co,idx2[x+0][1],idx2[x+0][2]
					else:
						v4=mesh.vertices[idx2[x+1][0]].co,idx2[x+1][1],idx2[x+1][2]
						
					if str(obj.name).split("_")[1][:1] in ["f","r"]:
						vlist.append(v3),vlist.append(v1),vlist.append(v2),vlist.append(v4)
					else:
						vlist.append(v4),vlist.append(v2),vlist.append(v1),vlist.append(v3)
					row=round((v1[0]-v3[0]).length,1)
			else:
				print("Bad Mesh Faces for %s Crowd Part, Fix it before export !!" %obj.name)
			if scn.part_info == "AUDIAREA":
				stancename = obj.vertex_groups[g.group].name
				ha = crowd_type[stancename]
				if not stancename in stancelist:
					stancelist.append(stancename)
			else:
				ha = 1
			row2=round((row/(5.0+scn.crowd_row_space)),1)
			audifile.write(pack("I",f))
			audifile.write(pack("3f",row2,ha,ha))
			for w in vlist:
				audifile.write(pack("3f",w[0][0],w[0][2],w[0][1]*-1))
			for m in vlist:
				audifile.write(pack("2f",m[1],m[2]))
		
	outpath_crowd_data = outpath
	audifile=open(outpath_crowd_data,"wb")
	audifile.write(pack("2I48s",1,1,"".encode()))
	off_list,cr_list_temp = [],[]
	stancelist=[]
	for cr in bpy.data.objects[partList].children:
		cr_list_temp.append(cr.name)
	for ob in obj_part:
		if ob in cr_list_temp:
			crowd(bpy.data.objects[ob])
			for stance in stancelist:
				if "C1" in stance:
					print("Audiarea Type: %s -> Stance Type: Normal"%stance)
				elif "C2" in stance:
					print("Audiarea Type: %s -> Stance Type: Standing Non-chair"%stance)
				else:
					print("Audiarea Type: %s -> Stance Type: Standing with Chair"%stance)
			stancelist.clear()
			print("***"*20)
		else:
			off_list.append(0)
	audifile.seek(8,0)
	for o in enumerate(off_list):
		audifile.write(pack("I",o[1]))
	print("\n")
	audifile.flush(),audifile.close()

	if bpy.ops.object.mode_set():
		bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')

class Crowd_OT(bpy.types.Operator):
	"""Export Crowd"""
	bl_idname = "crowd.operator"
	bl_label = str()

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		stid=context.scene.STID
		if len(bpy.data.objects['MESH_CROWD'].children) > 0:
			for ob in  bpy.data.objects['MESH_CROWD'].children:
				if ob.name not in crowd_part:
					self.report( {"WARNING"}, "%s Crowd Part Name is Wrong, Fix it before Export... "%ob.name)
					return {'CANCELLED'}
				if "C_" not in ob.name:
					self.report( {"WARNING"}, "Mesh [%s] name isn't correct!!" %ob.name)
					return {'CANCELLED'}
			if len(stid) == 5:
				if context.scene.export_path == str():
					self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					return {'CANCELLED'}

				if not stid in context.scene.export_path:
					self.report({"WARNING"}, "Stadium ID doesn't match!!")
					print("Stadium ID doesn't match!!")
					return {'CANCELLED'}

				if not context.scene.export_path.endswith(stid+"\\"):
					self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					return {'CANCELLED'}
			else:
				self.report({"WARNING"}, "Stadium ID isn't correct!!")
				return {'CANCELLED'}
			try:
				print("\nStarting Crowd Parts Exporting...")
				#Create fpk for audiarea
				assetDirname = "/Assets/pes16/model/bg/%s/audi/" % stid
				makeXML(context.scene.export_path+"audi\\#Win\\audiarea_%s"%stid+".fpk.xml", assetDirname+"audiarea.bin", "audiarea_%s.fpk"%stid,"Fpk","FpkFile", False)
				assetDir = os.path.join(context.scene.export_path,"audi", "#Win", "audiarea_%s_fpk"%stid, "Assets","pes16","model","bg",stid,"audi\\audiarea.bin")
				dir_to_remove = os.path.join(context.scene.export_path,"audi", "#Win", "audiarea_%s_fpk"%stid)
				makedir("audi\\#Win\\audiarea_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\audi".format(stid,stid),True)
				Crowd_Export(assetDir,'MESH_CROWD', crowd_part)
				pack_unpack_Fpk(dir_to_remove[:-4]+".fpk.xml")
				remove_dir(dir_to_remove)
				remove_file(dir_to_remove[:-4]+".fpk.xml")
				#Create fpkd for audiarea
				makedir("audi\\#Win\\audiarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\audi".format(stid,stid),True)
				fox2xml("Crowd.xml","audi\\#Win\\audiarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\audi\\audiarea_{2}.fox2.xml".format(stid,stid,stid))
				makeXML(context.scene.export_path+"audi\\#Win\\audiarea_%s"%stid+".fpkd.xml", assetDirname+"audiarea_%s.fox2"%stid, "audiarea_%s.fpkd"%stid,"Fpk","FpkFile", False)
				compileXML("{0}audi\\#Win\\audiarea_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\audi\\audiarea_{3}.fox2.xml".format(context.scene.export_path,stid,stid,stid))
				pack_unpack_Fpk(dir_to_remove[:-4]+".fpkd.xml")
				remove_dir(dir_to_remove+"d")
				remove_file(dir_to_remove[:-4]+".fpkd.xml")
				self.report({"INFO"}, "Exporting Crowd succesfully...!")
				print("\nExporting Crowd succesfully...!")
			except Exception as exception:
				self.report({"WARNING"}, format(exception) + " more info see => System Console (^_^)")
				print(format(type(exception).__name__), format(exception))
				if "index 0 out of range" in format(exception):
					print("\nInfo: Check out mesh have associate Behavior Crowd?, make sure vertex weight is fine, to check weight Go To Weight Paint mode")
				return {'CANCELLED'}
		else:
			self.report( {"WARNING"}, "No Crowd Objects under MESH_CROWD parent !" )
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
		stid=context.scene.STID
		if len(bpy.data.objects['MESH_FLAGAREA'].children) > 0:
			for ob in  bpy.data.objects['MESH_FLAGAREA'].children:
				if ob.name not in flags_part:
					self.report( {"WARNING"}, "%s Flagarea Part Name is Wrong, Fix it before Export... "%ob.name)
					return {'CANCELLED'}
				if "F_" not in ob.name:
					self.report( {"WARNING"}, "Mesh [%s] flag area name isn't correct!!" %ob.name)
					return {'CANCELLED'}
			if len(stid) == 5:
				if context.scene.export_path == str():
					self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
					return {'CANCELLED'}

				if not stid in context.scene.export_path:
					self.report({"WARNING"}, "Stadium ID doesn't match!!")
					print("Stadium ID doesn't match!!")
					return {'CANCELLED'}

				if not context.scene.export_path.endswith(stid+"\\"):
					self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
					return {'CANCELLED'}
			else:
				self.report({"WARNING"}, "Stadium ID isn't correct!!")
				return {'CANCELLED'}
			try:
				print("\nStarting Flagarea Exporting...")
				#Create fpk for Flagarea
				assetDirname = "/Assets/pes16/model/bg/%s/standsFlag/" % stid
				makeXML(context.scene.export_path+"standsFlag\\#Win\\flagarea_%s"%stid+".fpk.xml", assetDirname+"flagarea.bin", "flagarea_%s.fpk"%stid,"Fpk","FpkFile", False)
				assetDir = os.path.join(context.scene.export_path,"standsFlag", "#Win", "flagarea_%s_fpk"%stid, "Assets","pes16","model","bg",stid,"standsFlag\\flagarea.bin")
				dir_to_remove = os.path.join(context.scene.export_path,"standsFlag", "#Win", "flagarea_%s_fpk"%stid)
				makedir("standsFlag\\#Win\\flagarea_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\standsFlag".format(stid,stid),True)
				Crowd_Export(assetDir,'MESH_FLAGAREA', flags_part)
				pack_unpack_Fpk(dir_to_remove[:-4]+".fpk.xml")
				remove_dir(dir_to_remove)
				remove_file(dir_to_remove[:-4]+".fpk.xml")
				#Create fpkd for Flagarea
				makedir("standsFlag\\#Win\\flagarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\standsFlag".format(stid,stid),True)
				fox2xml("Flagarea.xml","standsFlag\\#Win\\flagarea_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\standsFlag\\flagarea_{2}.fox2.xml".format(stid,stid,stid))
				makeXML(context.scene.export_path+"standsFlag\\#Win\\flagarea_%s"%stid+".fpkd.xml", assetDirname+"flagarea_%s.fox2"%stid, "flagarea_%s.fpkd"%stid,"Fpk","FpkFile", False)
				compileXML("{0}standsFlag\\#Win\\flagarea_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\standsFlag\\flagarea_{3}.fox2.xml".format(context.scene.export_path,stid,stid,stid))
				pack_unpack_Fpk(dir_to_remove[:-4]+".fpkd.xml")
				remove_dir(dir_to_remove+"d")
				remove_file(dir_to_remove[:-4]+".fpkd.xml")
				self.report({"INFO"}, "Exporting Flagarea succesfully...!")
				print("\nExporting Flagarea succesfully...!")
			except Exception as exception:
				self.report({"WARNING"}, format(exception))
				print(format(type(exception).__name__), format(exception))
				return {'CANCELLED'}
		else:
			self.report( {"WARNING"}, "No Flagarea Objects under MESH_FLAGAREA parent !" )
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
		mainColumn=mainColumn.row()
		mainColumn.prop(scn, 'crowd_type_enum0')
		mainColumn.operator("assign.operator", icon='PLUS').opname = "stance0"
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(scn, 'crowd_type_enum1')
		mainColumn.operator("assign.operator", icon='PLUS').opname = "stance1"
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(scn, 'crowd_type_enum2')
		mainColumn.operator("assign.operator", icon='PLUS').opname = "stance2"
	pass
		

class PES_21_OT_assign_crowd_type(bpy.types.Operator):
	"""Click to assign selected vertices to the selected crowd type"""
	bl_idname = "assign.operator"
	bl_label = str()
	opname : StringProperty()

	def execute(self, context):
		if self.opname == "stance0":
			try:
				crowd_groups(context.scene.crowd_type_enum0)
			except ValueError as msg:
				self.report({"WARNING"}, format(msg))
		if self.opname == "stance1":
			try:
				crowd_groups(context.scene.crowd_type_enum1)
			except ValueError as msg:
				self.report({"WARNING"}, format(msg))
		if self.opname == "stance2":
			try:
				crowd_groups(context.scene.crowd_type_enum2)
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

def checkNegativeScale(self, context):
	for child in bpy.data.objects[context.scene.part_info].children:
		if child.type == 'EMPTY' and child is not None:
			for ob in bpy.data.objects[child.name].children:
				if ob is not None:
					for obj in bpy.data.objects[ob.name].children:
						if obj is not None:
							for dimensions in obj.scale:
								if dimensions < 0:
									print("\nNegative scale is unsupported, Object '%s --> %s' please fix it !!"%(obj.parent.name, obj.name))
									print("Make sure the object don't have negative scale")
									print("Select object problem->CTRL+A->Apply->All Transforms")
									print("\nand make sure the object don't have normals flipped")
									return True

def lightfximport(fname):

	lockstar=open(fname, 'rb')
	lockstar.seek(0xf0)
	lamp_len = unpack('4b', lockstar.read(4))[0]
	lockstar.seek(0x100)
	side=str()
	for i in range(lamp_len):
		lamp_data_x = unpack('4f', lockstar.read(16))
		lamp_data_y = unpack('4f', lockstar.read(16))
		lamp_data_z = unpack('4f', lockstar.read(16))
		Energy=lamp_data_y[0]
		if Energy == 1.0:
			Energy=lamp_data_z[3]
		light_data = bpy.data.lights.new(name="L_Point", type='POINT')
		light_data.energy = 10
		light_object = bpy.data.objects.new(name="L_Point", object_data=light_data)
		bpy.context.collection.objects.link(light_object)
		bpy.context.view_layer.objects.active = light_object
		light_object.location = (lamp_data_x[2],lamp_data_z[2]*-1,lamp_data_y[2])
		light_object.l_Energy = Energy
		if 'back' in fname:
			side='L_BACK'
		if 'front' in fname:
			side='L_FRONT'
		if 'left' in fname:
			side='L_LEFT'
		if 'right' in fname:
			side='L_RIGHT'
		parent = bpy.data.objects.get(side)
		child = bpy.data.objects.get(light_data.name)
		child.parent = parent
		print(f"Light name: {light_data.name}, Location: {lamp_data_x[2],lamp_data_z[2]*-1,lamp_data_y[2]}, Energy: {Energy}")

def effect_config(filename):
	domData =  minidom.parse(filename)
	light_object=object
	light_data=object
	side=str()
	sideList=[]
	idx=0
	create = domData.getElementsByTagName("create")
	for create_setting in create:
		create_type = create_setting.getAttribute("dir")
		if create_type != "":
			sideList.append(create_type)

	effect = domData.getElementsByTagName("setting")
	for effect_setting in effect:
		effect_type = effect_setting.getAttribute("type")
		if effect_type == "LightBillboard":
			param = effect_setting.getElementsByTagName("param")
			for param_type in param:
				id = param_type.getAttribute("id")
				if id == "texturePath":
					texturePath = str(param_type.getAttribute("value")).split('/')[8]
					if "tex_star" in texturePath:
						bpy.context.scene.l_fx_tex = texturePath
					
		if effect_type == "LensFlare":
			param = effect_setting.getElementsByTagName("param")
			for param_type in param:
				id = param_type.getAttribute("id")
				if id == "texturePath":
					texturePath = str(param_type.getAttribute("value")).split('/')[8]
					if "tex_ghost" in texturePath:
						bpy.context.scene.lensflaretex = texturePath
				if id == "trans":
					trans = param_type.getAttribute("value")
					trans_val=str(trans).split(",")[0],str(trans).split(",")[1],str(trans).split(",")[2]
					light_data = bpy.data.lights.new(name="F_Area", type='AREA')
					light_data.energy = 10
					light_object = bpy.data.objects.new(name="F_Area", object_data=light_data)
					bpy.context.collection.objects.link(light_object)
					bpy.context.view_layer.objects.active = light_object
					light_object.location = (float(trans_val[0]),float(trans_val[2])*-1,float(trans_val[1]))
				if id == "quat":
					quat = param_type.getAttribute("value")
					quat_val=str(quat).split(",")[0],str(quat).split(",")[1],str(quat).split(",")[2],str(quat).split(",")[3]
					light_object.rotation_mode = "QUATERNION"
					light_object.rotation_quaternion.w = float(quat_val[3])
					light_object.rotation_quaternion.x = float(quat_val[0])*-1
					light_object.rotation_quaternion.y = float(quat_val[2])
					light_object.rotation_quaternion.z = float(quat_val[1])

			side="F_%s"%str(sideList[idx]).upper()
			parent = bpy.data.objects.get(side)
			child = bpy.data.objects.get(light_data.name)
			child.parent = parent
			idx+=1

		if effect_type == "Halo":
			param = effect_setting.getElementsByTagName("param")
			for param_type in param:
				id = param_type.getAttribute("id")
				if id == "texturePath":
					texturePath = str(param_type.getAttribute("value")).split('/')[8]
					light_data = bpy.data.lights.new(name="H_Area", type='AREA')
					light_data.energy = 10
					light_object = bpy.data.objects.new(name="H_Area", object_data=light_data)
					bpy.context.collection.objects.link(light_object)
					bpy.context.view_layer.objects.active = light_object
					light_object.HaloTex = texturePath
				if id == "pivot":
					pivot = param_type.getAttribute("value")
					pivot_val=str(pivot).split(",")[0],str(pivot).split(",")[1],str(pivot).split(",")[2]
					light_object.Pivot.x = float(pivot_val[0])
					light_object.Pivot.y = float(pivot_val[1])
					light_object.Pivot.z = float(pivot_val[2])
				if id == "scale":
					scale = param_type.getAttribute("value")
					scale_val=str(scale).split(",")[0],str(scale).split(",")[1],str(scale).split(",")[2]
					light_data.shape = "RECTANGLE"
					light_data.size = float(scale_val[0])
					light_data.size_y = float(scale_val[1])
				if id == "quat":
					quat = param_type.getAttribute("value")
					quat_val=str(quat).split(",")[0],str(quat).split(",")[1],str(quat).split(",")[2],str(quat).split(",")[3]
					light_object.rotation_mode = "QUATERNION"
					light_object.rotation_quaternion.w = float(quat_val[3])
					light_object.rotation_quaternion.x = float(quat_val[0])
					light_object.rotation_quaternion.y = float(quat_val[2])*-1
					light_object.rotation_quaternion.z = float(quat_val[1])
				if id == "trans":
					trans = param_type.getAttribute("value")
					trans_val=str(trans).split(",")[0],str(trans).split(",")[1],str(trans).split(",")[2]
					light_object.location = (float(trans_val[0]),float(trans_val[2])*-1,float(trans_val[1]))
				if id == "color":
					color = param_type.getAttribute("value")
					color_val=str(color).split(",")[0],str(color).split(",")[1],str(color).split(",")[2]
					light_data.color = (float(color_val[0]),float(color_val[2]),float(color_val[1]))
				if id == "fixRotY":
					fixRotY = param_type.getAttribute("value")
					light_object.rotY = int(fixRotY)

			side="H_%s"%str(sideList[idx]).upper()
			parent = bpy.data.objects.get(side)
			child = bpy.data.objects.get(light_data.name)
			child.parent = parent
			idx+=1
			
class Import_lightfx_OT(bpy.types.Operator):
	"""Light FX Importer"""
	bl_idname = "ligtfx_importer.operator"
	bl_label = str()

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		stid=context.scene.STID
		exportPath=context.scene.export_path
		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}
		checks=checkStadiumID(context, True)
		if checks:
			self.report({"WARNING"}, "Stadium ID isn't match, more info see => System Console (^_^)")
			return {'CANCELLED'}
		fpkfilename="%seffect\\#Win\\effect_%s_nf.fpk"%(exportPath,stid)
		config_xml="%seffect\\#Win\\effect_%s_nf_fpk\\effect_config.xml"%(exportPath,stid)
		pack_unpack_Fpk(fpkfilename)
		basedir = os.path.dirname(fpkfilename)
		
		for root, directories, filenames in os.walk(basedir):
			for fileName in filenames:
				filename, extension = os.path.splitext(fileName)
				if extension.lower() == '.model':
					lightfximport(os.path.join(root, fileName))

		effect_config(config_xml)
		self.report({"INFO"}, "Importing Light-FX succesfully...")
		if bpy.ops.object.mode_set():
			bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
		remove_dir("%seffect\\#Win\\effect_%s_nf_fpk"%(exportPath,stid))
		remove_file("%seffect\\#Win\\effect_%s_nf.fpk.xml"%(exportPath,stid))
		return {'FINISHED'}
	pass

def checkMeshMaterialUvs(self, context):
	for child in bpy.data.objects[context.scene.part_info].children:
		if child.type == 'EMPTY' and child is not None:
			for ob in bpy.data.objects[child.name].children:
				if ob is not None:
					for ob2 in bpy.data.objects[ob.name].children:
						if ob2 is not None:
							uv = bpy.data.meshes[ob2.data.name].uv_layers
							mat = bpy.data.objects[ob2.name].material_slots
							if len(uv) == 0:
								self.report({"WARNING"}, "Mesh [%s] does not have a primary UV map set!" % ob2.name)
								print("Mesh [%s] does not have a primary UV map set!" % ob2.name)
								print(f"Check in {context.scene.part_info}-->{child.name}-->{ob.name}-->{ob2.name}!")
								return True
							elif len(uv) >= 3:
								self.report({"WARNING"}, "Mesh [%s] too much UVMap slots, need to remove!" % ob2.name)
								print("Mesh [%s] too much UVMap slots, need to remove!" % ob2.name)
								print(f"Check in {context.scene.part_info}-->{child.name}-->{ob.name}-->{ob2.name}!")
								return True
							elif len(uv) == 1:
								if uv[0].name != 'UVMap':
									self.report({"WARNING"}, "Mesh [%s] UVMap name isn't correct!" % ob2.name)
									print("Mesh [%s] UVMap name isn't correct!" % ob2.name)
									print(f"Check in {context.scene.part_info}-->{child.name}-->{ob.name}-->{ob2.name}!")
									return True
							elif len(uv) == 2:
								if uv[1].name != 'normal_map':
									self.report({"WARNING"}, "Mesh [%s] normal_map name isn't correct!" % ob2.name)
									print("Mesh [%s] normal_map name isn't correct!" % ob2.name)
									print(f"Check in {context.scene.part_info}-->{child.name}-->{ob.name}-->{ob2.name}!")
									return True
							if len(mat) == 0:
								self.report({"WARNING"}, "Mesh [%s] does not have an associated material!" % ob2.name)
								print(f"Mesh {ob2.name} does not have an associated material!")
								print(f"Check in {context.scene.part_info}-->{child.name}-->{ob.name}-->{ob2.name}!")
								return True
							if len(mat) >= 2:
								self.report({"WARNING"}, "Mesh [%s] too much material slots need to remove!" % ob2.name)
								print("Mesh [%s] too much material slots need to remove!" % ob2.name)
								print(f"Check in {context.scene.part_info}-->{child.name}-->{ob.name}-->{ob2.name}!")
								return True
	return False

class Export_OT(bpy.types.Operator):
	"""Export Stadium"""
	bl_idname = "export_stadium.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):

		stid=context.scene.STID
		exportPath=context.scene.export_path

		if checkMeshMaterialUvs(self, context):
			return {'CANCELLED'}

		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}
		checks=checkStadiumID(context, True)
		if checks:
			self.report({"WARNING"}, "Stadium ID isn't match, more info see => System Console (^_^)")
			return {'CANCELLED'}
		checksscale=checkNegativeScale(self,context)
		if checksscale:
			self.report({"WARNING"}, "Negative scale is unsupported, more info see => System Console (^_^)")
			return {'CANCELLED'}
		if self.opname == "mainstadium":
			files,files2=[],[]
			for en in PesEnlighten.EnlightenAsset:
				en=en.replace("stid",stid)
				files2.append(en)
			shearTransformlist,pivotTransformlist,dataList=[],[],[]
			Stadium_Model,TransformEntityList,Stadium_Kinds,Stadium_Dir=[],[],[],[]
			arraySize=0
			print('\nStarting export object as .FMDL')
			assetDirname = "/Assets/pes16/model/bg/%s/scenes/" % stid
			assetDir = "{0}#Win\\{1}_fpk\\Assets\\pes16\\model\\bg\\{2}\\scenes\\".format(exportPath,stid,stid)

			for child in bpy.data.objects[context.scene.part_info].children:
				if child.type == 'EMPTY' and child is not None:
					for ob in bpy.data.objects[child.name].children[:1]:
						if ob is not None:
							for ob2 in bpy.data.objects[ob.name].children[:1]:
								if ob2 is not None:
									print('\n********************************')
									arraySize +=1
									makedir("#Win\\{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes".format(stid,stid),True)
									makedir("#Win\\{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}".format(stid,stid),True)
									objName = child.name
									fmdlName = child.name
									try:
										addr=hxd(transformlist[datalist.index(fmdlName)],8)
										shearTransformaddr=hxd(shearTransform[datalist.index(fmdlName)],8)
										pivotTransformaddr=hxd(pivotTransform[datalist.index(fmdlName)],8)
										Transformaddr=hxd(TransformEntity[datalist.index(fmdlName)],8)
										Stadium_Model.append(StadiumModel[datalist.index(fmdlName)])
										Stadium_Kinds.append(StadiumKind[datalist.index(fmdlName)])
										Stadium_Dir.append(StadiumDir[datalist.index(fmdlName)])
									except Exception as msg:
										self.report({"WARNING"}, format(msg) + " more info see => System Console (^_^)")
										print("\n\nInfo: Need to delete "+format(msg))
										print("\n\nInfo: Make sure mesh object in correct parent set your mesh object to parent list: %s" % datalist)
										return {'CANCELLED'}
									fileName = assetDir + fmdlName+".fmdl"
									meshID = str(fileName).split('..')[0].split('\\')[-1:][0]									
									print('Exporting ==> %s' % meshID)
									print('********************************')
									files.append(assetDirname +fmdlName+".fmdl")
									files2.append(assetDirname +fmdlName+".fmdl")
									dataList.append(addr)
									shearTransformlist.append(shearTransformaddr)
									pivotTransformlist.append(pivotTransformaddr)
									TransformEntityList.append(Transformaddr)
									export_fmdl(self, context, fileName, meshID, objName)
			makeXML(exportPath+ "#Win\\"+stid+".fpk.xml", files2, "%s.fpk"%stid,"Fpk","FpkFile", True)
			makeXML(exportPath+ "#Win\\"+stid+".fpkd.xml", "/Assets/pes16/model/bg/{0}/{1}_modelset.fox2".format(stid,stid), "%s.fpkd"%stid,"Fpkd","FpkFile", False)
			fox2XmlPath="{0}#Win\\{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\{3}_modelset.fox2.xml".format(exportPath,stid,stid,stid)
			try:
				PesFoxXML.makeXMLForStadium(fox2XmlPath, dataList, arraySize, files, shearTransformlist, pivotTransformlist, Stadium_Model,TransformEntityList,Stadium_Kinds,Stadium_Dir)
				compileXML(fox2XmlPath)
			except Exception as msg:
				self.report({"INFO"}, format(msg))
				return {'CANCELLED'}
			#Create Enlighten System
			EnlightenPathOut="#Win\\{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\EnlightenOutput".format(stid,stid)
			makedir(EnlightenPathOut,True)
			for filenames in os.walk(EnlightenPath):
				for fname in filenames[2]:
					oldName=str(fname)
					newName=oldName.replace("stid",stid)
					shutil.copyfile(EnlightenPath+oldName,exportPath+EnlightenPathOut+"\\"+newName)
			pack_unpack_Fpk("{0}#Win\\{1}.fpk.xml".format(exportPath,stid))
			remove_dir("{0}#Win\\{1}_fpk".format(exportPath,stid))
			remove_file("{0}#Win\\{1}.fpk.xml".format(exportPath,stid))
			pack_unpack_Fpk("{0}#Win\\{1}.fpkd.xml".format(exportPath,stid))
			remove_dir("{0}#Win\\{1}_fpkd".format(exportPath,stid))
			remove_file("{0}#Win\\{1}.fpkd.xml".format(exportPath,stid))
			self.report({"INFO"}, "Exporting stadium succesfully...!")
			return {'FINISHED'}
		if self.opname == "extrastadium":
			print('\nStarting export object as .FMDL')
			for timemode in ["df", "dr", "nf", "nr"]:
				files,files2=[],[]
				shearTransformlist,pivotTransformlist,dataList=[],[],[]
				Stadium_Model,TransformEntityList,Stadium_Kinds,Stadium_Dir=[],[],[],[]
				arraySize=0
				mode=str()
				next_mode=False
				for child in bpy.data.objects[context.scene.part_info].children:
					if child.type == 'EMPTY' and child is not None:
						for ob in bpy.data.objects[child.name].children[:1]:
							if ob is not None:
								for ob2 in bpy.data.objects[ob.name].children[:1]:
									if ob2 is not None:
										mode = str(ob.name).split('_')[2]
										
										if timemode == mode:
											next_mode = True
											assetDirname = "/Assets/pes16/model/bg/%s/scenes/" % stid
											assetDir = f"{exportPath}#Win\\{stid}_{mode}_fpk\\Assets\\pes16\\model\\bg\\{stid}\\scenes\\"
											print('\n********************************')
											arraySize +=1
											makedir(f"#Win\\{stid}_{mode}_fpk\\Assets\\pes16\\model\\bg\\{stid}\\scenes",True)
											makedir(f"#Win\\{stid}_{mode}_fpkd\\Assets\\pes16\\model\\bg\\{stid}",True)
											objName = child.name
											fmdlName = child.name
											try:
												addr=hxd(transformlist2[datalist2.index(fmdlName)],8)
												shearTransformaddr=hxd(shearTransform2[datalist2.index(fmdlName)],8)
												pivotTransformaddr=hxd(pivotTransform2[datalist2.index(fmdlName)],8)
												Transformaddr=hxd(TransformEntity2[datalist2.index(fmdlName)],8)
												Stadium_Model.append(StadiumModel2[datalist2.index(fmdlName)])
												Stadium_Kinds.append(StadiumKind2[datalist2.index(fmdlName)])
												Stadium_Dir.append(StadiumDir2[datalist2.index(fmdlName)])
											except Exception as msg:
												self.report({"WARNING"}, format(msg) + " more info see => System Console (^_^)")
												print("\n\nInfo: Need to delete "+format(msg))
												print("\n\nInfo: Make sure mesh object in correct parent set your mesh object to parent list: %s" % datalist)
												return {'CANCELLED'}
											fileName = assetDir + fmdlName+".fmdl"
											meshID = str(fileName).split('..')[0].split('\\')[-1:][0]									
											print('Exporting ==> %s' % meshID)
											print('********************************')
											files.append(assetDirname +fmdlName+".fmdl")
											files2.append(assetDirname +fmdlName+".fmdl")
											dataList.append(addr)
											shearTransformlist.append(shearTransformaddr)
											pivotTransformlist.append(pivotTransformaddr)
											TransformEntityList.append(Transformaddr)
											export_fmdl(self, context, fileName, meshID, objName)
				if next_mode:
					makeXML(exportPath+ f"#Win\\{stid}_{timemode}.fpk.xml", files2, f"{stid}_{timemode}.fpk","Fpk","FpkFile", True)
					makeXML(exportPath+ f"#Win\\{stid}_{timemode}.fpkd.xml", f"/Assets/pes16/model/bg/{stid}/{stid}_{timemode}.fox2", f"{stid}_{timemode}.fpkd","Fpkd","FpkFile", False)
					fox2XmlPath=f"{exportPath}#Win\\{stid}_{timemode}_fpkd\\Assets\\pes16\\model\\bg\\{stid}\\{stid}_{timemode}.fox2.xml"
					try:
						PesFoxXML.makeXMLForExtraStadium(fox2XmlPath, dataList, arraySize, files, shearTransformlist, pivotTransformlist, Stadium_Model,TransformEntityList,Stadium_Kinds,Stadium_Dir)
						compileXML(fox2XmlPath)
					except Exception as msg:
						self.report({"INFO"}, format(msg))
						return {'CANCELLED'}
					pack_unpack_Fpk(f"{exportPath}#Win\\{stid}_{timemode}.fpk.xml")
					remove_dir(f"{exportPath}#Win\\{stid}_{timemode}_fpk")
					remove_file(f"{exportPath}#Win\\{stid}_{timemode}.fpk.xml")
					pack_unpack_Fpk(f"{exportPath}#Win\\{stid}_{timemode}.fpkd.xml")
					remove_dir(f"{exportPath}#Win\\{stid}_{timemode}_fpkd")
					remove_file(f"{exportPath}#Win\\{stid}_{timemode}.fpkd.xml")
									
			self.report({"INFO"}, "Exporting extra stadium succesfully...!")
			return {'FINISHED'}
	pass

class Pitch_Objects(bpy.types.Operator):
	"""Export Pitch Objects"""
	bl_idname = "export_pitch.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT")
	
	def execute(self, context):
		stid=context.scene.STID
		exportPath=context.scene.export_path

		if checkMeshMaterialUvs(self, context):
			return {'CANCELLED'}

		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}

		if self.opname == "pitch_import":
			if 'MESH_Pitch' not in bpy.data.objects:
				Create_Parent_Part(self, context)
			try:
				inner_path = 'Object'
				if 'st081_pitch_0' not in bpy.data.objects:
					bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, 'st081_pitch_0'),directory=os.path.join(base_file_blend, inner_path),filename='st081_pitch_0')
					parent = bpy.data.objects.get('MESH_Pitch')
					child = bpy.data.objects.get('st081_pitch_0')
					child.parent = parent
				else:
					self.report({"WARNING"}, "Pitch already loaded !!")
					return {'CANCELLED'}
				if 'st081_pitch_1' not in bpy.data.objects:
					bpy.ops.wm.append(filepath=os.path.join(base_file_blend, inner_path, 'st081_pitch_1'),directory=os.path.join(base_file_blend, inner_path),filename='st081_pitch_1')
					parent = bpy.data.objects.get('MESH_Pitch')
					child = bpy.data.objects.get('st081_pitch_1')
					child.parent = parent
				else:
					self.report({"WARNING"}, "Pitch already loaded !!")
					return {'CANCELLED'}
			except Exception as e:
				self.report({"WARNING"}, format(e))
				return {'CANCELLED'}
			self.report({"INFO"}, "Load Pitch succesfully...!")
			return {'FINISHED'}
		if self.opname == "pitch_export":
			checks=checkStadiumID(context, True)
			if checks:
				self.report({"WARNING"}, "Stadium ID isn't match, more info see => System Console (^_^)")
				return {'CANCELLED'}
			assetDirname = "/Assets/pes16/model/bg/{0}/scenes/pitch_{1}.fmdl".format(stid,stid)
			assetDir = "{0}pitch\\#Win\\pitch_{1}_fpk\\Assets\\pes16\\model\\bg\\{2}\\scenes\\".format(exportPath,stid,stid)
			fpkdPath="pitch\\#Win\\pitch_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\pitch".format(stid,stid)
			for child in bpy.data.objects[context.scene.part_info].children:
				if child.type == 'EMPTY' and child is not None:
					for ob in bpy.data.objects[child.name].children[:1]:
						if ob is not None:
							for ob2 in bpy.data.objects[ob.name].children[:1]:
								if ob2 is not None:
									print('\n********************************')
									makedir("pitch\\#Win\\pitch_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes".format(stid,stid),True)
									makedir(fpkdPath,True)
									objName = child.name
									fileName = "{0}pitch_{1}.fmdl".format(assetDir, stid)
									meshID = str(fileName).split('..')[0].split('\\')[-1:][0]
									print("Exporting ==> pitch_%s.fmdl"%stid)
									print('********************************\n')
									export_fmdl(self, context, fileName, meshID, objName)

			makeXML("{0}pitch\\#Win\\pitch_{1}.fpk.xml".format(exportPath, stid), assetDirname, "pitch_%s.fpk"%stid,"Fpk","FpkFile", False)
			makeXML("{0}pitch\\#Win\\pitch_{1}.fpkd.xml".format(exportPath, stid), "/Assets/pes16/model/bg/{0}/pitch/pitch_{1}.fox2".format(stid,stid), "pitch_%s.fpkd"%stid,"Fpk","FpkFile", False)
			pitchXML=open(xml_dir+'Pitch.xml','rt').read()
			pitchXML=pitchXML.replace("stid", stid)
			writepitchXML=open("{0}{1}\\pitch_{2}.fox2.xml".format(exportPath,fpkdPath,stid),"wt")
			writepitchXML.write(pitchXML)
			writepitchXML.flush(),writepitchXML.close()

			compileXML("{0}{1}\\pitch_{2}.fox2.xml".format(exportPath,fpkdPath,stid))
			pack_unpack_Fpk("{0}pitch\\#Win\\pitch_{1}.fpk.xml".format(exportPath,stid))
			remove_dir("{0}pitch\\#Win\\pitch_{1}_fpk".format(exportPath,stid))
			remove_file("{0}pitch\\#Win\\pitch_{1}.fpk.xml".format(exportPath,stid))
			pack_unpack_Fpk("{0}pitch\\#Win\\pitch_{1}.fpkd.xml".format(exportPath,stid))
			remove_dir("{0}pitch\\#Win\\pitch_{1}_fpkd".format(exportPath,stid))
			remove_file("{0}pitch\\#Win\\pitch_{1}.fpkd.xml".format(exportPath,stid))
			self.report({"INFO"}, "Exporting Pitch succesfully...!")
			return {'FINISHED'}
	pass

class ExportStadium_AD(bpy.types.Operator):

	"""Export Adboard of Stadium"""
	bl_idname = "export_ad.operator"
	bl_label = str()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT")
	
	def execute(self, context):
		stid=context.scene.STID
		exportPath=context.scene.export_path
		
		if checkMeshMaterialUvs(self, context):
			return {'CANCELLED'}

		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}
		checks=checkStadiumID(context, True)
		if checks:
			self.report({"WARNING"}, "Stadium ID isn't match, more info see => System Console (^_^)")
			return {'CANCELLED'}
	
		for child in bpy.data.objects[context.scene.part_info].children:
			if child.type == 'EMPTY' and child is not None:
				for ob in bpy.data.objects[child.name].children[:1]:
					if ob is not None:
						for obt in bpy.data.objects[ob.name].children:
							if obt is not None:
								texture_directory = "/Assets/pes16/model/bg/common/ad/sourceimages/tga/"
								blenderMaterial = bpy.data.objects[obt.name].active_material
								for nodes in blenderMaterial.node_tree.nodes:
									if nodes.type == "TEX_IMAGE":
										get_texture_directory=blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory
										if not "common" in get_texture_directory:
											blenderMaterial.node_tree.nodes[nodes.name].fmdl_texture_directory = texture_directory
						for ob2 in bpy.data.objects[ob.name].children[:1]:
							if ob2 is not None:
								objName = child.name
								adName,adType=str(objName).split('_')[0],str(objName).split('_')[1]
								fmdlName="{0}_{1}_{2}.fmdl".format(adName,stid,adType)
								assetDirname = "/Assets/pes16/model/bg/common/ad/scenes/%s"%fmdlName
								assetDirnameFox2 = "/Assets/pes16/model/bg/common/ad/ad_{0}_{1}.fox2".format(stid,adType)
								assetDir = "{0}common\\ad\\#Win\\ad_{1}_{2}_fpk\\Assets\\pes16\\model\\bg\\common\\ad\\scenes\\".format(exportPath[:-6],stid,adType)
								fpkPath="common\\ad\\#Win\\ad_{0}_{1}_fpk\\Assets\\pes16\\model\\bg\\common\\ad\\scenes".format(stid,adType)
								fpkdPath="common\\ad\\#Win\\ad_{0}_{1}_fpkd\\Assets\\pes16\\model\\bg\\common\\ad".format(stid,adType)
								makeXML("{0}common\\ad\\#Win\\ad_{1}_{2}.fpk.xml".format(exportPath[:-6], stid,adType), assetDirname, "ad_{0}_{1}.fpk".format(stid,adType),"Fpk","FpkFile", False)
								makeXML("{0}common\\ad\\#Win\\ad_{1}_{2}.fpkd.xml".format(exportPath[:-6], stid,adType), assetDirnameFox2, "ad_{0}_{1}.fpkd".format(stid,adType),"Fpk","FpkFile", False)
								print('\n********************************')
								makedir(fpkPath,False)		
								makedir(fpkdPath,False)		
								fileName = assetDir +fmdlName
								meshID = fmdlName
								print("Exporting ==> %s"%fmdlName)
								print('********************************\n')
								export_fmdl(self, context, fileName, meshID, objName)
								pack_unpack_Fpk("{0}common\\ad\\#Win\\ad_{1}_{2}.fpk.xml".format(exportPath[:-6], stid,adType))
								remove_dir("{0}common\\ad\\#Win\\ad_{1}_{2}_fpk".format(exportPath[:-6], stid,adType))
								remove_file("{0}common\\ad\\#Win\\ad_{1}_{2}.fpk.xml".format(exportPath[:-6], stid,adType))
								adfpkd=open(xml_dir+"StadiumAd.xml", "rt").read()
								adfpkd=adfpkd.replace("assetPath",assetDirname)
								adfpkd=adfpkd.replace("adType",adType)
								Writeadfpkd=open(exportPath[:-6]+fpkdPath+"\\ad_{0}_{1}.fox2.xml".format(stid,adType), "wt")
								Writeadfpkd.write(adfpkd)
								Writeadfpkd.flush(),Writeadfpkd.close()
								compileXML(exportPath[:-6]+fpkdPath+"\\ad_{0}_{1}.fox2.xml".format(stid,adType))
								pack_unpack_Fpk("{0}common\\ad\\#Win\\ad_{1}_{2}.fpkd.xml".format(exportPath[:-6], stid,adType))
								remove_dir("{0}common\\ad\\#Win\\ad_{1}_{2}_fpkd".format(exportPath[:-6], stid,adType))
								remove_file("{0}common\\ad\\#Win\\ad_{1}_{2}.fpkd.xml".format(exportPath[:-6], stid,adType))
		self.report({"INFO"}, "Exporting Stadium Ads succesfully...!")
		return {'FINISHED'}

class Export_TV(bpy.types.Operator):
	"""Export TV"""
	bl_idname = "export_tv.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return (context.mode == "OBJECT")
	
	def execute(self, context):
		stid=context.scene.STID
		exportPath=context.scene.export_path

		if len(stid) == 5:
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				print("Choose path to export %s e:g [-->Asset\\model\\bg\\%s<--]!!" % (context.scene.part_info,stid))
				return {'CANCELLED'}

			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}

			if not context.scene.export_path.endswith(stid+"\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}
		checks=checkStadiumID(context, False)
		if checks:
			self.report({"WARNING"}, "Stadium ID isn't match, more info see => System Console (^_^)")
			return {'CANCELLED'}
		TvOb,files,TvMdl,addrs=[],[],[],[]
		arraySize,TvBoxSize,TvLineSize=0,0,0
		tvlist=["tv_%s_large_back.fmdl"%stid,
				"tv_%s_large_front.fmdl"%stid,
				"tv_%s_large_left.fmdl"%stid,
				"tv_%s_large_right.fmdl"%stid,
				"tv_%s_small_back.fmdl"%stid,
				"tv_%s_small_front.fmdl"%stid,
				"tv_%s_small_left.fmdl"%stid,
				"tv_%s_small_right.fmdl"%stid,
		]
		assetDirname = "/Assets/pes16/model/bg/%s/scenes/" % stid
		assetDir = "{0}tv\\#Win\\tv_{1}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes\\".format(exportPath,stid,stid)
		for child in bpy.data.objects[context.scene.part_info].children:
			if child.type == 'EMPTY' and child is not None:
				TvOb.append(child.name)
				for ob in bpy.data.objects[child.name].children[:1]:
					if ob is not None:
						uv = bpy.data.meshes[ob.data.name].uv_layers
						mat = bpy.data.objects[ob.name].material_slots
						if len(uv) == 0:
							self.report({"WARNING"}, "Mesh [%s] does not have a primary UV map set!" % ob.name)
							print("Mesh [%s] does not have a primary UV map set!" % ob.name)
							return {'CANCELLED'}
						elif len(uv) >= 3:
							self.report({"WARNING"}, "Mesh [%s] too much UVMap slots, need to remove!" % ob.name)
							print("Mesh [%s] too much UVMap slots, need to remove!" % ob.name)
							return {'CANCELLED'}
						elif len(uv) == 1:
							if uv[0].name != 'UVMap':
								self.report({"WARNING"}, "Mesh [%s] UVMap name isn't correct!" % ob.name)
								print("Mesh [%s] UVMap name isn't correct!" % ob.name)
								return {'CANCELLED'}
						elif len(uv) == 2:
							if uv[1].name != 'normal_map':
								self.report({"WARNING"}, "Mesh [%s] normal_map name isn't correct!" % ob.name)
								print("Mesh [%s] normal_map name isn't correct!" % ob.name)
								return {'CANCELLED'}
						if len(mat) == 0:
							self.report({"WARNING"}, "Mesh [%s] does not have an associated material!" % ob.name)
							print("Mesh [%s] does not have an associated material!" % ob.name)
							return {'CANCELLED'}
						if len(mat) >= 2:
							self.report({"WARNING"}, "Mesh [%s] too much material slots need to remove!" % ob.name)
							print("Mesh [%s] too much material slots need to remove!" % ob.name)
							return {'CANCELLED'}
						print('\n***************************************')
						fmdlName = child.name
						TvMdl.append(fmdlName)
						arraySize+=1
						if "_Large" in fmdlName:
							TvBoxSize+=1
						if "_Small" in fmdlName:
							TvLineSize+=1
						makedir("tv\\#Win\\tv_{0}_fpk\\Assets\\pes16\\model\\bg\\{1}\\scenes".format(stid,stid),True)
						makedir("tv\\#Win\\tv_{0}_fpkd\\Assets\\pes16\\model\\bg\\{1}\\tv".format(stid,stid),True)
						addrs.append(hxd(tvdatalist[TvOb.index(fmdlName)],8))
						TvName=tvlist[TvOb.index(fmdlName)]	
						fileName = assetDir + TvName
						files.append(assetDirname + TvName)
						meshID = str(fileName).split('..')[0].split('\\')[-1:][0]
						print("Exporting ==> %s"%TvName)
						print('***************************************\n')
						export_fmdl(self, context, fileName, meshID, fmdlName)
		makeXML(exportPath+ "tv\\#Win\\tv_"+stid+".fpk.xml", files, "tv_%s.fpk"%stid,"Fpk","FpkFile", True)
		makeXML(exportPath+ "tv\\#Win\\tv_"+stid+".fpkd.xml", "/Assets/pes16/model/bg/{0}/tv/tv_{1}.fox2".format(stid,stid), "tv_%s.fpkd"%stid,"Fpk","FpkFile", False)
		fox2XmlPath="{0}tv\\#Win\\tv_{1}_fpkd\\Assets\\pes16\\model\\bg\\{2}\\tv\\tv_{3}.fox2.xml".format(exportPath,stid,stid,stid)
		try:
			PesFoxXML.makeXMLForTv(fox2XmlPath,TvMdl,arraySize,addrs,files,TvBoxSize,TvLineSize)
			compileXML(fox2XmlPath)
		except Exception as msg:
			self.report({"WARNING"}, format(msg))
			return {'CANCELLED'}

		pack_unpack_Fpk("{0}tv\\#Win\\tv_{1}.fpk.xml".format(exportPath,stid))
		remove_dir("{0}tv\\#Win\\tv_{1}_fpk".format(exportPath,stid))
		remove_file("{0}tv\\#Win\\tv_{1}.fpk.xml".format(exportPath,stid))
		pack_unpack_Fpk("{0}tv\\#Win\\tv_{1}.fpkd.xml".format(exportPath,stid))
		remove_dir("{0}tv\\#Win\\tv_{1}_fpkd".format(exportPath,stid))
		remove_file("{0}tv\\#Win\\tv_{1}.fpkd.xml".format(exportPath,stid))
		self.report({"INFO"}, "Exporting TV succesfully...!")
		return {'FINISHED'}
	pass

TexDimensions=["8","16","32","48","64","80","96","112","128","144","160","176","192","208",
"224","240","256","272","288","304","320","336","352","368","384","400","416","432","448",
"464","480","496","512","528","544","560","576","592","608","624","640","656","672","688",
"704","720","736","752","768","784","800","816","832","848","864","880","896","912","928",
"944","960","976","992","1008","1024","1040","1056","1072","1088","1104","1120","1136","1152",
"1168","1184","1200","1216","1232","1248","1264","1280","1296","1312","1328","1344","1360","1376",
"1392","1408","1424","1440","1456","1472","1488","1504","1520","1536","1552","1568","1584","1600",
"1616","1632","1648","1664","1680","1696","1712","1728","1744","1760","1776","1792","1808","1824",
"1840","1856","1872","1888","1904","1920","1936","1952","1968","1984","2000","2016","2032","2048",
"2064","2080","2096","2112","2128","2144","2160","2176","2192","2208","2224","2240","2256","2272",
"2288","2304","2320","2336","2352","2368","2384","2400","2416","2432","2448","2464","2480","2496",
"2512","2528","2544","2560","2576","2592","2608","2624","2640","2656","2672","2688","2704","2720",
"2736","2752","2768","2784","2800","2816","2832","2848","2864","2880","2896","2912","2928","2944",
"2960","2976","2992","3008","3024","3040","3056","3072","3088","3104","3120","3136","3152","3168",
"3184","3200","3216","3232","3248","3264","3280","3296","3312","3328","3344","3360","3376","3392",
"3408","3424","3440","3456","3472","3488","3504","3520","3536","3552","3568","3584","3600","3616",
"3632","3648","3664","3680","3696","3712","3728","3744","3760","3776","3792","3808","3824","3840",
"3856","3872","3888","3904","3920","3936","3952","3968","3984","4000","4016","4032","4048","4064",
"4080","4096","4112","4128","4144","4160","4176","4192","4208","4224","4240","4256","4272","4288",
"4304","4320","4336","4352","4368","4384","4400","4416","4432","4448","4464","4480","4496","4512",
"4528","4544","4560","4576","4592","4608","4624","4640","4656","4672","4688","4704","4720","4736",
"4752","4768","4784","4800","4816","4832","4848","4864","4880","4896","4912","4928","4944","4960",
"4976","4992","5008","5024","5040","5056","5072","5088","5104","5120","5136","5152","5168","5184",
"5200","5216","5232","5248","5264","5280","5296","5312","5328","5344","5360","5376","5392","5408",
"5424","5440","5456","5472","5488","5504","5520","5536","5552","5568","5584","5600","5616","5632",
"5648","5664","5680","5696","5712","5728","5744","5760","5776","5792","5808","5824","5840","5856",
"5872","5888","5904","5920","5936","5952","5968","5984","6000","6016","6032","6048","6064","6080",
"6096","6112","6128","6144","6160","6176","6192","6208","6224","6240","6256","6272","6288","6304",
"6320","6336","6352","6368","6384","6400","6416","6432","6448","6464","6480","6496","6512","6528",
"6544","6560","6576","6592","6608","6624","6640","6656","6672","6688","6704","6720","6736","6752",
"6768","6784","6800","6816","6832","6848","6864","6880","6896","6912","6928","6944","6960","6976",
"6992","7008","7024","7040","7056","7072","7088","7104","7120","7136","7152","7168","7184","7200",
"7216","7232","7248","7264","7280","7296","7312","7328","7344","7360","7376","7392","7408","7424",
"7440","7456","7472","7488","7504","7520","7536","7552","7568","7584","7600","7616","7632","7648",
"7664","7680"]

class Convert_OT(bpy.types.Operator):
	"""Export and Convert all texture to FTEX"""
	bl_idname = "convert.operator"
	bl_label = str()

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		stid = context.scene.STID
		filePath = str()

		# Checking stadium id length, otherwise stadium id not length 5 he will error
		if len(stid) == 5:
			# Checking if output path is nothing
			if context.scene.export_path == str():
				self.report({"WARNING"}, "Export path can't be empty!!")
				print("Export path can't be empty!!")
				return {'CANCELLED'}
			# Checking stadium id in blender and output path
			if not stid in context.scene.export_path:
				self.report({"WARNING"}, "Stadium ID doesn't match!!")
				print("Stadium ID doesn't match!!")
				return {'CANCELLED'}
			# Checking output path before converting texture
			if not context.scene.export_path.endswith(stid + "\\"):
				self.report({"WARNING"}, "Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				print("Selected path is wrong, select like e:g [-->Asset\\model\\bg\\%s<--]!!" % stid)
				return {'CANCELLED'}
		else:
			self.report({"WARNING"}, "Stadium ID isn't correct!!")
			return {'CANCELLED'}
		checks = checkStadiumID(context, True)
		# Checking stadium id before converting texture
		if checks:
			self.report({"WARNING"}, "Stadium ID doesn't match, see more info => Window -> Toggle System Console")
			return {'CANCELLED'}
		if checkMeshMaterialUvs(self, context):
			return {'CANCELLED'}
		bpy.ops.file.make_paths_absolute()
		isConvertedDict = {}
		isConvertedDict.clear()
		if context.scene.part_info == "AD":
			# Output path texture for stadium ads
			outpath = context.scene.export_path[:-6] + "common\\ad\\sourceimages\\tga\\#windx11"
		else:
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
										# Checking texture in node, if node not have texture assigment he will error
										try:
											filePath = nodes.image.filepath
										except:
											self.report({"WARNING"}, "Error when converting texture, check in Blender Console => Window -> Toggle System Console !!")
											print("\nError when converting texture!!")
											print("Check out Object in Parent ({0} --> {1} --> {2}) in Mesh object ({3}) in role ({4})"
													.format(context.scene.part_info, ob.parent.name,ob2.parent.name, ob2.name, nodes.name))
											return {'CANCELLED'}
										
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

										filenames, extension = os.path.splitext(fileName)
										if extension != str():
											# If input texture format is .png will covert first to .dds
											if extension.lower() == '.png':
												fileName = filenames + extension
												PNGPath = os.path.join(dirpath, fileName)
												texconv(PNGPath, dirpath, " -r -y -l -f DXT5 -ft dds -srgb -o ", False)
												newPath = os.path.join(dirpath, filenames + ".dds")
												inPath = newPath
											# If input texture format is .tga will covert first to .dds
											elif extension.lower() == '.tga':
												fileName = filenames + extension
												TGAPath = os.path.join(dirpath, fileName)
												texconv(TGAPath, dirpath, " -r -y -l -f DXT5 -ft dds -srgb -o ", False)
												newPath = os.path.join(dirpath, filenames + ".dds")
												inPath = newPath
											# If input texture format is .dds
											elif extension.lower() == '.dds':
												inPath = filePath
											else:
												# If input texture format not .png/.tga/.dds will not support will cancel operation
												self.report({"WARNING"}, "Not supported texture format, check in Blender Console => Window -> Toggle System Console !!")
												print("\nNot supported texture format!!, Texture format must be .PNG .DDS .TGA")
												print("Conversion Failed !! (File Not Found or Unsupported format)")
												print("**" * len(filenames + extension))
												print("File (" + filenames + extension + ") isn't the right texture format!!")
												print("**" * len(filenames + extension))
												print("\nCheck out Object in Parent ({0} --> {1} --> {2}) in Mesh object ({3}) in role ({4})"
														.format(context.scene.part_info, ob.parent.name,ob2.parent.name, ob2.name, nodes.name))
												return {'CANCELLED'}
											if not os.path.isfile(filePath):
												self.report({"WARNING"}, "Error when converting, file not found, check in Blender Console => Window -> Toggle System Console !!")
												print("\nFile not found in source texture")
												print("\nCheck out Object in Parent ({0} --> {1} --> {2}) in Mesh object ({3}) in role ({4})"
														.format(context.scene.part_info, ob.parent.name,ob2.parent.name, ob2.name, nodes.name))
												print (f"Check out Texture in -> Texture Filename: ({fileName}), Filepath: ({filePath}).")
												return {'CANCELLED'}
											width = nodes.image.size[0]
											height = nodes.image.size[1]
											print (f"Texture Dimensions:({width} x {height})")
											if width > 7680 or height > 7680:
												self.report({"WARNING"}, "Error when converting, texture dimensions out of range, check in Blender Console => Window -> Toggle System Console !!")
												print("\nTexture dimensions out of range, maximum texture dimension is 7680 (8K)?")
												print (f"Check out texture in -> Texture Filename: ({filenames + extension}), Texture Dimensions: ({width} x {height})")
												return {'CANCELLED'}
											if not str(width) in TexDimensions or not str(height) in TexDimensions:
												self.report({"WARNING"}, "Error when converting, texture dimensions isn't correct, check in Blender Console => Window -> Toggle System Console !!")
												print("\nTexture dimensions isn't correct")
												print (f"Check out texture in -> Texture Filename: ({filenames + extension}), Texture Dimensions: ({width} x {height})")
												return {'CANCELLED'}
											if os.path.isfile(inPath):
												convert_dds(inPath, outpath)
												print("Converting texture from object->({0}) in role->({1})-->({2}) ==> ({3}ftex) ".format(
														ob2.name, nodes.name, fileName, fileName[:-3]))
												# if the original texture was .dds itself, no need to delete it
												# otherwise, it was the temp texture we made, so it will be deleted
												if extension.lower() != '.dds':
													try:
														os.remove(inPath)
													except Exception as msg:
														self.report({"WARNING"}, format(msg))
														return {'CANCELLED'}
		self.report({"INFO"}, "Converting texture succesfully...!")
		print("Converting texture succesfully...!")
		return {'FINISHED'}

	pass

class Clear_OT(bpy.types.Operator):
	"""Clear Temporary Data"""
	bl_idname = "clear_temp.operator"
	bl_label = str()
	opname : StringProperty()

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		with open(csvPath, "r") as f:
			filename=f.read()
		if self.opname == "cleartemp":
			fpkdir = os.path.dirname(filename)
			getTextureDir = str()
			textureDir = f"{findDirectory(fpkdir)}sourceimages"
			if os.path.exists(textureDir):
				getTextureDir = getDirPath(textureDir)
			try:
				remove_dir(filename[:-4]+"_fpk")
				remove_file(filename+".xml")
				remove_dds(getTextureDir)
				self.report({"INFO"}, "Clear temporary data succesfully!")
			except:
				self.report({"WARNING"}, "No temporary data found!")
		if self.opname == "cleartempdata":
			dirpath=context.scene.export_path+"\\sourceimages\\tga\\#windx11\\"
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
			self.report({"WARNING"}, format(exception) + " more info see => System Console (^_^)")
			if 'nodes' in format(exception):
				print("\nInfo: ", format(exception) + " more info see => System Console (^_^)")
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
			shutil.copy(baseStartupFile,startupFile)
		bpy.ops.wm.read_homefile()
		return {'FINISHED'}
	pass

class Create_Main_Parts(bpy.types.Operator):
	"""Create Stadium Parts"""
	bl_idname = "main_parts.operator"
	bl_label = str()

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		scn = context.scene
		Create_Parent_Part(self, context)

		if scn.part_info == "AUDIAREA" or scn.part_info == "FLAGAREA" or scn.part_info == "TV":
			parentlist = [(ob.name,ob.name,ob.name) for ob in (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if ob.name in main_list
			if ob.name not in ['LIGHTS','L_FRONT','L_BACK','L_RIGHT','L_LEFT','LightBillboard','LensFlare','Halo','Staff Coach','Steward', 'Staff Walk','Ballboy','Cameraman Crew']]
		else:
			parentlist = [("MESH_"+ob.name,"MESH_"+ob.name,"MESH_"+ob.name) for ob in (bpy.context.scene.objects[context.scene.part_info].children) if ob.type == 'EMPTY' if ob.name in main_list 
			if ob.name not in ['LIGHTS','L_FRONT','L_BACK','L_RIGHT','L_LEFT', 'MESH_CROWD', 'MESH_FLAGAREA','Staff Coach','Steward', 'Staff Walk','Ballboy','Cameraman Crew']]
		parentlist.sort(reverse=0)
		bpy.types.Object.droplist = EnumProperty(name="Parent List", items=parentlist)
		self.report({"INFO"},"Stadium main parts (Parents) has been created...")
		return {'FINISHED'}
	pass

class FMDL_21_PT_Texture_Panel(bpy.types.Panel, bpy.types.AnyType):
	bl_label = "FMDL Texture Settings"
	bl_space_type = 'NODE_EDITOR'
	bl_region_type = 'UI'
	bl_category = 'Tool'
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
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.label(text="Image File")
		mainColumn.operator(FMDL_Scene_Open_Image.bl_idname, icon="FILE_FOLDER")
		mainColumn.operator("edit.operator", text="", icon="FILE_IMAGE")
		mainColumn.operator("reload.operator", text="", icon="FILE_REFRESH")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(node, "fmdl_texture_role", text="Role")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(node, "fmdl_texture_filename", text="Filename")
		mainColumn = self.layout.column()
		mainColumn=mainColumn.row()
		mainColumn.prop(node, "fmdl_texture_directory", text="Directory")

class FMDL_Scene_Open_Image(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	"""Add a Image Texture DDS / PNG / TGA"""
	bl_idname = "open.image"
	bl_label = "Add Texture"
	bl_options = {'REGISTER', 'UNDO'}

	
	import_label = "Add Texture"
	
	filename_ext = "DDS, PNG, TGA"
	filter_glob : StringProperty(default="*.dds;*.png;*.tga", options={'HIDDEN'})

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
		blenderImage=bpy.data.images[fileName]
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
		imagePath = bpy.data.materials[mat_name].node_tree.nodes[node_name].image.filepath
		try:
			bpy.ops.image.external_edit(filepath=imagePath)
		except Exception as msg:
			self.report({"WARNING"}, format(msg))
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
		self.fmdl_material_preset = self.fmdl_material_shader
	except:
		pass

def update_alpha_list(self, context):
	try:
		self.fmdl_alpha_enum = int(self.fmdl_alpha_enum_select)
	except:
		pass

def update_alpha_enum(self, context):
	try:
		if self.fmdl_alpha_enum in [0,16,17,32,48,49,80,112,128,160,192]:
			self.fmdl_alpha_enum_select = f"{self.fmdl_alpha_enum}"
		else:
			self.fmdl_alpha_enum_select = 'Custom'
	except:
		pass

def update_shadow_list(self, context):
	try:
		self.fmdl_shadow_enum = int(self.fmdl_shadow_enum_select)
	except:
		pass

def update_shadow_enum(self, index):
	try:
		if self.fmdl_shadow_enum in [0,1,2,3,4,5,36,38,64,65]:
			self.fmdl_shadow_enum_select = str(self.fmdl_shadow_enum)
		else:
			self.fmdl_shadow_enum_select = 'Custom'
	except:
		pass

def updList(self, context):
	if "_N" in self.HaloTex:
		self.Pivot.y = 0.454784
	elif "_S" in self.HaloTex:
		self.Pivot.y = 0.9
	else:
		self.Pivot.x = 0.0
		self.Pivot.y = 0.0
		self.Pivot.z = 0.0
	pass

def FMDL_Mesh_Flags_twosided_get(self):
	return self.fmdl_alpha_enum & 32 > 0

def FMDL_Mesh_Flags_twosided_set(self, enabled):
	if enabled:
		self.fmdl_alpha_enum |= 32
	else:
		self.fmdl_alpha_enum &= ~32

def FMDL_Mesh_Flags_transparent_get(self):
	return self.fmdl_alpha_enum & 128 > 0

def FMDL_Mesh_Flags_transparent_set(self, enabled):
	if enabled:
		self.fmdl_alpha_enum |= 128
	else:
		self.fmdl_alpha_enum &= ~128

def FMDL_Mesh_Flags_castshadow_get(self):
	return self.fmdl_shadow_enum & 1 == 0

def FMDL_Mesh_Flags_castshadow_set(self, enabled):
	if enabled:
		self.fmdl_shadow_enum &= ~1
	else:
		self.fmdl_shadow_enum |= 1

def FMDL_Mesh_Flags_invisible_get(self):
	return self.fmdl_shadow_enum & 2 > 0

def FMDL_Mesh_Flags_invisible_set(self, enabled):
	if enabled:
		self.fmdl_shadow_enum |= 2
	else:
		self.fmdl_shadow_enum &= ~2
classes = [

	FDMDL_OT_Import_Main_Stadium,
	FDMDL_OT_Import_Extra_Stadium,

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
	Import_Crowd_OT,
	Flags_Area_OT,
	Light_FX,
	Export_TV,
	TV_Objects,
	Pitch_Objects,
	Staff_Coach_Pos,
	New_STID,
	ExportStadium_AD,
	Refresh_Light_Side,
	Stadium_Banner,
	Stadium_Scarecrow,
	Import_lightfx_OT,

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
	pcoll.load("icon_2", os.path.join(icons_dir, "icon_2.dds"), 'IMAGE')
	pcoll.load("icon_3", os.path.join(icons_dir, "icon_3.dds"), 'IMAGE')
	pcoll.load("icon_4", os.path.join(icons_dir, "icon_4.dds"), 'IMAGE')
	pcoll.load("icon_5", os.path.join(icons_dir, "icon_5.dds"), 'IMAGE')
	icons_collections["custom_icons"] = pcoll
	for c in classes:
		bpy.utils.register_class(c)

	domData = minidom.parse(xml_dir+"PesFoxShader.xml")
	shaders = [(shader.getAttribute("shader"), shader.getAttribute("technique"), "Shader Type: "+shader.getAttribute("shader")) 
					for shader in domData.getElementsByTagName("FoxShader") if shader.getAttribute("technique")]
	shaders.sort(reverse=0)
	bpy.types.Material.fmdl_material_preset = EnumProperty(name="Preset", items=shaders)
	bpy.types.Material.fmdl_material_parameters = CollectionProperty(name="Material Parameters", type=FMDL_MaterialParameter)
	bpy.types.Material.fmdl_material_parameter_active = IntProperty(name="FMDL_Material_Parameter_Name_List index", default=-1, options={'SKIP_SAVE'})
	bpy.types.Material.fmdl_material_shader = StringProperty(name="Shader", update=update_shader_list)
	bpy.types.Material.fmdl_material_technique = StringProperty(name="Technique")
	bpy.types.ShaderNodeTexImage.fmdl_texture_filename = StringProperty(name="Texture Filename")
	bpy.types.ShaderNodeTexImage.fmdl_texture_directory = StringProperty(name="Texture Directory")
	bpy.types.ShaderNodeTexImage.fmdl_texture_role = StringProperty(name="Texture Role")

	bpy.types.Object.fmdl_file = BoolProperty(name="Is FMDL file", options={'SKIP_SAVE'})
	bpy.types.Object.fmdl_filename = StringProperty(name="FMDL filename", options={'SKIP_SAVE'})
	bpy.types.Mesh.fmdl_alpha_enum_select = EnumProperty(name="Alpha Enum", 
		items=PesFoxShader.AlphaEnum, 
		default="0",
		update=update_alpha_list,
		options = {'SKIP_SAVE'}
	)
	bpy.types.Mesh.fmdl_shadow_enum_select = EnumProperty(name="Shadow Enum", items=PesFoxShader.ShadowEnum, default="0", update=update_shadow_list, options = {'SKIP_SAVE'})
	bpy.types.Mesh.fmdl_alpha_enum = IntProperty(name="Alpha Flag", default=0, min=0, max=255, update=update_alpha_enum, options = {'SKIP_SAVE'})
	bpy.types.Mesh.fmdl_shadow_enum = IntProperty(name="Shadow Flag", default=0, min=0, max=255, update=update_shadow_enum, options = {'SKIP_SAVE'})
	bpy.types.Mesh.TwoSided = bpy.props.BoolProperty(name = "Two Side",
		get = FMDL_Mesh_Flags_twosided_get,
		set = FMDL_Mesh_Flags_twosided_set,
		options = {'SKIP_SAVE'}
	)
	bpy.types.Mesh.Transparent = bpy.props.BoolProperty(name = "Transparent",
		get = FMDL_Mesh_Flags_transparent_get,
		set = FMDL_Mesh_Flags_transparent_set,
		options = {'SKIP_SAVE'}
	)
	bpy.types.Mesh.fmdl_flags_castshadow = bpy.props.BoolProperty(name = "Cast Shadow",
		get = FMDL_Mesh_Flags_castshadow_get,
		set = FMDL_Mesh_Flags_castshadow_set,
		options = {'SKIP_SAVE'}
	)
	bpy.types.Mesh.fmdl_flags_invisible = bpy.props.BoolProperty(name = "Invisible",
		get = FMDL_Mesh_Flags_invisible_get,
		set = FMDL_Mesh_Flags_invisible_set,
		options = {'SKIP_SAVE'}
	)
	bpy.types.Object.fmdl_export_extensions_enabled = BoolProperty(name="Enable PES FMDL extensions",  default=True)
	bpy.types.Object.fmdl_export_loop_preservation = BoolProperty(name="Preserve split vertices",   default=True)
	bpy.types.Object.fmdl_export_mesh_splitting = BoolProperty(name="Autosplit overlarge meshes",   default=True)
	bpy.types.Scene.fmdl_import_extensions_enabled = BoolProperty(name="Enable PES FMDL extensions", default=True)
	bpy.types.Scene.fmdl_import_loop_preservation = BoolProperty(name="Preserve split vertices", default=True)
	bpy.types.Scene.fmdl_import_mesh_splitting = BoolProperty(name="Autosplit overlarge meshes", default=True)
	bpy.types.Scene.fmdl_import_load_textures = BoolProperty(name="Load textures", default=True)
	bpy.types.Scene.fmdl_import_all_bounding_boxes = BoolProperty(name="Import all bounding boxes", default=False)
	bpy.types.Scene.fixmeshesmooth = BoolProperty(name="FIX-Smooth Meshes", default=True)
	bpy.types.Scene.useFastConvertTexture = BoolProperty(name="Skip Non-Modified textures", default=True)

	bpy.types.Scene.crowd_row_space = FloatProperty(name=" ",step=1,subtype='FACTOR',default=5.0,min=0.0,max=50.0,description="Set a value for vertical space of seat rows. (Default: 5.00)")   
	bpy.types.Object.droplist = EnumProperty(name="Parent List", items=parentlist)

	# bpy.types.Scene.texture_path = StringProperty(name="Texture Path", subtype='DIR_PATH')
	bpy.types.Scene.export_path = StringProperty(name="Export Path", subtype='DIR_PATH')
	bpy.types.Scene.fpk_path = StringProperty(name="Fpk File Path", default='*.fpk', subtype='FILE_PATH')
	bpy.types.Scene.part_info = EnumProperty(name="Part List", items=part_export)
	bpy.types.Scene.STID = StringProperty(name="ID", default="st081")

	bpy.types.Scene.crowd_type_enum0 = EnumProperty(items=behavior0,name='Type C1')
	bpy.types.Scene.crowd_type_enum1 = EnumProperty(items=behavior1,name='Type C2')
	bpy.types.Scene.crowd_type_enum2 = EnumProperty(items=behavior2,name='Type C3')
	
	bpy.types.Scene.tvobject = EnumProperty(name="TV",items=[("tv_large_c","tv_large_c","tv_large_c"),
															("tv_small_c","tv_small_c","tv_small_c")])
	bpy.types.Scene.l_lit_side = EnumProperty(name="Select Side for Lights",items=light_sidelist)
	bpy.types.Object.l_Energy = FloatProperty(name="Energy", min=0.25, max=5.0, subtype='FACTOR', default=1.5)
	bpy.types.Scene.l_fxe = FloatProperty(name="Energy ",min=0.25,max=5.0,subtype='FACTOR',default=2.5)

	lfx_tex_list.sort(reverse=1)
	bpy.types.Scene.l_fx_tex= EnumProperty(name="Texture Type for Light Billboard", items=lfx_tex_list, default="tex_star_02.ftex")
	bpy.types.Scene.lensflaretex= EnumProperty(name="Texture Type for Lens Flare", items=LensFlareTexList, default="tex_ghost_05.ftex")
	bpy.types.Scene.time_mode = EnumProperty(name="Select Time/Weather", items=timeMode, default="nf")

	HaloTexList.sort(reverse=1)
	bpy.types.Object.HaloTex = EnumProperty(name="Texture Type for Halo",items=HaloTexList, update=updList)
	bpy.types.Object.rotY = BoolProperty(name="fixRotY", default=0)
	bpy.types.Object.Pivot = FloatVectorProperty(name="Pivot", default=(0.0, 0.9, 0.0), min= 0.0, max= 1.0, subtype = 'XYZ')

	bpy.types.Object.scrName = StringProperty(name="Name")
	bpy.types.Object.scrTransformEntity = StringProperty(name="Transform")
	bpy.types.Object.scrEntityPtr = StringProperty(name="EntityPtr")
	bpy.types.Object.scrKind = IntProperty(name="Kind")
	bpy.types.Object.scrDirection = IntProperty(name="Direction")
	bpy.types.Object.scrDemoGroup = IntProperty(name="DemoGroup")
	bpy.types.Object.scrLimitedRotatable = BoolProperty(name="Limited Rotatable Object Links", default=False)
	bpy.types.Scene.scrGenerateFpkd = BoolProperty(name="Only Generate .FPKD", default=False)
	bpy.types.Object.ObjectLinksName = StringProperty(name="Entity Name")
	bpy.types.Object.EntityObjectLinks = StringProperty(name="Entity Links")
	bpy.types.Object.packagePathHash = StringProperty(name="Path Hash")
	bpy.types.Object.maxRotDegreeLeft = IntProperty(name="Degree Left", min= 0, max= 99)
	bpy.types.Object.maxRotDegreeRight = IntProperty(name="Degree Right", min= 0, max= 99)
	bpy.types.Object.maxRotSpeedLeft = IntProperty(name="Speed Left", min= 0, max= 99)
	bpy.types.Object.maxRotSpeedRight = IntProperty(name="Speed Right", min= 0, max= 99)

def unregister():
	for pcoll in icons_collections.values():
		bpy.utils.previews.remove(pcoll)
	icons_collections.clear()
	for c in classes[::-1]:
		bpy.utils.unregister_class(c)
