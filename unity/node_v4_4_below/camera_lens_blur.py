import bpy
from ..node import *

class CompositorNodeCameraLensBlur(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeCameraLensBlur'
	bl_label='Camera Lens Blur'
	bl_icon='VIEW_CAMERA'

	def update_flaps(self, context):
		self.node_tree.nodes["Bokeh Image"].flaps = self.flaps

	def update_angle(self, context):
		self.node_tree.nodes["Bokeh Image"].angle = self.angle

	def update_rounding(self, context):
		self.node_tree.nodes["Bokeh Image"].rounding = self.rounding

	def update_catadioptric(self, context):
		self.node_tree.nodes["Bokeh Image"].catadioptric= self.catadioptric

	def update_shift(self, context):
		self.node_tree.nodes["Bokeh Image"].shift = self.shift

	flaps : bpy.props.IntProperty(default = 5, min = 3, max = 24, name = "Flaps", update = update_flaps)
	angle : bpy.props.FloatProperty(default = 0, name = "Angle", update = update_angle, subtype= 'ANGLE')
	rounding : bpy.props.FloatProperty(default = 0, min = 0, max = 1, name = "Rounding", update = update_rounding)
	catadioptric : bpy.props.FloatProperty(default = 0, min = 0, max = 1, name = "Catadioptric", update = update_catadioptric)
	shift : bpy.props.FloatProperty(default = 0, min = -1, max = 1, name = "Lens Shift", update = update_shift)

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Blur"].default_value = 1.0
		self.inputs["Bounding Box"].default_value = 1.0

	def draw_buttons(self, context, layout):
		layout.prop(self, "flaps")
		layout.prop(self, "angle")
		layout.prop(self, "rounding")
		layout.prop(self, "catadioptric")
		layout.prop(self, "shift")

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

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Blur
		blur_socket = node_tree.interface.new_socket(name = "Blur", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_socket.default_value = 1.0
		blur_socket.min_value = 0.0
		blur_socket.max_value = 10.0
		blur_socket.subtype = 'NONE'
		blur_socket.attribute_domain = 'POINT'

		#Socket Bounding box
		bounding_box_socket = node_tree.interface.new_socket(name = "Bounding Box", in_out='INPUT', socket_type = 'NodeSocketFloat')
		bounding_box_socket.default_value = 1.0
		bounding_box_socket.min_value = 0.0
		bounding_box_socket.max_value = 1.0
		bounding_box_socket.subtype = 'NONE'
		bounding_box_socket.attribute_domain = 'POINT'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Bokeh Image
		bokeh_image = node_tree.nodes.new("CompositorNodeBokehImage")
		bokeh_image.name = "Bokeh Image"
		bokeh_image.angle = 0.0
		bokeh_image.catadioptric = 0.0
		bokeh_image.flaps = 5
		bokeh_image.rounding = 0.0
		bokeh_image.shift = 0.0

		#node Bokeh Blur
		bokeh_blur = node_tree.nodes.new("CompositorNodeBokehBlur")
		bokeh_blur.name = "Bokeh Blur"
		bokeh_blur.blur_max = 16.0
		bokeh_blur.use_extended_bounds = True
		bokeh_blur.use_variable_size = False

		#initialize node_tree links
		#bokeh_image.Image -> bokeh_blur.Bokeh
		node_tree.links.new(bokeh_image.outputs[0], bokeh_blur.inputs[1])
		#group_input.Image -> bokeh_blur.Image
		node_tree.links.new(group_input.outputs[0], bokeh_blur.inputs[0])
		#bokeh_blur.Image -> group_output.Image
		node_tree.links.new(bokeh_blur.outputs[0], group_output.inputs[0])
		#group_input.Blur -> bokeh_blur.Size
		node_tree.links.new(group_input.outputs[1], bokeh_blur.inputs[2])
		#group_input.Bounding box -> bokeh_blur.Bounding box
		node_tree.links.new(group_input.outputs[2], bokeh_blur.inputs[3])
		return node_tree
