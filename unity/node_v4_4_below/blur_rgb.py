import bpy
from ..node import *

class CompositorNodeBlurRGB(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeBlurRGB'
	bl_label='Blur RGB'
	bl_icon='PROP_CON'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Distortion"].default_value = 45
		self.inputs["G"].default_value = 0.15
		self.inputs["B"].default_value = 0.25

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
		image_socket.hide_value = True

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket X
		x_socket = node_tree.interface.new_socket(name = "X", in_out='INPUT', socket_type = 'NodeSocketFloat')
		x_socket.default_value = 0.0
		x_socket.min_value = -1.0
		x_socket.max_value = 1.0
		x_socket.subtype = 'FACTOR'
		x_socket.attribute_domain = 'POINT'

		#Socket Y
		y_socket = node_tree.interface.new_socket(name = "Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
		y_socket.default_value = 0.0
		y_socket.min_value = -1.0
		y_socket.max_value = 1.0
		y_socket.subtype = 'FACTOR'
		y_socket.attribute_domain = 'POINT'

		#Socket Distortion
		distortion_socket = node_tree.interface.new_socket(name = "Distortion", in_out='INPUT', socket_type = 'NodeSocketFloat')
		distortion_socket.default_value = 40.0
		distortion_socket.min_value = 0.0
		distortion_socket.max_value = 100.0
		distortion_socket.subtype = 'NONE'
		distortion_socket.attribute_domain = 'POINT'

		#Socket Blur Amount
		blur_amount_socket = node_tree.interface.new_socket(name = "Blur Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_amount_socket.default_value = 0.0
		blur_amount_socket.min_value = 0.0
		blur_amount_socket.max_value = 1.0
		blur_amount_socket.subtype = 'FACTOR'
		blur_amount_socket.attribute_domain = 'POINT'

		#Panel Blur
		blur_panel = node_tree.interface.new_panel("Blur")
		#Socket R
		r_socket = node_tree.interface.new_socket(name = "R", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		r_socket.default_value = 0.0
		r_socket.min_value = 0.0
		r_socket.max_value = 1.0
		r_socket.subtype = 'FACTOR'
		r_socket.attribute_domain = 'POINT'

		#Socket G
		g_socket = node_tree.interface.new_socket(name = "G", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		g_socket.default_value = 0.15000000596046448
		g_socket.min_value = 0.0
		g_socket.max_value = 1.0
		g_socket.subtype = 'FACTOR'
		g_socket.attribute_domain = 'POINT'

		#Socket B
		b_socket = node_tree.interface.new_socket(name = "B", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		b_socket.default_value = 0.25
		b_socket.min_value = 0.0
		b_socket.max_value = 1.0
		b_socket.subtype = 'FACTOR'
		b_socket.attribute_domain = 'POINT'



		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node RGB Curves
		rgb_curves = node_tree.nodes.new("CompositorNodeCurveRGB")
		rgb_curves.name = "RGB Curves"
		#mapping settings
		rgb_curves.mapping.extend = 'EXTRAPOLATED'
		rgb_curves.mapping.tone = 'STANDARD'
		rgb_curves.mapping.black_level = (0.0, 0.0, 0.0)
		rgb_curves.mapping.white_level = (1.0, 1.0, 1.0)
		rgb_curves.mapping.clip_min_x = 0.0
		rgb_curves.mapping.clip_min_y = 0.0
		rgb_curves.mapping.clip_max_x = 1.0
		rgb_curves.mapping.clip_max_y = 1.0
		rgb_curves.mapping.use_clip = True
		#curve 0
		rgb_curves_curve_0 = rgb_curves.mapping.curves[0]
		rgb_curves_curve_0_point_0 = rgb_curves_curve_0.points[0]
		rgb_curves_curve_0_point_0.location = (1.0, 1.0)
		rgb_curves_curve_0_point_0.handle_type = 'AUTO'
		rgb_curves_curve_0_point_1 = rgb_curves_curve_0.points[1]
		rgb_curves_curve_0_point_1.location = (1.0, 1.0)
		rgb_curves_curve_0_point_1.handle_type = 'AUTO'
		#curve 1
		rgb_curves_curve_1 = rgb_curves.mapping.curves[1]
		rgb_curves_curve_1_point_0 = rgb_curves_curve_1.points[0]
		rgb_curves_curve_1_point_0.location = (1.0, 0.0)
		rgb_curves_curve_1_point_0.handle_type = 'AUTO'
		rgb_curves_curve_1_point_1 = rgb_curves_curve_1.points[1]
		rgb_curves_curve_1_point_1.location = (1.0, 1.0)
		rgb_curves_curve_1_point_1.handle_type = 'AUTO'
		#curve 2
		rgb_curves_curve_2 = rgb_curves.mapping.curves[2]
		rgb_curves_curve_2_point_0 = rgb_curves_curve_2.points[0]
		rgb_curves_curve_2_point_0.location = (1.0, 0.0)
		rgb_curves_curve_2_point_0.handle_type = 'AUTO'
		rgb_curves_curve_2_point_1 = rgb_curves_curve_2.points[1]
		rgb_curves_curve_2_point_1.location = (1.0, 1.0)
		rgb_curves_curve_2_point_1.handle_type = 'AUTO'
		#curve 3
		rgb_curves_curve_3 = rgb_curves.mapping.curves[3]
		rgb_curves_curve_3_point_0 = rgb_curves_curve_3.points[0]
		rgb_curves_curve_3_point_0.location = (0.0, 0.0)
		rgb_curves_curve_3_point_0.handle_type = 'AUTO'
		rgb_curves_curve_3_point_1 = rgb_curves_curve_3.points[1]
		rgb_curves_curve_3_point_1.location = (1.0, 1.0)
		rgb_curves_curve_3_point_1.handle_type = 'AUTO'
		#update curve after changes
		rgb_curves.mapping.update()
		#Fac
		rgb_curves.inputs[0].default_value = 1.0
		#Black Level
		rgb_curves.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
		#White Level
		rgb_curves.inputs[3].default_value = (1.0, 1.0, 1.0, 1.0)

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"

		#node RGB Curves.001
		rgb_curves_001 = node_tree.nodes.new("CompositorNodeCurveRGB")
		rgb_curves_001.name = "RGB Curves.001"
		#mapping settings
		rgb_curves_001.mapping.extend = 'EXTRAPOLATED'
		rgb_curves_001.mapping.tone = 'STANDARD'
		rgb_curves_001.mapping.black_level = (0.0, 0.0, 0.0)
		rgb_curves_001.mapping.white_level = (1.0, 1.0, 1.0)
		rgb_curves_001.mapping.clip_min_x = 0.0
		rgb_curves_001.mapping.clip_min_y = 0.0
		rgb_curves_001.mapping.clip_max_x = 1.0
		rgb_curves_001.mapping.clip_max_y = 1.0
		rgb_curves_001.mapping.use_clip = True
		#curve 0
		rgb_curves_001_curve_0 = rgb_curves_001.mapping.curves[0]
		rgb_curves_001_curve_0_point_0 = rgb_curves_001_curve_0.points[0]
		rgb_curves_001_curve_0_point_0.location = (1.0, 0.0)
		rgb_curves_001_curve_0_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_0_point_1 = rgb_curves_001_curve_0.points[1]
		rgb_curves_001_curve_0_point_1.location = (1.0, 1.0)
		rgb_curves_001_curve_0_point_1.handle_type = 'AUTO'
		#curve 1
		rgb_curves_001_curve_1 = rgb_curves_001.mapping.curves[1]
		rgb_curves_001_curve_1_point_0 = rgb_curves_001_curve_1.points[0]
		rgb_curves_001_curve_1_point_0.location = (1.0, 1.0)
		rgb_curves_001_curve_1_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_1_point_1 = rgb_curves_001_curve_1.points[1]
		rgb_curves_001_curve_1_point_1.location = (1.0, 1.0)
		rgb_curves_001_curve_1_point_1.handle_type = 'AUTO'
		#curve 2
		rgb_curves_001_curve_2 = rgb_curves_001.mapping.curves[2]
		rgb_curves_001_curve_2_point_0 = rgb_curves_001_curve_2.points[0]
		rgb_curves_001_curve_2_point_0.location = (1.0, 0.0)
		rgb_curves_001_curve_2_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_2_point_1 = rgb_curves_001_curve_2.points[1]
		rgb_curves_001_curve_2_point_1.location = (1.0, 1.0)
		rgb_curves_001_curve_2_point_1.handle_type = 'AUTO'
		#curve 3
		rgb_curves_001_curve_3 = rgb_curves_001.mapping.curves[3]
		rgb_curves_001_curve_3_point_0 = rgb_curves_001_curve_3.points[0]
		rgb_curves_001_curve_3_point_0.location = (0.0, 0.0)
		rgb_curves_001_curve_3_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_3_point_1 = rgb_curves_001_curve_3.points[1]
		rgb_curves_001_curve_3_point_1.location = (1.0, 1.0)
		rgb_curves_001_curve_3_point_1.handle_type = 'AUTO'
		#update curve after changes
		rgb_curves_001.mapping.update()
		#Fac
		rgb_curves_001.inputs[0].default_value = 1.0
		#Black Level
		rgb_curves_001.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
		#White Level
		rgb_curves_001.inputs[3].default_value = (1.0, 1.0, 1.0, 1.0)

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'LIGHTEN'
		mix.use_alpha = False
		mix.use_clamp = False
		#Fac
		mix.inputs[0].default_value = 1.0

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'LIGHTEN'
		mix_001.use_alpha = False
		mix_001.use_clamp = False
		#Fac
		mix_001.inputs[0].default_value = 1.0

		#node RGB Curves.003
		rgb_curves_003 = node_tree.nodes.new("CompositorNodeCurveRGB")
		rgb_curves_003.name = "RGB Curves.003"
		#mapping settings
		rgb_curves_003.mapping.extend = 'EXTRAPOLATED'
		rgb_curves_003.mapping.tone = 'STANDARD'
		rgb_curves_003.mapping.black_level = (0.0, 0.0, 0.0)
		rgb_curves_003.mapping.white_level = (1.0, 1.0, 1.0)
		rgb_curves_003.mapping.clip_min_x = 0.0
		rgb_curves_003.mapping.clip_min_y = 0.0
		rgb_curves_003.mapping.clip_max_x = 1.0
		rgb_curves_003.mapping.clip_max_y = 1.0
		rgb_curves_003.mapping.use_clip = True
		#curve 0
		rgb_curves_003_curve_0 = rgb_curves_003.mapping.curves[0]
		rgb_curves_003_curve_0_point_0 = rgb_curves_003_curve_0.points[0]
		rgb_curves_003_curve_0_point_0.location = (1.0, 0.0)
		rgb_curves_003_curve_0_point_0.handle_type = 'AUTO'
		rgb_curves_003_curve_0_point_1 = rgb_curves_003_curve_0.points[1]
		rgb_curves_003_curve_0_point_1.location = (1.0, 1.0)
		rgb_curves_003_curve_0_point_1.handle_type = 'AUTO'
		#curve 1
		rgb_curves_003_curve_1 = rgb_curves_003.mapping.curves[1]
		rgb_curves_003_curve_1_point_0 = rgb_curves_003_curve_1.points[0]
		rgb_curves_003_curve_1_point_0.location = (1.0, 0.0)
		rgb_curves_003_curve_1_point_0.handle_type = 'AUTO'
		rgb_curves_003_curve_1_point_1 = rgb_curves_003_curve_1.points[1]
		rgb_curves_003_curve_1_point_1.location = (1.0, 1.0)
		rgb_curves_003_curve_1_point_1.handle_type = 'AUTO'
		#curve 2
		rgb_curves_003_curve_2 = rgb_curves_003.mapping.curves[2]
		rgb_curves_003_curve_2_point_0 = rgb_curves_003_curve_2.points[0]
		rgb_curves_003_curve_2_point_0.location = (1.0, 1.0)
		rgb_curves_003_curve_2_point_0.handle_type = 'AUTO'
		rgb_curves_003_curve_2_point_1 = rgb_curves_003_curve_2.points[1]
		rgb_curves_003_curve_2_point_1.location = (1.0, 1.0)
		rgb_curves_003_curve_2_point_1.handle_type = 'AUTO'
		#curve 3
		rgb_curves_003_curve_3 = rgb_curves_003.mapping.curves[3]
		rgb_curves_003_curve_3_point_0 = rgb_curves_003_curve_3.points[0]
		rgb_curves_003_curve_3_point_0.location = (0.0, 0.0)
		rgb_curves_003_curve_3_point_0.handle_type = 'AUTO'
		rgb_curves_003_curve_3_point_1 = rgb_curves_003_curve_3.points[1]
		rgb_curves_003_curve_3_point_1.location = (1.0, 1.0)
		rgb_curves_003_curve_3_point_1.handle_type = 'AUTO'
		#update curve after changes
		rgb_curves_003.mapping.update()
		#Fac
		rgb_curves_003.inputs[0].default_value = 1.0
		#Black Level
		rgb_curves_003.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
		#White Level
		rgb_curves_003.inputs[3].default_value = (1.0, 1.0, 1.0, 1.0)

		#node Translate
		translate = node_tree.nodes.new("CompositorNodeTranslate")
		translate.name = "Translate"
		if bpy.app.version >= (4, 4, 0):
			translate.interpolation = 'NEAREST'
		else:
			translate.interpolation = 'Nearest'
		translate.use_relative = False
		translate.wrap_axis = 'NONE'

		#node Translate.001
		translate_001 = node_tree.nodes.new("CompositorNodeTranslate")
		translate_001.name = "Translate.001"
		if bpy.app.version >= (4, 4, 0):
			translate_001.interpolation = 'NEAREST'
		else:
			translate_001.interpolation = 'Nearest'
		translate_001.use_relative = False
		translate_001.wrap_axis = 'NONE'

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'ABSOLUTE'
		math.use_clamp = False

		#node Math.001
		math_001 = node_tree.nodes.new("CompositorNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'ABSOLUTE'
		math_001.use_clamp = False

		#node Math.002
		math_002 = node_tree.nodes.new("CompositorNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY'
		math_002.use_clamp = False

		#node Math.003
		math_003 = node_tree.nodes.new("CompositorNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'MULTIPLY'
		math_003.use_clamp = False

		#node Math.004
		math_004 = node_tree.nodes.new("CompositorNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'DIVIDE'
		math_004.use_clamp = False
		#Value_001
		math_004.inputs[1].default_value = 45.0

		#node Math.005
		math_005 = node_tree.nodes.new("CompositorNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'DIVIDE'
		math_005.use_clamp = False
		#Value_001
		math_005.inputs[1].default_value = 45.0

		#node Math.006
		math_006 = node_tree.nodes.new("CompositorNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'MULTIPLY_ADD'
		math_006.use_clamp = False
		#Value_001
		math_006.inputs[1].default_value = 0.10000000149011612
		#Value_002
		math_006.inputs[2].default_value = 1.0

		#node Math.007
		math_007 = node_tree.nodes.new("CompositorNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'MULTIPLY_ADD'
		math_007.use_clamp = False
		#Value_001
		math_007.inputs[1].default_value = 0.10000000149011612
		#Value_002
		math_007.inputs[2].default_value = 1.0

		#node Scale
		scale = node_tree.nodes.new("CompositorNodeScale")
		scale.name = "Scale"
		scale.frame_method = 'STRETCH'
		scale.offset_x = 0.0
		scale.offset_y = 0.0
		scale.space = 'RELATIVE'

		#node Math.008
		math_008 = node_tree.nodes.new("CompositorNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'MULTIPLY'
		math_008.use_clamp = False
		#Value_001
		math_008.inputs[1].default_value = 50.0

		#node Math.009
		math_009 = node_tree.nodes.new("CompositorNodeMath")
		math_009.name = "Math.009"
		math_009.operation = 'MULTIPLY'
		math_009.use_clamp = False
		#Value_001
		math_009.inputs[1].default_value = 50.0

		#node Math.010
		math_010 = node_tree.nodes.new("CompositorNodeMath")
		math_010.name = "Math.010"
		math_010.operation = 'SUBTRACT'
		math_010.use_clamp = False
		#Value
		math_010.inputs[0].default_value = 0.0

		#node Math.011
		math_011 = node_tree.nodes.new("CompositorNodeMath")
		math_011.name = "Math.011"
		math_011.operation = 'SUBTRACT'
		math_011.use_clamp = False
		#Value
		math_011.inputs[0].default_value = 0.0

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.aspect_correction = 'NONE'
		blur.factor = 0.0
		blur.factor_x = 0.0
		blur.factor_y = 0.0
		blur.filter_type = 'GAUSS'
		blur.size_x = 300
		blur.size_y = 300
		blur.use_bokeh = False
		blur.use_extended_bounds = False
		blur.use_gamma_correction = False
		blur.use_relative = False
		blur.use_variable_size = False

		#node Blur.001
		blur_001 = node_tree.nodes.new("CompositorNodeBlur")
		blur_001.name = "Blur.001"
		blur_001.aspect_correction = 'NONE'
		blur_001.factor = 0.0
		blur_001.factor_x = 0.0
		blur_001.factor_y = 0.0
		blur_001.filter_type = 'FAST_GAUSS'
		blur_001.size_x = 300
		blur_001.size_y = 300
		blur_001.use_bokeh = False
		blur_001.use_extended_bounds = False
		blur_001.use_gamma_correction = False
		blur_001.use_relative = False
		blur_001.use_variable_size = False

		#node Blur.002
		blur_002 = node_tree.nodes.new("CompositorNodeBlur")
		blur_002.name = "Blur.002"
		blur_002.aspect_correction = 'NONE'
		blur_002.factor = 0.0
		blur_002.factor_x = 0.0
		blur_002.factor_y = 0.0
		blur_002.filter_type = 'FAST_GAUSS'
		blur_002.size_x = 300
		blur_002.size_y = 300
		blur_002.use_bokeh = False
		blur_002.use_extended_bounds = False
		blur_002.use_gamma_correction = False
		blur_002.use_relative = False
		blur_002.use_variable_size = False

		#node Blur.003
		blur_003 = node_tree.nodes.new("CompositorNodeBlur")
		blur_003.name = "Blur.003"
		blur_003.aspect_correction = 'NONE'
		blur_003.factor = 0.0
		blur_003.factor_x = 0.0
		blur_003.factor_y = 0.0
		blur_003.filter_type = 'FAST_GAUSS'
		blur_003.size_x = 300
		blur_003.size_y = 300
		blur_003.use_bokeh = False
		blur_003.use_extended_bounds = False
		blur_003.use_gamma_correction = False
		blur_003.use_relative = False
		blur_003.use_variable_size = False

		#initialize node_tree links
		#blur_003.Image -> group_output.Image
		node_tree.links.new(blur_003.outputs[0], group_output.inputs[0])
		#translate.Image -> rgb_curves.Image
		node_tree.links.new(translate.outputs[0], rgb_curves.inputs[1])
		#blur.Image -> mix.Image
		node_tree.links.new(blur.outputs[0], mix.inputs[1])
		#blur_001.Image -> mix.Image
		node_tree.links.new(blur_001.outputs[0], mix.inputs[2])
		#mix.Image -> mix_001.Image
		node_tree.links.new(mix.outputs[0], mix_001.inputs[1])
		#blur_002.Image -> mix_001.Image
		node_tree.links.new(blur_002.outputs[0], mix_001.inputs[2])
		#translate_001.Image -> rgb_curves_003.Image
		node_tree.links.new(translate_001.outputs[0], rgb_curves_003.inputs[1])
		#reroute.Output -> rgb_curves_001.Image
		node_tree.links.new(reroute.outputs[0], rgb_curves_001.inputs[1])
		#reroute.Output -> translate_001.Image
		node_tree.links.new(reroute.outputs[0], translate_001.inputs[0])
		#group_input.X -> math.Value
		node_tree.links.new(group_input.outputs[1], math.inputs[0])
		#group_input.Y -> math_001.Value
		node_tree.links.new(group_input.outputs[2], math_001.inputs[0])
		#math.Value -> math_002.Value
		node_tree.links.new(math.outputs[0], math_002.inputs[0])
		#group_input.Distortion -> math_002.Value
		node_tree.links.new(group_input.outputs[3], math_002.inputs[1])
		#group_input.Distortion -> math_003.Value
		node_tree.links.new(group_input.outputs[3], math_003.inputs[1])
		#math_001.Value -> math_003.Value
		node_tree.links.new(math_001.outputs[0], math_003.inputs[0])
		#math_002.Value -> math_004.Value
		node_tree.links.new(math_002.outputs[0], math_004.inputs[0])
		#math_003.Value -> math_005.Value
		node_tree.links.new(math_003.outputs[0], math_005.inputs[0])
		#math_004.Value -> math_006.Value
		node_tree.links.new(math_004.outputs[0], math_006.inputs[0])
		#math_005.Value -> math_007.Value
		node_tree.links.new(math_005.outputs[0], math_007.inputs[0])
		#math_006.Value -> scale.X
		node_tree.links.new(math_006.outputs[0], scale.inputs[1])
		#math_007.Value -> scale.Y
		node_tree.links.new(math_007.outputs[0], scale.inputs[2])
		#group_input.Image -> scale.Image
		node_tree.links.new(group_input.outputs[0], scale.inputs[0])
		#scale.Image -> reroute.Input
		node_tree.links.new(scale.outputs[0], reroute.inputs[0])
		#reroute.Output -> translate.Image
		node_tree.links.new(reroute.outputs[0], translate.inputs[0])
		#group_input.X -> math_008.Value
		node_tree.links.new(group_input.outputs[1], math_008.inputs[0])
		#group_input.Y -> math_009.Value
		node_tree.links.new(group_input.outputs[2], math_009.inputs[0])
		#math_008.Value -> translate.X
		node_tree.links.new(math_008.outputs[0], translate.inputs[1])
		#math_010.Value -> translate_001.X
		node_tree.links.new(math_010.outputs[0], translate_001.inputs[1])
		#math_009.Value -> translate.Y
		node_tree.links.new(math_009.outputs[0], translate.inputs[2])
		#math_011.Value -> translate_001.Y
		node_tree.links.new(math_011.outputs[0], translate_001.inputs[2])
		#math_008.Value -> math_010.Value
		node_tree.links.new(math_008.outputs[0], math_010.inputs[1])
		#math_009.Value -> math_011.Value
		node_tree.links.new(math_009.outputs[0], math_011.inputs[1])
		#rgb_curves.Image -> blur.Image
		node_tree.links.new(rgb_curves.outputs[0], blur.inputs[0])
		#rgb_curves_001.Image -> blur_001.Image
		node_tree.links.new(rgb_curves_001.outputs[0], blur_001.inputs[0])
		#rgb_curves_003.Image -> blur_002.Image
		node_tree.links.new(rgb_curves_003.outputs[0], blur_002.inputs[0])
		#group_input.B -> blur_002.Size
		node_tree.links.new(group_input.outputs[7], blur_002.inputs[1])
		#group_input.G -> blur_001.Size
		node_tree.links.new(group_input.outputs[6], blur_001.inputs[1])
		#group_input.R -> blur.Size
		node_tree.links.new(group_input.outputs[5], blur.inputs[1])
		#mix_001.Image -> blur_003.Image
		node_tree.links.new(mix_001.outputs[0], blur_003.inputs[0])
		#group_input.Blur Amount -> blur_003.Size
		node_tree.links.new(group_input.outputs[4], blur_003.inputs[1])
		return node_tree

