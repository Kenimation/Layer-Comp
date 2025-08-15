import bpy

class Mask_Node:
	def update_x(self, context):
		self.node_tree.nodes["Mask"].x = self.x

	def update_y(self, context):
		self.node_tree.nodes["Mask"].y = self.y

	def update_width(self, context):
		self.node_tree.nodes["Mask"].mask_width = self.width

	def update_height(self, context):
		self.node_tree.nodes["Mask"].mask_height = self.height

	def update_rotation(self, context):
		self.node_tree.nodes["Mask"].rotation = self.rotation

	x : bpy.props.FloatProperty(default = 0.5, min=-1,max=2, name = "X", update = update_x)
	y : bpy.props.FloatProperty(default = 0.5, min=-1,max=2, name = "Y", update = update_y)

	width : bpy.props.FloatProperty(default = 1, min=0,max=2, name = "Width", update = update_width)
	height : bpy.props.FloatProperty(default = 0.55, min=0,max=2, name = "Height", update = update_height)

	rotation : bpy.props.FloatProperty(default = 0, name = "Rotation", update = update_rotation, subtype= 'ANGLE')

	def draw_mask(self, layout):
		row = layout.row(align=True)
		row.prop(self, "x")
		row.prop(self, "y")
		row = layout.row(align=True)
		row.prop(self, "width", slider=True)
		row.prop(self, "height", slider=True)
		layout.prop(self, "rotation")

class Key_Node:

	def update_h(self, context):
		for node in self.node_tree.nodes:
			if node.type == 'COLOR_MATTE':
				node.color_hue = self.color_hue

	def update_s(self, context):
		for node in self.node_tree.nodes:
			if node.type == 'COLOR_MATTE':
				node.color_saturation = self.color_saturation

	def update_v(self, context):
		for node in self.node_tree.nodes:
			if node.type == 'COLOR_MATTE':
				node.color_value = self.color_value

	color_hue : bpy.props.FloatProperty(default = 0.15, min = 0, max=1, name = "H", update = update_h)
	color_saturation : bpy.props.FloatProperty(default = 0.15, min = 0, max=1, name = "S", update = update_s)
	color_value : bpy.props.FloatProperty(default = 0.15, min = 0, max=1, name = "V", update = update_v)

	def init_key(self):
		self.color_hue = 0.15
		self.color_saturation = 0.15
		self.color_value = 0.15

	def draw_key(self, layout):
		col = layout.column(align=True)
		col.prop(self, "color_hue", slider = True)
		col.prop(self, "color_saturation", slider = True)
		col.prop(self, "color_value", slider = True)