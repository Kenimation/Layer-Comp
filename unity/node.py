import bpy
import importlib
from pathlib import Path
import os
from typing import List, Tuple, Type

def create_mix_node(node_group):
	version = bpy.app.version
	if version >= (4, 5, 0):
		mix_node = node_group.nodes.new("ShaderNodeMix")
		mix_node.data_type = 'RGBA'
	elif version < (4, 5, 0):
		mix_node = node_group.nodes.new("CompositorNodeMixRGB")
		mix_node.use_alpha = True
	return mix_node

def get_mix_node_inputs(mix_node, input):
	version = bpy.app.version
	if version >= (4, 5, 0):
		if input == 0:
			inputs = mix_node.inputs[0]
		elif input == 1:
			inputs = mix_node.inputs[6]
		elif input == 2:
			inputs = mix_node.inputs[7]
	elif version < (4, 5, 0):
		inputs = mix_node.inputs[input]
	return inputs

def get_mix_node_outputs(mix_node):
	version = bpy.app.version
	if version >= (4, 5, 0):
		outputs = mix_node.outputs['Result']
	elif version < (4, 5, 0):
		outputs = mix_node.outputs[0]
	return outputs

def get_invert_node_inputs(invert_node, input, value):
	version = bpy.app.version
	if version >= (4, 5, 0):
		if input == 'Color':
			invert_node.inputs[3].default_value = value
		elif input == 'Alpha':
			invert_node.inputs[2].default_value = value
	elif version < (4, 5, 0):
		if input == 'Color':
			invert_node.invert_alpha = value
		elif input == 'Alpha':
			invert_node.invert_rgb = value

class Node:
	def free(self):
		if self.node_tree.users == 1:
			bpy.data.node_groups.remove(self.node_tree, do_unlink=True)

	def addSocket(self, is_output, sockettype, name):
		if is_output == True:
			socket = self.node_tree.interface.new_socket(
				name, in_out="OUTPUT", socket_type=sockettype
			)
		else:
			socket = self.node_tree.interface.new_socket(
				name, in_out="INPUT", socket_type=sockettype
			)

		return socket
	
class Mix_Node:
	blend_items=(('MIX', 'Mix', 'Mix'),
		('DARKEN', 'Darken', 'Darken'),
		('MULTIPLY', 'Multiply', 'Multiply'),
		('BURN', 'Color Burn', 'Burn'),
		('LIGHTEN', 'Lighten', 'Lighten'),
		('DODGE', 'Color Dodge', 'Color Dodge'),
		('ADD', 'Add', 'Add'),
		('OVERLAY', 'Overlay', 'Overlay'),
		('SOFT_LIGHT', 'Soft Light', 'Soft Light'),
		('LINEAR_LIGHT', 'Linear Light', 'Linear Light'),
		('DIFFERENCE', 'Difference', 'Difference'),
		('EXCLUSION', 'Exclusion', 'Exclusion'),
		('SUBTRACT', 'Subtract', 'Subtract'),
		('DIVIDE', 'Divide', 'Divide'),
		('HUE', 'Hue', 'Hue'),
		('SATURATION', 'Saturation', 'Saturation'),
		('COLOR', 'Color', 'Color'),
		('VALUE', 'Value', 'Value'),
		)

	def update_blend(self, context):
		if self.node_tree:
			self.node_tree.nodes["Mix"].blend_type = self.blend_type

	blend_type : bpy.props.EnumProperty(default = 'MIX', items = blend_items, name = "Blend", update = update_blend)

class NodeLib:
	BASE_DIR = Path(os.path.join(os.path.dirname(os.path.abspath(__file__))))

	@staticmethod
	def get_node() -> List[Type]:
		"""Safely retrieve node definitions"""
		try:
			return NodeLib()()
		except Exception as e:
			print(f"Error loading node definitions: {e}")
			return []
		
	@staticmethod
	def import_classes_from_folder(folder_path):

		folder_name = folder_path.name
		imported_classes = []
		prefix = "CompositorNode"

		# Pre-fetch all .py files
		py_files = [
			f
			for f in folder_path.iterdir()
			if f.suffix == ".py" and f.stem not in {"__init__", "_utils"}
		]

		for py_file in py_files:
			module_name = f".{folder_name}.{py_file.stem}"

			try:
				module = importlib.import_module(module_name, package=__package__)
			except ImportError as e:
				continue

			for attr_name, attr in module.__dict__.items():
				if (
					isinstance(attr, type)
					and attr_name.startswith(prefix)
					and attr_name != prefix
				):
					imported_classes.append(attr)
				
		return imported_classes

	@classmethod
	def __call__(cls):
		version = bpy.app.version

		if version >= (4, 5, 0):
			folder = cls.BASE_DIR / "node_main"
		elif version < (4, 5, 0):
			folder = cls.BASE_DIR / "node_v4_4_below"
			
		classes = cls.import_classes_from_folder(folder)

		return classes

def register():
	nodes = NodeLib.get_node()
	for cls in nodes:
		bpy.utils.register_class(cls)

def unregister():
	nodes = NodeLib.get_node()
	for cls in nodes:
		bpy.utils.unregister_class(cls)