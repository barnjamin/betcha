Betcha
======


An account creates a Betcha app

This account can create new wagers with some details including title, description, and odds 

Users view outstanding wagers in some browser that looks at the current Application state of the Betcha App 

Users select a wager and send a deposit with an app call
On Settlement, the payout is sent to the winning party account.  To settle a wager, both the Bettor and app creator need to agree on the outcome 

App create

Bet create  (only from creator)
    Assign Seq id and place new bet in global state

Bet destroy (only from creator, only if no bets outstanding)
    Delete seq from global state IFF it has no outstanding bets

Wager create (only from bettor)
    Create Wager app with bettor && creator && bet details

Wager settlement

    -No Oracle: (needed from both bettor and creator)
        Transactions tracked with settlement on both sides  
        Initial state is claim from both parties
        Changing one to match the other allows settlement to the other party

    - Oracle: (only needed from oracle source)
        Oracle Source updates with data
        data evaluated to choose winner

    Settlement Types: to bettor | to creator | draw/cancel 

App delete (only if no bets outstanding)