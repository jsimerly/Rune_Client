from ecs_engine import Entity
from ui.components.visual import TextVisualComponent, UIPositionComponent, RectangleVisualComponent

def calculate_component_text_pos(ui_entity: Entity) -> tuple[int, int]:
    text_comp = ui_entity.get_component(TextVisualComponent)
    pos_comp = ui_entity.get_component(UIPositionComponent)
    rect_comp = ui_entity.get_component(RectangleVisualComponent)

    alignment = text_comp.alignment
    container_size = rect_comp.size
    container_pos = pos_comp.pos
    text_size = text_comp.text_size
    margin = text_comp.margin

    return calculate_component_pos_rect(
        alignment, container_size, container_pos, text_size, margin
    )


def calculate_component_pos_rect(alignment: str, container_size: tuple[int, int], container_pos: tuple[int, int], component_size: tuple[int, int], margin: int) -> tuple[int, int]:
    alignment_map = {
        'top_left': ('left', 'top'),
        'top_center': ('center', 'top'),
        'top_right': ('right', 'top'),
        'center_left': ('left', 'center'),
        'center': ('center', 'center'),
        'center_right': ('right', 'center'),
        'bottom_left': ('left', 'bottom'),
        'bottom_center': ('center', 'bottom'),
        'bottom_right': ('right', 'bottom'),
    }

    container_width, container_height = container_size
    container_x, container_y = container_pos
    component_width, component_height = component_size

    x_align, y_align = alignment_map[alignment]

    if x_align == 'left':
        component_x = container_x + margin
    elif x_align == 'center':
        component_x = container_x + (container_width - component_width) / 2
    elif x_align == 'right':
        component_x = container_x + container_width - component_width - margin

    if y_align == 'top':
        component_y = container_y + margin
    elif y_align == 'center':
        component_y = container_y + (container_height - component_height) / 2
    elif y_align == 'bottom':
        component_y = container_y + container_height - component_height - margin

    return component_x, component_y