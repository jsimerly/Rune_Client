from __future__ import annotations
from ecs_engine import System, subscribe_to_event
from src.drafting.components.draft_state import DraftStateSingletonComponent
from src.drafting.components.character import SelectedCharacterSingleton
from src.drafting.components.markers import CountdownMarker
from src.ui.components.visual import TextVisualComponent
from src.network import MessageType, NetworkManager
from src.user.user import User
from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from src.drafting.drafting import NetworkDraftInfo


class DraftSystem(System):
    network = NetworkManager()
    countdown_ended_ctas: dict[str, str] = {
        'pre_draft': 'Drafting Beginning',
        'completed': 'Game Starting...'
    }

    @subscribe_to_event('update_dt')
    def update(self, dt:int):
        draft_state = self.get_singleton_component(DraftStateSingletonComponent)
        self._update_countdown(dt, draft_state)

    @subscribe_to_event('recv_draft_update')
    def update_draft(self, message: MessageType):
        draft_state = self.get_singleton_component(DraftStateSingletonComponent)

        data = message['data']['update_info']
        print(data)
        draft_state.state = data['phase']['state']
        draft_state.count_down_ms = data['phase']['alloted_time_sec'] * 1000

        for update in data['updates']:
            print(update)

    def _handle_network_update(self):
        ...

    @subscribe_to_event('char_icon_selected')
    def char_icon_selected(self, char_id: int):
        selected_char = self.get_singleton_component(SelectedCharacterSingleton)
        selected_char.char_id = char_id

    @subscribe_to_event('lock_in_clicked')
    def lock_in_clicked(self):
        draft_state = self.get_singleton_component(DraftStateSingletonComponent)
        if draft_state.is_client_turn:
            self._send_selection()
        else:
            print('You cannot lock in yet.')

    @subscribe_to_event('recv_force_selection')
    def force_selection(self, message: MessageType):
        self._send_selection()

    def _send_selection(self):
        selected_char_comp = self.get_singleton_component(SelectedCharacterSingleton)
        draft_state = self.get_singleton_component(DraftStateSingletonComponent)
  
        if not selected_char_comp.char_id:
            raise Exception('WE NEED TO CANCEL THE DRAFT IF NOTHING IS SELECTED')

        message = {
            'type': 'draft_selection',
            'draft_id': draft_state.id,
            'char_id': selected_char_comp.char_id
        }
        self.network.send_message(user=User().serialized, type='draft', serialized_message=message)

    def handle_network_state_change(self, message: NetworkDraftInfo, draft_state: DraftStateSingletonComponent):
        draft_state.available_picks = message['available']
        draft_state.unavailable_picks = message['unavailable']
        draft_state.current_phase = message['current_phase']
            
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
