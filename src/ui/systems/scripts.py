from ecs_engine import Entity
from src.ui.components.visual import RectangleVisualComponent
from src.ui.components.animation import UIAnimationComponent
from typing import TypedDict, Callable

def double_border(entity: Entity, animation_comp: UIAnimationComponent):
    if animation_comp.state == 'start':
        rect_comp = entity.get_component(RectangleVisualComponent)
        if rect_comp:
            rect_comp.attributes['border_thickness'] = int(rect_comp.attributes['border_thickness'] * 2)
            rect_comp.focus_attributes['border_thickness'] = int(rect_comp.focus_attributes['border_thickness'] * 2)

    if animation_comp.state == 'end':
        rect_comp = entity.get_component(RectangleVisualComponent)
        if rect_comp:
            rect_comp.attributes['border_thickness'] = rect_comp.attributes['border_thickness'] // 2
            rect_comp.focus_attributes['border_thickness'] = rect_comp.focus_attributes['border_thickness'] // 2


AnimationFunction = Callable[[Entity, UIAnimationComponent], None]

default_animation_scripts: dict[str, AnimationFunction] = {
    'double_border': double_border
}