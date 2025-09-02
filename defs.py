import bpy
import re
import os

def get_addon_preference(context):
	addon_prefs = context.preferences.addons[__package__].preferences
	return addon_prefs

def offset_node(node_group, offset_node, type, offset):
	for node in node_group.nodes:
		if node.parent == offset_node.parent and node != offset_node:
			if type == 'X':
				if node.location[0] >= offset_node.location[0] - 1:
					node.location[0] = node.location[0] + offset
			elif type == 'Y':
				if node.location[1] >= offset_node.location[1] - 101:
					node.location[1] = node.location[1] + offset				

def create_transform_node_group():
    __transform = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = ".*Transform")

    __transform.color_tag = 'NONE'
    __transform.description = ""
    __transform.default_group_node_width = 140
    

    #__transform interface
    #Socket Image
    image_socket = __transform.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket_1 = __transform.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.hide_value = True

    #Socket X
    x_socket = __transform.interface.new_socket(name = "X", in_out='INPUT', socket_type = 'NodeSocketFloat')
    x_socket.default_value = 0.0
    x_socket.min_value = -10000.0
    x_socket.max_value = 10000.0
    x_socket.subtype = 'NONE'
    x_socket.attribute_domain = 'POINT'

    #Socket Y
    y_socket = __transform.interface.new_socket(name = "Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
    y_socket.default_value = 0.0
    y_socket.min_value = -10000.0
    y_socket.max_value = 10000.0
    y_socket.subtype = 'NONE'
    y_socket.attribute_domain = 'POINT'

    #Socket Rotate
    rotate_socket = __transform.interface.new_socket(name = "Rotate", in_out='INPUT', socket_type = 'NodeSocketFloat')
    rotate_socket.default_value = 0.0
    rotate_socket.min_value = -10000.0
    rotate_socket.max_value = 10000.0
    rotate_socket.subtype = 'ANGLE'
    rotate_socket.attribute_domain = 'POINT'

    #Socket X
    x_socket_1 = __transform.interface.new_socket(name = "X", in_out='INPUT', socket_type = 'NodeSocketFloat')
    x_socket_1.default_value = 1.0
    x_socket_1.min_value = 9.999999747378752e-05
    x_socket_1.max_value = 12000.0
    x_socket_1.subtype = 'NONE'
    x_socket_1.attribute_domain = 'POINT'

    #Socket Y
    y_socket_1 = __transform.interface.new_socket(name = "Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
    y_socket_1.default_value = 1.0
    y_socket_1.min_value = 9.999999747378752e-05
    y_socket_1.max_value = 12000.0
    y_socket_1.subtype = 'NONE'
    y_socket_1.attribute_domain = 'POINT'


    #initialize __transform nodes
    #node Group Output
    group_output = __transform.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    #node Group Input
    group_input = __transform.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Scale
    scale = __transform.nodes.new("CompositorNodeScale")
    scale.name = "Scale"
    scale.frame_method = 'STRETCH'
    scale.space = 'RELATIVE'

    #node Rotate
    rotate = __transform.nodes.new("CompositorNodeRotate")
    rotate.name = "Rotate"
    rotate.filter_type = 'BILINEAR'

    #node Translate
    translate = __transform.nodes.new("CompositorNodeTranslate")
    translate.name = "Translate"
    translate.interpolation = 'NEAREST'
    translate.use_relative = False
    translate.wrap_axis = 'NONE'


    #Set locations
    group_output.location = (350.03118896484375, 0.0)
    group_input.location = (-360.0312194824219, 0.0)
    scale.location = (-160.03121948242188, 0.6955108642578125)
    rotate.location = (-4.1747283935546875, -0.6955108642578125)
    translate.location = (160.03121948242188, -0.6954803466796875)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    scale.width, scale.height = 140.0, 100.0
    rotate.width, rotate.height = 140.0, 100.0
    translate.width, translate.height = 140.0, 100.0

    #initialize __transform links
    #rotate.Image -> translate.Image
    __transform.links.new(rotate.outputs[0], translate.inputs[0])
    #scale.Image -> rotate.Image
    __transform.links.new(scale.outputs[0], rotate.inputs[0])
    #translate.Image -> group_output.Image
    __transform.links.new(translate.outputs[0], group_output.inputs[0])
    #group_input.Image -> scale.Image
    __transform.links.new(group_input.outputs[0], scale.inputs[0])
    #group_input.X -> translate.X
    __transform.links.new(group_input.outputs[1], translate.inputs[1])
    #group_input.Y -> translate.Y
    __transform.links.new(group_input.outputs[2], translate.inputs[2])
    #group_input.Rotate -> rotate.Degr
    __transform.links.new(group_input.outputs[3], rotate.inputs[1])
    #group_input.X -> scale.X
    __transform.links.new(group_input.outputs[4], scale.inputs[1])
    #group_input.Y -> scale.Y
    __transform.links.new(group_input.outputs[5], scale.inputs[2])
    return __transform

def get_scene_compositor(context):
	tree = context.scene.node_tree
	compositor = []
	for node in tree.nodes:
		if node.type == "GROUP" and node.node_tree.compositor_props.name != "":
			compositor.append(node.node_tree.name)
	return compositor

def get_all_icon():
	icon_items = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.items()
	icon_dict = {tup[1].identifier: tup[1].value for tup in icon_items}
	i = 0
	list = []
	for identifier, value in icon_dict.items():
		list.append((identifier, '', '', identifier, i))
		i+1
	return list

def unique_name(base_name, existing_names):
    if base_name not in existing_names:
        return base_name

    match = re.match(r"^(.*?)(\.(\d+))?$", base_name)
    if match:
        base = match.group(1)
        number = int(match.group(3)) if match.group(3) else 1

        while f"{base}.{number:03d}" in existing_names:
            number += 1

        return f"{base}.{number:03d}"
    else:
        return base_name

def append_node(name, preset, nodes):
	filepath = get_filepath()
	blendfile = os.path.join(filepath, f'{preset}.blend')

	if name not in bpy.data.node_groups:
		with bpy.data.libraries.load(blendfile) as (data_from, data_to):
			data_to.node_groups = [name for name in data_from.node_groups if name == name]

	node_group = bpy.data.node_groups[name]
	new_node = nodes.new("CompositorNodeGroup")
	new_node.node_tree = node_group

	return new_node

def get_presets():
	presets = []
	filepath = get_filepath()
	for item in os.listdir(filepath):
		if not item.startswith('.') and item.endswith('.blend') :
			presets.append(item.replace(".blend", ""))
	return presets

def get_effect_presets(preset):
	effects = []
	filepath = get_filepath()
	blendfile  = os.path.join(filepath, f"{preset}.blend")
	with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
		for node_group in data_from.node_groups:
			effects.append(node_group)
	return effects

def get_filepath():
	filepath = os.path.dirname(os.path.abspath(__file__))
	blendfolder = os.path.join(filepath, "Blends")
	return blendfolder

def convert_node_data(node, convert_node):
	if node.type not in ["IMAGE","TEXTURE"]:
		for attr in node.bl_rna.properties.keys():
			if attr not in ['name', 'location', 'location_absolute', 'parent']:
				if hasattr(node, attr) and not node.bl_rna.properties[attr].is_readonly:
					setattr(convert_node, attr, getattr(node, attr))

	if node.type in ["IMAGE", "TEXTURE"]:
		if node.type == "IMAGE":
			convert_node.image = node.image
		elif node.type == "TEXTURE":
			convert_node.texture = node.texture

	for i, inputs in enumerate(node.inputs):
		convert_node.inputs[i].default_value = node.inputs[i].default_value
	for i, outputs in enumerate(node.outputs):
		convert_node.outputs[i].default_value = node.outputs[i].default_value

def get_inputs(node):
	inputs = None
	if node.inputs.get('Image'):
		inputs = node.inputs['Image']
	elif node.inputs.get('Color'):
		inputs = node.inputs['Color']
	elif node.inputs.get('Fac'):
		inputs = node.inputs['Fac']
	elif node.inputs:
		inputs = node.inputs[0]
	return inputs

def get_outputs(node, item):
	if item:
		outputs = node.outputs[item.channel]
	else:
		if node.outputs.get('Image'):
			outputs = node.outputs['Image']
		elif node.outputs.get('Color'):
			outputs = node.outputs['Color']
		elif node.outputs.get('Fac'):
			outputs = node.outputs['Fac']
		else:
			outputs = node.outputs[0]

	return outputs