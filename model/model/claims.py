
import random
CLAIM_CONST = 10


def should_make_claims(params, step, sL, s):
    """
    each subcontractor with a_i > 0 makes a claim if: rng > CLAIM_CONST / a_i
    """
    # key subcontractor_id, value bool whether to make a claim
    should_make_claims = {}
    funds_to_claim = 0
    # does each subcontractor make a claim?
    for subcontractor_id, subcontractor in s['subcontractors'].items():
        if subcontractor.claimable_funds > 0:
            rng = random.random()
            should_make_claim = rng > CLAIM_CONST / subcontractor.claimable_funds
            should_make_claims[subcontractor_id] = should_make_claim
            if should_make_claim:
                funds_to_claim += subcontractor.claimable_funds
    #print(f'{should_make_claims=}')
    return {'should_make_claims': should_make_claims,
            'funds_to_claim': funds_to_claim}


def make_claims(params, step, sL, s, inputs):
    """ increase holdings for each subcontractor making a claim by the
    amount of their claimable_funds
    """

    should_make_claims = inputs['should_make_claims']
    # apply each claim

    for subcontractor_id, should_make_claim in should_make_claims.items():
        if should_make_claim:
            s['subcontractors'][subcontractor_id].holdings += \
                 s['subcontractors'][subcontractor_id].claimable_funds
            s['subcontractors'][subcontractor_id].claimable_funds = 0

    key = 'make_claims'
    value = s['subcontractors']
    return key, value


def decrement_allocated_funds_by_claims(params, step, sL, s, inputs):
    """ decrease unallocated_funds for each subcontractor making a claim by the
    amount of their claimable_funds
    """

    allocated_funds = s['unallocated_funds'] - inputs['funds_to_claim']

    key = 'allocated_funds'
    value = allocated_funds
    return key, value
