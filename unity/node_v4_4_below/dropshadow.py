import bpy
from ..node import *

class CompositorNodeDropShadow(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeDropShadow'
	bl_label='DropShadow'
	bl_icon='SELECT_SUBTRACT'

	def init(self, context):
		self.getNodetree(context)
		self.inputs[2].default_value = 0.6108649969100952
		self.inputs[3].default_value = 15
		self.inputs[4].default_value = 0.2
		self.inputs[5].default_value = 1

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'

		#Socket Shadow
		shadow_socket = node_tree.interface.new_socket(name = "Shadow", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		shadow_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		shadow_socket.attribute_domain = 'POINT'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'

		#Socket Angle
		angle_socket = node_tree.interface.new_socket(name = "Angle", in_out='INPUT', socket_type = 'NodeSocketFloat')
		angle_socket.default_value = 0.6108649969100952
		angle_socket.min_value = -3.4028234663852886e+38
		angle_socket.max_value = 3.4028234663852886e+38
		angle_socket.subtype = 'ANGLE'
		angle_socket.attribute_domain = 'POINT'

		#Socket Distance
		distance_socket = node_tree.interface.new_socket(name = "Distance", in_out='INPUT', socket_type = 'NodeSocketFloat')
		distance_socket.default_value = 15.0
		distance_socket.min_value = 0.0
		distance_socket.max_value = 3.4028234663852886e+38
		distance_socket.subtype = 'NONE'
		distance_socket.attribute_domain = 'POINT'

		#Socket Blur Amount
		blur_amount_socket = node_tree.interface.new_socket(name = "Blur Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_amount_socket.default_value = 0.20000000298023224
		blur_amount_socket.min_value = 0.0
		blur_amount_socket.max_value = 1.0
		blur_amount_socket.subtype = 'NONE'
		blur_amount_socket.attribute_domain = 'POINT'

		#Socket Opacity
		opacity_socket = node_tree.interface.new_socket(name = "Opacity", in_out='INPUT', socket_type = 'NodeSocketFloat')
		opacity_socket.default_value = 1.0
		opacity_socket.min_value = 0.0
		opacity_socket.max_value = 1.0
		opacity_socket.subtype = 'FACTOR'
		opacity_socket.attribute_domain = 'POINT'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Alpha Over
		alpha_over = node_tree.nodes.new("CompositorNodeAlphaOver")
		alpha_over.name = "Alpha Over"
		alpha_over.premul = 0.0
		alpha_over.use_premultiply = False
		#Fac
		alpha_over.inputs[0].default_value = 1.0

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.use_alpha = False
		mix.use_clamp = False
		#Image
		mix.inputs[1].default_value = (0.0, 0.0, 0.0, 1.0)

		#node Set Alpha
		set_alpha = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha.name = "Set Alpha"
		set_alpha.mode = 'APPLY'

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.aspect_correction = 'NONE'
		blur.factor = 0.0
		blur.factor_x = 0.0
		blur.factor_y = 0.0
		blur.filter_type = 'GAUSS'
		blur.size_x = 75
		blur.size_y = 75
		blur.use_bokeh = False
		blur.use_extended_bounds = True
		blur.use_gamma_correction = False
		blur.use_relative = False
		blur.use_variable_size = False

		#node Translate
		translate = node_tree.nodes.new("CompositorNodeTranslate")
		translate.name = "Translate"
		translate.interpolation = 'NEAREST'
		translate.use_relative = False
		translate.wrap_axis = 'NONE'

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False
		#Value_001
		math.inputs[1].default_value = 5.0

		#node Math.001
		math_001 = node_tree.nodes.new("CompositorNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = -1.0

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'COSINE'
		math_002.use_clamp = False

		#node Math.003
		math_003 = node_tree.nodes.new("CompositorNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'SINE'
		math_003.use_clamp = False

		#node Math.004
		math_004 = node_tree.nodes.new("CompositorNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'MULTIPLY'
		math_004.use_clamp = False

		#node Math.005
		math_005 = node_tree.nodes.new("CompositorNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'MULTIPLY'
		math_005.use_clamp = False

		#initialize node_tree links
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#alpha_over.Image -> group_output.Image
		node_tree.links.new(alpha_over.outputs[0], group_output.inputs[0])
		#translate.Image -> alpha_over.Image
		node_tree.links.new(translate.outputs[0], alpha_over.inputs[1])
		#separate_color.Alpha -> mix.Image
		node_tree.links.new(separate_color.outputs[3], mix.inputs[2])
		#mix.Image -> set_alpha.Alpha
		node_tree.links.new(mix.outputs[0], set_alpha.inputs[1])
		#set_alpha.Image -> blur.Image
		node_tree.links.new(set_alpha.outputs[0], blur.inputs[0])
		#group_input.Blur Amount -> blur.Size
		node_tree.links.new(group_input.outputs[4], blur.inputs[1])
		#blur.Image -> translate.Image
		node_tree.links.new(blur.outputs[0], translate.inputs[0])
		#group_input.Distance -> math.Value
		node_tree.links.new(group_input.outputs[3], math.inputs[0])
		#group_input.Angle -> math_001.Value
		node_tree.links.new(group_input.outputs[2], math_001.inputs[0])
		#math_001.Value -> math_002.Value
		node_tree.links.new(math_001.outputs[0], math_002.inputs[0])
		#math_001.Value -> math_003.Value
		node_tree.links.new(math_001.outputs[0], math_003.inputs[0])
		#math_002.Value -> math_004.Value
		node_tree.links.new(math_002.outputs[0], math_004.inputs[0])
		#math.Value -> math_004.Value
		node_tree.links.new(math.outputs[0], math_004.inputs[1])
		#math_003.Value -> math_005.Value
		node_tree.links.new(math_003.outputs[0], math_005.inputs[0])
		#math.Value -> math_005.Value
		node_tree.links.new(math.outputs[0], math_005.inputs[1])
		#math_004.Value -> translate.X
		node_tree.links.new(math_004.outputs[0], translate.inputs[1])
		#math_005.Value -> translate.Y
		node_tree.links.new(math_005.outputs[0], translate.inputs[2])
		#translate.Image -> group_output.Shadow
		node_tree.links.new(translate.outputs[0], group_output.inputs[1])
		#group_input.Image -> alpha_over.Image
		node_tree.links.new(group_input.outputs[0], alpha_over.inputs[2])
		#group_input.Color -> set_alpha.Image
		node_tree.links.new(group_input.outputs[1], set_alpha.inputs[0])
		#group_input.Opacity -> mix.Fac
		node_tree.links.new(group_input.outputs[5], mix.inputs[0])
		return node_tree
