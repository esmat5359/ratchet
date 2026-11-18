# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""PayoutProbe: a 20-line diagnostic contract (GenVM v0.2.16).

It answers one question about the network, nothing else: when a contract emits a plain
value transfer to an externally owned account, which delivery mode does the network
actually honour and credit? (`on="accepted"` or `on="finalized"`.)
"""
from genlayer import *


class PayoutProbe(gl.Contract):
    paid: u256

    def __init__(self) -> None:
        self.paid = u256(0)

    @gl.public.write.payable
    def fund(self) -> None:
        pass

    @gl.public.write
    def pay(self, to: str, amount: int, on: str) -> None:
        if on not in ("accepted", "finalized"):
            raise gl.vm.UserError("on must be accepted or finalized")
        self.paid = u256(int(self.paid) + int(amount))
        gl.get_contract_at(Address(to)).emit_transfer(value=u256(int(amount)), on=on)

    @gl.public.view
    def held(self) -> str:
        return str(int(self.balance))
