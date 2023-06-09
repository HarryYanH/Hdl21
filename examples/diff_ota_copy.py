""" 
# Fully Differential OTA Example 

Highlights the capacity to use `Diff` signals and `Pair`s of instances 
for differential circuits. 

"""

import sys
from copy import deepcopy
import hdl21 as h


""" 
Create a small "PDK" consisting of an externally-defined Nmos and Pmos transistor. 
Real versions will have some more parameters; these just have multiplier "m". 
"""


@h.paramclass
class MosParams:
    m = h.Param(dtype=int, desc="Transistor Multiplier")


nmos = h.ExternalModule(
    name="nmos",
    desc="Nmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=MosParams,
)
pmos = h.ExternalModule(
    name="pmos",
    desc="Pmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=MosParams,
)


@h.generator
def DiffOta(_: h.HasNoParams) -> h.Module:
    """# Fully Differential OTA
    With input-stage common-mode feedback."""

    @h.module
    class DiffOta:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        out = h.Diff(desc="Differential Output", port=True, role=h.Diff.Roles.SOURCE)
        vg, ibias = 2 * h.Input()

        # Internal Signals
        net1, net2, net3, net4, net5, net6, net7 = h.Signals(7)
        cm = h.Signal()

        # Input Stage & CMFB Bias
        mp1 = pmos(m=1)(d=net4, g=net4, s=VDD, b=VDD)
        mp2 = pmos(m=1)(d=net5, g=net4, s=VDD, b=VDD)
        mn1 = pmos(m=1)(d=net4, g=net1, s=net3, b=net3)
        mn2 = pmos(m=1)(d=net5, g=net1, s=net3, b=net3)
        mn3 = pmos(m=1)(d=net3, g=net7, s=VSS, b=VSS)

        # Output Stage
        mp3 = pmos(m=1)(d=net6, g=net5, s=VDD, b=VDD)
        mn5 = nmos(m=1)(d = net6, g = net7, s = VSS, b = VSS)
        CL = h.Cap(c=1e-11)(p = net6, n = VSS)

        # Biasing
        mn4 = nmos(m = 1)(d = net7, g = net7, s = VSS, b = VSS)
        isource = h.Isrc(dc = 3e-5)(p = net7, n = VDD)

        out.p=net6
        out.n=VSS

        # xndiode = nmos(m=1)(d=ibias, g=ibias, s=VSS, b=VSS)
        # xnsrc = nmos(m=1)(d=pbias, g=ibias, s=VSS, b=VSS)
        # xpdiode = pmos(m=6)(d=pbias, g=pbias, s=VDD, b=VDD)

        # Compensation Network
        Cc = h.Cap(c = 3e-12)(p = net5, n = net6)

    return DiffOta


@h.module
class CapCell:
    """# Compensation Capacitor Cell"""

    p, n, VDD, VSS = 4 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class ResCell:
    """# Compensation Resistor Cell"""

    p, n, sub = 3 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class Compensation:
    """# Single Ended RC Compensation Network"""

    a, b, VDD, VSS = 4 * h.Port()
    r = ResCell(p=a, sub=VDD)
    c = CapCell(p=r.n, n=b, VDD=VDD, VSS=VSS)


def main():
    h.netlist(DiffOta(), sys.stdout)


if __name__ == "__main__":
    main()
