import bpy
from ..defs import *
from .node_data import *

class Effect_Props(bpy.types.PropertyGroup):
	def update_name(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		effect_node = node_group.nodes.get(f'{layer.name}.Effect.{self.sub_name}')

		# Update Effect node name
		if effect_node:
			effect_node.name = f'{layer.name}.Effect.{self.name}'
			self.sub_name = self.name

	def update_hide(self, context):
		# Mute Mix node
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		if layer.fx:
			node = node_group.nodes.get(f'{layer.name}.Effect.{self.name}')
			node.mute = self.hide

			if any(effect.solo for effect in layer.effect):
				if self.solo:
					node.mute = self.hide
				else:
					return
			else:
				node.mute = self.hide

	def update_effect_solo(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		if any(effect.solo for effect in layer.effect):
			for effect in layer.effect:
				effect_node = node_group.nodes.get(f'{layer.name}.Effect.{effect.name}')
				effect_node.mute = not effect.solo
		else:
			for effect in layer.effect:
				effect_node = node_group.nodes.get(f'{layer.name}.Effect.{effect.name}')
				effect_node.mute = effect.hide

	def effect_channel(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		
		effect_node = node_group.nodes.get(f'{layer.name}.Effect.{self.name}')

		list = []
		i = 0
		for item in effect_node.outputs:
			if item.enabled:
				if bpy.app.version >= (4, 5, 0):
					list.append((item.name, item.name, '', socket_data[item.type], i))
				elif bpy.app.version < (4, 5, 0):
					list.append((item.name, item.name, ''))
				i += 1
		return list
	
	def update_effect_channel(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		effect_node = node_group.nodes.get(f'{layer.name}.Effect.{self.name}')

		for link in node_group.links:
			if link.from_node == effect_node:
				output_socket = link.to_socket
				break

		node_group.links.new(effect_node.outputs[self.channel], output_socket)

	name : bpy.props.StringProperty(name='Effect Name', update=update_name)
	sub_name : bpy.props.StringProperty()
	type : bpy.props.StringProperty()
	sub_type : bpy.props.StringProperty()
	icon : bpy.props.StringProperty()
	hide : bpy.props.BoolProperty(name='Hide Effect', update=update_hide)
	solo : bpy.props.BoolProperty(name='Solo Effect', update = update_effect_solo)
	channel : bpy.props.EnumProperty(
							items = effect_channel,
							update = update_effect_channel
									)

	drag : bpy.props.BoolProperty()

class Add_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_add_effect"
	bl_label = "Add Compositor Layer Effect"
	bl_description = "Add Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	type : bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		return layer

	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		# Define nodes
		node_group = bpy.data.node_groups[compositor.name]
		transform_node = node_group.nodes.get(f"{layer.name}.Transform")
		frame = node_group.nodes.get(f"{layer.name}.Frame")

		# Create effect node
		if self.type in effect_node_data:
			node_data = effect_node_data
		elif self.type in feature_node_data:
			node_data = feature_node_data

		effect_node = node_group.nodes.new(node_data[self.type][1])
		effect_node.name = f'{layer.name}.Effect.{node_data[self.type][0]}'
		effect_node.parent = frame
		effect_node.location = (transform_node.location[0], transform_node.location[1] - 100)
		
		# Offset nodes
		offset_node(node_group, effect_node, 'X', 200)

		# Connect effect node
		for link in node_group.links:
			if link.to_socket == transform_node.inputs[0]:
				input_socket = link.from_socket
				break

		inputs = get_inputs(effect_node)

		node_group.links.new(input_socket, inputs)
		node_group.links.new(effect_node.outputs[0], transform_node.inputs[0])

		# Set propterties
		item = layer.effect.add()
		item.name = effect_node.name.replace(f'{layer.name}.Effect.', '')
		item.sub_name = effect_node.name.replace(f'{layer.name}.Effect.', '')
		if self.type in feature_node_data:
			item.type = self.type
		else:
			item.type = effect_node.type
		item.icon = node_data[self.type][2]
		item.channel = get_outputs(effect_node, item).name

		return {"FINISHED"}
	
class Append_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_append_effect"
	bl_label = "Append Compositor Layer Effect"
	bl_description = "Append Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})
	type : bpy.props.StringProperty(options={'HIDDEN'})
	icon : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		# Define nodes
		node_group = bpy.data.node_groups[compositor.name]
		transform_node = node_group.nodes.get(f"{layer.name}.Transform")
		frame = node_group.nodes.get(f"{layer.name}.Frame")

		# Create effect node
		effect_node = append_node(self.name, f'{self.type}', node_group.nodes)
		effect_node.name = f'{layer.name}.Effect.{self.name}'
		effect_node.parent = frame
		effect_node.location = transform_node.location
		
		# Offset nodes
		offset_node(node_group, effect_node, 'X', 200)

		# Connect effect node
		for link in node_group.links:
			if link.to_socket == transform_node.inputs[0]:
				input_socket = link.from_socket
				break

		inputs = get_inputs(effect_node)

		node_group.links.new(input_socket, inputs)
		node_group.links.new(effect_node.outputs[0], transform_node.inputs[0])

		# Set propterties
		item = layer.effect.add()
		item.name = effect_node.name.replace(f'{layer.name}.Effect.', '')
		item.sub_name = effect_node.name.replace(f'{layer.name}.Effect.', '')
		item.type = self.type
		item.sub_type = self.name
		item.icon = self.icon
		item.channel = get_outputs(effect_node, item).name

		return {"FINISHED"}

class Append_OT_Effect_Preset(bpy.types.Operator):
	bl_idname = "scene.comp_append_effect_preset"
	bl_label = "Append Compositor Layer Effect Preset"
	bl_description = "Append Compositor Layer Effect Preset"
	bl_options = {'REGISTER', 'UNDO'}

	preset : bpy.props.StringProperty(options={'HIDDEN'})

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_popup(self, event)

	def draw(self, context):
		layout = self.layout
		for effect in get_effect_presets(self.preset):
			add = layout.operator("scene.comp_append_effect",text=effect, emboss = False)
			add.name = effect
			add.type = self.preset
			add.icon = "PRESET"

	def execute(self, context):
		return {"FINISHED"}

class Remove_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_remove_effect"
	bl_label = "Remove Compositor Layer Effect"
	bl_description = "Remove Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		effect = layer.effect[self.index]

		# Define nodes
		effect_node = node_group.nodes.get(f'{layer.name}.Effect.{effect.name}')

		# Offset nodes
		offset_node(node_group, effect_node, 'X', -200)

		# Connect effect node
		inputs = get_inputs(effect_node)

		for link in node_group.links:
			if link.to_socket == inputs:
				input_socket = link.from_socket
				break
		for link in node_group.links:
			if link.from_socket == effect_node.outputs[effect.channel]:
				output_socket = link.to_socket
				break

		node_group.links.new(input_socket, output_socket)

		# Remove nodes
		node_group.nodes.remove(effect_node)

		# Remove propterties
		layer.effect.remove(self.index)
	
		return {"FINISHED"}

class Clear_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_clear_effect"
	bl_label = "Clear Compositor Layer Effect"
	bl_description = "Clear Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		return len(layer.effect) > 0
	
	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		for i in range(len(layer.effect)):
			bpy.ops.scene.comp_remove_effect(index=0)

		return {"FINISHED"}

class Duplicate_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_duplicate_effect"
	bl_label = "Duplicate Compositor Layer Effect"
	bl_description = "Duplicate Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		addon_prefs = get_addon_preference(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		effect = layer.effect[self.index]

		# Define nodes
		effect_node = node_group.nodes.get(f'{layer.name}.Effect.{effect.name}')

		if effect_node.type != 'GROUP':
			bpy.ops.scene.comp_add_effect(type=effect.type)
		else:
			bpy.ops.scene.comp_append_effect(name=effect.sub_type , type=effect.type, icon=effect.icon)

		new_effect = layer.effect[len(layer.effect)-1]
		new_effect_node = node_group.nodes.get(f'{layer.name}.Effect.{new_effect.name}')

		convert_node_data(effect_node, new_effect_node)

		# Check existing name
		existing_names = [item.name for item in layer.effect]
		source_name = unique_name(effect.name, existing_names)
		new_effect.name = source_name
		new_effect.channel = effect.channel

		if addon_prefs.duplicate_effect_option == "Next":
			for i in range(len(layer.effect) - 1, -1, -1):
				if i > self.index + 1:
					bpy.ops.scene.comp_move_effect(index=i, direction='UP')

		return {"FINISHED"}
	
class Move_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_move_effect"
	bl_label = "Move Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})
	direction : bpy.props.StringProperty(options={'HIDDEN'})

	def swap_node(self, node, swap_node, effect, swap_effect):
		location = node.location.copy()
		swap_location = swap_node.location.copy()

		node.location = swap_location
		swap_node.location = location
		
		inputs = get_inputs(node)
		swap_inputs = get_inputs(swap_node)

		outputs = get_outputs(node, effect)
		swap_outputs = get_outputs(swap_node, swap_effect)

		return inputs, swap_inputs, outputs, swap_outputs

	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		effect = layer.effect[self.index]
		
		effect_node = node_group.nodes.get(f'{layer.name}.Effect.{effect.name}')

		if self.direction == 'DOWN' and self.index < len(layer.effect) - 1:

			# Define nodes
			next_effect = layer.effect[self.index+1]
			next_effect_node = node_group.nodes.get(f'{layer.name}.Effect.{next_effect.name}')

			inputs, swap_inputs, outputs, swap_outputs = self.swap_node(effect_node, next_effect_node, effect, next_effect)

			for link in node_group.links:
				if link.to_socket == inputs:
					input_socket = link.from_socket
					break

			for link in node_group.links:
				if link.from_socket == swap_outputs:
					output_socket = link.to_socket
					break

			node_group.links.new(input_socket, swap_inputs)

			node_group.links.new(outputs, output_socket)

			node_group.links.new(swap_outputs, inputs)

			layer.effect.move(self.index, self.index + 1)

			layer.effect_index = self.index + 1
			
		elif self.direction == 'UP' and self.index > 0:

			# Define nodes
			last_effect = layer.effect[self.index-1]
			last_effect_node = node_group.nodes.get(f'{layer.name}.Effect.{last_effect.name}')

			inputs, swap_inputs, outputs, swap_outputs = self.swap_node(effect_node, last_effect_node, effect, last_effect)

			for link in node_group.links:
				if link.to_socket == swap_inputs:
					input_socket = link.from_socket
					break

			for link in node_group.links:
				if link.from_socket == outputs:
					output_socket = link.to_socket
					break

			node_group.links.new(input_socket, inputs)

			node_group.links.new(swap_outputs, output_socket)

			node_group.links.new(outputs, swap_inputs)

			layer.effect.move(self.index, self.index - 1)

			layer.effect_index = self.index - 1

		return {"FINISHED"}

class Drag_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_drag_effect"
	bl_label = "Drag Compositor Layer Effect"
	bl_description = "Drag Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	index: bpy.props.IntProperty(options={'HIDDEN'})
	step_counter: int = 0

	mouse_region_x = None
	mouse_region_y = None

	def modal(self, context, event):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		if event.type == 'MOUSEMOVE':
			# Increment the step counter
			self.step_counter += 1

			# Check if the step counter reaches the specified interval
			if self.step_counter >= 5:
				if event.mouse_region_y < self.mouse_region_y:
					if self.index < len(layer.effect) - 1:
						bpy.ops.scene.comp_move_effect(index=self.index, direction='DOWN')
						self.index += 1
				elif event.mouse_region_y > self.mouse_region_y:
					if self.index > 0:
						bpy.ops.scene.comp_move_effect(index=self.index, direction='UP')
						self.index -= 1

				context.area.tag_redraw()
				self.mouse_region_y = event.mouse_region_y

				# Reset the step counter after triggering the operator
				self.step_counter = 0

		if event.type in ('LEFTMOUSE', 'RIGHTMOUSE'):
			layer.effect[self.index].drag = False
			return {'FINISHED'}
		
		return {'RUNNING_MODAL'}
		
	def invoke(self, context, event):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		layer.effect[self.index].drag = True
		self.mouse_region_x = event.mouse_region_x
		self.mouse_region_y = event.mouse_region_y
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class Copy_OT_Effect(bpy.types.Operator):
	bl_idname = "scene.comp_copy_effect"
	bl_label = "Copy Compositor Layer Effect"
	bl_description = "Copy Compositor Layer Effect"
	bl_options = {'REGISTER', 'UNDO'}

	def compositor_item(self, context):
		tree = context.scene.node_tree
		list = []
		for i, name in enumerate(get_scene_compositor(context)):
			node_group = tree.nodes[name].node_tree
			compositor = node_group.compositor_props
			if compositor.layer:
				list.append((name, name, ''))
		return list
	
	def layer_item(self, context):
		tree = context.scene.node_tree
		node_group = tree.nodes[self.compositor].node_tree
		compositor = node_group.compositor_props
		list = []
		for i, item in enumerate(compositor.layer):
			if item.effect:
				list.append((str(i), item.name, '', item.icon, i))
		return list
	
	def effect_item(self, context):
		tree = context.scene.node_tree
		node_group = tree.nodes[self.compositor].node_tree
		compositor = node_group.compositor_props
		list = []
		layer = compositor.layer[int(self.layer)]
		if bpy.app.version >= (4, 4, 0):
			list.append(('All', 'All', '', 'STRIP_COLOR_01', 0))
		else:
			list.append(('All', 'All', '', 'SEQUENCE_COLOR_01', 0))
		for i, item in enumerate(layer.effect):
			list.append((str(i+1), item.name, '', item.icon, i+1))
		return list
	
	compositor : bpy.props.EnumProperty(
						name = "Compositor",
						items = compositor_item,
								)
	
	layer : bpy.props.EnumProperty(
						name = "Layer",
						items = layer_item,
								)
	
	effect : bpy.props.EnumProperty(
						name = "Effect",
						items = effect_item,
								)
	
	@classmethod
	def poll(cls, context):
		tree = context.scene.node_tree
		for name in get_scene_compositor(context):
			node_group = tree.nodes[name].node_tree
			comp = node_group.compositor_props
			for layer in comp.layer:
				if len(layer.effect) > 0:
					return True
		return False

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def execute(self, context):
		if not (self.layer and self.effect and self.compositor):
			self.report({"INFO"}, "No effect item")
			return {"FINISHED"}
		
		tree = context.scene.node_tree
		props = context.scene.compositor_layer_props

		node_group = tree.nodes[props.compositor_panel].node_tree
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		copy_node_group = tree.nodes[self.compositor].node_tree
		copy_compositor = copy_node_group.compositor_props
		copy_layer = copy_compositor.layer[int(self.layer)]

		if self.effect != 'All':
			copy_effect = copy_layer.effect[int(self.effect)-1]
			copy_effect_node = copy_node_group.nodes.get(f'{copy_layer.name}.Effect.{copy_effect.name}')

			if copy_effect_node.type != 'GROUP':
				bpy.ops.scene.comp_add_effect(type=copy_effect.type)
			else:
				bpy.ops.scene.comp_append_effect(name=copy_effect.sub_type , type=copy_effect.type, icon=copy_effect.icon)

			effect = layer.effect[-1]
			node_group = bpy.data.node_groups[compositor.name]
			new_effect_node = node_group.nodes.get(f'{layer.name}.Effect.{effect.name}')

			convert_node_data(copy_effect_node, new_effect_node)

			if len(copy_effect_node.outputs) > 1:
				effect.channel = copy_effect.channel

		else:

			for copy_effect in copy_layer.effect:
				if not copy_effect.sub_type:
					bpy.ops.scene.comp_add_effect(type=copy_effect.type)
				else:
					bpy.ops.scene.comp_append_effect(name=copy_effect.sub_type , type=copy_effect.type, icon=copy_effect.icon)

				copy_node_group = bpy.data.node_groups[copy_compositor.name]
				copy_effect_node = copy_node_group.nodes.get(f'{copy_layer.name}.Effect.{copy_effect.name}')

				effect = layer.effect[-1]
				node_group = bpy.data.node_groups[compositor.name]
				new_effect_node = node_group.nodes.get(f'{layer.name}.Effect.{effect.name}')

				convert_node_data(copy_effect_node, new_effect_node)

				if len(copy_effect_node.outputs) > 1:
					effect.channel = copy_effect.channel

		return {"FINISHED"}
	
class CompositorAddMenu:

	@classmethod
	def operator_add_effect(cls, layout, node_data, name):
		data = node_data[name]
		layout.operator(
			"scene.comp_add_effect",
			text=data[0],
			text_ctxt=data[0],
			icon=data[2],
		).type = name

class COMPOSITOR_MT_add_effects(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Effect"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		version = bpy.app.version

		layout = self.layout
		if layout.operator_context == 'EXEC_REGION_WIN':
			layout.operator_context = 'INVOKE_REGION_WIN'
			layout.operator("WM_OT_search_single_menu", text="Search...",
							icon='VIEWZOOM').menu_idname = "COMPOSITOR_MT_add_effects"
			layout.separator()

		layout.operator_context = 'EXEC_REGION_WIN'
		layout.menu("COMPOSITOR_MT_add_effects_adjustment")
		layout.menu("COMPOSITOR_MT_add_effects_filter")
		layout.menu("COMPOSITOR_MT_add_effects_blur")
		layout.menu("COMPOSITOR_MT_add_effects_keying")
		layout.menu("COMPOSITOR_MT_add_effects_transform")
		layout.separator()
		layout.label(text="Feature", icon="SHADERFX")
		layout.menu("COMPOSITOR_MT_add_effects_features_color")
		layout.menu("COMPOSITOR_MT_add_effects_features_looks")
		if version >= (4, 5, 0):
			layout.menu("COMPOSITOR_MT_add_effects_features_other")
		layout.separator()
		layout.menu("COMPOSITOR_MT_add_effects_presets", icon="PRESET")

class COMPOSITOR_MT_add_effects_adjustment(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Adjustment"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, effect_node_data, "BRIGHTCONTRAST")
		self.operator_add_effect(layout, effect_node_data, "VALTORGB")
		self.operator_add_effect(layout, effect_node_data, "COLORBALANCE")
		self.operator_add_effect(layout, effect_node_data, "COLORCORRECTION")
		self.operator_add_effect(layout, effect_node_data, "EXPOSURE")
		self.operator_add_effect(layout, effect_node_data, "GAMMA")
		self.operator_add_effect(layout, effect_node_data, "HUECORRECT")
		self.operator_add_effect(layout, effect_node_data, "HUE_SAT")
		self.operator_add_effect(layout, effect_node_data, "CURVE_RGB")
		self.operator_add_effect(layout, effect_node_data, "TONEMAP")
		self.operator_add_effect(layout, effect_node_data, "INVERT")
		self.operator_add_effect(layout, effect_node_data, "CONVERT_COLORSPACE")
		self.operator_add_effect(layout, effect_node_data, "SEPARATE_COLOR")

class COMPOSITOR_MT_add_effects_filter(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Filter"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout

		self.operator_add_effect(layout, effect_node_data, "ANTIALIASING")
		self.operator_add_effect(layout, effect_node_data, "INPAINT")
		self.operator_add_effect(layout, effect_node_data, "FILTER")
		self.operator_add_effect(layout, effect_node_data, "GLARE")
		self.operator_add_effect(layout, effect_node_data, "KUWAHARA")
		self.operator_add_effect(layout, effect_node_data, "PIXELATE")
		self.operator_add_effect(layout, effect_node_data, "POSTERIZE")
		self.operator_add_effect(layout, effect_node_data, "SUNBEAMS")
		self.operator_add_effect(layout, effect_node_data, "LENSDIST")

class COMPOSITOR_MT_add_effects_blur(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Blur"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, effect_node_data, "BILATERALBLUR")
		self.operator_add_effect(layout, effect_node_data, "BLUR")
		self.operator_add_effect(layout, effect_node_data, "BOKEHBLUR")
		self.operator_add_effect(layout, effect_node_data, "DEFOCUS")
		self.operator_add_effect(layout, effect_node_data, "DBLUR")

class COMPOSITOR_MT_add_effects_keying(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Keying"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, effect_node_data, "CRYPTOMATTE")
		layout.separator()
		self.operator_add_effect(layout, effect_node_data, "CHANNEL_MATTE")
		self.operator_add_effect(layout, effect_node_data, "CHROMA_MATTE")
		self.operator_add_effect(layout, effect_node_data, "COLOR_MATTE")
		self.operator_add_effect(layout, effect_node_data, "COLOR_SPILL")
		self.operator_add_effect(layout, effect_node_data, "DISTANCE_MATTE")
		self.operator_add_effect(layout, effect_node_data, "KEYING")
		self.operator_add_effect(layout, effect_node_data, "LUMA_MATTE")

class COMPOSITOR_MT_add_effects_transform(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Transform"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, effect_node_data, "TRANSFORM")
		self.operator_add_effect(layout, effect_node_data, "TRANSLATE")
		self.operator_add_effect(layout, effect_node_data, "ROTATE")
		self.operator_add_effect(layout, effect_node_data, "SCALE")

		self.operator_add_effect(layout, effect_node_data, "CORNERPIN")
		self.operator_add_effect(layout, effect_node_data, "CROP")
		self.operator_add_effect(layout, effect_node_data, "FLIP")

class COMPOSITOR_MT_add_effects_features(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Features"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		version = bpy.app.version
		layout = self.layout
		layout.menu("COMPOSITOR_MT_add_effects_features_color")
		layout.menu("COMPOSITOR_MT_add_effects_features_looks")
		if version >= (4, 5, 0):
			layout.menu("COMPOSITOR_MT_add_effects_features_other")

class COMPOSITOR_MT_add_effects_features_color(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Color"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeFill")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeSpotFill")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeColorSelection")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeReplaceColor")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeInnerShadow")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeInnerShadowSingle")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeBoundaryLine")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeSeparateRGBA")

class COMPOSITOR_MT_add_effects_features_looks(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Looks"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		version = bpy.app.version
		layout = self.layout
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeSpotExposure")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeCameraLensBlur")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeChromaticAberration")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeVignette")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeEdgeSoftness")
		if version >= (4, 5, 0):
			self.operator_add_effect(layout, feature_node_data, "CompositorNodeSwingTilt")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeShutterStreak")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeBlurRGB")
		if version >= (4, 5, 0):
			self.operator_add_effect(layout, feature_node_data, "CompositorNodeTwitch")
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeRenoiser")

class COMPOSITOR_MT_add_effects_features_other(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Other"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, feature_node_data, "CompositorNodeWiggleTransfrom")

class COMPOSITOR_MT_add_effects_presets(bpy.types.Menu):
	bl_label = "Presets"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		presets = get_presets()
		layout = self.layout
		if len(presets) > 0:
			for preset in presets:
				layout.operator("scene.comp_append_effect_preset",text=preset).preset = preset
		else:
			layout.label(text="No Preset")

class COMPOSITOR_MT_effects_specials(bpy.types.Menu):
	bl_label = "Effect Specials"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		layout.operator("wm.call_menu", text="Add Effect", icon='ADD').name = "COMPOSITOR_MT_add_effects"
		layout.separator()
		layout.operator("scene.comp_copy_effect", text="Copy effect from layer", icon = 'PASTEDOWN', emboss = False)
		layout.separator()
		layout.operator("scene.comp_clear_effect", text="Clear Effects", icon='TRASH', emboss = False)

class NODE_MT_add_feature_node(bpy.types.Menu):
	bl_idname = 'NODE_MT_add_feature_node'
	bl_label = 'Feature'

	def draw(self, context):
		layout = self.layout
		for name in feature_node_data:
			if bpy.app.version < (4, 5, 0) and name in feature_node_data_4_5:
				continue
			data = feature_node_data[name]
			layout.operator('node.add_node', text=data[0], icon = data[2]).type = data[1]

def draw_effect(self, context, box):
	tree = context.scene.node_tree
	props = context.scene.compositor_layer_props
	node_group = tree.nodes[props.compositor_panel].node_tree
	compositor = node_group.compositor_props
	layer = compositor.layer[compositor.layer_index]

	filtered = None
	if compositor.search:
		filtered = list(filter(lambda x: any(y in x for y in [compositor.search.lower()]), [effect.name.lower() for effect in layer.effect]))

	for i, effect in enumerate(layer.effect):

		if compositor.search and filtered != []:
			if effect.name.lower() not in filtered:
				continue

		node = node_group.nodes[f'{layer.name}.Effect.{effect.name}']

		header, panel = box.panel(idname=f'{layer.name}.Effect.{effect.name}', default_closed=False)
		row = header.row(align=True)
		row.label(text="", icon = effect.icon)
		row.prop(effect, "hide", text = "", icon = "HIDE_ON" if effect.hide == True else "HIDE_OFF", invert_checkbox=True)
		row.prop(effect, "solo", text = "", icon = "LAYER_ACTIVE" if effect.solo == True else "LAYER_USED")
		row.prop(effect, "name", text = "")
		rest = row.operator("scene.comp_rest_node", text="", icon='FILE_REFRESH')
		rest.node_group = node_group.name
		rest.node = node.name
		row.operator("scene.comp_duplicate_effect", text="", icon='DUPLICATE').index = i
		row.operator("scene.comp_remove_effect", text="", icon='X').index = i
		move = header.operator("scene.comp_drag_effect", text="", icon='LAYER_ACTIVE' if effect.drag else 'COLLAPSEMENU', emboss = False)
		move.index = i
		if panel:
			panel.use_property_split = True
			panel.use_property_decorate = False
			panel_box = panel.box()
			panel_box.template_node_inputs(node)
			if len(node.outputs) > 1:
				sub = panel_box.row()
				sub.active = not node.mute
				sub.prop(effect, "channel", text="Channel")

def feature_node_menu(self, context):
	if context.space_data.tree_type == "CompositorNodeTree":
		self.layout.separator()
		self.layout.menu('NODE_MT_add_feature_node', icon = 'SHADERFX')
		self.layout.menu("COMPOSITOR_MT_add_effects_presets", icon="PRESET")

classes = (
	Effect_Props,
	Add_OT_Effect,
	Append_OT_Effect,
	Append_OT_Effect_Preset,
	Remove_OT_Effect,
	Clear_OT_Effect,
	Duplicate_OT_Effect,
	Move_OT_Effect,
	Drag_OT_Effect,
	Copy_OT_Effect,
	COMPOSITOR_MT_add_effects,
	COMPOSITOR_MT_add_effects_adjustment,
	COMPOSITOR_MT_add_effects_filter,
	COMPOSITOR_MT_add_effects_blur,
	COMPOSITOR_MT_add_effects_keying,
	COMPOSITOR_MT_add_effects_transform,
	COMPOSITOR_MT_add_effects_features,
	COMPOSITOR_MT_add_effects_features_color,
	COMPOSITOR_MT_add_effects_features_looks,
	COMPOSITOR_MT_add_effects_features_other,
	COMPOSITOR_MT_add_effects_presets,
	COMPOSITOR_MT_effects_specials,
	NODE_MT_add_feature_node,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.NODE_MT_add.append(feature_node_menu)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	bpy.types.NODE_MT_add.remove(feature_node_menu)