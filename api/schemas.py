"""Raw-input and response contracts for the API."""
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, FiniteFloat

class ClienteInput(BaseModel):
    """Required raw feature keys, with nulls delegated to train-fitted imputers.

    Financial balances can be signed, as in the source dataset. A null field
    differs from an absent field. IDs, campaign metadata, target and manually
    transformed columns are intentionally not accepted by this endpoint.
    """

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, strict=True)
    LINEA_RENOVADO: FiniteFloat | None
    PLAZO_RENOVADO: FiniteFloat | None
    USO_LINEA_TOTAL_TC_T2: FiniteFloat | None
    USO_TRIM_LINEA_BBVA: FiniteFloat | None
    NR_ENTIDADES_TOTAL_T2: FiniteFloat | None
    DIFF_NRO_ENTIDA_TOTALES_T2_T12: FiniteFloat | None
    SDO_CONSUMO_T2: FiniteFloat | None
    RESENCIA_OFERTA_PLD_RENOVADO: FiniteFloat | None
    Ahorro_Sldo_Bco_T1: FiniteFloat | None
    PConsumo_Sldo_Bco_T1: FiniteFloat | None
    SDO_BCO_tot_sm_pasivo_Bco_6M: FiniteFloat | None
    EDAD: FiniteFloat | None
    ANTIGUEDAD_MES: FiniteFloat | None
    FLAG_LIMA_PROVINCIA: FiniteFloat | None
    SUELDO_ESTIMADO: FiniteFloat | None
    CUBRIR_DEUDA_CONSUMO_SF_RENOVA_PLD: FiniteFloat | None
    SEXO: str | None
    EST_CIVIL: str | None
    REGION: str | None


class PrediccionOutput(BaseModel):
    """A score and saved decision threshold for a commercial renewal label."""

    score_propension: Annotated[FiniteFloat, Field(ge=0, le=1)]
    flag_venta: Literal[0, 1]
    umbral: Annotated[FiniteFloat, Field(ge=0, le=1)]
    modelo: str
