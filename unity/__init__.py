from . import(
    node,
    preset,
    mask,
    effect,
    layer,
    source,
    compositor,
    output,
)

module_list = (
    node,
    preset,
    mask,
    effect,
    layer,
    source,
    compositor,
    output,
)

def register():
    for mod in module_list:
        mod.register()
        
def unregister():
    for mod in reversed(module_list):
        mod.unregister()

if __name__ == "__main__":
    register()