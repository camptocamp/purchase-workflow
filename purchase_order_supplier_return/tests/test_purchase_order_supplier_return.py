# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests.common import TransactionCase


class TestPurchaseOrderSupplierReturn(TransactionCase):
    def setUp(self):
        super().setUp()

        self.product = self.env["product.product"].create(
            {"name": "Product Test", "list_price": 5.0}
        )
        self.partner = self.env["res.partner"].create(
            {
                "name": "Partner",
            }
        )
        self.purchase_order = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )
        self.purchase_order_line_1 = self.env["purchase.order.line"].create(
            {
                "order_id": self.purchase_order.id,
                "product_id": self.product.id,
                "product_qty": -1,
            }
        )
        self.purchase_order_line_2 = self.env["purchase.order.line"].create(
            {
                "order_id": self.purchase_order.id,
                "product_id": self.product.id,
                "product_qty": 1,
            }
        )

    def test_negative_purchase_order_line(self):
        """Test that the negative purchase_order_line is correctly received
        with the negative quantity when the related picking is validated."""
        self.purchase_order.button_confirm()
        assert self.purchase_order_line_1.qty_received == 0
        assert self.purchase_order_line_1.qty_received == 0

        # Validate the pickings related to the purchase order
        for picking in self.purchase_order.picking_ids:
            picking.action_set_quantities_to_reservation()
            picking.button_validate()

        self.purchase_order.order_line._compute_qty_received()

        assert self.purchase_order_line_1.move_ids._is_purchase_return() is True
        assert self.purchase_order_line_1.move_ids.to_refund is True
        assert self.purchase_order_line_1.qty_received == -1

        assert self.purchase_order_line_2.move_ids._is_purchase_return() is False
        assert self.purchase_order_line_2.move_ids.to_refund is False
        assert self.purchase_order_line_2.qty_received == 1
