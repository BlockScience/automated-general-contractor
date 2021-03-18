class Subcontractor:
    # autoincrementing id.
    subcontractor_counter = 0

    def __init__(self):
        # initialize subcontractor state
        self.id = Subcontractor.subcontractor_counter

        # money that can be claimed by this subcontractor
        self.claimable_funds = 0

        # amount of money that is put in escrow,
        # subcontractor loses it if they leave when not allowed
        self.stake = 5

        # amount of money this subcontractor has
        self.holdings = 0

        # member of the agreement (True/False)
        self.member = True

        # how long the subcontractor has been attached to the agreement
        self.time_attached = 0

        # is the subcontractor allowed to leave?
        self.allowed_to_leave = False

        Subcontractor.subcontractor_counter += 1
