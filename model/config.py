from cadCAD import configuration

from .psub import psubs
from .state import genesis_state

# Parameters
# Values are lists because they support sweeping.
simulation_config = configuration.utils.config_sim({
    "T": range(90),
    "N": 1,
    'M': {
        "required_stake": [5],        # S_min
        "epoch_length": [1],          # in days
        "min_epochs": [28],           # tau
        "allocation_per_epoch": [25],
        "min_horizon": [7],           # H_min
        "min_subcontractors": [3],           # n_min
        "max_subcontractors": [5],           # n_max
    }
})

exp = configuration.Experiment()

exp.append_configs(sim_configs=simulation_config,
                   initial_state=genesis_state,
                   partial_state_update_blocks=psubs)
