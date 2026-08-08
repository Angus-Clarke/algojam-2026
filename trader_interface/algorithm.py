import numpy as np

# Constants
SIZZLE_SAFETY_MARGIN = 0.002 # 1% Increase
UQ_DOLLAR_WAIT = 20
UQ_SAFETY_MARGIN = 0.002

# Custom trading Algorithm
class Algorithm():

    # FUNCTION TO SETUP ALGORITHM CLASS
    def __init__(self, positions):
        self.data = {}              # Historical data of all instruments
        self.positionLimits = {}    # Initialise position limits
        self.day = 0                # Initialise the current day as 0
        self.positions = positions  # Initialise the current positions
        
    def get_current_price(self, instrument):
        """
        Helper function to fetch current price of an instrument.
        """
        return self.data[instrument][-1]
    
    # RETURN DESIRED POSITIONS IN DICT FORM
    def get_positions(self):
        # Get current position
        currentPositions = self.positions
        # Get position limits
        positionLimits = self.positionLimits
        
        # Declare a store for desired positions
        desiredPositions = {}
        # Loop through all the instruments you can take positions on.
        for instrument, positionLimit in positionLimits.items():
            # For each instrument initilise desired position to zero
            desiredPositions[instrument] = 0

        # IMPLEMENT CODE HERE TO DECIDE WHAT POSITIONS YOU WANT 
        #######################################################################
        # Display the current trading day
        print("Starting Algorithm for Day:", self.day)
        
        
        # Trade thrifted jeans and the sausage sizzle
        trade_instruments = ["Thrifted Jeans"]
        
        # Display the prices of instruments I want to trade
        for ins in trade_instruments:
            print(f"{ins}: ${self.get_current_price(ins)}")

############################################################################################
        # UQ Dollar Trading
        if self.day > UQ_DOLLAR_WAIT:
            UQ_dollar_avg = 100
            if self.data["UQ Dollar"][-1]/UQ_dollar_avg > 1 + UQ_SAFETY_MARGIN:
                desiredPositions["UQ Dollar"] = -positionLimits["UQ Dollar"]
            elif self.data["UQ Dollar"][-1]/UQ_dollar_avg < 1 - UQ_SAFETY_MARGIN:
                desiredPositions["UQ Dollar"] = positionLimits["UQ Dollar"]
        
        # If its 10th day or more, then trade
        if self.day >= 10:
            for ins in trade_instruments:
                # if price has gone down, buy
                todays_price = self.data[ins][-1]
                yesterdays_price = self.data[ins][-2]
                if yesterdays_price > todays_price:
                    desiredPositions[ins] = positionLimits[ins]
                else: # else, short
                    desiredPositions[ins] = -positionLimits[ins]

            # Thrifted Jeans Trading (Swing Trading)
            todays_price = self.data["Thrifted Jeans"][-1]
            yesterdays_price = self.data["Thrifted Jeans"][-2]
            if yesterdays_price > todays_price:
                desiredPositions["Thrifted Jeans"] = positionLimits["Thrifted Jeans"]
            elif yesterdays_price < todays_price: # else, short
                desiredPositions["Thrifted Jeans"] = -positionLimits["Thrifted Jeans"]

            # Sausage Sizzle Trading (Index Trading)
            print(f"{"Sausage Sizzle"}: ${self.get_current_price("Sausage Sizzle")}")

            bread_change = self.data["Bread"][-1] / self.data["Bread"][-2]
            sausage_change = self.data["Sausage"][-1] / self.data["Sausage"][-2]
            menu_dash_change = self.data["MenuDash"][-1] / self.data["MenuDash"][-2]

            avg_change = (bread_change + sausage_change + menu_dash_change) / 3
            
            sausage_sizzle_change = self.data["Sausage Sizzle"][-1] / self.data["Sausage Sizzle"][-2]
            if sausage_sizzle_change > avg_change:
                desiredPositions["Sausage Sizzle"] = -positionLimits["Sausage Sizzle"]
            else:
                desiredPositions["Sausage Sizzle"] = positionLimits["Sausage Sizzle"]

            # Sausage Sizzle Component Trading (i.e. Bread, Sausage, MenuDash)
            if bread_change > sausage_sizzle_change + SIZZLE_SAFETY_MARGIN:
                desiredPositions["Bread"] = -positionLimits["Bread"]
            elif bread_change < sausage_sizzle_change - SIZZLE_SAFETY_MARGIN:
                desiredPositions["Bread"] = positionLimits["Bread"]

            if sausage_change > sausage_sizzle_change + SIZZLE_SAFETY_MARGIN:
                desiredPositions["Sausage"] = -positionLimits["Sausage"]
            elif sausage_change < sausage_sizzle_change - SIZZLE_SAFETY_MARGIN:
                desiredPositions["Sausage"] = positionLimits["Sausage"]

            if menu_dash_change > sausage_sizzle_change + SIZZLE_SAFETY_MARGIN:
                desiredPositions["MenuDash"] = -positionLimits["MenuDash"]
            elif menu_dash_change < sausage_sizzle_change - SIZZLE_SAFETY_MARGIN:
                desiredPositions["MenuDash"] = positionLimits["MenuDash"]

        # Boat Party Ticket Trading
        if self.day % 365 <= 30:
            desiredPositions["Boat Party Ticket"] = positionLimits["Boat Party Ticket"]
        elif 30 < self.day % 365 <= 130:
            desiredPositions["Boat Party Ticket"] = -positionLimits["Boat Party Ticket"]
        elif 130 < self.day % 365 <= 190:
            desiredPositions["Boat Party Ticket"] = positionLimits["Boat Party Ticket"]
        elif 190 < self.day % 365 <= 300:
            desiredPositions["Boat Party Ticket"] = -positionLimits["Boat Party Ticket"]
        elif 300 < self.day % 365:
            desiredPositions["Boat Party Ticket"] = positionLimits["Boat Party Ticket"]
                                
                    
        # Display the end of trading day
        print("Ending Algorithm for Day:", self.day, "\n")
        #######################################################################
        # Return the desired positions
        return desiredPositions
