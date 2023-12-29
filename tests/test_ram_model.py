import json
import pytest
from pydantic import ValidationError
from paicorelib import *


@pytest.mark.parametrize(
    "params",
    [
        {
            "dest_coords": [Coord(0, 0)],
            "tick_relative": [0] * 100 + [1] * 100,
            "addr_axon": list(range(0, 200)),
            "addr_core_x": 0,
            "addr_core_y": 1,
            "addr_core_x_ex": 0,
            "addr_core_y_ex": 0,
            "addr_chip_x": 0,
            "addr_chip_y": 0,
        },
        {
            "dest_coords": [Coord(0, 0), Coord(1, 0)],
            "tick_relative": [0] * 100,
            "addr_axon": list(range(0, 100)),
            "addr_core_x": 0,
            "addr_core_y": 1,
            "addr_core_x_ex": 0,
            "addr_core_y_ex": 0,
            "addr_chip_x": 0,
            "addr_chip_y": 0,
        },
    ],
)
def test_NeuronDestInfo_instance(ensure_dump_dir, params):
    dest_info = NeuronDestInfo.model_validate(params, strict=True)

    dest_info_dict = dest_info.model_dump(by_alias=True)

    with open(ensure_dump_dir / f"ram_model_dest.json", "w") as f:
        json.dump(dest_info_dict, f, indent=4, ensure_ascii=True)


@pytest.mark.parametrize(
    "params",
    [
        {
            "reset_mode": RM.MODE_NORMAL,
            "reset_v": -1,
            "leaking_comparison": LCM.LEAK_BEFORE_COMP,
            "threshold_mask_bits": 1,
            "neg_thres_mode": NTM.MODE_RESET,
            "neg_threshold": -1,
            "pos_threshold": 0,
            "leaking_direction": LDM.MODE_FORWARD,
            "leaking_integration_mode": LIM.MODE_DETERMINISTIC,
            "leak_v": 1,
            "synaptic_integration_mode": SIM.MODE_DETERMINISTIC,
            "bit_truncate": 1,
            "vjt_init": 1,
        },
        {
            "reset_mode": RM.MODE_NORMAL,
            "reset_v": 0,
            "leaking_comparison": LCM.LEAK_BEFORE_COMP,
            "threshold_mask_bits": -1,
            "neg_thres_mode": NTM.MODE_RESET,
            "neg_threshold": 1 << 10,
            "pos_threshold": 1 << 10,
            "leaking_direction": LDM.MODE_REVERSAL,
            "leaking_integration_mode": LIM.MODE_STOCHASTIC,
            "leak_v": -1,
            "synaptic_integration_mode": SIM.MODE_STOCHASTIC,
            "bit_truncate": 0,
            "vjt_init": 0,
        },
        {
            "reset_mode": RM.MODE_NONRESET,
            "reset_v": 1,
            "leaking_comparison": LCM.LEAK_AFTER_COMP,
            "threshold_mask_bits": 0,
            "neg_thres_mode": NTM.MODE_SATURATION,
            "neg_threshold": 1 << 10,
            "pos_threshold": 1 << 10,
            "leaking_direction": LDM.MODE_FORWARD,
            "leaking_integration_mode": LIM.MODE_DETERMINISTIC,
            "leak_v": -1,
            "synaptic_integration_mode": SIM.MODE_STOCHASTIC,
            "bit_truncate": -1,
            "vjt_init": 0,
        },
    ],
)
def test_NeuronAttrs_instance_illegal(params):
    with pytest.raises(ValidationError):
        NeuronAttrs.model_validate(params)
