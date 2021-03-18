import random


# policy
def should_leaves(params, step, sL, s):
    # complex, iterate later -- if you would be leaving and not penalized,
    # probability is 1/10.  if there would be a penalty, probability is 1/50
    # each subcontractor has a chance to leave.

    # key=subcontractorId, value=boolean representing whether the subcontractor should leave
    # print(f'{s=}')

    should_leaves = {}
    funds_to_claim = 0
    removed_stake = 0
    forfeit_stake = 0
    for subcontractor_id, b in s['subcontractors'].items():
        horizon = s["unallocated_funds"]/params["allocation_per_epoch"]
        if b.allowed_to_leave:
            p = 1/horizon
        else:
            p = 1/(10*horizon)

        rng = random.random()
        should_leaves[subcontractor_id] = rng < p
        if should_leaves[subcontractor_id]:
            # when a subcontractor leaves, they take their
            # claimable_funds funds with them.
            funds_to_claim += b.claimable_funds
            if b.allowed_to_leave:
                removed_stake += b.stake
            else:
                forfeit_stake += b.stake

    return {
        'should_leaves': should_leaves,
        'funds_to_claim': funds_to_claim,
        'removed_stake': removed_stake,
        'forfeit_stake': forfeit_stake
        }


# mechanism

# subcontractor is allowed to leave if they have stayed in longer than
# min_epochs or unallocated_funds < min_horizon
def allowed_to_leave(params, step, sL, s, inputs):
    # 1) first check the horizon (if the horizon is too short all subcontractors can leave)
    # 2) if the horizon is not too short then only subcontractors who have been members
    # longer than the min period can leave

    # calculate the horizon
    # print(f'')
    horizon = s['unallocated_funds'] / params['allocation_per_epoch']
    subcontractors = s['subcontractors']

    if len(subcontractors) > 0:
        for b in subcontractors.values():
            if horizon < params['min_horizon'] or b.time_attached >= params['min_epochs']:
                b.allowed_to_leave = True
    
    key = 'subcontractors'
    value = subcontractors
    return key, value


def leaves(params, step, sL, s, inputs):
    """ When a subcontractor leaves,
    1) member is set to False
    2) they take their stake
    3) they take their claimable_funds

    """
    for should_leave in inputs['should_leaves']:
        if inputs['should_leaves'][should_leave]:
            subcontractor = s['subcontractors'][should_leave]
            subcontractor.member = False
            subcontractor.stake = 0
            subcontractor.holdings += subcontractor.claimable_funds
            subcontractor.claimable_funds = 0
            if subcontractor.allowed_to_leave:
                subcontractor.holdings += subcontractor.stake

    key = 'subcontractors'
    value = s['subcontractors']
    return key, value


def decrement_allocated_funds_due_to_leaves(params, step, sL, s, inputs):
    """ when a subcontractor leaves,
    1) the allocated_funds is decreased by the claimable_funds.
        allocated_funds = s['allocated_funds']
    """

    key = 'allocated_funds'
    value = s['allocated_funds'] - inputs['funds_to_claim']
    return key, value


def increment_unallocated_funds_due_to_forfeit_stake(params, step, sL, s, inputs):
    """ when a subcontractor leaves,
    3) the unallocated_funds is increased by the forfeit_stake
    """

    key = "unallocated_funds"
    value = s["unallocated_funds"] + inputs['forfeit_stake']
    return key, value
