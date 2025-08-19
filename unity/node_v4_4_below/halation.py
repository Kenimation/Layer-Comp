import bpy
from ..node import *

class CompositorNodeHalation(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeHalation'
	bl_label='Halation'
	bl_icon='SHADERFX'

	def init(self, context):
		self.getNodetree(context)
		self.inputs[1].default_value = (1,0,0,1)
		self.inputs[2].default_value = 0.3
		self.inputs[3].default_value = 1
		self.inputs[4].default_value = 0.2
		self.inputs[5].default_value = 1.0

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		image_socket.attribute_domain = 'POINT'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (1.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'

		#Socket Threshold
		threshold_socket = node_tree.interface.new_socket(name = "Threshold", in_out='INPUT', socket_type = 'NodeSocketFloat')
		threshold_socket.default_value = 0.30000001192092896
		threshold_socket.min_value = 0.0
		threshold_socket.max_value = 1.0
		threshold_socket.subtype = 'NONE'
		threshold_socket.attribute_domain = 'POINT'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 10000.0
		strength_socket.subtype = 'NONE'
		strength_socket.attribute_domain = 'POINT'

		#Socket Blur Size
		blur_size_socket = node_tree.interface.new_socket(name = "Blur Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_size_socket.default_value = 0.20000000298023224
		blur_size_socket.min_value = 0.0
		blur_size_socket.max_value = 1.0
		blur_size_socket.subtype = 'NONE'
		blur_size_socket.attribute_domain = 'POINT'

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

		#node RGB to BW
		rgb_to_bw = node_tree.nodes.new("CompositorNodeRGBToBW")
		rgb_to_bw.name = "RGB to BW"

		#node Map Range
		map_range = node_tree.nodes.new("CompositorNodeMapRange")
		map_range.name = "Map Range"
		map_range.use_clamp = True
		#From Max
		map_range.inputs[2].default_value = 1.0
		#To Min
		map_range.inputs[3].default_value = 0.0
		#To Max
		map_range.inputs[4].default_value = 1.0

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.aspect_correction = 'X'
		blur.factor = 0.0
		blur.factor_x = 14.606743812561035
		blur.factor_y = 14.606743812561035
		blur.filter_type = 'FAST_GAUSS'
		blur.size_x = 250
		blur.size_y = 250
		blur.use_bokeh = False
		blur.use_extended_bounds = True
		blur.use_gamma_correction = False
		blur.use_relative = False
		blur.use_variable_size = False

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'SCREEN'
		mix.use_alpha = False
		mix.use_clamp = True

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.use_alpha = False
		mix_001.use_clamp = True

		#initialize node_tree links
		#map_range.Value -> blur.Image
		node_tree.links.new(map_range.outputs[0], blur.inputs[0])
		#rgb_to_bw.Val -> map_range.Value
		node_tree.links.new(rgb_to_bw.outputs[0], map_range.inputs[0])
		#mix.Image -> mix_001.Image
		node_tree.links.new(mix.outputs[0], mix_001.inputs[2])
		#blur.Image -> math.Value
		node_tree.links.new(blur.outputs[0], math.inputs[0])
		#math.Value -> mix.Fac
		node_tree.links.new(math.outputs[0], mix.inputs[0])
		#group_input.Image -> rgb_to_bw.Image
		node_tree.links.new(group_input.outputs[0], rgb_to_bw.inputs[0])
		#group_input.Image -> mix_001.Image
		node_tree.links.new(group_input.outputs[0], mix_001.inputs[1])
		#mix_001.Image -> group_output.Image
		node_tree.links.new(mix_001.outputs[0], group_output.inputs[0])
		#group_input.Threshold -> map_range.From Min
		node_tree.links.new(group_input.outputs[2], map_range.inputs[1])
		#group_input.Strength -> math.Value
		node_tree.links.new(group_input.outputs[3], math.inputs[1])
		#group_input.Blur Size -> blur.Size
		node_tree.links.new(group_input.outputs[4], blur.inputs[1])
		#group_input.Opacity -> mix_001.Fac
		node_tree.links.new(group_input.outputs[5], mix_001.inputs[0])
		#group_input.Image -> mix.Image
		node_tree.links.new(group_input.outputs[0], mix.inputs[1])
		#group_input.Color -> mix.Image
		node_tree.links.new(group_input.outputs[1], mix.inputs[2])
		return node_tree