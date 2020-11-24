from typing import Iterable, Dict, Tuple

from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from randovania.game_description.item.ammo import Ammo
from randovania.interface_common.preset_editor import PresetEditor
from randovania.layout.ammo_state import AmmoState
from randovania.layout.preset import Preset


def _update_ammo_visibility(elements: Tuple[QtWidgets.QWidget, ...], is_visible: bool):
    elements[2].setVisible(is_visible)
    elements[3].setVisible(is_visible)
    if elements[2].text() == "-":
        elements[4].setVisible(is_visible)


class SplitAmmoWidget(QtWidgets.QCheckBox):
    def __init__(self, parent: QtWidgets.QWidget, editor: PresetEditor,
                 unified_ammo: Ammo, split_ammo: Iterable[Ammo]):
        super().__init__(parent)
        self._editor = editor
        self.unified_ammo = unified_ammo
        self.split_ammo = list(split_ammo)
        self.setTristate(True)
        self.clicked.connect(self.change_split)

    def on_preset_changed(self, preset: Preset, ammo_pickup_widgets: Dict[Ammo, Tuple[QtWidgets.QWidget, ...]]):
        ammo_configuration = preset.layout_configuration.ammo_configuration

        has_unified = ammo_configuration.items_state[self.unified_ammo].pickup_count > 0
        has_split = any(ammo_configuration.items_state[item].pickup_count > 0
                        for item in self.split_ammo)

        if has_unified:
            new_state = Qt.PartiallyChecked if has_split else Qt.Unchecked
        else:
            new_state = Qt.Checked
        self.setCheckState(new_state)

        _update_ammo_visibility(ammo_pickup_widgets[self.unified_ammo], has_unified)
        for item in self.split_ammo:
            _update_ammo_visibility(ammo_pickup_widgets[item], has_split)

    def change_split(self, has_split: bool):
        with self._editor as editor:
            ammo_configuration = editor.ammo_configuration

            current_total = sum(
                ammo_configuration.items_state[ammo].pickup_count
                for ammo in (self.unified_ammo, *self.split_ammo)
            )
            if has_split:
                split_state = AmmoState(pickup_count=current_total // len(self.split_ammo))
                unified_state = AmmoState()
            else:
                split_state = AmmoState()
                unified_state = AmmoState(pickup_count=current_total)

            new_states = {self.unified_ammo: unified_state}
            for ammo in self.split_ammo:
                new_states[ammo] = split_state

            editor.ammo_configuration = ammo_configuration.replace_states(new_states)
