# Copyright 2014-2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import json
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "analytic.mixin"]

    analytic_distribution = fields.Json(
        inverse="_inverse_analytic_distribution",
        help="This analytic distribution will be propagated to all lines "
        "analytic distributions, if you need to use different "
        "analytic distribution, define it at line level.",
    )

    @api.depends("order_line.analytic_distribution")
    def _compute_analytic_distribution(self):
        """Set the analytic distribution on the order based on its order lines.

        If all order lines have the same analytic distribution,
        then set it on the order, otherwise left the field empty.
        """
        res = None
        if hasattr(super(), "_compute_analytic_distribution"):
            res = super()._compute_analytic_distribution()
        for order in self:
            if distributions := order.mapped("order_line.analytic_distribution"):
                # Dump the first distribution to be able to compare for equality
                try:
                    common_distribution = json.dumps(distributions[0], sort_keys=True)
                except Exception as error:
                    _logger.error(
                        f"Analytic distribution is not dumped, check the error: {error}"
                    )
                    # If dumping fails, fall back to a regular comparison.
                    common_distribution = distributions[0]
                # Check that every distribution equals the first.
                if all(
                    (
                        json.dumps(distribute, sort_keys=True)
                        if isinstance(distribute, (dict | list))
                        else distribute
                    )
                    == common_distribution
                    for distribute in distributions
                ):
                    order.analytic_distribution = distributions[0]
                else:
                    order.analytic_distribution = False
            else:
                order.analytic_distribution = False
        return res

    def _inverse_analytic_distribution(self):
        """Propagate the analytic distribution to order lines if set on the order"""
        for order in self:
            if order.analytic_distribution:
                order.order_line.analytic_distribution = order.analytic_distribution
