import bpy
from .defs import *

class AddonPref_Properties:
	active_node_panel : bpy.props.BoolProperty(default = True, description = "Show active node panel in compositor area.")
	effect_preset_panel : bpy.props.BoolProperty(default = True, description = "Show effect preset panel.")
	layer_name : bpy.props.EnumProperty(default = "Layer",
							items = [('Layer', 'Layer', ''),
									('Source', 'Source', ''),
									],
							description = "Layer name display type."
									)
	panel_type : bpy.props.EnumProperty(default = "Expand",
							items = [('List', 'List', ''),
									('Expand', 'Expand', ''),
									],
							description = "Properties panel type."
									)
	view3d : bpy.props.BoolProperty(default = True, description = "Show Panel in 3D Viewport")

	search : bpy.props.BoolProperty(default = True, description = "Search Layer in Compositor")
	
	label : bpy.props.BoolProperty(default = True, description = "Show label icon in layer.")
	fx_toggle : bpy.props.BoolProperty(default = True, description = "Show FX toggle in layer.")
	blend_mode : bpy.props.BoolProperty(default = True, description = "Show blend mode in layer.")
	mix : bpy.props.BoolProperty(default = True, description = "Show mix in layer.")

	new_compositor_option : bpy.props.EnumProperty(default = "First",
							items = [('Never', 'Never', ''),
									('First', 'First', ''),
									('Any', 'Any', ''),
									],
							description = "New compositor will add reder layer."
									)
	
	duplicate_layer_option : bpy.props.EnumProperty(default = "Next",
							items = [('Next', 'Next', ''),
									('Top', 'Top', ''),
									],
							description = "Duplicated item position."
									)
	duplicate_effect_option : bpy.props.EnumProperty(default = "Next",
							items = [('Next', 'Next', ''),
									('Top', 'Top', ''),
									],
							description = "Duplicated item position."
									)

class AddonPreferences(bpy.types.AddonPreferences, AddonPref_Properties):
	bl_idname = __package__

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		self.draw_preferences(context, col)

	def draw_preferences(self, context, col):
		col.use_property_split = True
		col.use_property_decorate = False

		row = col.row()

		box = row.box()
		box.scale_x= 0.4
		box.label(text="UI Settings")
		col = box.column(heading="Panel", align=True)
		col.prop(self, "view3d", text="3D Viewport Panel")
		col.prop(self, "active_node_panel", text="Active Node")
		col.prop(self, "effect_preset_panel", text="Effect Presets")
		col = box.column(heading = "Compositor")
		col.prop(self, "search", text="Search Box")
		sub = col.row()
		sub.prop(self, "layer_name", text="Layer Name", expand=True)

		sub = col.row(heading="Layer Display", align=True)
		sub.prop(self, "label", text="Label", toggle = True)
		sub.prop(self, "fx_toggle", text="FX", toggle = True)
		sub.prop(self, "blend_mode", text="Blend", toggle = True)
		sub.prop(self, "mix", text="Mix", toggle = True)
		col = box.column(heading="Properties", align=True)
		sub = col.row()
		sub.prop(self, "panel_type", text="Panel Type", expand=True)
		box.label(text="Operator")
		col = box.column(heading="", align=True)
		col.row().prop(self, "new_compositor_option", text="New Compositor", expand = True)
		col = box.column(heading="", align=True)
		col.row().prop(self, "duplicate_layer_option", text="Duplicate Layer", expand = True)
		col.row().prop(self, "duplicate_effect_option", text="Effect", expand = True)

		box = row.box()
		col = box.column()
		colrow = col.row()
		colrow.label(text="Effect Presets")
		colrow.operator("scene.comp_new_effect_preset", text="", icon='ADD', emboss = False)
		colrow.operator("scene.comp_load_preset", text='', icon = "IMPORT", emboss = False)
		colrow.menu("COMPOSITOR_MT_export_presets", text='', icon = "EXPORT")

		presets = get_presets()
		if len(presets) > 0:
			col = box.column()
			for preset in presets:
				header, panel = col.panel(idname=f"{preset}.presets", default_closed=True)
				header.label(text=preset)
				header.operator("scene.comp_remove_preset", text='', icon = "X", emboss=False).name = preset
				if panel:
					effects = get_effect_presets(preset)
					panel_box = panel.box()
					if len(effects) > 0:
						sub = panel_box.column()
						for effect in effects:
							row = sub.row()
							row.label(text=effect, icon = "SHADERFX")
							remove = row.operator("scene.comp_remove_effect_preset", text='', icon = "REMOVE", emboss=False)
							remove.preset = preset
							remove.target = effect
					else:
						panel_box.label(text="Preset has no effect", icon = "FILEBROWSER")
		else:
			box.label(text="No Presets", icon = "FILEBROWSER")

classes = (
	AddonPreferences,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
