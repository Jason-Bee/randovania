from __future__ import annotations

from typing import TYPE_CHECKING

from randovania.game_description.db.node_identifier import NodeIdentifier
from randovania.gui.widgets.node_selector_widget import NodeSelectorWidget

if TYPE_CHECKING:
    import pytestqt.qtbot  # type: ignore[import-untyped]

    from randovania.game_description.game_description import GameDescription


def test_select_by_identifier(skip_qtbot: pytestqt.qtbot.QtBot, blank_game_description: GameDescription) -> None:
    widget = NodeSelectorWidget(blank_game_description.region_list)
    skip_qtbot.addWidget(widget)

    identifier = NodeIdentifier.create("Intro", "Explosive Depot", "Pickup (Explosive)")
    assert widget.selected_node() is None
    widget.select_by_identifier(identifier)

    assert widget.selected_node().identifier == identifier
