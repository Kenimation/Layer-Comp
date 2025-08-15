import bpy
from ..node import *

class CompositorNodeBoundaryLine(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeBoundaryLine'
	bl_label='BoundaryLine'
	bl_icon='MOD_LINEART'
	
	filter_items=(('LAPLACE', 'Laplace', 'Laplace'),
		('SOBEL', 'Sobel', 'Sobel'),
		('PREWITT', 'Prewitt', 'Prewitt'),
		('KIRSCH', 'Kirsch', 'Kirsch'))

	def update_filter_type(self, context):
		self.node_tree.nodes["Filter"].filter_type = self.filter_type

	filter_type : bpy.props.EnumProperty(default = 'LAPLACE', items = filter_items, name = "Falloff", update = update_filter_type)

	def init(self, context):
		self.getNodetree(context)
		self.filter_type = 'LAPLACE'
		self.inputs["Line Color"].default_value = (1, 0, 0, 1)
		self.inputs["Strength"].default_value = 1
		self.inputs["Threshold"].default_value = 0.5

	def draw_buttons(self, context, layout):
		layout.prop(self, 'filter_type', text='')

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
		image_socket.hide_value = True

		#Socket Line
		line_socket = node_tree.interface.new_socket(name = "Line", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		line_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		line_socket.attribute_domain = 'POINT'
		line_socket.hide_value = True

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Line Color
		line_color_socket = node_tree.interface.new_socket(name = "Line Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		line_color_socket.default_value = (1.0, 0.0, 0.0, 1.0)
		line_color_socket.attribute_domain = 'POINT'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 10000.0
		strength_socket.subtype = 'NONE'
		strength_socket.attribute_domain = 'POINT'

		#Socket Threshold
		threshold_socket = node_tree.interface.new_socket(name = "Threshold", in_out='INPUT', socket_type = 'NodeSocketFloat')
		threshold_socket.default_value = 0.5
		threshold_socket.min_value = 0.0
		threshold_socket.max_value = 10000.0
		threshold_socket.subtype = 'NONE'
		threshold_socket.attribute_domain = 'POINT'

		#Socket Fill
		fill_socket = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketFloat')
		fill_socket.default_value = 0.0
		fill_socket.min_value = 0.0
		fill_socket.max_value = 1.0
		fill_socket.subtype = 'FACTOR'
		fill_socket.attribute_domain = 'POINT'

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Filter
		filter = node_tree.nodes.new("CompositorNodeFilter")
		filter.name = "Filter"
		filter.filter_type = 'LAPLACE'
		#Fac
		filter.inputs[0].default_value = 1.0

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False

		#node Math.001
		math_001 = node_tree.nodes.new("CompositorNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = 0.10000000149011612

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'GREATER_THAN'
		math_002.use_clamp = False

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.use_alpha = False
		mix.use_clamp = False

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.use_alpha = False
		mix_001.use_clamp = False
		#Image
		mix_001.inputs[1].default_value = (0.0, 0.0, 0.0, 0.0)

		#node Mix.002
		mix_002 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.use_alpha = False
		mix_002.use_clamp = False

		#initialize node_tree links
		#math.Value -> math_002.Value
		node_tree.links.new(math.outputs[0], math_002.inputs[0])
		#math_002.Value -> mix.Fac
		node_tree.links.new(math_002.outputs[0], mix.inputs[0])
		#math_002.Value -> mix_001.Fac
		node_tree.links.new(math_002.outputs[0], mix_001.inputs[0])
		#filter.Image -> math.Value
		node_tree.links.new(filter.outputs[0], math.inputs[0])
		#math_001.Value -> math_002.Value
		node_tree.links.new(math_001.outputs[0], math_002.inputs[1])
		#group_input.Image -> filter.Image
		node_tree.links.new(group_input.outputs[0], filter.inputs[1])
		#mix_002.Image -> mix.Image
		node_tree.links.new(mix_002.outputs[0], mix.inputs[1])
		#mix.Image -> group_output.Image
		node_tree.links.new(mix.outputs[0], group_output.inputs[0])
		#group_input.Line Color -> mix.Image
		node_tree.links.new(group_input.outputs[1], mix.inputs[2])
		#group_input.Line Color -> mix_001.Image
		node_tree.links.new(group_input.outputs[1], mix_001.inputs[2])
		#mix_001.Image -> group_output.Line
		node_tree.links.new(mix_001.outputs[0], group_output.inputs[1])
		#group_input.Strength -> math.Value
		node_tree.links.new(group_input.outputs[2], math.inputs[1])
		#group_input.Threshold -> math_001.Value
		node_tree.links.new(group_input.outputs[3], math_001.inputs[0])
		#group_input.Fill -> mix_002.Fac
		node_tree.links.new(group_input.outputs[4], mix_002.inputs[0])
		#group_input.Image -> mix_002.Image
		node_tree.links.new(group_input.outputs[0], mix_002.inputs[1])
		#group_input.Color -> mix_002.Image
		node_tree.links.new(group_input.outputs[5], mix_002.inputs[2])
		return node_tree
