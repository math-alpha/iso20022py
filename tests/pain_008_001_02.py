import unittest
import xml.etree.ElementTree as ET
from datetime import date, datetime
from decimal import Decimal
from ..pain_008_001_02 import *


class TestPain00800102(unittest.TestCase):

    def setUp(self):
        # Create a sample Pain00800102 object for testing
        self.pain008 = Pain00800102Class(
            doc=Document(
                CstmrDrctDbtInitn=CstmrDrctDbtInitn(
                    GrpHdr=GrpHdr(
                        MsgId="MSGID-1234",
                        CreDtTm=datetime(2023, 12, 22, 10, 0, 0),
                        NbOfTxs="0",
                        InitgPty=InitgPty(
                            Nm="Initiating Party"
                        )
                    ),
                    PmtInf=[]
                )
            )
        )

        self.pmt_inf_id = "PMT-INF-001"
        self.reqd_colltn_dt = datetime(2024, 1, 15)
        self.cdtr_nm = "Creditor Corp"
        self.cdtr_acct_iban = "DE89370400440532013000"
        self.cdtr_agt_bic = "DEUTDEFF500"

    def test_create_group_header(self):
        grp_hdr = GrpHdr(
            MsgId="MSGID-001",
            CreDtTm=datetime(2023, 12, 21, 10, 0, 0),
            NbOfTxs="1",
            CtrlSum=100.00,
            InitgPty=InitgPty(Nm="Test Initiating Party")
        )
        self.pain008.add_group_header(grp_hdr)
        retrieved_grp_hdr = self.pain008.get_group_header()

        self.assertIsNotNone(retrieved_grp_hdr)
        self.assertEqual(retrieved_grp_hdr.MsgId, "MSGID-001")
        self.assertEqual(retrieved_grp_hdr.CreDtTm, datetime(2023, 12, 21, 10, 0, 0))
        self.assertEqual(retrieved_grp_hdr.NbOfTxs, "1")
        self.assertEqual(retrieved_grp_hdr.CtrlSum, 100.00)
        self.assertEqual(retrieved_grp_hdr.InitgPty.Nm, "Test Initiating Party")

    def test_add_and_get_payment_instruction(self):
        drct_dbt_tx_inf = [
            DirectDebitTransaction(
                instd_amt=Decimal("100.00"),
                instd_amt_ccy="EUR",
                mndt_id="MNDT-ID-001",
                dbtr_nm="Debtor One",
                dbtr_acct_iban="NL00ABCD1234567890",
                dbtr_agt_bic="ABNANL2A",
                rmt_inf="Payment for Invoice 1"
            )
        ]
        pmt_inf = PmtInfElement(
            PmtInfId=self.pmt_inf_id,
            PmtMtd=PmtMtd.DD,
            ReqdColltnDt=self.reqd_colltn_dt,
            Cdtr=InitgPty(Nm=self.cdtr_nm),
            CdtrAcct=CdtrAcct(
                Id=CdtrAcctID(
                    IBAN=self.cdtr_acct_iban,
                    Othr=IDOthr(Id="OTHERID")
                ),
            ),
            CdtrAgt=FwdgAgt(
                FinInstnId=FinInstnID(
                    BIC=self.cdtr_agt_bic
                )
            ),
            DrctDbtTxInf=[
                DrctDbtTxInfElement(
                    PmtId=PmtID(EndToEndId="ENDTOENDID-001"),
                    InstdAmt=InstdAmt(Value=100.00, Ccy="EUR"),
                    DrctDbtTx=DrctDbtTx(
                        MndtRltdInf=MndtRltdInf(MndtId="MNDT-ID-001", DtOfSgntr=datetime(2023, 1, 1))
                    ),
                    DbtrAgt=FwdgAgt(FinInstnId=FinInstnID(BIC="ABNANL2A")),
                    Dbtr=InitgPty(Nm="Debtor One"),
                    DbtrAcct=CdtrAcct(
                        Id=CdtrAcctID(IBAN="NL00ABCD1234567890", Othr=IDOthr(Id="OTHERID"))
                    ),
                    RmtInf=RmtInf(Ustrd=["Payment for Invoice 1"]),
                )
            ]
        )
        self.pain008.add_payment_instruction(pmt_inf)
        retrieved_pmt_infs = self.pain008.get_payment_instructions()

        self.assertEqual(len(retrieved_pmt_infs), 1)
        self.assertEqual(retrieved_pmt_infs[0].PmtInfId, self.pmt_inf_id)
        self.assertEqual(retrieved_pmt_infs[0].Cdtr.Nm, self.cdtr_nm)

    def test_add_payment_instruction(self):
        # Create a list of direct debit transactions
        drct_dbt_tx_inf_list = [
            DirectDebitTransaction(
                instd_amt=Decimal("50.00"),
                instd_amt_ccy="EUR",
                mndt_id="MNDT-ID-001",
                dbtr_nm="Debtor One",
                dbtr_acct_iban="NL00ABCD1234567890",
                dbtr_agt_bic="ABNANL2A",
                rmt_inf="Payment for Invoice 1"
            ),
            DirectDebitTransaction(
                instd_amt=Decimal("75.00"),
                instd_amt_ccy="EUR",
                mndt_id="MNDT-ID-002",
                dbtr_nm="Debtor Two",
                dbtr_acct_iban="NL00XYZB9876543210",
                dbtr_agt_bic="XYZBNL2A",
                rmt_inf="Payment for Subscription"
            )
        ]

        # Create a payment instruction with the list of transactions
        pmt_inf = PaymentInstruction(
            pmt_inf_id=self.pmt_inf_id,
            reqd_colltn_dt=self.reqd_colltn_dt,
            cdtr_nm=self.cdtr_nm,
            cdtr_acct_iban=self.cdtr_acct_iban,
            cdtr_agt_bic=self.cdtr_agt_bic,
            drct_dbt_tx_inf=drct_dbt_tx_inf_list
        )
        self.pain008.add_payment_instruction(pmt_inf)

        # Retrieve the payment instructions and validate
        retrieved_pmt_infs = self.pain008.get_payment_instructions()
        self.assertEqual(len(retrieved_pmt_infs), 1)
        retrieved_pmt_inf = retrieved_pmt_infs[0]
        self.assertEqual(retrieved_pmt_inf.PmtInfId, self.pmt_inf_id)
        self.assertEqual(retrieved_pmt_inf.CdtrNm, self.cdtr_nm)

        # Validate the direct debit transactions
        self.assertEqual(len(retrieved_pmt_inf.DrctDbtTxInf), 2)
        self.assertEqual(retrieved_pmt_inf.DrctDbtTxInf[0].InstdAmt, Decimal("50.00"))
        self.assertEqual(retrieved_pmt_inf.DrctDbtTxInf[0].DbtrNm, "Debtor One")
        self.assertEqual(retrieved_pmt_inf.DrctDbtTxInf[1].InstdAmt, Decimal("75.00"))
        self.assertEqual(retrieved_pmt_inf.DrctDbtTxInf[1].DbtrNm, "Debtor Two")


if __name__ == '__main__':
    unittest.main()
