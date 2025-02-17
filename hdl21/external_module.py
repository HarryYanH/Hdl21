"""
# External Module

Wrapper for circuits defined outside Hdl21. 
"""

from typing import Any, Optional, List, Type, Dict
from pydantic.dataclasses import dataclass

# VLSIR Imports
from vlsirtools import SpiceType

# Local imports
from .default import Default
from .call import param_call
from .source_info import source_info, SourceInfo
from .params import HasNoParams, isparamclass, _unique_name
from .signal import Signal, Visibility
from .instance import calls_instantiate
from .qualname import qualname_magic_methods


@dataclass
@qualname_magic_methods
class ExternalModule:
    """
    # External Module

    Wrapper for circuits defined outside Hdl21, such as:
    * Inclusion of existing SPICE or Verilog netlists
    * Foundry or technology-specific primitives

    Unlike `Modules`, `ExternalModules` include parameters to support legacy HDLs.
    Said parameters may only take on a limited number of datatypes, and may not be nested.
    Each `ExternalModule` stores a parameter-type field `paramtype`.
    Parameter types may be either `hdl21.paramclass`es or the built-in `dict`.
    Parameter-values are checked to be instances of `paramtype` at creation time.
    """

    name: str  # Module name. Used *directly* when exporting.
    port_list: List[Signal]  # Ordered Ports
    paramtype: Type = HasNoParams  # Parameter-type `paramclass`
    desc: Optional[str] = None  # Description
    domain: Optional[str] = None  # Domain name, for references upon export
    spicetype: SpiceType = SpiceType.SUBCKT  # Spice type, for SPICE export

    @property
    def ports(self) -> dict:
        """Port dictionary, from name to `Signal`."""
        return {p.name: p for p in self.port_list}

    @property
    def Params(self) -> Type:
        """Type-style alias for the parameter-type."""
        return self.paramtype

    def __post_init__(self):
        # Check for a valid parameter-type
        if not isparamclass(self.paramtype) and self.paramtype not in (dict, Dict):
            msg = f"Invalid parameter type {self.paramtype} for {self}. "
            msg += "Param types must be either `@paramclass`es or `dict`."
            raise ValueError(msg)

        # Internal tracking data: defining module/import-path
        self._source_info: Optional[SourceInfo] = source_info(get_pymodule=True)
        self._importpath = None

    def __post_init_post_parse__(self):
        """After type-checking, do some more checks on values"""
        for p in self.port_list:
            if not p.name:
                raise ValueError(f"Unnamed Primitive Port {p} for {self.name}")
            if p.vis != Visibility.PORT:
                msg = f"Invalid Primitive Port {p.name} on {self.name}; must have PORT visibility"
                raise ValueError(msg)

    def __call__(self, arg: Any = Default, **kwargs) -> "ExternalModuleCall":
        """Call to set an `ExternalModule`'s parameters.
        Returns an `ExternalModuleCall` combining the `ExternalModule` and parameter values.
        """
        params = param_call(callee=self, arg=arg, **kwargs)
        return ExternalModuleCall(module=self, params=params)

    def __eq__(self, other) -> bool:
        # Identity is equality
        return other is self

    def __hash__(self) -> bool:
        # Identity is equality
        return hash(id(self))


@calls_instantiate
@dataclass
class ExternalModuleCall:
    """# External Module Call
    A combination of an `ExternalModule` and its Parameter-values, typically generated by calling the `ExternalModule`.
    """

    module: ExternalModule
    params: Any

    def __post_init_post_parse__(self):
        # Type-validate our parameters
        if not isinstance(self.params, self.module.paramtype):
            msg = f"Invalid parameter type {type(self.params)} for ExternalModule {self.module.name}. Must be {self.module.paramtype}"
            raise TypeError(msg)

    @property
    def name(self) -> str:
        return self.module.name + "(" + _unique_name(self.params) + ")"

    @property
    def ports(self) -> Dict[str, Signal]:
        return self.module.ports

    def __eq__(self, other) -> bool:
        """Call equality requires:
        * *Identity* between modules, and
        * *Equality* between parameter-values."""
        return self.module is other.module and self.params == other.params

    def __hash__(self):
        """Generator-Call hashing, consistent with `__eq__` above, uses:
        * *Identity* of its module, and
        * *Value* of its parameters.
        The two are joined for hashing as a two-element tuple."""
        return hash((id(self.module), self.params))


__all__ = ["ExternalModule", "ExternalModuleCall"]
