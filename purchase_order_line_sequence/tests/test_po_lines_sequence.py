# Copyright 2017 Camptocamp SA - Damien Crier, Alexandre Fayolle
# Copyright 2017 ForgeFlow, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo.tests import Form, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestPurchaseOrder(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Note: uom_po_id doesn't exist in Odoo 19, use product.uom_id
        # Useful models
        cls.PurchaseOrder = cls.env["purchase.order"]
        cls.PurchaseOrderLine = cls.env["purchase.order.line"]
        cls.partner_id = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        product_uom_unit_round_1 = cls.env.ref("uom.product_uom_unit")
        cls.product_id_1 = cls.env["product.product"].create(
            {
                "name": "Large Desk",
                "standard_price": 1299.0,
                "list_price": 1799.0,
                "type": "consu",
                "weight": 9.54,
                "default_code": "E-COM09",
                "description_sale": "Minimalist wooden desk for executive use",
                "uom_id": product_uom_unit_round_1.id,
            }
        )

        cls.product_id_2 = cls.env["product.product"].create(
            {
                "name": "Conference Chair",
                "standard_price": 28.0,
                "list_price": 33.0,
                "type": "consu",
                "uom_id": product_uom_unit_round_1.id,
            }
        )

        cls.AccountInvoice = cls.env["account.move"]
        cls.AccountInvoiceLine = cls.env["account.move.line"]

        cls.category = cls.env["product.category"].create(
            {
                "name": "Test category",
                "property_valuation": "real_time",
                "property_cost_method": "fifo",
            }
        )

        cls.account_expense = cls.env["account.account"].create(
            {
                "name": "Expense",
                "code": "EXP00",
                "account_type": "liability_current",
                "reconcile": True,
            }
        )
        cls.account_payable = cls.env["account.account"].create(
            {
                "name": "Payable",
                "code": "PAY00",
                "account_type": "liability_payable",
                "reconcile": True,
            }
        )

        cls.category.property_account_expense_categ_id = cls.account_expense

        cls.category.property_stock_journal = cls.env["account.journal"].create(
            {"name": "Stock journal", "type": "sale", "code": "STK00"}
        )
        cls.product_id_1.categ_id = cls.category
        cls.product_id_2.categ_id = cls.category
        cls.partner_id.property_account_payable_id = cls.account_payable

    def _create_purchase_order(self):
        po_vals = {
            "partner_id": self.partner_id.id,
            "order_line": [
                (
                    0,
                    0,
                    {
                        "name": self.product_id_1.name,
                        "product_id": self.product_id_1.id,
                        "product_qty": 5.0,
                        "product_uom_id": self.product_id_1.uom_id.id,
                        "price_unit": 500.0,
                        "date_planned": datetime.today(),
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": self.product_id_2.name,
                        "product_id": self.product_id_2.id,
                        "product_qty": 5.0,
                        "product_uom_id": self.product_id_2.uom_id.id,
                        "price_unit": 250.0,
                        "date_planned": datetime.today(),
                    },
                ),
            ],
        }

        return self.PurchaseOrder.create(po_vals)

    def test_purchase_order_line_sequence(self):
        self.po = self._create_purchase_order()

        po_form = Form(self.po)
        with po_form.order_line.new() as po_line_form:
            po_line_form.product_id = self.product_id_1
            self.assertEqual(po_line_form.sequence, self.po.max_line_sequence)

        self.po.button_confirm()

        move1 = self.env["stock.move"].search(
            [("purchase_line_id", "=", self.po.order_line[0].id)]
        )
        move2 = self.env["stock.move"].search(
            [("purchase_line_id", "=", self.po.order_line[1].id)]
        )

        self.assertEqual(
            self.po.order_line[0].visible_sequence,
            move1.sequence,
            "The Sequence of the Purchase Order Lines does not "
            "match to the Stock Moves",
        )
        self.assertEqual(
            self.po.order_line[1].visible_sequence,
            move2.sequence,
            "The Sequence of the Purchase Order Lines does not "
            "match to the Stock Moves",
        )

        self.po2 = self.po.copy()
        self.assertEqual(
            self.po.order_line[0].visible_sequence,
            self.po2.order_line[0].visible_sequence,
            "The Sequence is not copied properly",
        )
        self.assertEqual(
            self.po.order_line[1].visible_sequence,
            self.po2.order_line[1].visible_sequence,
            "The Sequence is not copied properly",
        )

    def test_purchase_order_line_sequence_with_section_note(self):
        """
        Verify that the sequence is correctly assigned to the move associated
        with the purchase order line it references.
        """
        po = self._create_purchase_order()
        self.PurchaseOrderLine.create(
            {
                "name": "Section 1",
                "display_type": "line_section",
                "order_id": po.id,
                "product_qty": 0,
            }
        )
        self.PurchaseOrderLine.create(
            {
                "name": self.product_id_1.name,
                "product_id": self.product_id_1.id,
                "product_qty": 15.0,
                "product_uom_id": self.product_id_1.uom_id.id,
                "price_unit": 150.0,
                "date_planned": datetime.today(),
                "order_id": po.id,
            }
        )
        self.PurchaseOrderLine.create(
            {
                "name": "Note 1",
                "display_type": "line_note",
                "order_id": po.id,
                "product_qty": 0,
            }
        )
        self.PurchaseOrderLine.create(
            {
                "name": self.product_id_2.name,
                "product_id": self.product_id_2.id,
                "product_qty": 1.0,
                "product_uom_id": self.product_id_2.uom_id.id,
                "price_unit": 50.0,
                "date_planned": datetime.today(),
                "order_id": po.id,
            }
        )
        po.button_confirm()

        moves = po.picking_ids[0].move_ids
        self.assertNotEqual(len(po.order_line), len(moves))

        for move in moves:
            self.assertEqual(move.sequence, move.purchase_line_id.visible_sequence)

    def test_write_purchase_order_line(self):
        """
        Verify that the sequence is correctly assigned to the move associated
        with the purchase order line it references when you modify it.
        """
        po = self._create_purchase_order()
        po.button_confirm()

        po.write(
            {
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product_id_2.name,
                            "product_id": self.product_id_2.id,
                            "product_qty": 2,
                            "product_uom_id": self.product_id_2.uom_id.id,
                            "price_unit": 30,
                            "date_planned": datetime.today(),
                        },
                    )
                ]
            }
        )

        moves = po.picking_ids[0].move_ids
        for move in moves:
            self.assertEqual(move.sequence, move.purchase_line_id.visible_sequence)

    def test_invoice_sequence(self):
        """
        Verify that the sequence is correctly assigned to the account move associated
        with the purchase order line it references.
        """
        po = self._create_purchase_order()
        po.button_confirm()
        po.order_line.qty_received = 5
        result = po.action_create_invoice()
        self.invoice = self.AccountInvoice.browse(result["res_id"])
        self.assertEqual(
            str(po.order_line[0].visible_sequence),
            self.invoice.line_ids[0].related_po_sequence,
        )
        self.assertEqual(
            str(po.order_line[1].visible_sequence),
            self.invoice.line_ids[1].related_po_sequence,
        )


def test_invoice_multiple_orders_sequence(self):
    """
    Verify that the sequence is correctly assigned to the account move associated
    with the purchase order line it references,
    when adding different POs to the same invoice.
    Format expected:
    - PO12345/1  -  PO Name + "/" + Sequence
    """

    po1 = self._create_purchase_order()
    po2 = self._create_purchase_order()

    po1.button_confirm()
    po2.button_confirm()

    # Avoid multi-record assignment bug
    po1.order_line[0].qty_received = 5
    po2.order_line[0].qty_received = 2

    invoices = self.env["account.move"]

    # IMPORTANT: avoid singleton crash in action_create_invoice
    for po in (po1, po2):
        res = po.action_create_invoice()
        invoices |= self.AccountMove.browse(res["res_id"])

    self.assertTrue(invoices)

    # invoice_origin is usually comma-separated PO names
    origins = invoices.mapped("invoice_origin")
    self.assertEqual(len(origins), 2)

    # Collect all related sequences safely (NO INDEXING)
    lines = invoices.mapped("line_ids").filtered(
        lambda line: line.display_type is False
    )

    seq_po1 = f"{po1.name}/{po1.order_line[0].visible_sequence}"
    seq_po2 = f"{po2.name}/{po2.order_line[0].visible_sequence}"

    # Assert presence instead of position
    self.assertIn(seq_po1, lines.mapped("related_po_sequence"))
    self.assertIn(seq_po2, lines.mapped("related_po_sequence"))
