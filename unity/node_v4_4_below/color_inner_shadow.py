import bpy
from ..node import *
from ._utils import *

class CompositorNodeColorInnerShadowSingle(bpy.types.CompositorNodeCustomGroup, Node, Key_Node):
	bl_name='CompositorNodeColorInnerShadowSingle'
	bl_label='Color Inner Shadow (Single)'
	bl_icon='ANTIALIASED'
	
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

	def update_count(self, context):
		if self.count >= 2:
			self.node_tree.nodes["Mix.002"].mute = False
		else:
			self.node_tree.nodes["Mix.002"].mute = True

		if self.count >= 3:
			self.node_tree.nodes["Mix.003"].mute = False
		else:
			self.node_tree.nodes["Mix.003"].mute = True

		if self.count >= 4:
			self.node_tree.nodes["Mix.004"].mute = False
		else:
			self.node_tree.nodes["Mix.004"].mute = True

	def update_invert(self, context):
		self.node_tree.nodes["Invert Color"].invert_rgb = self.invert

	mode : bpy.props.EnumProperty(default = 'FEATHER', items = mode_items, name = "Mode", update = update_mode)

	falloff : bpy.props.EnumProperty(default = 'SHARP', items = falloff_items, name = "Falloff", update = update_falloff)

	edge : bpy.props.FloatProperty(default = 0, name = "Edge", update = update_edge, min=-100, max=100)

	distance : bpy.props.IntProperty(default = 35, name = "Size", update = update_distance, min=-100, max=100)

	count : bpy.props.IntProperty(default = 1, name = "Count", update = update_count, min=1, max=4)

	invert : bpy.props.BoolProperty(default = False, name = "Invert", update = update_invert)

	def init(self, context):
		self.getNodetree(context)
		self.count = 1
		self.init_key()
		self.mode = 'FEATHER'
		self.falloff = 'SHARP'
		self.distance = 35
		
		for input in self.inputs:
			if input.name == "Shadow Color":
				input.default_value = (0.92,0,0.059,1)
			elif "Color" in input.name:
				input.default_value = (0, 0.456, 0.9, 1.0)

	def draw_buttons(self, context, layout):
		layout.prop(self, 'mode', text='Mode')
		if self.mode == "FEATHER":
			layout.prop(self, 'falloff', text='Falloff')

		if self.mode == "THRESHOLD":
			layout.prop(self, 'edge')
			
		layout.prop(self, 'distance')

		self.draw_key(layout)
		layout.prop(self, "count")
		layout.prop(self, "invert")

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

		#Socket Bias
		bias_socket = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat')
		bias_socket.default_value = 0.0
		bias_socket.min_value = 0.0
		bias_socket.max_value = 1.0
		bias_socket.subtype = 'FACTOR'
		bias_socket.attribute_domain = 'POINT'

		#Socket Shadow
		shadow_socket = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		shadow_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		shadow_socket.attribute_domain = 'POINT'

		#Panel Key Color
		key_color_panel = node_tree.interface.new_panel("Key Color")
		#Socket Color1
		color1_socket = node_tree.interface.new_socket(name = "Color1", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color1_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color1_socket.attribute_domain = 'POINT'

		#Socket Color2
		color2_socket = node_tree.interface.new_socket(name = "Color2", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color2_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color2_socket.attribute_domain = 'POINT'

		#Socket Color3
		color3_socket = node_tree.interface.new_socket(name = "Color3", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color3_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color3_socket.attribute_domain = 'POINT'

		#Socket Color4
		color4_socket = node_tree.interface.new_socket(name = "Color4", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color4_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color4_socket.attribute_domain = 'POINT'


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
		color_key.color_hue = 0.25
		color_key.color_saturation = 0.25
		color_key.color_value = 0.25

		#node Color Key.001
		color_key_001 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_001.name = "Color Key.001"
		color_key_001.color_hue = 0.25
		color_key_001.color_saturation = 0.25
		color_key_001.color_value = 0.25

		#node Color Key.002
		color_key_002 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_002.name = "Color Key.002"
		color_key_002.color_hue = 0.25
		color_key_002.color_saturation = 0.25
		color_key_002.color_value = 0.25

		#node Color Key.003
		color_key_003 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_003.name = "Color Key.003"
		color_key_003.color_hue = 0.25
		color_key_003.color_saturation = 0.25
		color_key_003.color_value = 0.25

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

		#node Map Range
		map_range = node_tree.nodes.new("CompositorNodeMapRange")
		map_range.name = "Map Range"
		map_range.use_clamp = True
		#From Min
		map_range.inputs[1].default_value = 0.0
		#To Min
		map_range.inputs[3].default_value = 0.0
		#To Max
		map_range.inputs[4].default_value = 1.0

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'SUBTRACT'
		math.use_clamp = True
		#Value
		math.inputs[0].default_value = 1.0010000467300415

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MULTIPLY'
		mix_001.use_alpha = False
		mix_001.use_clamp = False
		#Fac
		mix_001.inputs[0].default_value = 1.0
		#Image
		mix_001.inputs[1].default_value = (1.0, 1.0, 1.0, 1.0)

		#node Mix.002
		mix_002 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MULTIPLY'
		mix_002.use_alpha = False
		mix_002.use_clamp = False
		#Fac
		mix_002.inputs[0].default_value = 1.0

		#node Mix.003
		mix_003 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_003.name = "Mix.003"
		mix_003.blend_type = 'MULTIPLY'
		mix_003.use_alpha = False
		mix_003.use_clamp = False
		#Fac
		mix_003.inputs[0].default_value = 1.0

		#node Mix.004
		mix_004 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'MULTIPLY'
		mix_004.use_alpha = False
		mix_004.use_clamp = False
		#Fac
		mix_004.inputs[0].default_value = 1.0

		#node Invert Color
		invert_color = node_tree.nodes.new("CompositorNodeInvert")
		invert_color.name = "Invert Color"
		invert_color.invert_alpha = False
		invert_color.invert_rgb = False
		#Fac
		invert_color.inputs[0].default_value = 1.0

		#node Dilate/Erode
		dilate_erode = node_tree.nodes.new("CompositorNodeDilateErode")
		dilate_erode.name = "Dilate/Erode"
		dilate_erode.distance = 24
		dilate_erode.edge = 0.0
		dilate_erode.falloff = 'SHARP'
		dilate_erode.mode = 'FEATHER'

		#node Math.001
		math_001 = node_tree.nodes.new("CompositorNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY'
		math_001.use_clamp = True

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'SUBTRACT'
		math_002.use_clamp = True

		#initialize node_tree links
		#mix.Image -> group_output.Image
		node_tree.links.new(mix.outputs[0], group_output.inputs[0])
		#group_input.Image -> color_key.Image
		node_tree.links.new(group_input.outputs[0], color_key.inputs[0])
		#group_input.Color1 -> color_key.Key Color
		node_tree.links.new(group_input.outputs[3], color_key.inputs[1])
		#group_input.Image -> color_key_001.Image
		node_tree.links.new(group_input.outputs[0], color_key_001.inputs[0])
		#group_input.Image -> color_key_002.Image
		node_tree.links.new(group_input.outputs[0], color_key_002.inputs[0])
		#group_input.Image -> color_key_003.Image
		node_tree.links.new(group_input.outputs[0], color_key_003.inputs[0])
		#group_input.Color2 -> color_key_001.Key Color
		node_tree.links.new(group_input.outputs[4], color_key_001.inputs[1])
		#group_input.Color3 -> color_key_002.Key Color
		node_tree.links.new(group_input.outputs[5], color_key_002.inputs[1])
		#group_input.Color4 -> color_key_003.Key Color
		node_tree.links.new(group_input.outputs[6], color_key_003.inputs[1])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#math.Value -> map_range.From Max
		node_tree.links.new(math.outputs[0], map_range.inputs[2])
		#group_input.Bias -> math.Value
		node_tree.links.new(group_input.outputs[1], math.inputs[1])
		#color_key.Matte -> mix_001.Image
		node_tree.links.new(color_key.outputs[1], mix_001.inputs[2])
		#mix_001.Image -> mix_002.Image
		node_tree.links.new(mix_001.outputs[0], mix_002.inputs[1])
		#color_key_001.Matte -> mix_002.Image
		node_tree.links.new(color_key_001.outputs[1], mix_002.inputs[2])
		#mix_002.Image -> mix_003.Image
		node_tree.links.new(mix_002.outputs[0], mix_003.inputs[1])
		#color_key_002.Matte -> mix_003.Image
		node_tree.links.new(color_key_002.outputs[1], mix_003.inputs[2])
		#mix_003.Image -> mix_004.Image
		node_tree.links.new(mix_003.outputs[0], mix_004.inputs[1])
		#color_key_003.Matte -> mix_004.Image
		node_tree.links.new(color_key_003.outputs[1], mix_004.inputs[2])
		#mix_004.Image -> invert_color.Color
		node_tree.links.new(mix_004.outputs[0], invert_color.inputs[1])
		#invert_color.Color -> dilate_erode.Mask
		node_tree.links.new(invert_color.outputs[0], dilate_erode.inputs[0])
		#dilate_erode.Mask -> math_001.Value
		node_tree.links.new(dilate_erode.outputs[0], math_001.inputs[0])
		#separate_color.Alpha -> math_001.Value
		node_tree.links.new(separate_color.outputs[3], math_001.inputs[1])
		#math_001.Value -> math_002.Value
		node_tree.links.new(math_001.outputs[0], math_002.inputs[0])
		#invert_color.Color -> math_002.Value
		node_tree.links.new(invert_color.outputs[0], math_002.inputs[1])
		#math_002.Value -> map_range.Value
		node_tree.links.new(math_002.outputs[0], map_range.inputs[0])
		#map_range.Value -> mix.Fac
		node_tree.links.new(map_range.outputs[0], mix.inputs[0])
		#group_input.Shadow -> mix.Image
		node_tree.links.new(group_input.outputs[2], mix.inputs[2])
		#map_range.Value -> group_output.Matte
		node_tree.links.new(map_range.outputs[0], group_output.inputs[1])
		#group_input.Image -> mix.Image
		node_tree.links.new(group_input.outputs[0], mix.inputs[1])
		return node_tree
			
class CompositorNodeColorInnerShadow(bpy.types.CompositorNodeCustomGroup, Node, Key_Node):
	bl_name='CompositorNodeColorInnerShadow'
	bl_label='Color Inner Shadow'
	bl_icon='ANTIALIASED'
	
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
		for node in self.node_tree.nodes:
			if "Inner Shadow (Single)" in node.name:
				node.mode = self.mode
	
	def update_falloff(self, context):
		for node in self.node_tree.nodes:
			if "Inner Shadow (Single)" in node.name:
				node.falloff = self.falloff

	def update_count(self, context):
		if self.count >= 2:
			self.node_tree.nodes["Mix"].mute = False
			self.node_tree.nodes["Math"].mute = False
		else:
			self.node_tree.nodes["Mix"].mute = True
			self.node_tree.nodes["Math"].mute = True

		if self.count >= 3:
			self.node_tree.nodes["Mix.001"].mute = False
			self.node_tree.nodes["Math.001"].mute = False
		else:
			self.node_tree.nodes["Mix.001"].mute = True
			self.node_tree.nodes["Math.001"].mute = True

		if self.count >= 4:
			self.node_tree.nodes["Mix.002"].mute = False
			self.node_tree.nodes["Math.002"].mute = False
		else:
			self.node_tree.nodes["Mix.002"].mute = True
			self.node_tree.nodes["Math.002"].mute = True

	def update_edge(self, context):
		for node in self.node_tree.nodes:
			if "Inner Shadow (Single)" in node.name:
				node.edge = self.edge

	def update_distance(self, context):
		for node in self.node_tree.nodes:
			if "Inner Shadow (Single)" in node.name:
				node.distance = self.distance

	count : bpy.props.IntProperty(default = 1, name = "Count", update = update_count, min=1, max=4)

	mode : bpy.props.EnumProperty(default = 'FEATHER', items = mode_items, name = "Mode", update = update_mode)

	falloff : bpy.props.EnumProperty(default = 'SHARP', items = falloff_items, name = "Falloff", update = update_falloff)

	edge : bpy.props.FloatProperty(default = 0, name = "Edge", update = update_edge, min=-100, max=100)

	distance : bpy.props.IntProperty(default = 35, name = "Size", update = update_distance, min=-100, max=100)

	def init(self, context):
		self.getNodetree(context)
		self.count = 1
		self.init_key()
		self.mode = 'FEATHER'
		self.falloff = 'SHARP'
		self.distance = 35
		
		for node in self.node_tree.nodes:
			if "Inner Shadow (Single)" in node.name:
				node.count = 4

		for input in self.inputs:
			if input.name == "Shadow Color":
				input.default_value = (0.92,0,0.059,1)
			elif "Color" in input.name:
				input.default_value = (0, 0.456, 0.9, 1.0)

	def draw_buttons(self, context, layout):
		layout.prop(self, 'mode', text='Mode')
		if self.mode == "FEATHER":
			layout.prop(self, 'falloff', text='Falloff')

		if self.mode == "THRESHOLD":
			layout.prop(self, 'edge')

		layout.prop(self, 'distance')

		self.draw_key(layout)
		layout.prop(self, "count")

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		image_socket.attribute_domain = 'POINT'

		#Socket Matte
		matte_socket = node_tree.interface.new_socket(name = "Matte", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte_socket.default_value = 0.0
		matte_socket.min_value = -3.4028234663852886e+38
		matte_socket.max_value = 3.4028234663852886e+38
		matte_socket.subtype = 'NONE'
		matte_socket.attribute_domain = 'POINT'

		#Socket Matte1
		matte1_socket = node_tree.interface.new_socket(name = "Matte1", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte1_socket.default_value = 0.0
		matte1_socket.min_value = -3.4028234663852886e+38
		matte1_socket.max_value = 3.4028234663852886e+38
		matte1_socket.subtype = 'NONE'
		matte1_socket.attribute_domain = 'POINT'

		#Socket Matte2
		matte2_socket = node_tree.interface.new_socket(name = "Matte2", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte2_socket.default_value = 0.0
		matte2_socket.min_value = -3.4028234663852886e+38
		matte2_socket.max_value = 3.4028234663852886e+38
		matte2_socket.subtype = 'NONE'
		matte2_socket.attribute_domain = 'POINT'

		#Socket Matte3
		matte3_socket = node_tree.interface.new_socket(name = "Matte3", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte3_socket.default_value = 0.0
		matte3_socket.min_value = -3.4028234663852886e+38
		matte3_socket.max_value = 3.4028234663852886e+38
		matte3_socket.subtype = 'NONE'
		matte3_socket.attribute_domain = 'POINT'

		#Socket Matte4
		matte4_socket = node_tree.interface.new_socket(name = "Matte4", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte4_socket.default_value = 0.0
		matte4_socket.min_value = -3.4028234663852886e+38
		matte4_socket.max_value = 3.4028234663852886e+38
		matte4_socket.subtype = 'NONE'
		matte4_socket.attribute_domain = 'POINT'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Panel Shadow1
		shadow1_panel = node_tree.interface.new_panel("Shadow1")
		#Socket Bias
		bias_socket = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow1_panel)
		bias_socket.default_value = 0.0
		bias_socket.min_value = 0.0
		bias_socket.max_value = 1.0
		bias_socket.subtype = 'FACTOR'
		bias_socket.attribute_domain = 'POINT'

		#Socket Shadow Color
		shadow_color_socket = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow1_panel)
		shadow_color_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		shadow_color_socket.attribute_domain = 'POINT'

		#Panel Key Color
		key_color_panel = node_tree.interface.new_panel("Key Color")
		#Socket Color1
		color1_socket = node_tree.interface.new_socket(name = "Color1", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color1_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color1_socket.attribute_domain = 'POINT'

		#Socket Color2
		color2_socket = node_tree.interface.new_socket(name = "Color2", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color2_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color2_socket.attribute_domain = 'POINT'

		#Socket Color3
		color3_socket = node_tree.interface.new_socket(name = "Color3", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color3_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color3_socket.attribute_domain = 'POINT'

		#Socket Color4
		color4_socket = node_tree.interface.new_socket(name = "Color4", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel)
		color4_socket.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color4_socket.attribute_domain = 'POINT'


		node_tree.interface.move_to_parent(key_color_panel, shadow1_panel, 10)

		#Panel Shadow2
		shadow2_panel = node_tree.interface.new_panel("Shadow2", default_closed=True)
		#Socket Bias
		bias_socket_1 = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow2_panel)
		bias_socket_1.default_value = 0.0
		bias_socket_1.min_value = 0.0
		bias_socket_1.max_value = 1.0
		bias_socket_1.subtype = 'FACTOR'
		bias_socket_1.attribute_domain = 'POINT'

		#Socket Shadow Color
		shadow_color_socket_1 = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow2_panel)
		shadow_color_socket_1.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		shadow_color_socket_1.attribute_domain = 'POINT'

		#Panel Key Color
		key_color_panel_1 = node_tree.interface.new_panel("Key Color")
		#Socket Color1
		color1_socket_1 = node_tree.interface.new_socket(name = "Color1", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_1)
		color1_socket_1.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color1_socket_1.attribute_domain = 'POINT'

		#Socket Color2
		color2_socket_1 = node_tree.interface.new_socket(name = "Color2", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_1)
		color2_socket_1.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color2_socket_1.attribute_domain = 'POINT'

		#Socket Color3
		color3_socket_1 = node_tree.interface.new_socket(name = "Color3", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_1)
		color3_socket_1.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color3_socket_1.attribute_domain = 'POINT'

		#Socket Color4
		color4_socket_1 = node_tree.interface.new_socket(name = "Color4", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_1)
		color4_socket_1.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color4_socket_1.attribute_domain = 'POINT'


		node_tree.interface.move_to_parent(key_color_panel_1, shadow2_panel, 18)

		#Panel Shadow3
		shadow3_panel = node_tree.interface.new_panel("Shadow3", default_closed=True)
		#Socket Bias
		bias_socket_2 = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow3_panel)
		bias_socket_2.default_value = 0.0
		bias_socket_2.min_value = 0.0
		bias_socket_2.max_value = 1.0
		bias_socket_2.subtype = 'FACTOR'
		bias_socket_2.attribute_domain = 'POINT'

		#Socket Shadow Color
		shadow_color_socket_2 = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow3_panel)
		shadow_color_socket_2.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		shadow_color_socket_2.attribute_domain = 'POINT'

		#Panel Key Color
		key_color_panel_2 = node_tree.interface.new_panel("Key Color")
		#Socket Color1
		color1_socket_2 = node_tree.interface.new_socket(name = "Color1", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_2)
		color1_socket_2.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color1_socket_2.attribute_domain = 'POINT'

		#Socket Color2
		color2_socket_2 = node_tree.interface.new_socket(name = "Color2", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_2)
		color2_socket_2.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color2_socket_2.attribute_domain = 'POINT'

		#Socket Color3
		color3_socket_2 = node_tree.interface.new_socket(name = "Color3", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_2)
		color3_socket_2.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color3_socket_2.attribute_domain = 'POINT'

		#Socket Color4
		color4_socket_2 = node_tree.interface.new_socket(name = "Color4", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_2)
		color4_socket_2.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color4_socket_2.attribute_domain = 'POINT'


		node_tree.interface.move_to_parent(key_color_panel_2, shadow3_panel, 26)

		#Panel Shadow4
		shadow4_panel = node_tree.interface.new_panel("Shadow4", default_closed=True)
		#Socket Bias
		bias_socket_3 = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow4_panel)
		bias_socket_3.default_value = 0.0
		bias_socket_3.min_value = 0.0
		bias_socket_3.max_value = 1.0
		bias_socket_3.subtype = 'FACTOR'
		bias_socket_3.attribute_domain = 'POINT'

		#Socket Shadow Color
		shadow_color_socket_3 = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow4_panel)
		shadow_color_socket_3.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		shadow_color_socket_3.attribute_domain = 'POINT'

		#Panel Key Color
		key_color_panel_3 = node_tree.interface.new_panel("Key Color")
		#Socket Color1
		color1_socket_3 = node_tree.interface.new_socket(name = "Color1", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_3)
		color1_socket_3.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color1_socket_3.attribute_domain = 'POINT'

		#Socket Color2
		color2_socket_3 = node_tree.interface.new_socket(name = "Color2", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_3)
		color2_socket_3.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color2_socket_3.attribute_domain = 'POINT'

		#Socket Color3
		color3_socket_3 = node_tree.interface.new_socket(name = "Color3", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_3)
		color3_socket_3.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color3_socket_3.attribute_domain = 'POINT'

		#Socket Color4
		color4_socket_3 = node_tree.interface.new_socket(name = "Color4", in_out='INPUT', socket_type = 'NodeSocketColor', parent = key_color_panel_3)
		color4_socket_3.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color4_socket_3.attribute_domain = 'POINT'


		node_tree.interface.move_to_parent(key_color_panel_3, shadow4_panel, 34)

		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Inner Shadow (Single)
		inner_shadow__single_ = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single_.name = "Inner Shadow (Single)"

		#node Inner Shadow (Single).001
		inner_shadow__single__001 = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single__001.name = "Inner Shadow (Single).001"

		#node Inner Shadow (Single).002
		inner_shadow__single__002 = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single__002.name = "Inner Shadow (Single).002"

		#node Inner Shadow (Single).003
		inner_shadow__single__003 = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single__003.name = "Inner Shadow (Single).003"

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

		#node Mix.002
		mix_002 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.use_alpha = False
		mix_002.use_clamp = False

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'ADD'
		math.use_clamp = False

		#node Math.001
		math_001 = node_tree.nodes.new("CompositorNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'ADD'
		math_001.use_clamp = False

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'ADD'
		math_002.use_clamp = False

		#initialize node_tree links
		#mix_002.Image -> group_output.Image
		node_tree.links.new(mix_002.outputs[0], group_output.inputs[0])
		#group_input.Image -> inner_shadow__single_.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single_.inputs[0])
		#group_input.Bias -> inner_shadow__single_.Bias
		node_tree.links.new(group_input.outputs[1], inner_shadow__single_.inputs[1])
		#group_input.Shadow Color -> inner_shadow__single_.Shadow
		node_tree.links.new(group_input.outputs[2], inner_shadow__single_.inputs[2])
		#group_input.Color1 -> inner_shadow__single_.Color1
		node_tree.links.new(group_input.outputs[3], inner_shadow__single_.inputs[3])
		#group_input.Color2 -> inner_shadow__single_.Color2
		node_tree.links.new(group_input.outputs[4], inner_shadow__single_.inputs[4])
		#group_input.Color3 -> inner_shadow__single_.Color3
		node_tree.links.new(group_input.outputs[5], inner_shadow__single_.inputs[5])
		#group_input.Color4 -> inner_shadow__single_.Color4
		node_tree.links.new(group_input.outputs[6], inner_shadow__single_.inputs[6])
		#group_input.Bias -> inner_shadow__single__001.Bias
		node_tree.links.new(group_input.outputs[7], inner_shadow__single__001.inputs[1])
		#group_input.Image -> inner_shadow__single__001.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single__001.inputs[0])
		#group_input.Shadow Color -> inner_shadow__single__001.Shadow
		node_tree.links.new(group_input.outputs[8], inner_shadow__single__001.inputs[2])
		#group_input.Color1 -> inner_shadow__single__001.Color1
		node_tree.links.new(group_input.outputs[9], inner_shadow__single__001.inputs[3])
		#group_input.Color2 -> inner_shadow__single__001.Color2
		node_tree.links.new(group_input.outputs[10], inner_shadow__single__001.inputs[4])
		#group_input.Color3 -> inner_shadow__single__001.Color3
		node_tree.links.new(group_input.outputs[11], inner_shadow__single__001.inputs[5])
		#group_input.Color4 -> inner_shadow__single__001.Color4
		node_tree.links.new(group_input.outputs[12], inner_shadow__single__001.inputs[6])
		#group_input.Bias -> inner_shadow__single__002.Bias
		node_tree.links.new(group_input.outputs[13], inner_shadow__single__002.inputs[1])
		#group_input.Image -> inner_shadow__single__002.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single__002.inputs[0])
		#group_input.Shadow Color -> inner_shadow__single__002.Shadow
		node_tree.links.new(group_input.outputs[14], inner_shadow__single__002.inputs[2])
		#group_input.Color1 -> inner_shadow__single__002.Color1
		node_tree.links.new(group_input.outputs[15], inner_shadow__single__002.inputs[3])
		#group_input.Color2 -> inner_shadow__single__002.Color2
		node_tree.links.new(group_input.outputs[16], inner_shadow__single__002.inputs[4])
		#group_input.Color3 -> inner_shadow__single__002.Color3
		node_tree.links.new(group_input.outputs[17], inner_shadow__single__002.inputs[5])
		#group_input.Color4 -> inner_shadow__single__002.Color4
		node_tree.links.new(group_input.outputs[18], inner_shadow__single__002.inputs[6])
		#group_input.Bias -> inner_shadow__single__003.Bias
		node_tree.links.new(group_input.outputs[19], inner_shadow__single__003.inputs[1])
		#group_input.Image -> inner_shadow__single__003.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single__003.inputs[0])
		#group_input.Shadow Color -> inner_shadow__single__003.Shadow
		node_tree.links.new(group_input.outputs[20], inner_shadow__single__003.inputs[2])
		#group_input.Color1 -> inner_shadow__single__003.Color1
		node_tree.links.new(group_input.outputs[21], inner_shadow__single__003.inputs[3])
		#group_input.Color2 -> inner_shadow__single__003.Color2
		node_tree.links.new(group_input.outputs[22], inner_shadow__single__003.inputs[4])
		#group_input.Color3 -> inner_shadow__single__003.Color3
		node_tree.links.new(group_input.outputs[23], inner_shadow__single__003.inputs[5])
		#group_input.Color4 -> inner_shadow__single__003.Color4
		node_tree.links.new(group_input.outputs[24], inner_shadow__single__003.inputs[6])
		#inner_shadow__single_.Image -> mix.Image
		node_tree.links.new(inner_shadow__single_.outputs[0], mix.inputs[1])
		#inner_shadow__single__001.Matte -> mix.Fac
		node_tree.links.new(inner_shadow__single__001.outputs[1], mix.inputs[0])
		#inner_shadow__single__001.Image -> mix.Image
		node_tree.links.new(inner_shadow__single__001.outputs[0], mix.inputs[2])
		#mix.Image -> mix_001.Image
		node_tree.links.new(mix.outputs[0], mix_001.inputs[1])
		#inner_shadow__single__002.Matte -> mix_001.Fac
		node_tree.links.new(inner_shadow__single__002.outputs[1], mix_001.inputs[0])
		#inner_shadow__single__002.Image -> mix_001.Image
		node_tree.links.new(inner_shadow__single__002.outputs[0], mix_001.inputs[2])
		#mix_001.Image -> mix_002.Image
		node_tree.links.new(mix_001.outputs[0], mix_002.inputs[1])
		#inner_shadow__single__003.Matte -> mix_002.Fac
		node_tree.links.new(inner_shadow__single__003.outputs[1], mix_002.inputs[0])
		#inner_shadow__single__003.Image -> mix_002.Image
		node_tree.links.new(inner_shadow__single__003.outputs[0], mix_002.inputs[2])
		#inner_shadow__single_.Matte -> math.Value
		node_tree.links.new(inner_shadow__single_.outputs[1], math.inputs[0])
		#inner_shadow__single__001.Matte -> math.Value
		node_tree.links.new(inner_shadow__single__001.outputs[1], math.inputs[1])
		#math.Value -> math_001.Value
		node_tree.links.new(math.outputs[0], math_001.inputs[0])
		#inner_shadow__single__002.Matte -> math_001.Value
		node_tree.links.new(inner_shadow__single__002.outputs[1], math_001.inputs[1])
		#math_001.Value -> math_002.Value
		node_tree.links.new(math_001.outputs[0], math_002.inputs[0])
		#inner_shadow__single__003.Matte -> math_002.Value
		node_tree.links.new(inner_shadow__single__003.outputs[1], math_002.inputs[1])
		#math_002.Value -> group_output.Matte
		node_tree.links.new(math_002.outputs[0], group_output.inputs[1])
		#inner_shadow__single_.Matte -> group_output.Matte1
		node_tree.links.new(inner_shadow__single_.outputs[1], group_output.inputs[2])
		#inner_shadow__single__001.Matte -> group_output.Matte2
		node_tree.links.new(inner_shadow__single__001.outputs[1], group_output.inputs[3])
		#inner_shadow__single__002.Matte -> group_output.Matte3
		node_tree.links.new(inner_shadow__single__002.outputs[1], group_output.inputs[4])
		#inner_shadow__single__003.Matte -> group_output.Matte4
		node_tree.links.new(inner_shadow__single__003.outputs[1], group_output.inputs[5])
		return node_tree
