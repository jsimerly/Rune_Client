from ecs_engine import System, subscribe_to_event
from src.drafting.components.draft_state import DraftStateSingletonComponent
from src.drafting.components.markers import CountdownMarker
from src.ui.components.visual import TextVisualComponent
from src.utility.sizing import calculate_component_text_pos

class DraftSystem(System):
    countdown_ended_ctas: dict[str, str] = {
        'pre_draft': 'Drafting Beginning',
        'completed': 'Game Starting...'
    }

    @subscribe_to_event('update_dt')
    def update(self, dt:int):
        draft_state = self.get_singleton_component(DraftStateSingletonComponent)
        self._update_countdown(dt, draft_state)
        
    def _update_countdown(self, dt:int, draft_state: DraftStateSingletonComponent):
        count_down_entities = self.get_entities_intersect([CountdownMarker])
        draft_state.count_down_ms -= dt

        for entity in count_down_entities:
            text_comp = entity.get_component(TextVisualComponent)
            if text_comp:
                seconds = draft_state.count_down_ms//1000
                if seconds > -1:
                    seconds_str = f'{str(seconds)}s'
                else:
                    if draft_state.state in self.countdown_ended_ctas:
                        seconds_str = self.countdown_ended_ctas[draft_state.state]
                    elif draft_state.is_client_turn:
                        seconds_str ='Lock In.'
                    else:
                        seconds_str = '-'
                
                text_comp.update_text_realign(seconds_str)
