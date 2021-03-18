from . import subcontractor
import random
from . import helper_functions


# policy
def should_join(params, step, sL, s):
    # flip a coin (1 joins if there's room and random says to)
    should_join = False
    is_spot_open = (params['max_subcontractors'] >
                    helper_functions.count_members(s['subcontractors']))

    if is_spot_open:
        rng = random.random()
        horizon = s["unallocated_funds"]/params["allocation_per_epoch"]
        if rng >= 1/horizon:
            should_join = True

    return {"should_join": should_join}


# mechanism
def joins(params, step, sL, s, inputs):
    # add new members
    if inputs['should_join']:
        b = subcontractor.Subcontractor()
        s['subcontractors'][b.id] = b

    key = "subcontractors"
    value = s['subcontractors']
    return key, value
