import bpy
from ..node import *
from ._utils import *

class CompositorNodeColorReplace(bpy.types.CompositorNodeCustomGroup, Node, Key_Node):
	bl_name='CompositorNodeColorReplace'
	bl_label='Color Replace'
	bl_icon='OVERLAY'

	def update_count(self, context):
		if self.count >= 2:
			self.node_tree.nodes["Mix.002"].mute = False
			self.node_tree.nodes["Math.002"].mute = False
		else:
			self.node_tree.nodes["Mix.002"].mute = True
			self.node_tree.nodes["Math.002"].mute = True

		if self.count >= 3:
			self.node_tree.nodes["Mix.003"].mute = False
			self.node_tree.nodes["Math.003"].mute = False
		else:
			self.node_tree.nodes["Mix.003"].mute = True
			self.node_tree.nodes["Math.003"].mute = True

		if self.count >= 4:
			self.node_tree.nodes["Mix.004"].mute = False
			self.node_tree.nodes["Math.004"].mute = False
		else:
			self.node_tree.nodes["Mix.004"].mute = True
			self.node_tree.nodes["Math.004"].mute = True

		if self.count >= 5:
			self.node_tree.nodes["Mix.005"].mute = False
			self.node_tree.nodes["Math.005"].mute = False
		else:
			self.node_tree.nodes["Mix.005"].mute = True
			self.node_tree.nodes["Math.005"].mute = True

		if self.count >= 6:
			self.node_tree.nodes["Mix.006"].mute = False
			self.node_tree.nodes["Math.006"].mute = False
		else:
			self.node_tree.nodes["Mix.006"].mute = True
			self.node_tree.nodes["Math.006"].mute = True

		if self.count >= 7:
			self.node_tree.nodes["Mix.007"].mute = False
			self.node_tree.nodes["Math.007"].mute = False
		else:
			self.node_tree.nodes["Mix.007"].mute = True
			self.node_tree.nodes["Math.007"].mute = True

		if self.count >= 8:
			self.node_tree.nodes["Mix.008"].mute = False
			self.node_tree.nodes["Math.008"].mute = False
		else:
			self.node_tree.nodes["Mix.008"].mute = True
			self.node_tree.nodes["Math.008"].mute = True

	count : bpy.props.IntProperty(default = 1, name = "Count", update = update_count, min=1, max=8)

	def init(self, context):
		self.getNodetree(context)
		self.count = 1
		self.init_key()
		for input in self.inputs:
			if input.name == "Key Color":
				input.default_value = (0.92,0,0.059,1)
			if input.name == "Replace Color":
				input.default_value = (0, 0.456, 0.9, 1.0)

	def draw_buttons(self, context, layout):
		layout.prop(self, "count")
		self.draw_key(layout)

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"	
		
		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'

		#Socket Matte
		matte_socket = node_tree.interface.new_socket(name = "Matte", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte_socket.default_value = 0.0
		matte_socket.min_value = -3.4028234663852886e+38
		matte_socket.max_value = 3.4028234663852886e+38
		matte_socket.subtype = 'NONE'
		matte_socket.attribute_domain = 'POINT'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Panel Color1
		color1_panel = node_tree.interface.new_panel("Color1")
		#Socket Key Color
		key_color_socket = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel)
		key_color_socket.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel)
		replace_color_socket.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket.attribute_domain = 'POINT'
		replace_color_socket.description = "Value of the first color input"


		#Panel Color2
		color2_panel = node_tree.interface.new_panel("Color2")
		#Socket Key Color
		key_color_socket_1 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel)
		key_color_socket_1.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket_1.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket_1 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel)
		replace_color_socket_1.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket_1.attribute_domain = 'POINT'
		replace_color_socket_1.description = "Value of the first color input"


		#Panel Color3
		color3_panel = node_tree.interface.new_panel("Color3")
		#Socket Key Color
		key_color_socket_2 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel)
		key_color_socket_2.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket_2.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket_2 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel)
		replace_color_socket_2.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket_2.attribute_domain = 'POINT'
		replace_color_socket_2.description = "Value of the first color input"


		#Panel Color4
		color4_panel = node_tree.interface.new_panel("Color4")
		#Socket Key Color
		key_color_socket_3 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel)
		key_color_socket_3.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket_3.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket_3 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel)
		replace_color_socket_3.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket_3.attribute_domain = 'POINT'
		replace_color_socket_3.description = "Value of the first color input"


		#Panel Color5
		color5_panel = node_tree.interface.new_panel("Color5")
		#Socket Key Color
		key_color_socket_4 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color5_panel)
		key_color_socket_4.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket_4.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket_4 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color5_panel)
		replace_color_socket_4.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket_4.attribute_domain = 'POINT'
		replace_color_socket_4.description = "Value of the first color input"


		#Panel Color6
		color6_panel = node_tree.interface.new_panel("Color6")
		#Socket Key Color
		key_color_socket_5 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color6_panel)
		key_color_socket_5.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket_5.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket_5 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color6_panel)
		replace_color_socket_5.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket_5.attribute_domain = 'POINT'
		replace_color_socket_5.description = "Value of the first color input"


		#Panel Color7
		color7_panel = node_tree.interface.new_panel("Color7")
		#Socket Key Color
		key_color_socket_6 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color7_panel)
		key_color_socket_6.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket_6.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket_6 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color7_panel)
		replace_color_socket_6.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket_6.attribute_domain = 'POINT'
		replace_color_socket_6.description = "Value of the first color input"


		#Panel Color8
		color8_panel = node_tree.interface.new_panel("Color8")
		#Socket Key Color
		key_color_socket_7 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color8_panel)
		key_color_socket_7.default_value = (1.0, 0.0, 0.0, 1.0)
		key_color_socket_7.attribute_domain = 'POINT'

		#Socket Replace Color
		replace_color_socket_7 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color8_panel)
		replace_color_socket_7.default_value = (0.0, 0.2650200128555298, 1.0, 1.0)
		replace_color_socket_7.attribute_domain = 'POINT'
		replace_color_socket_7.description = "Value of the first color input"



		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Color Key
		color_key = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key.name = "Color Key"
		color_key.color_hue = 0.10000000149011612
		color_key.color_saturation = 0.10000000149011612
		color_key.color_value = 0.10000000149011612

		#node Alpha
		alpha = node_tree.nodes.new("CompositorNodeMixRGB")
		alpha.name = "Alpha"
		alpha.blend_type = 'MIX'
		alpha.use_alpha = False
		alpha.use_clamp = False

		#node Alpha.001
		alpha_001 = node_tree.nodes.new("CompositorNodeMath")
		alpha_001.name = "Alpha.001"
		alpha_001.operation = 'SUBTRACT'
		alpha_001.use_clamp = False

		#node Mix.002
		mix_002 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.use_alpha = False
		mix_002.use_clamp = False

		#node Color Key.001
		color_key_001 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_001.name = "Color Key.001"
		color_key_001.color_hue = 0.10000000149011612
		color_key_001.color_saturation = 0.10000000149011612
		color_key_001.color_value = 0.10000000149011612

		#node Alpha.002
		alpha_002 = node_tree.nodes.new("CompositorNodeMath")
		alpha_002.name = "Alpha.002"
		alpha_002.operation = 'SUBTRACT'
		alpha_002.use_clamp = False

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'ADD'
		math_002.use_clamp = False

		#node Color Key.002
		color_key_002 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_002.name = "Color Key.002"
		color_key_002.color_hue = 0.10000000149011612
		color_key_002.color_saturation = 0.10000000149011612
		color_key_002.color_value = 0.10000000149011612

		#node Alpha.003
		alpha_003 = node_tree.nodes.new("CompositorNodeMath")
		alpha_003.name = "Alpha.003"
		alpha_003.operation = 'SUBTRACT'
		alpha_003.use_clamp = False

		#node Mix.003
		mix_003 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_003.name = "Mix.003"
		mix_003.blend_type = 'MIX'
		mix_003.use_alpha = False
		mix_003.use_clamp = False

		#node Math.003
		math_003 = node_tree.nodes.new("CompositorNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'ADD'
		math_003.use_clamp = False

		#node Color Key.003
		color_key_003 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_003.name = "Color Key.003"
		color_key_003.color_hue = 0.10000000149011612
		color_key_003.color_saturation = 0.10000000149011612
		color_key_003.color_value = 0.10000000149011612

		#node Alpha.004
		alpha_004 = node_tree.nodes.new("CompositorNodeMath")
		alpha_004.name = "Alpha.004"
		alpha_004.operation = 'SUBTRACT'
		alpha_004.use_clamp = False

		#node Math.004
		math_004 = node_tree.nodes.new("CompositorNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'ADD'
		math_004.use_clamp = False

		#node Mix.004
		mix_004 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'MIX'
		mix_004.use_alpha = False
		mix_004.use_clamp = False

		#node Color Key.004
		color_key_004 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_004.name = "Color Key.004"
		color_key_004.color_hue = 0.10000000149011612
		color_key_004.color_saturation = 0.10000000149011612
		color_key_004.color_value = 0.10000000149011612

		#node Alpha.005
		alpha_005 = node_tree.nodes.new("CompositorNodeMath")
		alpha_005.name = "Alpha.005"
		alpha_005.operation = 'SUBTRACT'
		alpha_005.use_clamp = False

		#node Color Key.005
		color_key_005 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_005.name = "Color Key.005"
		color_key_005.color_hue = 0.10000000149011612
		color_key_005.color_saturation = 0.10000000149011612
		color_key_005.color_value = 0.10000000149011612

		#node Alpha.006
		alpha_006 = node_tree.nodes.new("CompositorNodeMath")
		alpha_006.name = "Alpha.006"
		alpha_006.operation = 'SUBTRACT'
		alpha_006.use_clamp = False

		#node Color Key.006
		color_key_006 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_006.name = "Color Key.006"
		color_key_006.color_hue = 0.10000000149011612
		color_key_006.color_saturation = 0.10000000149011612
		color_key_006.color_value = 0.10000000149011612

		#node Alpha.007
		alpha_007 = node_tree.nodes.new("CompositorNodeMath")
		alpha_007.name = "Alpha.007"
		alpha_007.operation = 'SUBTRACT'
		alpha_007.use_clamp = False

		#node Color Key.007
		color_key_007 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_007.name = "Color Key.007"
		color_key_007.color_hue = 0.10000000149011612
		color_key_007.color_saturation = 0.10000000149011612
		color_key_007.color_value = 0.10000000149011612

		#node Alpha.008
		alpha_008 = node_tree.nodes.new("CompositorNodeMath")
		alpha_008.name = "Alpha.008"
		alpha_008.operation = 'SUBTRACT'
		alpha_008.use_clamp = False

		#node Mix.005
		mix_005 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_005.name = "Mix.005"
		mix_005.blend_type = 'MIX'
		mix_005.use_alpha = False
		mix_005.use_clamp = False

		#node Mix.006
		mix_006 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_006.name = "Mix.006"
		mix_006.blend_type = 'MIX'
		mix_006.use_alpha = False
		mix_006.use_clamp = False

		#node Mix.007
		mix_007 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_007.name = "Mix.007"
		mix_007.blend_type = 'MIX'
		mix_007.use_alpha = False
		mix_007.use_clamp = False

		#node Mix.008
		mix_008 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_008.name = "Mix.008"
		mix_008.blend_type = 'MIX'
		mix_008.use_alpha = False
		mix_008.use_clamp = False

		#node Math.005
		math_005 = node_tree.nodes.new("CompositorNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'ADD'
		math_005.use_clamp = False

		#node Math.006
		math_006 = node_tree.nodes.new("CompositorNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'ADD'
		math_006.use_clamp = False

		#node Math.007
		math_007 = node_tree.nodes.new("CompositorNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'ADD'
		math_007.use_clamp = False

		#node Math.008
		math_008 = node_tree.nodes.new("CompositorNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'ADD'
		math_008.use_clamp = False

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketFloat"

		#Set locations
		group_output.location = (2584.32080078125, -924.9249877929688)
		group_input.location = (-325.8885192871094, 0.0)
		color_key.location = (-42.03734588623047, 11.316295623779297)
		alpha.location = (421.4525146484375, 83.5213623046875)
		alpha_001.location = (180.302490234375, -4.6454176902771)
		mix_002.location = (682.9976196289062, -50.94557189941406)
		color_key_001.location = (-32.93232727050781, -219.41566467285156)
		alpha_002.location = (180.54991149902344, -201.98194885253906)
		math_002.location = (679.3096313476562, -307.3265380859375)
		color_key_002.location = (-30.521018981933594, -453.9954528808594)
		alpha_003.location = (185.1234130859375, -417.350830078125)
		mix_003.location = (942.2559204101562, -228.4564208984375)
		math_003.location = (943.3591918945312, -480.7840576171875)
		color_key_003.location = (-28.56441307067871, -659.3790283203125)
		alpha_004.location = (190.708251953125, -620.5457153320312)
		math_004.location = (1188.4066162109375, -627.13818359375)
		mix_004.location = (1179.1033935546875, -292.4670715332031)
		color_key_004.location = (-17.675668716430664, -863.0944213867188)
		alpha_005.location = (201.59698486328125, -824.2611694335938)
		color_key_005.location = (-14.564595222473145, -1088.5810546875)
		alpha_006.location = (202.22508239746094, -1037.334716796875)
		color_key_006.location = (-14.564595222473145, -1302.0894775390625)
		alpha_007.location = (204.7080535888672, -1263.2562255859375)
		color_key_007.location = (-8.19024658203125, -1525.1263427734375)
		alpha_008.location = (217.86558532714844, -1537.1595458984375)
		mix_005.location = (1396.7630615234375, -370.9894104003906)
		mix_006.location = (1591.1920166015625, -420.9679260253906)
		mix_007.location = (1823.34619140625, -560.2403564453125)
		mix_008.location = (2112.177978515625, -721.5086059570312)
		math_005.location = (1394.4930419921875, -686.7207641601562)
		math_006.location = (1608.0283203125, -753.7512817382812)
		math_007.location = (1838.9443359375, -865.4688110351562)
		math_008.location = (2102.0048828125, -975.5089721679688)
		separate_color.location = (-38.54753494262695, 237.33021545410156)
		reroute.location = (116.9259033203125, 20.758174896240234)

		#Set dimensions
		group_output.width, group_output.height = 140.0, 100.0
		group_input.width, group_input.height = 140.0, 100.0
		color_key.width, color_key.height = 140.0, 100.0
		alpha.width, alpha.height = 140.0, 100.0
		alpha_001.width, alpha_001.height = 140.0, 100.0
		mix_002.width, mix_002.height = 140.0, 100.0
		color_key_001.width, color_key_001.height = 140.0, 100.0
		alpha_002.width, alpha_002.height = 140.0, 100.0
		math_002.width, math_002.height = 140.0, 100.0
		color_key_002.width, color_key_002.height = 140.0, 100.0
		alpha_003.width, alpha_003.height = 140.0, 100.0
		mix_003.width, mix_003.height = 140.0, 100.0
		math_003.width, math_003.height = 140.0, 100.0
		color_key_003.width, color_key_003.height = 140.0, 100.0
		alpha_004.width, alpha_004.height = 140.0, 100.0
		math_004.width, math_004.height = 140.0, 100.0
		mix_004.width, mix_004.height = 140.0, 100.0
		color_key_004.width, color_key_004.height = 140.0, 100.0
		alpha_005.width, alpha_005.height = 140.0, 100.0
		color_key_005.width, color_key_005.height = 140.0, 100.0
		alpha_006.width, alpha_006.height = 140.0, 100.0
		color_key_006.width, color_key_006.height = 140.0, 100.0
		alpha_007.width, alpha_007.height = 140.0, 100.0
		color_key_007.width, color_key_007.height = 140.0, 100.0
		alpha_008.width, alpha_008.height = 140.0, 100.0
		mix_005.width, mix_005.height = 140.0, 100.0
		mix_006.width, mix_006.height = 140.0, 100.0
		mix_007.width, mix_007.height = 140.0, 100.0
		mix_008.width, mix_008.height = 140.0, 100.0
		math_005.width, math_005.height = 140.0, 100.0
		math_006.width, math_006.height = 140.0, 100.0
		math_007.width, math_007.height = 140.0, 100.0
		math_008.width, math_008.height = 140.0, 100.0
		separate_color.width, separate_color.height = 140.0, 100.0
		reroute.width, reroute.height = 8.0, 100.0

		#initialize node_tree links
		#group_input.Image -> color_key.Image
		node_tree.links.new(group_input.outputs[0], color_key.inputs[0])
		#group_input.Key Color -> color_key_001.Key Color
		node_tree.links.new(group_input.outputs[3], color_key_001.inputs[1])
		#group_input.Image -> color_key_001.Image
		node_tree.links.new(group_input.outputs[0], color_key_001.inputs[0])
		#group_input.Key Color -> color_key_002.Key Color
		node_tree.links.new(group_input.outputs[5], color_key_002.inputs[1])
		#group_input.Image -> color_key_002.Image
		node_tree.links.new(group_input.outputs[0], color_key_002.inputs[0])
		#group_input.Key Color -> color_key_003.Key Color
		node_tree.links.new(group_input.outputs[7], color_key_003.inputs[1])
		#group_input.Image -> color_key_003.Image
		node_tree.links.new(group_input.outputs[0], color_key_003.inputs[0])
		#group_input.Key Color -> color_key_004.Key Color
		node_tree.links.new(group_input.outputs[9], color_key_004.inputs[1])
		#group_input.Image -> color_key_004.Image
		node_tree.links.new(group_input.outputs[0], color_key_004.inputs[0])
		#group_input.Key Color -> color_key_005.Key Color
		node_tree.links.new(group_input.outputs[11], color_key_005.inputs[1])
		#group_input.Image -> color_key_005.Image
		node_tree.links.new(group_input.outputs[0], color_key_005.inputs[0])
		#group_input.Key Color -> color_key_006.Key Color
		node_tree.links.new(group_input.outputs[13], color_key_006.inputs[1])
		#group_input.Image -> color_key_006.Image
		node_tree.links.new(group_input.outputs[0], color_key_006.inputs[0])
		#group_input.Key Color -> color_key_007.Key Color
		node_tree.links.new(group_input.outputs[15], color_key_007.inputs[1])
		#group_input.Image -> color_key_007.Image
		node_tree.links.new(group_input.outputs[0], color_key_007.inputs[0])
		#group_input.Replace Color -> alpha.Image
		node_tree.links.new(group_input.outputs[2], alpha.inputs[2])
		#alpha.Image -> mix_002.Image
		node_tree.links.new(alpha.outputs[0], mix_002.inputs[1])
		#group_input.Replace Color -> mix_002.Image
		node_tree.links.new(group_input.outputs[4], mix_002.inputs[2])
		#group_input.Replace Color -> mix_003.Image
		node_tree.links.new(group_input.outputs[6], mix_003.inputs[2])
		#mix_002.Image -> mix_003.Image
		node_tree.links.new(mix_002.outputs[0], mix_003.inputs[1])
		#mix_003.Image -> mix_004.Image
		node_tree.links.new(mix_003.outputs[0], mix_004.inputs[1])
		#group_input.Replace Color -> mix_004.Image
		node_tree.links.new(group_input.outputs[8], mix_004.inputs[2])
		#mix_004.Image -> mix_005.Image
		node_tree.links.new(mix_004.outputs[0], mix_005.inputs[1])
		#group_input.Replace Color -> mix_005.Image
		node_tree.links.new(group_input.outputs[10], mix_005.inputs[2])
		#mix_005.Image -> mix_006.Image
		node_tree.links.new(mix_005.outputs[0], mix_006.inputs[1])
		#mix_007.Image -> mix_008.Image
		node_tree.links.new(mix_007.outputs[0], mix_008.inputs[1])
		#mix_008.Image -> group_output.Image
		node_tree.links.new(mix_008.outputs[0], group_output.inputs[0])
		#group_input.Replace Color -> mix_006.Image
		node_tree.links.new(group_input.outputs[12], mix_006.inputs[2])
		#group_input.Replace Color -> mix_007.Image
		node_tree.links.new(group_input.outputs[14], mix_007.inputs[2])
		#group_input.Replace Color -> mix_008.Image
		node_tree.links.new(group_input.outputs[16], mix_008.inputs[2])
		#color_key.Matte -> alpha_001.Value
		node_tree.links.new(color_key.outputs[1], alpha_001.inputs[1])
		#separate_color.Alpha -> alpha_001.Value
		node_tree.links.new(separate_color.outputs[3], alpha_001.inputs[0])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#color_key_001.Matte -> alpha_002.Value
		node_tree.links.new(color_key_001.outputs[1], alpha_002.inputs[1])
		#separate_color.Alpha -> alpha_002.Value
		node_tree.links.new(separate_color.outputs[3], alpha_002.inputs[0])
		#color_key_002.Matte -> alpha_003.Value
		node_tree.links.new(color_key_002.outputs[1], alpha_003.inputs[1])
		#separate_color.Alpha -> alpha_003.Value
		node_tree.links.new(separate_color.outputs[3], alpha_003.inputs[0])
		#color_key_003.Matte -> alpha_004.Value
		node_tree.links.new(color_key_003.outputs[1], alpha_004.inputs[1])
		#separate_color.Alpha -> alpha_004.Value
		node_tree.links.new(separate_color.outputs[3], alpha_004.inputs[0])
		#color_key_004.Matte -> alpha_005.Value
		node_tree.links.new(color_key_004.outputs[1], alpha_005.inputs[1])
		#separate_color.Alpha -> alpha_005.Value
		node_tree.links.new(separate_color.outputs[3], alpha_005.inputs[0])
		#color_key_005.Matte -> alpha_006.Value
		node_tree.links.new(color_key_005.outputs[1], alpha_006.inputs[1])
		#separate_color.Alpha -> alpha_006.Value
		node_tree.links.new(separate_color.outputs[3], alpha_006.inputs[0])
		#color_key_006.Matte -> alpha_007.Value
		node_tree.links.new(color_key_006.outputs[1], alpha_007.inputs[1])
		#separate_color.Alpha -> alpha_007.Value
		node_tree.links.new(separate_color.outputs[3], alpha_007.inputs[0])
		#color_key_007.Matte -> alpha_008.Value
		node_tree.links.new(color_key_007.outputs[1], alpha_008.inputs[1])
		#separate_color.Alpha -> alpha_008.Value
		node_tree.links.new(separate_color.outputs[3], alpha_008.inputs[0])
		#alpha_001.Value -> alpha.Fac
		node_tree.links.new(alpha_001.outputs[0], alpha.inputs[0])
		#alpha_001.Value -> math_002.Value
		node_tree.links.new(alpha_001.outputs[0], math_002.inputs[0])
		#alpha_002.Value -> mix_002.Fac
		node_tree.links.new(alpha_002.outputs[0], mix_002.inputs[0])
		#alpha_002.Value -> math_002.Value
		node_tree.links.new(alpha_002.outputs[0], math_002.inputs[1])
		#alpha_003.Value -> mix_003.Fac
		node_tree.links.new(alpha_003.outputs[0], mix_003.inputs[0])
		#math_002.Value -> math_003.Value
		node_tree.links.new(math_002.outputs[0], math_003.inputs[0])
		#alpha_003.Value -> math_003.Value
		node_tree.links.new(alpha_003.outputs[0], math_003.inputs[1])
		#alpha_004.Value -> mix_004.Fac
		node_tree.links.new(alpha_004.outputs[0], mix_004.inputs[0])
		#alpha_004.Value -> math_004.Value
		node_tree.links.new(alpha_004.outputs[0], math_004.inputs[1])
		#math_003.Value -> math_004.Value
		node_tree.links.new(math_003.outputs[0], math_004.inputs[0])
		#alpha_005.Value -> mix_005.Fac
		node_tree.links.new(alpha_005.outputs[0], mix_005.inputs[0])
		#math_004.Value -> math_005.Value
		node_tree.links.new(math_004.outputs[0], math_005.inputs[0])
		#alpha_005.Value -> math_005.Value
		node_tree.links.new(alpha_005.outputs[0], math_005.inputs[1])
		#alpha_006.Value -> mix_006.Fac
		node_tree.links.new(alpha_006.outputs[0], mix_006.inputs[0])
		#math_005.Value -> math_006.Value
		node_tree.links.new(math_005.outputs[0], math_006.inputs[0])
		#alpha_006.Value -> math_006.Value
		node_tree.links.new(alpha_006.outputs[0], math_006.inputs[1])
		#math_006.Value -> math_007.Value
		node_tree.links.new(math_006.outputs[0], math_007.inputs[0])
		#mix_006.Image -> mix_007.Image
		node_tree.links.new(mix_006.outputs[0], mix_007.inputs[1])
		#alpha_007.Value -> mix_007.Fac
		node_tree.links.new(alpha_007.outputs[0], mix_007.inputs[0])
		#alpha_007.Value -> math_007.Value
		node_tree.links.new(alpha_007.outputs[0], math_007.inputs[1])
		#math_007.Value -> math_008.Value
		node_tree.links.new(math_007.outputs[0], math_008.inputs[0])
		#alpha_008.Value -> mix_008.Fac
		node_tree.links.new(alpha_008.outputs[0], mix_008.inputs[0])
		#alpha_008.Value -> math_008.Value
		node_tree.links.new(alpha_008.outputs[0], math_008.inputs[1])
		#math_008.Value -> group_output.Matte
		node_tree.links.new(math_008.outputs[0], group_output.inputs[1])
		#group_input.Image -> alpha.Image
		node_tree.links.new(group_input.outputs[0], alpha.inputs[1])
		#group_input.Key Color -> color_key.Key Color
		node_tree.links.new(group_input.outputs[1], color_key.inputs[1])
		return node_tree
