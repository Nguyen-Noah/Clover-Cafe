import imgui

from enum import Enum
from engine.editor.pimgui import PImGui
from engine.utils.elements import Element
from engine.primitives import vec2, vec3, vec4

class Component(Element):
    ID_COUNTER = 0      # global to component

    def __init__(self):
        super().__init__()
        self.entity = None  
        self.uid = -1       # unique to object

    def init(max_id):
        Component.ID_COUNTER = max_id

    def start(self):
        pass

    # can be used for things like: weapons breaking sound, hit sounds, etc.
    def destroy(self):
        pass

    def imgui(self):
        ignore = ['Register', '_singleton', 'Uid']
        try:
            for field_name, value in vars(self).items():
                field_type = type(value)
                name = field_name.capitalize()
                if name in ignore:
                    continue

                if field_type == int:
                    c, val = PImGui.drag_int(name, value)
                    if c:
                        setattr(self, field_name, val)

                elif field_type == float:
                    c, val = PImGui.drag_float(name, value)
                    if c:
                        setattr(self, field_name, val)

                elif field_type == vec2:
                    PImGui.draw_vec2_control(name, value)

                elif field_type == vec3:
                    im_vec = [value.x, value.y, value.z]
                    changed, im_vec = imgui.drag_float3(f"{name}", *im_vec)
                    if changed:
                        value.x, value.y, value.z = im_vec
                        setattr(self, field_name, value)

                elif field_type == vec4:
                    im_vec = [value.x, value.y, value.z, value.w]
                    changed, im_vec = imgui.drag_float4(f"{name}", *im_vec)
                    if changed:
                        value.x, value.y, value.z, value.w = im_vec
                        setattr(self, field_name, value)

                elif field_type == bool:
                    changed, im_val = imgui.checkbox(f"{name}", value)
                    if changed:
                        setattr(self, field_name, im_val)

                elif issubclass(field_type, Enum):
                    enum_map = {e.name.capitalize(): e for e in field_type}
                    enum_names = list(enum_map.keys())
                    current_index = enum_names.index(value.name.capitalize())

                    changed, new_index = imgui.combo(field_name, current_index, enum_names)
                    if changed:
                        setattr(self, field_name, enum_map[enum_names[new_index]])

        except Exception as e:
            print(e)

    def generate_id(self):
        if self.uid == -1:
            self.uid = Component.ID_COUNTER
            Component.ID_COUNTER += 1

    def editor_update(self, dt):
        pass

    def update(self, dt):
        pass

    def serialize(self):
        return {
            "type": self.__class__.__name__,
            "uid": self.uid
            }
