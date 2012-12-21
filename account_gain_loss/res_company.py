# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   account_gain_loss for OpenERP                                             #
#   Copyright (C) 2012 Akretion Benoît GUILLOT <benoit.guillot@akretion.com>  #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from openerp.osv import fields, osv
from openerp.osv.orm import Model


class res_company(Model):
    
    _inherit = "res.company"
    
    _columns = {
        'income_other_account_id': fields.many2one(
            'account.account',
            string="Various Gain Account",
            domain="[('type', '=', 'other')]",),
        'expense_other_account_id': fields.many2one(
            'account.account',
            string="Various Loss Account",
            domain="[('type', '=', 'other')]",),
    }

class account_config_settings(osv.osv_memory):
    _inherit = 'account.config.settings'
    _columns = {
        'income_other_account_id': fields.related(
            'company_id', 'income_other_account_id',
            type='many2one',
            relation='account.account',
            string="Various Gain Account"),
        'expense_other_account_id': fields.related(
            'company_id', 'expense_other_account_id',
            type="many2one",
            relation='account.account',
            string="Various Loss Account"),
    }
