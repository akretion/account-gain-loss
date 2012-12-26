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
        'write_off_journal_currency_id': fields.many2one(
            'account.journal',
            string="Currency Loss/Gain Journal",),
        'write_off_journal_other_id': fields.many2one(
            'account.journal',
            string="Various Loss/Gain Journal",),
    }

    def get_write_off_information(self, cr, uid, company_id, writeoff_reason, writeoff_type, context=None):
        """
        Return the information about the write off for the company selected
        :param int company_id: company id concern by the reconcilation
        :param str writeoff_reason: two value posible by default 'exchange' or 'various'
        :param str writeoff_type: two value posible by default 'income' or 'expense'
        :rtype tuple
        :return a tuple with the correct account_id and journal_id (account_id, journal_id)
        """
        if hasattr(company_id, '__iter__'):
            company_id = company_id[0]
        account_id = None
        journal_id = None
        if writeoff_reason and writeoff_type:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            if writeoff_reason == 'exchange':
                journal_id = company.write_off_journal_currency_id.id
                if writeoff_type == 'expense':
                    account_id = company.expense_currency_exchange_account_id.id
                elif writeoff_type == 'income':
                    account_id = company.income_currency_exchange_account_id.id
            elif writeoff_reason == 'various':
                journal_id = company.write_off_journal_other_id.id
                if writeoff_type == 'expense':
                    account_id = company.expense_other_account_id.id
                elif writeoff_type == 'income':
                    account_id = company.income_other_account_id.id
        return account_id, journal_id

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
        'write_off_journal_currency_id': fields.related(
            'company_id', 'write_off_journal_currency_id',
            type="many2one",
            relation='account.journal',
            string="Currency Loss/Gain Journal",),
        'write_off_journal_other_id': fields.related(
            'company_id', 'write_off_journal_other_id',
            type="many2one",
            relation='account.journal',
            string="Various Loss/Gain Journal",),
    }
