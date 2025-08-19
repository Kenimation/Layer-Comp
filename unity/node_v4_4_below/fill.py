import bpy
from ..node import *
from ._utils import *

class CompositorNodeFill(bpy.types.CompositorNodeCustomGroup, Node, Mix_Node):
	bl_name='CompositorNodeFill'
	bl_label='Fill'
	bl_icon='SNAP_FACE'

	def init(self, context):
		self.blend_type = 'MIX'
		self.getNodetree(context)
		self.inputs["Fill"].default_value = (1.0, 0.0, 0.0, 1.0)
		self.inputs["Strength"].default_value = 1

	def draw_buttons(self, context, layout):
		layout.prop(self, 'blend_type', text='')

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"	

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.hide_value = True

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (1.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.use_alpha = True
		mix.use_clamp = False

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.use_alpha = True
		mix_001.use_clamp = False
		#Image
		mix_001.inputs[1].default_value = (0.0, 0.0, 0.0, 0.0)

		#initialize node_tree links
		#mix_001.Image -> mix.Fac
		node_tree.links.new(mix_001.outputs[0], mix.inputs[0])
		#mix.Image -> group_output.Image
		node_tree.links.new(mix.outputs[0], group_output.inputs[0])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#group_input.Color -> mix.Image
		node_tree.links.new(group_input.outputs[1], mix.inputs[2])
		#separate_color.Alpha -> mix_001.Image
		node_tree.links.new(separate_color.outputs[3], mix_001.inputs[2])
		#group_input.Image -> mix.Image
		node_tree.links.new(group_input.outputs[0], mix.inputs[1])
		#group_input.Strength -> mix_001.Fac
		node_tree.links.new(group_input.outputs[2], mix_001.inputs[0])
		return node_tree

class CompositorNodeSpotFill(bpy.types.CompositorNodeCustomGroup, Node, Mix_Node, Mask_Node):
	bl_name='CompositorNodeSpotFill'
	bl_label='Spot Fill'
	bl_icon='SURFACE_NCIRCLE'

	def init(self, context):
		self.getNodetree(context)
		self.blend_type = 'MIX'
		self.inputs["Fill"].default_value = (1.0, 0.0, 0.0, 1.0)
		self.node_tree.nodes["Mask"].x = 0.5
		self.node_tree.nodes["Mask"].y = 0.5
		self.node_tree.nodes["Mask"].mask_width = 1
		self.node_tree.nodes["Mask"].mask_height = 0.55
		self.inputs["Falloff"].default_value = 1
		self.inputs["Strength"].default_value = 1

	def draw_buttons(self, context, layout):
		layout.prop(self, 'blend_type', text='')
		self.draw_mask(layout)

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"	
		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		image_socket.attribute_domain = 'POINT'

		#Socket Fill
		fill_socket = node_tree.interface.new_socket(name = "Fill", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		fill_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		fill_socket.attribute_domain = 'POINT'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (1.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'

		#Socket Falloff
		falloff_socket = node_tree.interface.new_socket(name = "Falloff", in_out='INPUT', socket_type = 'NodeSocketFloat')
		falloff_socket.default_value = 1.0
		falloff_socket.min_value = 0.0
		falloff_socket.max_value = 1.0
		falloff_socket.subtype = 'FACTOR'
		falloff_socket.attribute_domain = 'POINT'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Ellipse Mask
		ellipse_mask = node_tree.nodes.new("CompositorNodeEllipseMask")
		ellipse_mask.name = "Mask"
		ellipse_mask.mask_height = 0.550000011920929
		ellipse_mask.mask_type = 'MULTIPLY'
		ellipse_mask.mask_width = 1.0
		ellipse_mask.rotation = 0.0
		ellipse_mask.x = 0.5
		ellipse_mask.y = 0.5
		#Value
		ellipse_mask.inputs[1].default_value = 1.0

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.use_alpha = False
		mix.use_clamp = False

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.aspect_correction = 'NONE'
		blur.factor = 0.0
		blur.factor_x = 0.0
		blur.factor_y = 0.0
		blur.filter_type = 'FAST_GAUSS'
		blur.size_x = 350
		blur.size_y = 350
		blur.use_bokeh = False
		blur.use_extended_bounds = False
		blur.use_gamma_correction = False
		blur.use_relative = False
		blur.use_variable_size = False

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.use_alpha = False
		mix_001.use_clamp = False
		#Image
		mix_001.inputs[1].default_value = (0.0, 0.0, 0.0, 0.0)

		#initialize node_tree links
		#mix.Image -> group_output.Image
		node_tree.links.new(mix.outputs[0], group_output.inputs[0])
		#ellipse_mask.Mask -> blur.Image
		node_tree.links.new(ellipse_mask.outputs[0], blur.inputs[0])
		#group_input.Falloff -> blur.Size
		node_tree.links.new(group_input.outputs[3], blur.inputs[1])
		#blur.Image -> mix.Fac
		node_tree.links.new(blur.outputs[0], mix.inputs[0])
		#group_input.Image -> mix.Image
		node_tree.links.new(group_input.outputs[0], mix.inputs[1])
		#group_input.Color -> mix.Image
		node_tree.links.new(group_input.outputs[1], mix.inputs[2])
		#group_input.Strength -> ellipse_mask.Mask
		node_tree.links.new(group_input.outputs[2], ellipse_mask.inputs[0])
		#blur.Image -> mix_001.Fac
		node_tree.links.new(blur.outputs[0], mix_001.inputs[0])
		#group_input.Color -> mix_001.Image
		node_tree.links.new(group_input.outputs[1], mix_001.inputs[2])
		#mix_001.Image -> group_output.Fill
		node_tree.links.new(mix_001.outputs[0], group_output.inputs[1])
		return node_tree