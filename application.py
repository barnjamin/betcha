from typing import Final
from pyteal import *
from beaker import *

class BetDetails(abi.Namedtuple):
    title: abi.Field[abi.StaticBytes[32]]
    description: abi.Field[abi.StaticBytes[64]]
    odds: abi.Field[abi.Uint16]

class Wager(Application):
    bet_id: Final[ApplicationStateValue] = ApplicationStateValue(TealType.uint64)
    title: Final[ApplicationStateValue] = ApplicationStateValue(TealType.bytes)
    description: Final[ApplicationStateValue] = ApplicationStateValue(TealType.bytes)
    odds: Final[ApplicationStateValue] = ApplicationStateValue(TealType.uint64)

    creator: Final[ApplicationStateValue] = ApplicationStateValue(TealType.bytes)
    bettor: Final[ApplicationStateValue] = ApplicationStateValue(TealType.bytes)

    @create
    def create(self, bet: BetDetails, creator: abi.Address, bettor: abi.Address):
        return Seq(
            self.creator.set(creator),
            self.creator.set(bettor),
            self.title.set(bet.title),
            self.description.set(bet.description),
            self.odds.set(bet.odds)
        )



class Betcha(Application):

    #: Holds all the bets that are live
    live_bets: DynamicApplicationStateValue = DynamicApplicationStateValue(TealType.bytes, 64, key_gen=lambda x: Itob(x))

    min_bet: Int = 1*consts.Algo

    wager_app: Wager = Wager()


    @internal(TealType.uint64)
    def create_bet_app(self, bet: BetDetails):
        return Seq(
            InnerTxnBuilder.ExecuteMethodCall(
                app_id=Int(0), 
                method_signature=get_method_spec(Wager.create).get_signature(),
                args=[bet],
            ),
            InnerTxn.application_id()
        )


    @external(authorize=Authorize.only(Global.creator_address()))
    def create_bet(self, bet: BetDetails):
        return Seq(
            (appId := ScratchVar()).store(self.create_bet_app()),
            self.live_bets[appId.load()].set(bet.encode())
        )

    @external(authorize=Authorize.only(Global.creator_address()))
    def close_bet(self, id: abi.Uint64):
        # TODO: make sure its not outstanding
        return self.live_bets[id.get()].delete()

    @external
    def place_bet(self, deposit: abi.PaymentTransaction, id: abi.Uint64):
        return Seq(
            Assert(
                deposit.get().type_enum() == TxnType.Payment,
                deposit.get().receiver() == self.address,
                deposit.get().sender() == Txn.sender(),
                deposit.get().amount() > self.min_bet,
            ),
            # reserve the amount for this bet
            # 
        )

    @external
    def claim_bet(self, id: abi.Uint64):
        return Seq(
            # reserve the amount for this bet
            # 
        )