import pytest

from randovania.bitpacking import bitpacking
from randovania.bitpacking.bitpacking import BitPackDecoder
from randovania.game_description.item.item_category import ItemCategory
from randovania.game_description.item.major_item import MajorItem
from randovania.layout.base.major_item_state import MajorItemState


@pytest.fixture(
    params=[
        {"encoded": b'\x04', "json": {}},
        {"encoded": b'\x14', "json": {"num_shuffled_pickups": 1}},
        {"encoded": b'$', "json": {"num_shuffled_pickups": 2}},
        {"encoded": b'4', "json": {"num_shuffled_pickups": 3}},
        {"encoded": b'Me', "json": {"num_shuffled_pickups": 99}},

        {"encoded": b'EP', "category": "energy_tank", "json": {"num_shuffled_pickups": 6,
                                                               "num_included_in_starting_items": 10}},

        {"encoded": b'\x076D', "ammo_index": (10, 20), "json": {"included_ammo": [230, 200]}},
    ],
    name="state_with_data")
def _state_with_data(request, echoes_item_database):
    default_item_category = ItemCategory(
        name="visor",
        long_name="Visors",
        hint_details=("a ","visor"),
        is_major_category=True,
        is_key=False
    )

    item_category_name = request.param.get("category", "")
    item_category = echoes_item_database.item_categories[item_category_name] if item_category_name else default_item_category

    broad_category_name = request.param.get("broad_category", "")
    broad_category = echoes_item_database.item_categories[broad_category_name] if broad_category_name else default_item_category

    item = MajorItem(
        name="Item Name",
        item_category=item_category,
        broad_category=broad_category,
        model_name="Model Name",
        progression=(),
        ammo_index=request.param.get("ammo_index", ()),
        required=True,
        original_index=None,
        probability_offset=0,
    )
    return item, request.param["encoded"], MajorItemState.from_json(request.param["json"])


def test_decode(state_with_data):
    # Setup
    item, data, expected = state_with_data

    # Run
    decoder = BitPackDecoder(data)
    result = MajorItemState.bit_pack_unpack(decoder, item)

    # Assert
    assert result == expected


def test_encode(state_with_data):
    # Setup
    item, expected, value = state_with_data

    # Run
    result = bitpacking._pack_encode_results([
        (value_argument, value_format)
        for value_argument, value_format in value.bit_pack_encode(item)
    ])

    # Assert
    assert result == expected


def test_blank_as_json():
    assert MajorItemState().as_json == {}


def test_blank_from_json():
    assert MajorItemState.from_json({}) == MajorItemState()
