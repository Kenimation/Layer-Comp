import bpy
from ..node import *
from ..node_v4_4_below._utils import *

class CompositorNodeOuterGlow(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeOuterGlow'
	bl_label='Outer Glow'
	bl_icon='LIGHT_SUN'
	
	mode_items=(('STEP', 'Step', 'STEP'),
		('THRESHOLD', 'Threshould', 'THRESHOLD'),
		('DISTANCE', 'Distance', 'DISTANCE'),
		('FEATHER', 'Feather', 'FEATHER'))

	falloff_items=(('SMOOTH', 'Smooth', 'Smooth', 'SMOOTHCURVE', 0),
		('SPHERE', 'Sphere', 'Sphere', 'SPHERECURVE', 1),
		('ROOT', 'Root', 'Root', 'ROOTCURVE', 2),
		('INVERSE_SQUARE', 'Inverse Square', 'Inverse Square', 'INVERSESQUARECURVE', 3),
		('SHARP', 'Sharp', 'Sharp', 'SHARPCURVE', 4),
		('LINEAR', 'Linear', 'Linear', 'LINCURVE', 5))
		
	def update_mode(self, context):
		self.node_tree.nodes['Dilate/Erode'].mode = self.mode
	
	def update_falloff(self, context):
		self.node_tree.nodes['Dilate/Erode'].falloff = self.falloff

	def update_edge(self, context):
		self.node_tree.nodes["Dilate/Erode"].edge = self.edge

	def update_distance(self, context):
		self.node_tree.nodes["Dilate/Erode"].distance = self.distance

	mode : bpy.props.EnumProperty(default = 'FEATHER', items = mode_items, name = "Mode", update = update_mode)

	falloff : bpy.props.EnumProperty(default = 'SHARP', items = falloff_items, name = "Falloff", update = update_falloff)

	edge : bpy.props.FloatProperty(default = 0, name = "Edge", update = update_edge, min=-100, max=100)

	distance : bpy.props.IntProperty(default = 35, name = "Size", update = update_distance, min=-100, max=100)

	def init(self, context):
		self.getNodetree(context)
		self.inputs[1].default_value = (1.000000, 0.996410, 0.763167, 1.000000)
		self.mode = 'FEATHER'
		self.falloff = 'SMOOTH'
		self.distance = 35
		self.inputs[4].default_value = 1
	

	def draw_buttons(self, context, layout):
		layout.prop(self, 'mode', text='Mode')
		if self.mode == "FEATHER":
			layout.prop(self, 'falloff', text='Falloff')

		if self.mode == "THRESHOLD":
			layout.prop(self, 'edge')
			
		layout.prop(self, 'distance')

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

		#Socket Outer
		outer_socket = node_tree.interface.new_socket(name = "Outer", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		outer_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		outer_socket.attribute_domain = 'POINT'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (1.0, 0.9964100122451782, 0.7631670236587524, 1.0)
		color_socket.attribute_domain = 'POINT'

		#Socket Fill
		fill_socket = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketFloat')
		fill_socket.default_value = 0.0
		fill_socket.min_value = 0.0
		fill_socket.max_value = 1.0
		fill_socket.subtype = 'FACTOR'
		fill_socket.attribute_domain = 'POINT'

		#Socket Color
		color_socket_1 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
		color_socket_1.attribute_domain = 'POINT'

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
		mix.inputs[1].default_value = (0.0, 0.0, 0.0, 0.0)

		#node Dilate/Erode
		dilate_erode = node_tree.nodes.new("CompositorNodeDilateErode")
		dilate_erode.name = "Dilate/Erode"
		dilate_erode.distance = 35
		dilate_erode.edge = 0.0
		dilate_erode.falloff = 'SMOOTH'
		dilate_erode.mode = 'FEATHER'

		#node Set Alpha
		set_alpha = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha.name = "Set Alpha"
		set_alpha.mode = 'APPLY'

		#node Alpha Over
		alpha_over = node_tree.nodes.new("CompositorNodeAlphaOver")
		alpha_over.name = "Alpha Over"
		alpha_over.premul = 0.0
		alpha_over.use_premultiply = False
		#Fac
		alpha_over.inputs[0].default_value = 1.0

		#node Set Alpha.001
		set_alpha_001 = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha_001.name = "Set Alpha.001"
		set_alpha_001.mode = 'APPLY'

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'SUBTRACT'
		math.use_clamp = False
		#Value
		math.inputs[0].default_value = 1.0

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.use_alpha = False
		mix_001.use_clamp = False

		#initialize node_tree links
		#separate_color.Alpha -> math.Value
		node_tree.links.new(separate_color.outputs[3], math.inputs[1])
		#math.Value -> set_alpha_001.Alpha
		node_tree.links.new(math.outputs[0], set_alpha_001.inputs[1])
		#mix.Image -> dilate_erode.Mask
		node_tree.links.new(mix.outputs[0], dilate_erode.inputs[0])
		#separate_color.Alpha -> mix.Image
		node_tree.links.new(separate_color.outputs[3], mix.inputs[2])
		#dilate_erode.Mask -> set_alpha.Alpha
		node_tree.links.new(dilate_erode.outputs[0], set_alpha.inputs[1])
		#set_alpha.Image -> set_alpha_001.Image
		node_tree.links.new(set_alpha.outputs[0], set_alpha_001.inputs[0])
		#set_alpha.Image -> alpha_over.Image
		node_tree.links.new(set_alpha.outputs[0], alpha_over.inputs[1])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#alpha_over.Image -> group_output.Image
		node_tree.links.new(alpha_over.outputs[0], group_output.inputs[0])
		#group_input.Color -> set_alpha.Image
		node_tree.links.new(group_input.outputs[1], set_alpha.inputs[0])
		#mix_001.Image -> alpha_over.Image
		node_tree.links.new(mix_001.outputs[0], alpha_over.inputs[2])
		#group_input.Image -> mix_001.Image
		node_tree.links.new(group_input.outputs[0], mix_001.inputs[1])
		#group_input.Fill -> mix_001.Fac
		node_tree.links.new(group_input.outputs[2], mix_001.inputs[0])
		#group_input.Color -> mix_001.Image
		node_tree.links.new(group_input.outputs[3], mix_001.inputs[2])
		#group_input.Opacity -> mix.Fac
		node_tree.links.new(group_input.outputs[4], mix.inputs[0])
		#set_alpha_001.Image -> group_output.Outer
		node_tree.links.new(set_alpha_001.outputs[0], group_output.inputs[1])
		return node_tree
