# policies:
# no inputs, because the outputs here are the inputs
def check_subcontractors(params, step, sL, s):
    # print(f'4: {params=}')
    # True if the number of member subcontractors is
    # greater than or equal to the minimum number of subcontractors.
    value = s['num_member_subcontractors'] >= params['min_subcontractors']
    key = 'check_subcontractors'
    return {key: value}


# mechanisms:
def allocated_funds(params, step, sL, s, inputs):
    # print(f'1: {params=}')
    value = s['allocated_funds']
    # if there are enough subcontractors, put the allocation in the subcontractors' hands.
    if inputs['check_subcontractors']:
        value += params['allocation_per_epoch']

    key = 'allocated_funds'
    return key, value


def unallocated_funds(params, step, sL, s, inputs):
    # print(f'2: {params=}')
    value = s['unallocated_funds']
    if inputs['check_subcontractors']:
        value -= params['allocation_per_epoch']

    key = 'unallocated_funds'
    return key, value


def allocate_funds_to_member_subcontractors(params, step, sL, s, inputs):
    # print(f'3: {params=}')
    if inputs['check_subcontractors']:
        amount_allocated = (params['allocation_per_epoch'] /
                            s['num_member_subcontractors'])

        for subcontractor in s['subcontractors'].values():
            if subcontractor.member:
                subcontractor.claimable_funds += amount_allocated

    value = s['subcontractors']
    key = 'subcontractors'
    return key, value


def total_subcontractor_stake(params, step, sL, s, inputs):
    total_subcontractor_stake = 0
    for subcontractor in s['subcontractors'].values():
        if subcontractor.member:
            total_subcontractor_stake += subcontractor.stake

    value = total_subcontractor_stake
    key = 'total_subcontractor_stake'
    return key, value
