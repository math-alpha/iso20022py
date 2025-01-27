from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Namespace for pain.008.001.02
PAIN_008_NAMESPACE = "urn:iso:std:iso:20022:tech:xsd:pain.008.001.02"


class AuthstnCD(Enum):
    AUTH = "AUTH"
    FDET = "FDET"
    FSUM = "FSUM"
    ILEV = "ILEV"


@dataclass
class AuthstnElement:
    Cd: AuthstnCD
    Prtry: str


class AdrTp(Enum):
    ADDR = "ADDR"
    BIZZ = "BIZZ"
    DLVY = "DLVY"
    HOME = "HOME"
    MLTO = "MLTO"
    PBOX = "PBOX"


@dataclass
class PstlAdr:
    AdrLine: Optional[List[str]] = None
    AdrTp: Optional[AdrTp] = None
    BldgNb: Optional[str] = None
    Ctry: Optional[str] = None
    CtrySubDvsn: Optional[str] = None
    Dept: Optional[str] = None
    PstCd: Optional[str] = None
    StrtNm: Optional[str] = None
    SubDept: Optional[str] = None
    TwnNm: Optional[str] = None


@dataclass
class BrnchID:
    Id: Optional[str] = None
    Nm: Optional[str] = None
    PstlAdr: Optional[PstlAdr] = None


@dataclass
class CLRSysID:
    Cd: str
    Prtry: str


@dataclass
class CLRSysMmbID:
    MmbId: str
    ClrSysId: Optional[CLRSysID] = None


@dataclass
class PurpleSchmeNm:
    Cd: str
    Prtry: str


@dataclass
class FinInstnIDOthr:
    Id: str
    Issr: Optional[str] = None
    SchmeNm: Optional[PurpleSchmeNm] = None


@dataclass
class FinInstnID:
    BIC: Optional[str] = None
    ClrSysMmbId: Optional[CLRSysMmbID] = None
    Nm: Optional[str] = None
    Othr: Optional[FinInstnIDOthr] = None
    PstlAdr: Optional[PstlAdr] = None


@dataclass
class FwdgAgt:
    FinInstnId: FinInstnID
    BrnchId: Optional[BrnchID] = None


class NmPrfx(Enum):
    DOCT = "DOCT"
    MADM = "MADM"
    MISS = "MISS"
    MIST = "MIST"


@dataclass
class CtctDtls:
    EmailAdr: Optional[str] = None
    FaxNb: Optional[str] = None
    MobNb: Optional[str] = None
    Nm: Optional[str] = None
    NmPrfx: Optional[NmPrfx] = None
    Othr: Optional[str] = None
    PhneNb: Optional[str] = None


@dataclass
class FluffySchmeNm:
    Cd: str
    Prtry: str


@dataclass
class OrgIDOthr:
    Id: str
    Issr: Optional[str] = None
    SchmeNm: Optional[FluffySchmeNm] = None


@dataclass
class OrgID:
    BICOrBEI: Optional[str] = None
    Othr: Optional[List[OrgIDOthr]] = None


@dataclass
class DtAndPLCOfBirth:
    BirthDt: datetime
    CityOfBirth: str
    CtryOfBirth: str
    PrvcOfBirth: Optional[str] = None


@dataclass
class TentacledSchmeNm:
    Cd: str
    Prtry: str


@dataclass
class PrvtIDOthr:
    Id: str
    Issr: Optional[str] = None
    SchmeNm: Optional[TentacledSchmeNm] = None


@dataclass
class PrvtID:
    DtAndPlcOfBirth: Optional[DtAndPLCOfBirth] = None
    Othr: Optional[List[PrvtIDOthr]] = None


@dataclass
class InitgPtyID:
    OrgId: OrgID
    PrvtId: PrvtID


@dataclass
class InitgPty:
    CtctDtls: Optional[CtctDtls] = None
    CtryOfRes: Optional[str] = None
    Id: Optional[InitgPtyID] = None
    Nm: Optional[str] = None
    PstlAdr: Optional[PstlAdr] = None


@dataclass
class GrpHdr:
    CreDtTm: datetime
    InitgPty: InitgPty
    MsgId: str
    NbOfTxs: str
    Authstn: Optional[List[AuthstnElement]] = None
    CtrlSum: Optional[float] = None
    FwdgAgt: Optional[FwdgAgt] = None


@dataclass
class StickySchmeNm:
    Cd: str
    Prtry: str


@dataclass
class IDOthr:
    Id: str
    Issr: Optional[str] = None
    SchmeNm: Optional[StickySchmeNm] = None


@dataclass
class CdtrAcctID:
    IBAN: str
    Othr: IDOthr


class TpCD(Enum):
    CACC = "CACC"
    CASH = "CASH"
    CHAR = "CHAR"
    CISH = "CISH"
    COMM = "COMM"
    LOAN = "LOAN"
    MGLD = "MGLD"
    MOMA = "MOMA"
    NREX = "NREX"
    ODFT = "ODFT"
    ONDP = "ONDP"
    SACC = "SACC"
    SLRY = "SLRY"
    SVGS = "SVGS"
    TAXE = "TAXE"
    TRAS = "TRAS"


@dataclass
class CdtrAcctTp:
    Cd: TpCD
    Prtry: str


@dataclass
class CdtrAcct:
    Id: CdtrAcctID
    Ccy: Optional[str] = None
    Nm: Optional[str] = None
    Tp: Optional[CdtrAcctTp] = None


class ChrgBr(Enum):
    CRED = "CRED"
    DEBT = "DEBT"
    SHAR = "SHAR"
    SLEV = "SLEV"


class OrgnlFrqcy(Enum):
    ADHO = "ADHO"
    DAIL = "DAIL"
    INDA = "INDA"
    MIAN = "MIAN"
    MNTH = "MNTH"
    QURT = "QURT"
    WEEK = "WEEK"
    YEAR = "YEAR"


@dataclass
class AmdmntInfDtls:
    OrgnlCdtrAgt: Optional[FwdgAgt] = None
    OrgnlCdtrAgtAcct: Optional[CdtrAcct] = None
    OrgnlCdtrSchmeId: Optional[InitgPty] = None
    OrgnlDbtr: Optional[InitgPty] = None
    OrgnlDbtrAcct: Optional[CdtrAcct] = None
    OrgnlDbtrAgt: Optional[FwdgAgt] = None
    OrgnlDbtrAgtAcct: Optional[CdtrAcct] = None
    OrgnlFnlColltnDt: Optional[datetime] = None
    OrgnlFrqcy: Optional[OrgnlFrqcy] = None
    OrgnlMndtId: Optional[str] = None


@dataclass
class MndtRltdInf:
    AmdmntInd: Optional[bool] = None
    AmdmntInfDtls: Optional[AmdmntInfDtls] = None
    DtOfSgntr: Optional[datetime] = None
    ElctrncSgntr: Optional[str] = None
    FnlColltnDt: Optional[datetime] = None
    Frqcy: Optional[OrgnlFrqcy] = None
    FrstColltnDt: Optional[datetime] = None
    MndtId: Optional[str] = None


@dataclass
class DrctDbtTx:
    CdtrSchmeId: Optional[InitgPty] = None
    MndtRltdInf: Optional[MndtRltdInf] = None
    PreNtfctnDt: Optional[datetime] = None
    PreNtfctnId: Optional[str] = None


@dataclass
class InstdAmt:
    Ccy: str
    Value: Optional[float] = None


@dataclass
class PmtID:
    EndToEndId: str
    InstrId: Optional[str] = None


@dataclass
class CtgyPurp:
    Cd: str
    Prtry: str


class InstrPrty(Enum):
    HIGH = "HIGH"
    NORM = "NORM"


@dataclass
class LclInstrm:
    Cd: str
    Prtry: str


class SeqTp(Enum):
    FNAL = "FNAL"
    FRST = "FRST"
    OOFF = "OOFF"
    RCUR = "RCUR"


@dataclass
class SVCLvl:
    Cd: str
    Prtry: str


@dataclass
class PmtTpInf:
    CtgyPurp: Optional[CtgyPurp] = None
    InstrPrty: Optional[InstrPrty] = None
    LclInstrm: Optional[LclInstrm] = None
    SeqTp: Optional[SeqTp] = None
    SvcLvl: Optional[SVCLvl] = None


@dataclass
class Purp:
    Cd: str
    Prtry: str


@dataclass
class Authrty:
    Ctry: Optional[str] = None
    Nm: Optional[str] = None


class DbtCdtRptgInd(Enum):
    BOTH = "BOTH"
    CRED = "CRED"
    DEBT = "DEBT"


@dataclass
class RgltryRptgDtl:
    Amt: Optional[InstdAmt] = None
    Cd: Optional[str] = None
    Ctry: Optional[str] = None
    Dt: Optional[datetime] = None
    Inf: Optional[List[str]] = None
    Tp: Optional[str] = None


@dataclass
class RgltryRptgElement:
    Authrty: Optional[Authrty] = None
    DbtCdtRptgInd: Optional[DbtCdtRptgInd] = None
    Dtls: Optional[List[RgltryRptgDtl]] = None


class RmtLctnMtd(Enum):
    EDIC = "EDIC"
    EMAL = "EMAL"
    FAXI = "FAXI"
    POST = "POST"
    SMSM = "SMSM"
    URID = "URID"


@dataclass
class RmtLctnPstlAdr:
    Adr: PstlAdr
    Nm: str


@dataclass
class RltdRmtInfElement:
    RmtId: Optional[str] = None
    RmtLctnElctrncAdr: Optional[str] = None
    RmtLctnMtd: Optional[RmtLctnMtd] = None
    RmtLctnPstlAdr: Optional[RmtLctnPstlAdr] = None


class PurpleCD(Enum):
    DISP = "DISP"
    FXDR = "FXDR"
    PUOR = "PUOR"
    RADM = "RADM"
    RPIN = "RPIN"
    SCOR = "SCOR"


@dataclass
class PurpleCDOrPrtry:
    Cd: PurpleCD
    Prtry: str


@dataclass
class CdtrRefInfTp:
    CdOrPrtry: PurpleCDOrPrtry
    Issr: Optional[str] = None


@dataclass
class CdtrRefInf:
    Ref: Optional[str] = None
    Tp: Optional[CdtrRefInfTp] = None


class CdtDbtInd(Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"


@dataclass
class AdjstmntAmtAndRsnElement:
    Amt: InstdAmt
    AddtlInf: Optional[str] = None
    CdtDbtInd: Optional[CdtDbtInd] = None
    Rsn: Optional[str] = None


@dataclass
class RfrdDocAmt:
    AdjstmntAmtAndRsn: Optional[List[AdjstmntAmtAndRsnElement]] = None
    CdtNoteAmt: Optional[InstdAmt] = None
    DscntApldAmt: Optional[InstdAmt] = None
    DuePyblAmt: Optional[InstdAmt] = None
    RmtdAmt: Optional[InstdAmt] = None
    TaxAmt: Optional[InstdAmt] = None


class FluffyCD(Enum):
    AROI = "AROI"
    BOLD = "BOLD"
    CINV = "CINV"
    CMCN = "CMCN"
    CNFA = "CNFA"
    CREN = "CREN"
    DEBN = "DEBN"
    DISP = "DISP"
    DNFA = "DNFA"
    HIRI = "HIRI"
    MSIN = "MSIN"
    SBIN = "SBIN"
    SOAC = "SOAC"
    TSUT = "TSUT"
    VCHR = "VCHR"


@dataclass
class FluffyCDOrPrtry:
    Cd: FluffyCD
    Prtry: str


@dataclass
class RfrdDocInfTp:
    CdOrPrtry: FluffyCDOrPrtry
    Issr: Optional[str] = None


@dataclass
class RfrdDocInfElement:
    Nb: Optional[str] = None
    RltdDt: Optional[datetime] = None
    Tp: Optional[RfrdDocInfTp] = None


@dataclass
class StrdElement:
    AddtlRmtInf: Optional[List[str]] = None
    CdtrRefInf: Optional[CdtrRefInf] = None
    Invcee: Optional[InitgPty] = None
    Invcr: Optional[InitgPty] = None
    RfrdDocAmt: Optional[RfrdDocAmt] = None
    RfrdDocInf: Optional[List[RfrdDocInfElement]] = None


@dataclass
class RmtInf:
    Strd: Optional[List[StrdElement]] = None
    Ustrd: Optional[List[str]] = None


@dataclass
class Cdtr:
    RegnId: Optional[str] = None
    TaxId: Optional[str] = None
    TaxTp: Optional[str] = None


@dataclass
class Authstn:
    Nm: Optional[str] = None
    Titl: Optional[str] = None


@dataclass
class Dbtr:
    Authstn: Optional[Authstn] = None
    RegnId: Optional[str] = None
    TaxId: Optional[str] = None
    TaxTp: Optional[str] = None


@dataclass
class FrToDt:
    FrDt: datetime
    ToDt: datetime


class TpEnum(Enum):
    HLF1 = "HLF1"
    HLF2 = "HLF2"
    MM01 = "MM01"
    MM02 = "MM02"
    MM03 = "MM03"
    MM04 = "MM04"
    MM05 = "MM05"
    MM06 = "MM06"
    MM07 = "MM07"
    MM08 = "MM08"
    MM09 = "MM09"
    MM10 = "MM10"
    MM11 = "MM11"
    MM12 = "MM12"
    QTR1 = "QTR1"
    QTR2 = "QTR2"
    QTR3 = "QTR3"
    QTR4 = "QTR4"


@dataclass
class Prd:
    FrToDt: Optional[FrToDt] = None
    Tp: Optional[TpEnum] = None
    Yr: Optional[datetime] = None


@dataclass
class TaxAmtDtl:
    Amt: InstdAmt
    Prd: Optional[Prd] = None


@dataclass
class TaxAmt:
    Dtls: Optional[List[TaxAmtDtl]] = None
    Rate: Optional[float] = None
    TaxblBaseAmt: Optional[InstdAmt] = None
    TtlAmt: Optional[InstdAmt] = None


@dataclass
class RcrdElement:
    AddtlInf: Optional[str] = None
    CertId: Optional[str] = None
    Ctgy: Optional[str] = None
    CtgyDtls: Optional[str] = None
    DbtrSts: Optional[str] = None
    FrmsCd: Optional[str] = None
    Prd: Optional[Prd] = None
    TaxAmt: Optional[TaxAmt] = None
    Tp: Optional[str] = None


@dataclass
class Tax:
    AdmstnZn: Optional[str] = None
    Cdtr: Optional[Cdtr] = None
    Dbtr: Optional[Dbtr] = None
    Dt: Optional[datetime] = None
    Mtd: Optional[str] = None
    Rcrd: Optional[List[RcrdElement]] = None
    RefNb: Optional[str] = None
    SeqNb: Optional[float] = None
    TtlTaxAmt: Optional[InstdAmt] = None
    TtlTaxblBaseAmt: Optional[InstdAmt] = None


@dataclass
class DrctDbtTxInfElement:
    Dbtr: InitgPty
    DbtrAcct: CdtrAcct
    DbtrAgt: FwdgAgt
    InstdAmt: InstdAmt
    PmtId: PmtID
    ChrgBr: Optional[ChrgBr] = None
    DbtrAgtAcct: Optional[CdtrAcct] = None
    DrctDbtTx: Optional[DrctDbtTx] = None
    InstrForCdtrAgt: Optional[str] = None
    PmtTpInf: Optional[PmtTpInf] = None
    Purp: Optional[Purp] = None
    RgltryRptg: Optional[List[RgltryRptgElement]] = None
    RltdRmtInf: Optional[List[RltdRmtInfElement]] = None
    RmtInf: Optional[RmtInf] = None
    Tax: Optional[Tax] = None
    UltmtCdtr: Optional[InitgPty] = None
    UltmtDbtr: Optional[InitgPty] = None


class PmtMtd(Enum):
    DD = "DD"


@dataclass
class PmtInfElement:
    Cdtr: InitgPty
    CdtrAcct: CdtrAcct
    CdtrAgt: FwdgAgt
    DrctDbtTxInf: List[DrctDbtTxInfElement]
    PmtInfId: str
    PmtMtd: PmtMtd
    ReqdColltnDt: datetime
    BtchBookg: Optional[bool] = None
    CdtrAgtAcct: Optional[CdtrAcct] = None
    CdtrSchmeId: Optional[InitgPty] = None
    ChrgBr: Optional[ChrgBr] = None
    ChrgsAcct: Optional[CdtrAcct] = None
    ChrgsAcctAgt: Optional[FwdgAgt] = None
    CtrlSum: Optional[float] = None
    NbOfTxs: Optional[str] = None
    PmtTpInf: Optional[PmtTpInf] = None
    UltmtCdtr: Optional[InitgPty] = None


@dataclass
class CstmrDrctDbtInitn:
    GrpHdr: GrpHdr
    PmtInf: List[PmtInfElement]


@dataclass
class Document:
    CstmrDrctDbtInitn: CstmrDrctDbtInitn


class PaymentMethodCode(Enum):
    DD = "DD"  # Direct Debit


class ServiceLevelCode(Enum):
    SEPA = "SEPA"


class ChargeBearerCode(Enum):
    SLEV = "SLEV"


class SequenceTypeCode(Enum):
    FRST = "FRST"
    RCUR = "RCUR"
    FNAL = "FNAL"
    OOFF = "OOFF"


class PaymentInstruction:
    def __init__(self, pmt_inf_id, reqd_colltn_dt, cdtr_nm, cdtr_acct_iban, cdtr_agt_bic, drct_dbt_tx_inf):
        self.PmtInfId = pmt_inf_id
        self.ReqdColltnDt = reqd_colltn_dt
        self.CdtrNm = cdtr_nm
        self.CdtrAcctIBAN = cdtr_acct_iban
        self.CdtrAgtBIC = cdtr_agt_bic
        self.DrctDbtTxInf = drct_dbt_tx_inf


class DirectDebitTransaction:
    def __init__(self, instd_amt, instd_amt_ccy, mndt_id, dbtr_nm, dbtr_acct_iban, dbtr_agt_bic, rmt_inf):
        self.InstdAmt = instd_amt
        self.InstdAmtCcy = instd_amt_ccy
        self.MndtId = mndt_id
        self.DbtrNm = dbtr_nm
        self.DbtrAcctIBAN = dbtr_acct_iban
        self.DbtrAgtBIC = dbtr_agt_bic
        self.RmtInf = rmt_inf


class Pain00800102Class:
    Document: Optional[Document] = None

    def __init__(self, doc: Optional[Document] = None):  # Allow doc to be optional
        self.root = None
        if doc:
            self.Document = doc
        else:
            self.create_empty_document()

    def add_payment_instruction(self, payment_instruction: PmtInfElement):
        if self.Document and self.Document.CstmrDrctDbtInitn:
            self.Document.CstmrDrctDbtInitn.PmtInf.append(payment_instruction)

    def get_payment_instructions(self) -> List[PmtInfElement]:
        if self.Document and self.Document.CstmrDrctDbtInitn:
            return self.Document.CstmrDrctDbtInitn.PmtInf
        return []

    def add_group_header(self, group_header: GrpHdr):
        if self.Document:
            self.Document.CstmrDrctDbtInitn.GrpHdr = group_header

    def get_group_header(self) -> Optional[GrpHdr]:
        if self.Document and self.Document.CstmrDrctDbtInitn:
            return self.Document.CstmrDrctDbtInitn.GrpHdr
        return None

    def get_document(self) -> Optional[Document]:
        return self.Document

    def create_empty_document(self):
        """Creates an empty pain.008.001.02 document structure."""
        ET.register_namespace('', PAIN_008_NAMESPACE)
        self.root = ET.Element("Document")
        self.root.attrib['xmlns'] = PAIN_008_NAMESPACE
        self.cstmr_drct_dbt_initn = ET.SubElement(self.root, "CstmrDrctDbtInitn")
        self.grp_hdr = None
        self.pmt_inf = []

    def create_message(self, grpHdr, pmtInf):
        """
        Creates a new pain.008.001.02 message.

        Args:
            grpHdr (GroupHeader): The group header information.
            pmtInf (list): List of PaymentInstruction objects.
        """
        # Use the existing root if it exists
        if self.root is None:
            ET.register_namespace('', PAIN_008_NAMESPACE)
            self.root = ET.Element("Document")
            self.root.attrib['xmlns'] = PAIN_008_NAMESPACE
            self.cstmr_drct_dbt_initn = ET.SubElement(self.root, "CstmrDrctDbtInitn")

        # Add Group Header
        self._add_group_header(self.cstmr_drct_dbt_initn, grpHdr)

        # Add Payment Information
        for pmt in pmtInf:
            self._add_payment_instruction(self.cstmr_drct_dbt_initn, pmt)

    def _add_group_header(self, parent, grpHdr):
        """Adds the GroupHeader to the XML."""
        grp_hdr = ET.SubElement(parent, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = grpHdr.MsgId
        ET.SubElement(grp_hdr, "CreDtTm").text = grpHdr.CreDtTm.isoformat()
        ET.SubElement(grp_hdr, "NbOfTxs").text = str(grpHdr.NbOfTxs)
        ET.SubElement(grp_hdr, "CtrlSum").text = str(grpHdr.CtrlSum)

        initg_pty = ET.SubElement(grp_hdr, "InitgPty")
        ET.SubElement(initg_pty, "Nm").text = grpHdr.InitgPty.Nm

        self.grp_hdr = grpHdr

    def _add_payment_instruction(self, parent, pmtInf):
        """Adds a PaymentInstruction to the XML."""
        pmt_inf = ET.SubElement(parent, "PmtInf")
        ET.SubElement(pmt_inf, "PmtInfId").text = pmtInf.PmtInfId
        ET.SubElement(pmt_inf, "PmtMtd").text = PaymentMethodCode.DD.value
        ET.SubElement(pmt_inf, "ReqdColltnDt").text = pmtInf.ReqdColltnDt.isoformat()

        cdtr = ET.SubElement(pmt_inf, "Cdtr")
        ET.SubElement(cdtr, "Nm").text = pmtInf.CdtrNm

        cdtr_acct = ET.SubElement(pmt_inf, "CdtrAcct")
        cdtr_acct_id = ET.SubElement(cdtr_acct, "Id")
        ET.SubElement(cdtr_acct_id, "IBAN").text = pmtInf.CdtrAcctIBAN

        cdtr_agt = ET.SubElement(pmt_inf, "CdtrAgt")
        cdtr_agt_fin_instn_id = ET.SubElement(cdtr_agt, "FinInstnId")
        ET.SubElement(cdtr_agt_fin_instn_id, "BIC").text = pmtInf.CdtrAgtBIC

        # Service Level - SEPA as an example

        svc_lvl_inf = ET.SubElement(pmt_inf, "PmtTpInf")  # Create PmtTpInf here
        svc_lvl = ET.SubElement(svc_lvl_inf, "SvcLvl")
        ET.SubElement(svc_lvl, "Cd").text = ServiceLevelCode.SEPA.value

        # Charge Bearer
        ET.SubElement(pmt_inf, "ChrgBr").text = ChargeBearerCode.SLEV.value

        for tx in pmtInf.DrctDbtTxInf:
            self._add_direct_debit_transaction(pmt_inf, tx, svc_lvl_inf)  # Pass PmtTpInf to the next function

        self.pmt_inf.append(pmtInf)

    def _add_direct_debit_transaction(self, parent, tx, pmt_tp_inf):  # add pmt_tp_inf
        """Adds a DirectDebitTransaction to the XML."""
        drct_dbt_tx_inf = ET.SubElement(parent, "DrctDbtTxInf")

        pmt_id = ET.SubElement(drct_dbt_tx_inf, "PmtId")
        ET.SubElement(pmt_id, "EndToEndId").text = str(uuid.uuid4())

        instd_amt = ET.SubElement(drct_dbt_tx_inf, "InstdAmt")
        instd_amt.text = str(tx.InstdAmt)
        instd_amt.set("Ccy", tx.InstdAmtCcy)

        drct_dbt_tx = ET.SubElement(drct_dbt_tx_inf, "DrctDbtTx")
        mndt_rltd_inf = ET.SubElement(drct_dbt_tx, "MndtRltdInf")
        ET.SubElement(mndt_rltd_inf, "MndtId").text = tx.MndtId
        ET.SubElement(mndt_rltd_inf, "DtOfSgntr").text = date.today().isoformat()

        dbtr_agt = ET.SubElement(drct_dbt_tx_inf, "DbtrAgt")
        dbtr_agt_fin_instn_id = ET.SubElement(dbtr_agt, "FinInstnId")
        ET.SubElement(dbtr_agt_fin_instn_id, "BIC").text = tx.DbtrAgtBIC

        dbtr = ET.SubElement(drct_dbt_tx_inf, "Dbtr")
        ET.SubElement(dbtr, "Nm").text = tx.DbtrNm

        dbtr_acct = ET.SubElement(drct_dbt_tx_inf, "DbtrAcct")
        dbtr_acct_id = ET.SubElement(dbtr_acct, "Id")
        ET.SubElement(dbtr_acct_id, "IBAN").text = tx.DbtrAcctIBAN

        rmt_inf = ET.SubElement(drct_dbt_tx_inf, "RmtInf")
        ET.SubElement(rmt_inf, "Ustrd").text = tx.RmtInf

        # Now you can add SeqTp because pmt_tp_inf exists
        ET.SubElement(pmt_tp_inf, "SeqTp").text = SequenceTypeCode.RCUR.value

    def to_xml_string(self):
        """
        Converts the current message to an XML string.

        Returns:
            str: The XML representation of the message.
        """
        if self.root is None:
            raise ValueError("Message not created. Call create_message() first.")

        xml_string = ET.tostring(self.root, encoding="utf-8")
        dom = minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")

    def parse_xml_file(self, file_path):
        """
        Parses a pain.008.001.02 XML file.

        Args:
            file_path (str): The path to the XML file.
        """
        tree = ET.parse(file_path)
        self.root = tree.getroot()

        # Extract Group Header (simplified example)
        grp_hdr_element = self.root.find(f"{{{PAIN_008_NAMESPACE}}}CstmrDrctDbtInitn/{{{PAIN_008_NAMESPACE}}}GrpHdr")
        if grp_hdr_element is not None:
            self.grpHdr = GrpHdr(
                msg_id=grp_hdr_element.find(f"{{{PAIN_008_NAMESPACE}}}MsgId").text,
                cre_dt_tm=datetime.fromisoformat(grp_hdr_element.find(f"{{{PAIN_008_NAMESPACE}}}CreDtTm").text),
                nb_of_txs=int(grp_hdr_element.find(f"{{{PAIN_008_NAMESPACE}}}NbOfTxs").text),
                ctrl_sum=Decimal(grp_hdr_element.find(f"{{{PAIN_008_NAMESPACE}}}CtrlSum").text),
                initg_pty_nm=grp_hdr_element.find(f"{{{PAIN_008_NAMESPACE}}}InitgPty/{{{PAIN_008_NAMESPACE}}}Nm").text,
            )

        # Extract Payment Instructions (simplified example)
        pmt_inf_elements = self.root.findall(
            f"{{{PAIN_008_NAMESPACE}}}CstmrDrctDbtInitn/{{{PAIN_008_NAMESPACE}}}PmtInf")
        for pmt_inf_element in pmt_inf_elements:
            drct_dbt_tx_inf = []
            drct_dbt_tx_inf_elements = pmt_inf_element.findall(f"{{{PAIN_008_NAMESPACE}}}DrctDbtTxInf")

            for drct_dbt_tx_inf_element in drct_dbt_tx_inf_elements:
                drct_dbt_tx_inf.append(DirectDebitTransaction(
                    instd_amt=Decimal(drct_dbt_tx_inf_element.find(f"{{{PAIN_008_NAMESPACE}}}InstdAmt").text),
                    instd_amt_ccy=drct_dbt_tx_inf_element.find(f"{{{PAIN_008_NAMESPACE}}}InstdAmt").get("Ccy"),
                    mndt_id=drct_dbt_tx_inf_element.find(
                        f"{{{PAIN_008_NAMESPACE}}}DrctDbtTx/{{{PAIN_008_NAMESPACE}}}MndtRltdInf/{{{PAIN_008_NAMESPACE}}}MndtId").text,
                    dbtr_nm=drct_dbt_tx_inf_element.find(
                        f"{{{PAIN_008_NAMESPACE}}}Dbtr/{{{PAIN_008_NAMESPACE}}}Nm").text,
                    dbtr_acct_iban=drct_dbt_tx_inf_element.find(
                        f"{{{PAIN_008_NAMESPACE}}}DbtrAcct/{{{PAIN_008_NAMESPACE}}}Id/{{{PAIN_008_NAMESPACE}}}IBAN").text,
                    dbtr_agt_bic=drct_dbt_tx_inf_element.find(
                        f"{{{PAIN_008_NAMESPACE}}}DbtrAgt/{{{PAIN_008_NAMESPACE}}}FinInstnId/{{{PAIN_008_NAMESPACE}}}BIC").text,
                    rmt_inf=drct_dbt_tx_inf_element.find(
                        f"{{{PAIN_008_NAMESPACE}}}RmtInf/{{{PAIN_008_NAMESPACE}}}Ustrd").text if drct_dbt_tx_inf_element.find(
                        f"{{{PAIN_008_NAMESPACE}}}RmtInf/{{{PAIN_008_NAMESPACE}}}Ustrd") is not None else None
                ))

            self.pmtInf.append(PaymentInstruction(
                pmt_inf_id=pmt_inf_element.find(f"{{{PAIN_008_NAMESPACE}}}PmtInfId").text,
                reqd_colltn_dt=date.fromisoformat(pmt_inf_element.find(f"{{{PAIN_008_NAMESPACE}}}ReqdColltnDt").text),
                cdtr_nm=pmt_inf_element.find(f"{{{PAIN_008_NAMESPACE}}}Cdtr/{{{PAIN_008_NAMESPACE}}}Nm").text,
                cdtr_acct_iban=pmt_inf_element.find(
                    f"{{{PAIN_008_NAMESPACE}}}CdtrAcct/{{{PAIN_008_NAMESPACE}}}Id/{{{PAIN_008_NAMESPACE}}}IBAN").text,
                cdtr_agt_bic=pmt_inf_element.find(
                    f"{{{PAIN_008_NAMESPACE}}}CdtrAgt/{{{PAIN_008_NAMESPACE}}}FinInstnId/{{{PAIN_008_NAMESPACE}}}BIC").text,
                drct_dbt_tx_inf=drct_dbt_tx_inf
            ))

    def get_transactions_by_debtor(self, debtor_iban):
        """
        Retrieves all transactions associated with a specific debtor IBAN.

        Args:
            debtor_iban (str): The IBAN of the debtor.

        Returns:
            list: A list of DirectDebitTransaction objects for the debtor, or an empty list if none are found.
        """
        transactions = []
        for pmt_instruction in self.pmt_inf:
            for transaction in pmt_instruction.DrctDbtTxInf:
                if transaction.DbtrAcctIBAN == debtor_iban:
                    transactions.append(transaction)
        return transactions

    def get_total_transaction_amount(self):
        """
        Calculates the total amount of all transactions in the message.

        Returns:
            Decimal: The total transaction amount.
        """
        total_amount = Decimal(0)
        for pmt_instruction in self.pmt_inf:
            for transaction in pmt_instruction.DrctDbtTxInf:
                total_amount += Decimal(transaction.InstdAmt)
        return total_amount

    def update_transaction_remittance_info(self, pmt_inf_id, end_to_end_id, new_remittance_info):
        """
        Updates the remittance information for a specific transaction.

        Args:
            pmt_inf_id (str): The PmtInfId of the payment instruction containing the transaction.
            end_to_end_id (str): The EndToEndId of the transaction to update.
            new_remittance_info (str): The new remittance information.
        """
        # Construct the XPath expression to find the specific transaction
        xpath_expr = f".//{{{PAIN_008_NAMESPACE}}}PmtInf" \
                     f"[@PmtInfId='{pmt_inf_id}']/" \
                     f"{{{PAIN_008_NAMESPACE}}}DrctDbtTxInf" \
                     f"[PmtId/EndToEndId='{end_to_end_id}']/" \
                     f"{{{PAIN_008_NAMESPACE}}}RmtInf/{{{PAIN_008_NAMESPACE}}}Ustrd"

        # Find the Ustrd element that needs to be updated
        ustrd_element = self.root.find(xpath_expr)

        if ustrd_element is not None:
            # Update the text of the Ustrd element with the new remittance information
            ustrd_element.text = new_remittance_info
        else:
            raise ValueError(
                f"Transaction with PmtInfId '{pmt_inf_id}' and EndToEndId '{end_to_end_id}' not found for remittance info update."
            )

    def update_transaction(self, pmt_inf_id, end_to_end_id, instd_amt=None, instd_amt_ccy=None, dbtr_nm=None,
                           dbtr_acct_iban=None, dbtr_agt_bic=None, rmt_inf=None):
        """
        Updates an existing DirectDebitTransaction.

        Args:
            pmt_inf_id (str): The ID of the payment instruction containing the transaction.
            end_to_end_id (str): The EndToEndId of the transaction to update.
            instd_amt (Decimal, optional): New instructed amount.
            instd_amt_ccy (str, optional): New currency for instructed amount.
            dbtr_nm (str, optional): New debtor name.
            dbtr_acct_iban (str, optional): New debtor account IBAN.
            dbtr_agt_bic (str, optional): New debtor agent BIC.
            rmt_inf (str, optional): New remittance information.
        """
        ns = {'ns': PAIN_008_NAMESPACE}

        # Find the payment instruction element
        pmt_inf_element = self.root.find(f".//ns:PmtInf[ns:PmtInfId='{pmt_inf_id}']", namespaces=ns)
        if pmt_inf_element is None:
            raise ValueError(f"Payment instruction with ID '{pmt_inf_id}' not found.")

        # Find the transaction element using EndToEndId
        tx_element = pmt_inf_element.find(
            f".//ns:DrctDbtTxInf[ns:PmtId/ns:EndToEndId='{end_to_end_id}']", namespaces=ns
        )
        if tx_element is None:
            raise ValueError(
                f"Transaction with EndToEndId '{end_to_end_id}' not found in payment instruction '{pmt_inf_id}'.")

        # Update transaction details
        if instd_amt is not None:
            instd_amt_element = tx_element.find("ns:InstdAmt", namespaces=ns)
            if instd_amt_element is not None:
                instd_amt_element.text = str(instd_amt)

        if instd_amt_ccy is not None:
            instd_amt_element = tx_element.find("ns:InstdAmt", namespaces=ns)
            if instd_amt_element is not None:
                instd_amt_element.set("Ccy", instd_amt_ccy)

        if dbtr_nm is not None:
            dbtr_element = tx_element.find("ns:Dbtr/ns:Nm", namespaces=ns)
            if dbtr_element is not None:
                dbtr_element.text = dbtr_nm

        if dbtr_acct_iban is not None:
            dbtr_acct_iban_element = tx_element.find("ns:DbtrAcct/ns:Id/ns:IBAN", namespaces=ns)
            if dbtr_acct_iban_element is not None:
                dbtr_acct_iban_element.text = dbtr_acct_iban

        if dbtr_agt_bic is not None:
            dbtr_agt_bic_element = tx_element.find("ns:DbtrAgt/ns:FinInstnId/ns:BIC", namespaces=ns)
            if dbtr_agt_bic_element is not None:
                dbtr_agt_bic_element.text = dbtr_agt_bic

        if rmt_inf is not None:
            rmt_inf_element = tx_element.find("ns:RmtInf/ns:Ustrd", namespaces=ns)
            if rmt_inf_element is not None:
                rmt_inf_element.text = rmt_inf

    def save_xml(self, file_path):
        """Saves the current pain.008.001.02 message to an XML file.

        Args:
            file_path (str): The path to the output XML file.
        """
        if self.root is None:
            raise ValueError("Message not created. Call create_message() first.")
        xml_string = ET.tostring(self.root, encoding="utf-8")
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")
        with open(file_path, "w") as f:
            f.write(pretty_xml)


# Example usage for an IoT scenario:
def create_iot_direct_debit(device_id, usage_data, amount, debtor_iban, debtor_name, creditor_iban, creditor_name,
                            creditor_bic, debtor_bic):
    """
    Creates a pain.008.001.02 message for an IoT device direct debit.

    Args:
        device_id (str): The ID of the IoT device.
        usage_data (str): Data related to the device usage (e.g., energy consumed, data transferred).
        amount (Decimal): The amount to be debited.
        debtor_iban (str): The IBAN of the debtor (customer).
        debtor_name (str): The name of the debtor.
        creditor_iban (str): The IBAN of the creditor (IoT company).
        creditor_name (str): The name of the creditor.
        creditor_bic (str) : The BIC of the creditor
        debtor_bic (str) : The BIC of the debtor

    Returns:
        Pain00800102: The created pain.008.001.02 message.
    """
    pain008 = Pain00800102Class()
    msg_id = str(uuid.uuid4())
    cre_dt_tm = datetime.now()
    nb_of_txs = 1
    ctrl_sum = amount
    initg_pty_nm = creditor_name

    grpHdr = GrpHdr(
        MsgId=msg_id,
        CreDtTm=cre_dt_tm,
        NbOfTxs=str(nb_of_txs),
        CtrlSum=ctrl_sum,
        InitgPty=InitgPty(Nm=initg_pty_nm)
    )

    pmt_inf_id = str(uuid.uuid4())
    reqd_colltn_dt = date.today()

    drct_dbt_tx_inf = [
        DirectDebitTransaction(
            instd_amt=amount,
            instd_amt_ccy="EUR",
            mndt_id=str(uuid.uuid4()),
            dbtr_nm=debtor_name,
            dbtr_acct_iban=debtor_iban,
            dbtr_agt_bic=debtor_bic,
            rmt_inf=f"Device: {device_id}, Usage: {usage_data}",
        )
    ]

    pmtInf = [
        PaymentInstruction(
            pmt_inf_id, reqd_colltn_dt, creditor_name, creditor_iban, creditor_bic, drct_dbt_tx_inf
        )
    ]

    pain008.create_message(grpHdr, pmtInf)
    return pain008


from lxml import etree


def validate_against_xsd(xml_string, xsd_file_path):
    try:
        xmlschema_doc = etree.parse(xsd_file_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        # Parse the XML string into an ElementTree object
        xml_doc = etree.fromstring(xml_string.encode('utf-8'))

        # Validate the XML against the schema
        is_valid = xmlschema.validate(xml_doc)

        if not is_valid:
            print("XML is NOT valid against the schema. Errors:")
            for error in xmlschema.error_log:
                print(error.message)
        else:
            print("XML is valid against the schema.")

        return is_valid
    except etree.XMLSchemaParseError as e:
        print(f"Error parsing XSD schema: {e}")
        return False
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML document: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# Example Usage for parsing:
def example_parse_and_process(pain008):
    print("Parsed XML:")
    print(f"  Message ID: {pain008.grp_hdr.MsgId}")
    print(f"  Number of Transactions: {pain008.grp_hdr.NbOfTxs}")
    print(f"  Initiating Party: {pain008.grp_hdr.InitgPty.Nm}")

    for pmt_inf in pain008.pmt_inf:
        print(f"\nPayment Instruction ID: {pmt_inf.PmtInfId}")
        print(f"  Creditor: {pmt_inf.CdtrNm}")
        print(f"  Creditor IBAN: {pmt_inf.CdtrAcctIBAN}")
        print(f"  Requested Collection Date: {pmt_inf.ReqdColltnDt}")

        for tx in pmt_inf.DrctDbtTxInf:
            print(f"\n  Transaction:")
            print(f"    Amount: {tx.InstdAmt} {tx.InstdAmtCcy}")
            print(f"    Mandate ID: {tx.MndtId}")
            print(f"    Debtor: {tx.DbtrNm}")
            print(f"    Debtor IBAN: {tx.DbtrAcctIBAN}")
            print(f"    Remittance Info: {tx.RmtInf}")

    # Example: Get transactions for a specific debtor
    debtor_transactions = pain008.get_transactions_by_debtor("NL00DUMMY1234567890")
    if debtor_transactions:
        print(f"\nTransactions for Debtor IBAN NL00DUMMY1234567890:")
        for tx in debtor_transactions:
            print(f"    Amount: {tx.InstdAmt} {tx.InstdAmtCcy}, Mandate ID: {tx.MndtId}")

    # Example: Get total transaction amount
    total_amount = pain008.get_total_transaction_amount()
    print(f"\nTotal Transaction Amount: {total_amount}")


# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Creating a pain.008 message for an IoT device
    iot_pain008 = create_iot_direct_debit(
        device_id="SMART-METER-001",
        usage_data="150 kWh",
        amount=Decimal("45.00"),
        debtor_iban="NL00DUMMY1234567890",
        debtor_name="John Doe",
        creditor_iban="NL00CREDIT1234567890",
        creditor_name="Energia",
        creditor_bic="ABNANL2A",
        debtor_bic="INGBNL2A"
    )
    iot_xml = iot_pain008.to_xml_string()
    print("Generated pain.008.001.02 XML:\n", iot_xml)

    # Save XML to file for testing
    iot_pain008.save_xml("iot_direct_debit.xml")

    # Example 2: Parsing and processing the generated XML file
    example_parse_and_process(iot_pain008)

    # Validate the generated XML
    is_valid = validate_against_xsd(iot_xml, "docs/pain.008.001.02.xsd")
    if is_valid:
        print("XML is valid against the pain.008.001.02 schema.")
    else:
        print("XML is NOT valid against the pain.008.001.02 schema.")
