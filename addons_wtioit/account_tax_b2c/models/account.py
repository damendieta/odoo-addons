# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import except_orm
from odoo.addons import decimal_precision as dp

import logging

_logger = logging.getLogger(__name__)


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    b2c_fiscal_position = fields.Boolean(string='B2C')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def get_taxes_values(self):
        if len(self) == 0:
            company_id = self.env.user.company_id
        else:
            company_id = self[0].company_id
        company = company_id.sudo()
        current_method = company.tax_calculation_rounding_method
        if not self.fiscal_position_id.b2c_fiscal_position:
            company.tax_calculation_rounding_method = 'round_globally'
        else:
            company.tax_calculation_rounding_method = 'round_per_line'
        tax_grouped = super(AccountInvoice, self).get_taxes_values()
        company.tax_calculation_rounding_method = current_method
        return tax_grouped
