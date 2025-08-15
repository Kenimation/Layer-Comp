import bpy
from ..node import *
from ._utils import *

class CompositorNodeColorSelection(bpy.types.CompositorNodeCustomGroup, Node, Key_Node):
	bl_name='CompositorNodeColorSelection'
	bl_label='Color Selection'
	bl_icon='VIS_SEL_11'

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
			if "Color" in input.name:
				input.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)

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

		#Socket Color1
		color1_socket = node_tree.interface.new_socket(name = "Color1", in_out='INPUT', socket_type = 'NodeSocketColor')
		color1_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color1_socket.attribute_domain = 'POINT'

		#Socket Color2
		color2_socket = node_tree.interface.new_socket(name = "Color2", in_out='INPUT', socket_type = 'NodeSocketColor')
		color2_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color2_socket.attribute_domain = 'POINT'

		#Socket Color3
		color3_socket = node_tree.interface.new_socket(name = "Color3", in_out='INPUT', socket_type = 'NodeSocketColor')
		color3_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color3_socket.attribute_domain = 'POINT'

		#Socket Color4
		color4_socket = node_tree.interface.new_socket(name = "Color4", in_out='INPUT', socket_type = 'NodeSocketColor')
		color4_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color4_socket.attribute_domain = 'POINT'

		#Socket Color5
		color5_socket = node_tree.interface.new_socket(name = "Color5", in_out='INPUT', socket_type = 'NodeSocketColor')
		color5_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color5_socket.attribute_domain = 'POINT'

		#Socket Color6
		color6_socket = node_tree.interface.new_socket(name = "Color6", in_out='INPUT', socket_type = 'NodeSocketColor')
		color6_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color6_socket.attribute_domain = 'POINT'

		#Socket Color7
		color7_socket = node_tree.interface.new_socket(name = "Color7", in_out='INPUT', socket_type = 'NodeSocketColor')
		color7_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color7_socket.attribute_domain = 'POINT'

		#Socket Color8
		color8_socket = node_tree.interface.new_socket(name = "Color8", in_out='INPUT', socket_type = 'NodeSocketColor')
		color8_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		color8_socket.attribute_domain = 'POINT'


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
		color_key.color_hue = 0.009999999776482582
		color_key.color_saturation = 0.10000000149011612
		color_key.color_value = 0.10000000149011612

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.use_alpha = False
		mix.use_clamp = False
		#Image
		mix.inputs[1].default_value = (0.0, 0.0, 0.0, 0.0)

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Alpha
		alpha = node_tree.nodes.new("CompositorNodeMath")
		alpha.name = "Alpha"
		alpha.operation = 'SUBTRACT'
		alpha.use_clamp = False

		#node Color Key.001
		color_key_001 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_001.name = "Color Key.001"
		color_key_001.color_hue = 0.009999999776482582
		color_key_001.color_saturation = 0.10000000149011612
		color_key_001.color_value = 0.10000000149011612

		#node Alpha.001
		alpha_001 = node_tree.nodes.new("CompositorNodeMath")
		alpha_001.name = "Alpha.001"
		alpha_001.operation = 'SUBTRACT'
		alpha_001.use_clamp = False

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'ADD'
		math_002.use_clamp = False

		#node Mix.002
		mix_002 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.use_alpha = False
		mix_002.use_clamp = False

		#node Color Key.002
		color_key_002 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_002.name = "Color Key.002"
		color_key_002.color_hue = 0.009999999776482582
		color_key_002.color_saturation = 0.10000000149011612
		color_key_002.color_value = 0.10000000149011612

		#node Color Key.003
		color_key_003 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_003.name = "Color Key.003"
		color_key_003.color_hue = 0.009999999776482582
		color_key_003.color_saturation = 0.10000000149011612
		color_key_003.color_value = 0.10000000149011612

		#node Color Key.004
		color_key_004 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_004.name = "Color Key.004"
		color_key_004.color_hue = 0.009999999776482582
		color_key_004.color_saturation = 0.10000000149011612
		color_key_004.color_value = 0.10000000149011612

		#node Color Key.005
		color_key_005 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_005.name = "Color Key.005"
		color_key_005.color_hue = 0.009999999776482582
		color_key_005.color_saturation = 0.10000000149011612
		color_key_005.color_value = 0.10000000149011612

		#node Color Key.006
		color_key_006 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_006.name = "Color Key.006"
		color_key_006.color_hue = 0.009999999776482582
		color_key_006.color_saturation = 0.10000000149011612
		color_key_006.color_value = 0.10000000149011612

		#node Color Key.007
		color_key_007 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_007.name = "Color Key.007"
		color_key_007.color_hue = 0.009999999776482582
		color_key_007.color_saturation = 0.10000000149011612
		color_key_007.color_value = 0.10000000149011612

		#node Alpha.002
		alpha_002 = node_tree.nodes.new("CompositorNodeMath")
		alpha_002.name = "Alpha.002"
		alpha_002.operation = 'SUBTRACT'
		alpha_002.use_clamp = False

		#node Alpha.003
		alpha_003 = node_tree.nodes.new("CompositorNodeMath")
		alpha_003.name = "Alpha.003"
		alpha_003.operation = 'SUBTRACT'
		alpha_003.use_clamp = False

		#node Alpha.004
		alpha_004 = node_tree.nodes.new("CompositorNodeMath")
		alpha_004.name = "Alpha.004"
		alpha_004.operation = 'SUBTRACT'
		alpha_004.use_clamp = False

		#node Alpha.005
		alpha_005 = node_tree.nodes.new("CompositorNodeMath")
		alpha_005.name = "Alpha.005"
		alpha_005.operation = 'SUBTRACT'
		alpha_005.use_clamp = False

		#node Alpha.006
		alpha_006 = node_tree.nodes.new("CompositorNodeMath")
		alpha_006.name = "Alpha.006"
		alpha_006.operation = 'SUBTRACT'
		alpha_006.use_clamp = False

		#node Alpha.007
		alpha_007 = node_tree.nodes.new("CompositorNodeMath")
		alpha_007.name = "Alpha.007"
		alpha_007.operation = 'SUBTRACT'
		alpha_007.use_clamp = False

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

		#node Mix.005
		mix_005 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_005.name = "Mix.005"
		mix_005.blend_type = 'MIX'
		mix_005.use_alpha = False
		mix_005.use_clamp = False

		#node Math.005
		math_005 = node_tree.nodes.new("CompositorNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'ADD'
		math_005.use_clamp = False

		#node Mix.006
		mix_006 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_006.name = "Mix.006"
		mix_006.blend_type = 'MIX'
		mix_006.use_alpha = False
		mix_006.use_clamp = False

		#node Math.006
		math_006 = node_tree.nodes.new("CompositorNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'ADD'
		math_006.use_clamp = False

		#node Mix.007
		mix_007 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_007.name = "Mix.007"
		mix_007.blend_type = 'MIX'
		mix_007.use_alpha = False
		mix_007.use_clamp = False

		#node Math.007
		math_007 = node_tree.nodes.new("CompositorNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'ADD'
		math_007.use_clamp = False

		#node Mix.008
		mix_008 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_008.name = "Mix.008"
		mix_008.blend_type = 'MIX'
		mix_008.use_alpha = False
		mix_008.use_clamp = False

		#node Math.008
		math_008 = node_tree.nodes.new("CompositorNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'ADD'
		math_008.use_clamp = False

		#initialize node_tree links
		#group_input.Image -> color_key.Image
		node_tree.links.new(group_input.outputs[0], color_key.inputs[0])
		#mix_008.Image -> group_output.Image
		node_tree.links.new(mix_008.outputs[0], group_output.inputs[0])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#color_key.Matte -> alpha.Value
		node_tree.links.new(color_key.outputs[1], alpha.inputs[1])
		#separate_color.Alpha -> alpha.Value
		node_tree.links.new(separate_color.outputs[3], alpha.inputs[0])
		#alpha.Value -> mix.Fac
		node_tree.links.new(alpha.outputs[0], mix.inputs[0])
		#group_input.Image -> mix.Image
		node_tree.links.new(group_input.outputs[0], mix.inputs[2])
		#math_008.Value -> group_output.Matte
		node_tree.links.new(math_008.outputs[0], group_output.inputs[1])
		#color_key_001.Matte -> alpha_001.Value
		node_tree.links.new(color_key_001.outputs[1], alpha_001.inputs[1])
		#separate_color.Alpha -> alpha_001.Value
		node_tree.links.new(separate_color.outputs[3], alpha_001.inputs[0])
		#alpha.Value -> math_002.Value
		node_tree.links.new(alpha.outputs[0], math_002.inputs[0])
		#alpha_001.Value -> math_002.Value
		node_tree.links.new(alpha_001.outputs[0], math_002.inputs[1])
		#mix.Image -> mix_002.Image
		node_tree.links.new(mix.outputs[0], mix_002.inputs[1])
		#alpha_001.Value -> mix_002.Fac
		node_tree.links.new(alpha_001.outputs[0], mix_002.inputs[0])
		#group_input.Image -> mix_002.Image
		node_tree.links.new(group_input.outputs[0], mix_002.inputs[2])
		#group_input.Image -> color_key_007.Image
		node_tree.links.new(group_input.outputs[0], color_key_007.inputs[0])
		#group_input.Image -> color_key_002.Image
		node_tree.links.new(group_input.outputs[0], color_key_002.inputs[0])
		#group_input.Image -> color_key_003.Image
		node_tree.links.new(group_input.outputs[0], color_key_003.inputs[0])
		#group_input.Image -> color_key_005.Image
		node_tree.links.new(group_input.outputs[0], color_key_005.inputs[0])
		#group_input.Image -> color_key_004.Image
		node_tree.links.new(group_input.outputs[0], color_key_004.inputs[0])
		#group_input.Image -> color_key_006.Image
		node_tree.links.new(group_input.outputs[0], color_key_006.inputs[0])
		#color_key_002.Matte -> alpha_002.Value
		node_tree.links.new(color_key_002.outputs[1], alpha_002.inputs[1])
		#color_key_003.Matte -> alpha_003.Value
		node_tree.links.new(color_key_003.outputs[1], alpha_003.inputs[1])
		#color_key_004.Matte -> alpha_004.Value
		node_tree.links.new(color_key_004.outputs[1], alpha_004.inputs[1])
		#color_key_005.Matte -> alpha_005.Value
		node_tree.links.new(color_key_005.outputs[1], alpha_005.inputs[1])
		#color_key_006.Matte -> alpha_006.Value
		node_tree.links.new(color_key_006.outputs[1], alpha_006.inputs[1])
		#color_key_007.Matte -> alpha_007.Value
		node_tree.links.new(color_key_007.outputs[1], alpha_007.inputs[1])
		#separate_color.Alpha -> alpha_007.Value
		node_tree.links.new(separate_color.outputs[3], alpha_007.inputs[0])
		#separate_color.Alpha -> alpha_002.Value
		node_tree.links.new(separate_color.outputs[3], alpha_002.inputs[0])
		#separate_color.Alpha -> alpha_003.Value
		node_tree.links.new(separate_color.outputs[3], alpha_003.inputs[0])
		#separate_color.Alpha -> alpha_004.Value
		node_tree.links.new(separate_color.outputs[3], alpha_004.inputs[0])
		#separate_color.Alpha -> alpha_005.Value
		node_tree.links.new(separate_color.outputs[3], alpha_005.inputs[0])
		#separate_color.Alpha -> alpha_006.Value
		node_tree.links.new(separate_color.outputs[3], alpha_006.inputs[0])
		#mix_002.Image -> mix_003.Image
		node_tree.links.new(mix_002.outputs[0], mix_003.inputs[1])
		#group_input.Image -> mix_003.Image
		node_tree.links.new(group_input.outputs[0], mix_003.inputs[2])
		#alpha_002.Value -> mix_003.Fac
		node_tree.links.new(alpha_002.outputs[0], mix_003.inputs[0])
		#math_002.Value -> math_003.Value
		node_tree.links.new(math_002.outputs[0], math_003.inputs[0])
		#alpha_002.Value -> math_003.Value
		node_tree.links.new(alpha_002.outputs[0], math_003.inputs[1])
		#math_003.Value -> math_004.Value
		node_tree.links.new(math_003.outputs[0], math_004.inputs[0])
		#alpha_003.Value -> math_004.Value
		node_tree.links.new(alpha_003.outputs[0], math_004.inputs[1])
		#mix_003.Image -> mix_004.Image
		node_tree.links.new(mix_003.outputs[0], mix_004.inputs[1])
		#alpha_003.Value -> mix_004.Fac
		node_tree.links.new(alpha_003.outputs[0], mix_004.inputs[0])
		#group_input.Image -> mix_004.Image
		node_tree.links.new(group_input.outputs[0], mix_004.inputs[2])
		#mix_004.Image -> mix_005.Image
		node_tree.links.new(mix_004.outputs[0], mix_005.inputs[1])
		#group_input.Image -> mix_005.Image
		node_tree.links.new(group_input.outputs[0], mix_005.inputs[2])
		#alpha_004.Value -> mix_005.Fac
		node_tree.links.new(alpha_004.outputs[0], mix_005.inputs[0])
		#math_004.Value -> math_005.Value
		node_tree.links.new(math_004.outputs[0], math_005.inputs[0])
		#alpha_004.Value -> math_005.Value
		node_tree.links.new(alpha_004.outputs[0], math_005.inputs[1])
		#mix_005.Image -> mix_006.Image
		node_tree.links.new(mix_005.outputs[0], mix_006.inputs[1])
		#alpha_005.Value -> mix_006.Fac
		node_tree.links.new(alpha_005.outputs[0], mix_006.inputs[0])
		#math_005.Value -> math_006.Value
		node_tree.links.new(math_005.outputs[0], math_006.inputs[0])
		#alpha_005.Value -> math_006.Value
		node_tree.links.new(alpha_005.outputs[0], math_006.inputs[1])
		#group_input.Image -> mix_006.Image
		node_tree.links.new(group_input.outputs[0], mix_006.inputs[2])
		#mix_006.Image -> mix_007.Image
		node_tree.links.new(mix_006.outputs[0], mix_007.inputs[1])
		#math_006.Value -> math_007.Value
		node_tree.links.new(math_006.outputs[0], math_007.inputs[0])
		#alpha_006.Value -> math_007.Value
		node_tree.links.new(alpha_006.outputs[0], math_007.inputs[1])
		#alpha_006.Value -> mix_007.Fac
		node_tree.links.new(alpha_006.outputs[0], mix_007.inputs[0])
		#group_input.Image -> mix_007.Image
		node_tree.links.new(group_input.outputs[0], mix_007.inputs[2])
		#mix_007.Image -> mix_008.Image
		node_tree.links.new(mix_007.outputs[0], mix_008.inputs[1])
		#math_007.Value -> math_008.Value
		node_tree.links.new(math_007.outputs[0], math_008.inputs[0])
		#alpha_007.Value -> math_008.Value
		node_tree.links.new(alpha_007.outputs[0], math_008.inputs[1])
		#alpha_007.Value -> mix_008.Fac
		node_tree.links.new(alpha_007.outputs[0], mix_008.inputs[0])
		#group_input.Image -> mix_008.Image
		node_tree.links.new(group_input.outputs[0], mix_008.inputs[2])
		#group_input.Color1 -> color_key.Key Color
		node_tree.links.new(group_input.outputs[1], color_key.inputs[1])
		#group_input.Color2 -> color_key_001.Key Color
		node_tree.links.new(group_input.outputs[2], color_key_001.inputs[1])
		#group_input.Image -> color_key_001.Image
		node_tree.links.new(group_input.outputs[0], color_key_001.inputs[0])
		#group_input.Color3 -> color_key_002.Key Color
		node_tree.links.new(group_input.outputs[3], color_key_002.inputs[1])
		#group_input.Color4 -> color_key_003.Key Color
		node_tree.links.new(group_input.outputs[4], color_key_003.inputs[1])
		#group_input.Color5 -> color_key_004.Key Color
		node_tree.links.new(group_input.outputs[5], color_key_004.inputs[1])
		#group_input.Color6 -> color_key_005.Key Color
		node_tree.links.new(group_input.outputs[6], color_key_005.inputs[1])
		#group_input.Color7 -> color_key_006.Key Color
		node_tree.links.new(group_input.outputs[7], color_key_006.inputs[1])
		#group_input.Color8 -> color_key_007.Key Color
		node_tree.links.new(group_input.outputs[8], color_key_007.inputs[1])
		return node_tree

