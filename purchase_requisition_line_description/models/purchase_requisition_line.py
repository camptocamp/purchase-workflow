# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.fields import first


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    name = fields.Text(string="Product Description")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """
        New method is triggered when the `product_id` field is changed.
        It updates the `name` field (description) based on the selected product
        and the partner's language and purchase description.
        """
        if self.product_id:
            partner = first(self.requisition_id.purchase_ids).partner_id
            product_lang = self.product_id.with_context(
                lang=partner.lang,
                partner_id=partner.id,
            )
            self.name = product_lang.display_name
            if product_lang.description_purchase:
                self.name += "\n" + product_lang.description_purchase
