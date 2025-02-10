import bpy
import requests

# server URL
SERVER_URL = "http://127.0.0.1:5000"

# send transform data to the server
def send_transform_data():
    obj = bpy.context.active_object
    if obj is None:
        print("No object selected.")
        return

    # Get transformation data
    transform_data = {
        "name": obj.name,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale),
    }

    try:
        response = requests.post(f"{SERVER_URL}/transform", json=transform_data)
        if response.status_code == 200:
            print("Transform data successfully sent!")
        else:
            print(f"Error: {response.json()}")
    except Exception as e:
        print(f"Failed to send data: {e}")

# Update transform data when selected object changes
def update_object_transform(self, context):
    obj = bpy.context.active_object
    if obj:
        name = obj.name
        position = tuple(obj.location)
        rotation = tuple(obj.rotation_euler)
        scale = tuple(obj.scale)
        endpoint = bpy.context.scene.ddc_endpoint
        send_transform_data(name, position, rotation, scale, endpoint)

# Blender UI Panel
class DDC_PT_ToolPanel(bpy.types.Panel):
    bl_label = "DDC Plugin"
    bl_idname = "DDC_PT_ToolPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DDC"

    def draw(self, context):
        layout = self.layout
        layout.operator("ddc.send_transform")


# send transform data manually
class DDC_OT_SendTransform(bpy.types.Operator):
    bl_idname = "ddc.send_transform"
    bl_label = "Send Transform Data"
    bl_description = "Send object transform data to the server"

    def execute(self, context):
        send_transform_data()
        return {'FINISHED'}

# update transform values
def update_transform(self, context):
    obj = bpy.data.objects.get(context.scene.ddc_selected_object)
    if obj:
        obj.location = context.scene.ddc_position
        obj.rotation_euler = context.scene.ddc_rotation
        obj.scale = context.scene.ddc_scale

def register():
    bpy.utils.register_class(DDC_PT_ToolPanel)
    bpy.utils.register_class(DDC_OT_SendTransform)

def unregister():
    bpy.utils.unregister_class(DDC_PT_ToolPanel)
    bpy.utils.unregister_class(DDC_OT_SendTransform)


if __name__ == "__main__":
    register()
