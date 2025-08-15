import bpy
from ..node import *

class CompositorNodeChromaticAberration(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeChromaticAberration'
	bl_label='Chromatic Aberration'
	bl_icon='SEQ_CHROMA_SCOPE'

	def init(self, context):
		self.getNodetree(context)

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
		image_socket.hide_value = True

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Red/Cyan
		red_cyan_socket = node_tree.interface.new_socket(name = "Red/Cyan", in_out='INPUT', socket_type = 'NodeSocketFloat')
		red_cyan_socket.default_value = 0.0
		red_cyan_socket.min_value = -10.0
		red_cyan_socket.max_value = 10.0
		red_cyan_socket.subtype = 'NONE'
		red_cyan_socket.attribute_domain = 'POINT'

		#Socket Green/Magenta
		green_magenta_socket = node_tree.interface.new_socket(name = "Green/Magenta", in_out='INPUT', socket_type = 'NodeSocketFloat')
		green_magenta_socket.default_value = 0.0
		green_magenta_socket.min_value = -10.0
		green_magenta_socket.max_value = 10.0
		green_magenta_socket.subtype = 'NONE'
		green_magenta_socket.attribute_domain = 'POINT'

		#Socket Blue/yellow
		blue_yellow_socket = node_tree.interface.new_socket(name = "Blue/yellow", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blue_yellow_socket.default_value = 0.0
		blue_yellow_socket.min_value = -10.0
		blue_yellow_socket.max_value = 10.0
		blue_yellow_socket.subtype = 'NONE'
		blue_yellow_socket.attribute_domain = 'POINT'


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

		#node Map Range
		map_range = node_tree.nodes.new("CompositorNodeMapRange")
		map_range.name = "Map Range"
		map_range.use_clamp = True
		#From Min
		map_range.inputs[1].default_value = 0.0
		#From Max
		map_range.inputs[2].default_value = 10.0
		#To Min
		map_range.inputs[3].default_value = 1.0
		#To Max
		map_range.inputs[4].default_value = 1.100000023841858

		#node Map Range.001
		map_range_001 = node_tree.nodes.new("CompositorNodeMapRange")
		map_range_001.name = "Map Range.001"
		map_range_001.use_clamp = True
		#From Min
		map_range_001.inputs[1].default_value = 0.0
		#From Max
		map_range_001.inputs[2].default_value = 10.0
		#To Min
		map_range_001.inputs[3].default_value = 1.0
		#To Max
		map_range_001.inputs[4].default_value = 1.100000023841858

		#node Map Range.002
		map_range_002 = node_tree.nodes.new("CompositorNodeMapRange")
		map_range_002.name = "Map Range.002"
		map_range_002.use_clamp = True
		#From Min
		map_range_002.inputs[1].default_value = 0.0
		#From Max
		map_range_002.inputs[2].default_value = 10.0
		#To Min
		map_range_002.inputs[3].default_value = 1.0
		#To Max
		map_range_002.inputs[4].default_value = 1.100000023841858

		#node Map Range.003
		map_range_003 = node_tree.nodes.new("CompositorNodeMapRange")
		map_range_003.name = "Map Range.003"
		map_range_003.use_clamp = True
		#From Min
		map_range_003.inputs[1].default_value = 0.0
		#From Max
		map_range_003.inputs[2].default_value = -10.0
		#To Min
		map_range_003.inputs[3].default_value = 1.0
		#To Max
		map_range_003.inputs[4].default_value = 1.100000023841858

		#node Map Range.004
		map_range_004 = node_tree.nodes.new("CompositorNodeMapRange")
		map_range_004.name = "Map Range.004"
		map_range_004.use_clamp = True
		#From Min
		map_range_004.inputs[1].default_value = 0.0
		#From Max
		map_range_004.inputs[2].default_value = -10.0
		#To Min
		map_range_004.inputs[3].default_value = 1.0
		#To Max
		map_range_004.inputs[4].default_value = 1.100000023841858

		#node Map Range.005
		map_range_005 = node_tree.nodes.new("CompositorNodeMapRange")
		map_range_005.name = "Map Range.005"
		map_range_005.use_clamp = True
		#From Min
		map_range_005.inputs[1].default_value = 0.0
		#From Max
		map_range_005.inputs[2].default_value = -10.0
		#To Min
		map_range_005.inputs[3].default_value = 1.0
		#To Max
		map_range_005.inputs[4].default_value = 1.100000023841858

		#node Math.006
		math_006 = node_tree.nodes.new("CompositorNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'MULTIPLY'
		math_006.use_clamp = False

		#node Math.007
		math_007 = node_tree.nodes.new("CompositorNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'MULTIPLY'
		math_007.use_clamp = False

		#node Math.008
		math_008 = node_tree.nodes.new("CompositorNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'MULTIPLY'
		math_008.use_clamp = False

		#node Math.009
		math_009 = node_tree.nodes.new("CompositorNodeMath")
		math_009.name = "Math.009"
		math_009.operation = 'MULTIPLY'
		math_009.use_clamp = False

		#node Math.010
		math_010 = node_tree.nodes.new("CompositorNodeMath")
		math_010.name = "Math.010"
		math_010.operation = 'MULTIPLY'
		math_010.use_clamp = False

		#node Math.011
		math_011 = node_tree.nodes.new("CompositorNodeMath")
		math_011.name = "Math.011"
		math_011.operation = 'MULTIPLY'
		math_011.use_clamp = False

		#node Scale
		scale = node_tree.nodes.new("CompositorNodeScale")
		scale.name = "Scale"
		scale.frame_method = 'STRETCH'
		scale.offset_x = 0.0
		scale.offset_y = 0.0
		scale.space = 'RELATIVE'

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"

		#node Scale.001
		scale_001 = node_tree.nodes.new("CompositorNodeScale")
		scale_001.name = "Scale.001"
		scale_001.frame_method = 'STRETCH'
		scale_001.offset_x = 0.0
		scale_001.offset_y = 0.0
		scale_001.space = 'RELATIVE'

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

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

		#node Scale.002
		scale_002 = node_tree.nodes.new("CompositorNodeScale")
		scale_002.name = "Scale.002"
		scale_002.frame_method = 'STRETCH'
		scale_002.offset_x = 0.0
		scale_002.offset_y = 0.0
		scale_002.space = 'RELATIVE'

		#node Set Alpha
		set_alpha = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha.name = "Set Alpha"
		set_alpha.mode = 'APPLY'
		#Alpha
		set_alpha.inputs[1].default_value = 1.0

		#node Set Alpha.001
		set_alpha_001 = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha_001.name = "Set Alpha.001"
		set_alpha_001.mode = 'APPLY'
		#Alpha
		set_alpha_001.inputs[1].default_value = 1.0

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

		#node Set Alpha.002
		set_alpha_002 = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha_002.name = "Set Alpha.002"
		set_alpha_002.mode = 'APPLY'

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


		#initialize node_tree links
		#mix_001.Image -> group_output.Image
		node_tree.links.new(mix_001.outputs[0], group_output.inputs[0])
		#group_input.Red/Cyan -> map_range.Value
		node_tree.links.new(group_input.outputs[1], map_range.inputs[0])
		#group_input.Green/Magenta -> map_range_001.Value
		node_tree.links.new(group_input.outputs[2], map_range_001.inputs[0])
		#group_input.Blue/yellow -> map_range_002.Value
		node_tree.links.new(group_input.outputs[3], map_range_002.inputs[0])
		#group_input.Red/Cyan -> map_range_003.Value
		node_tree.links.new(group_input.outputs[1], map_range_003.inputs[0])
		#group_input.Green/Magenta -> map_range_004.Value
		node_tree.links.new(group_input.outputs[2], map_range_004.inputs[0])
		#group_input.Blue/yellow -> map_range_005.Value
		node_tree.links.new(group_input.outputs[3], map_range_005.inputs[0])
		#map_range.Value -> math_006.Value
		node_tree.links.new(map_range.outputs[0], math_006.inputs[0])
		#map_range_004.Value -> math_006.Value
		node_tree.links.new(map_range_004.outputs[0], math_006.inputs[1])
		#map_range_001.Value -> math_007.Value
		node_tree.links.new(map_range_001.outputs[0], math_007.inputs[0])
		#map_range_003.Value -> math_007.Value
		node_tree.links.new(map_range_003.outputs[0], math_007.inputs[1])
		#map_range_002.Value -> math_008.Value
		node_tree.links.new(map_range_002.outputs[0], math_008.inputs[0])
		#map_range_003.Value -> math_008.Value
		node_tree.links.new(map_range_003.outputs[0], math_008.inputs[1])
		#math_006.Value -> math_009.Value
		node_tree.links.new(math_006.outputs[0], math_009.inputs[0])
		#map_range_005.Value -> math_009.Value
		node_tree.links.new(map_range_005.outputs[0], math_009.inputs[1])
		#math_007.Value -> math_010.Value
		node_tree.links.new(math_007.outputs[0], math_010.inputs[0])
		#map_range_005.Value -> math_010.Value
		node_tree.links.new(map_range_005.outputs[0], math_010.inputs[1])
		#math_008.Value -> math_011.Value
		node_tree.links.new(math_008.outputs[0], math_011.inputs[0])
		#map_range_004.Value -> math_011.Value
		node_tree.links.new(map_range_004.outputs[0], math_011.inputs[1])
		#reroute.Output -> scale.Image
		node_tree.links.new(reroute.outputs[0], scale.inputs[0])
		#group_input.Image -> reroute.Input
		node_tree.links.new(group_input.outputs[0], reroute.inputs[0])
		#math_009.Value -> scale.X
		node_tree.links.new(math_009.outputs[0], scale.inputs[1])
		#math_009.Value -> scale.Y
		node_tree.links.new(math_009.outputs[0], scale.inputs[2])
		#math_010.Value -> scale_001.X
		node_tree.links.new(math_010.outputs[0], scale_001.inputs[1])
		#math_010.Value -> scale_001.Y
		node_tree.links.new(math_010.outputs[0], scale_001.inputs[2])
		#reroute.Output -> scale_001.Image
		node_tree.links.new(reroute.outputs[0], scale_001.inputs[0])
		#reroute.Output -> separate_color.Image
		node_tree.links.new(reroute.outputs[0], separate_color.inputs[0])
		#scale.Image -> rgb_curves.Image
		node_tree.links.new(scale.outputs[0], rgb_curves.inputs[1])
		#scale_001.Image -> rgb_curves_001.Image
		node_tree.links.new(scale_001.outputs[0], rgb_curves_001.inputs[1])
		#math_011.Value -> scale_002.X
		node_tree.links.new(math_011.outputs[0], scale_002.inputs[1])
		#math_011.Value -> scale_002.Y
		node_tree.links.new(math_011.outputs[0], scale_002.inputs[2])
		#set_alpha.Image -> mix.Image
		node_tree.links.new(set_alpha.outputs[0], mix.inputs[1])
		#set_alpha_001.Image -> mix.Image
		node_tree.links.new(set_alpha_001.outputs[0], mix.inputs[2])
		#mix.Image -> mix_001.Image
		node_tree.links.new(mix.outputs[0], mix_001.inputs[1])
		#separate_color.Alpha -> set_alpha_002.Alpha
		node_tree.links.new(separate_color.outputs[3], set_alpha_002.inputs[1])
		#set_alpha_002.Image -> mix_001.Image
		node_tree.links.new(set_alpha_002.outputs[0], mix_001.inputs[2])
		#scale_002.Image -> rgb_curves_003.Image
		node_tree.links.new(scale_002.outputs[0], rgb_curves_003.inputs[1])
		#rgb_curves_003.Image -> set_alpha_002.Image
		node_tree.links.new(rgb_curves_003.outputs[0], set_alpha_002.inputs[0])
		#reroute.Output -> scale_002.Image
		node_tree.links.new(reroute.outputs[0], scale_002.inputs[0])
		#rgb_curves_001.Image -> set_alpha_001.Image
		node_tree.links.new(rgb_curves_001.outputs[0], set_alpha_001.inputs[0])
		#rgb_curves.Image -> set_alpha.Image
		node_tree.links.new(rgb_curves.outputs[0], set_alpha.inputs[0])
		return node_tree
