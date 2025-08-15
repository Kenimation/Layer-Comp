import bpy
from ..node import *

class CompositorNodeRenoiser(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeRenoiser'
	bl_label='Renoiser'
	bl_icon='TEXTURE'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Strength"].default_value = 0.2

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

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 0.20000000298023224
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'

		#Socket Sharpen
		sharpen_socket = node_tree.interface.new_socket(name = "Sharpen", in_out='INPUT', socket_type = 'NodeSocketFloat')
		sharpen_socket.default_value = 0.0
		sharpen_socket.min_value = 0.0
		sharpen_socket.max_value = 1.0
		sharpen_socket.subtype = 'FACTOR'
		sharpen_socket.attribute_domain = 'POINT'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Texture
		texture = node_tree.nodes.new("CompositorNodeTexture")
		new_texture = bpy.data.textures.get("Renoiser")
		if not new_texture:
			new_texture = bpy.data.textures.new(name = "Renoiser", type = 'NOISE')
		texture.texture = new_texture
		texture.node_output = 0
		#Scale
		texture.inputs[1].default_value = (1.0, 1.0, 1.0)

		#node Scene Time
		scene_time = node_tree.nodes.new("CompositorNodeSceneTime")
		scene_time.name = "Scene Time"

		#node Combine XYZ
		combine_xyz = node_tree.nodes.new("CompositorNodeCombineXYZ")
		combine_xyz.name = "Combine XYZ"
		#Y
		combine_xyz.inputs[1].default_value = 0.0
		#Z
		combine_xyz.inputs[2].default_value = 0.0

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'OVERLAY'
		mix.use_alpha = False
		mix.use_clamp = False

		#node Filter
		filter = node_tree.nodes.new("CompositorNodeFilter")
		filter.name = "Filter"
		filter.filter_type = 'SHARPEN'

		#initialize node_tree links
		#combine_xyz.Vector -> texture.Offset
		node_tree.links.new(combine_xyz.outputs[0], texture.inputs[0])
		#scene_time.Frame -> combine_xyz.X
		node_tree.links.new(scene_time.outputs[1], combine_xyz.inputs[0])
		#texture.Value -> mix.Image
		node_tree.links.new(texture.outputs[0], mix.inputs[2])
		#filter.Image -> mix.Image
		node_tree.links.new(filter.outputs[0], mix.inputs[1])
		#group_input.Image -> filter.Image
		node_tree.links.new(group_input.outputs[0], filter.inputs[1])
		#mix.Image -> group_output.Image
		node_tree.links.new(mix.outputs[0], group_output.inputs[0])
		#group_input.Sharpen -> filter.Fac
		node_tree.links.new(group_input.outputs[2], filter.inputs[0])
		#group_input.Strength -> mix.Fac
		node_tree.links.new(group_input.outputs[1], mix.inputs[0])
		return node_tree