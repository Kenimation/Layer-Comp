import bpy
from ..node import *

class CompositorNodeShutterStreak(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeShutterStreak'
	bl_label='Shutter Streak'
	bl_icon='CAMERA_STEREO'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Size"].default_value = 1
		self.inputs["Boost"].default_value = 1
		self.inputs["Falloff"].default_value = 1

	def draw_buttons(self, context, layout):
		return

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

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Size
		size_socket = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		size_socket.default_value = 1.0
		size_socket.min_value = 0.0
		size_socket.max_value = 5.0
		size_socket.subtype = 'NONE'
		size_socket.attribute_domain = 'POINT'

		#Socket Boost
		boost_socket = node_tree.interface.new_socket(name = "Boost", in_out='INPUT', socket_type = 'NodeSocketFloat')
		boost_socket.default_value = 1.0
		boost_socket.min_value = 0.0
		boost_socket.max_value = 10.0
		boost_socket.subtype = 'NONE'
		boost_socket.attribute_domain = 'POINT'

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

		#node Glare 
		glare_ = node_tree.nodes.new("CompositorNodeGlare")
		glare_.name = "Glare "
		glare_.glare_type = 'FOG_GLOW'
		glare_.quality = 'MEDIUM'
		#Maximum Highlights
		glare_.inputs[3].default_value = 0.0
		#Strength
		glare_.inputs[4].default_value = 1.0
		#Saturation
		glare_.inputs[5].default_value = 0.0
		#Tint
		glare_.inputs[6].default_value = (1.0, 1.0, 1.0, 1.0)
		#Size
		glare_.inputs[7].default_value = 1.0

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False
		#Value_001
		math.inputs[1].default_value = 0.25

		#node Color Ramp
		color_ramp = node_tree.nodes.new("CompositorNodeValToRGB")
		color_ramp.name = "Color Ramp"
		color_ramp.color_ramp.color_mode = 'RGB'
		color_ramp.color_ramp.hue_interpolation = 'NEAR'
		color_ramp.color_ramp.interpolation = 'B_SPLINE'

		#initialize color ramp elements
		color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
		color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
		color_ramp_cre_0.position = 0.0
		color_ramp_cre_0.alpha = 1.0
		color_ramp_cre_0.color = (1.0, 1.0, 1.0, 1.0)

		color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.4085365831851959)
		color_ramp_cre_1.alpha = 1.0
		color_ramp_cre_1.color = (0.0, 0.0, 0.0, 1.0)

		color_ramp_cre_2 = color_ramp.color_ramp.elements.new(0.7804877161979675)
		color_ramp_cre_2.alpha = 1.0
		color_ramp_cre_2.color = (0.0, 0.0, 0.0, 1.0)


		#node Glare .001
		glare__001 = node_tree.nodes.new("CompositorNodeGlare")
		glare__001.name = "Glare .001"
		glare__001.glare_type = 'STREAKS'
		glare__001.quality = 'LOW'
		#Maximum Highlights
		glare__001.inputs[3].default_value = 0.0
		#Strength
		glare__001.inputs[4].default_value = 1.0
		#Saturation
		glare__001.inputs[5].default_value = 1.0
		#Tint
		glare__001.inputs[6].default_value = (1.0, 1.0, 1.0, 1.0)
		#Streaks
		glare__001.inputs[8].default_value = 2
		#Streaks Angle
		glare__001.inputs[9].default_value = 1.5707963705062866
		#Iterations
		glare__001.inputs[10].default_value = 4
		#Fade
		glare__001.inputs[11].default_value = 1.0
		#Color Modulation
		glare__001.inputs[12].default_value = 0.25

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

		#node Math.001
		math_001 = node_tree.nodes.new("CompositorNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'SUBTRACT'
		math_001.use_clamp = False
		#Value
		math_001.inputs[0].default_value = 1.0

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY'
		math_002.use_clamp = False
		#Value_001
		math_002.inputs[1].default_value = 0.10000000149011612

		#initialize node_tree links
		#math_001.Value -> glare__001.Threshold
		node_tree.links.new(math_001.outputs[0], glare__001.inputs[1])
		#glare__001.Image -> mix.Image
		node_tree.links.new(glare__001.outputs[0], mix.inputs[2])
		#color_ramp.Image -> mix_001.Fac
		node_tree.links.new(color_ramp.outputs[0], mix_001.inputs[0])
		#glare_.Glare -> color_ramp.Fac
		node_tree.links.new(glare_.outputs[1], color_ramp.inputs[0])
		#math_002.Value -> math_001.Value
		node_tree.links.new(math_002.outputs[0], math_001.inputs[1])
		#glare__001.Glare -> mix_001.Image
		node_tree.links.new(glare__001.outputs[1], mix_001.inputs[2])
		#math.Value -> glare_.Threshold
		node_tree.links.new(math.outputs[0], glare_.inputs[1])
		#color_ramp.Image -> mix.Fac
		node_tree.links.new(color_ramp.outputs[0], mix.inputs[0])
		#group_input.Image -> glare_.Image
		node_tree.links.new(group_input.outputs[0], glare_.inputs[0])
		#group_input.Image -> glare__001.Image
		node_tree.links.new(group_input.outputs[0], glare__001.inputs[0])
		#group_input.Image -> mix.Image
		node_tree.links.new(group_input.outputs[0], mix.inputs[1])
		#mix.Image -> group_output.Image
		node_tree.links.new(mix.outputs[0], group_output.inputs[0])
		#group_input.Size -> math.Value
		node_tree.links.new(group_input.outputs[1], math.inputs[0])
		#group_input.Falloff -> glare_.Smoothness
		node_tree.links.new(group_input.outputs[3], glare_.inputs[2])
		#group_input.Boost -> math_002.Value
		node_tree.links.new(group_input.outputs[2], math_002.inputs[0])
		#group_input.Falloff -> glare__001.Smoothness
		node_tree.links.new(group_input.outputs[3], glare__001.inputs[2])
		return node_tree
