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


class account_move_line_reconcile_writeoff(osv.osv_memory):
    
    _inherit = "account.move.line.reconcile.writeoff"
    
    def _get_writeoff_type(self, cr, uid, context=None):
        wtype = False
        debit = 0.0
        credit = 0.0
        if context.get('active_ids'):
            for line in self.pool.get('account.move.line').browse(cr, uid, context.get('active_ids'), context=context):
                debit += line.debit
                credit += line.credit
            if debit > credit:
                wtype = 'expense'
            elif credit > debit:
                wtype = 'income' 
        return wtype
    
    
    _columns = {
        'writeoff_reason': fields.selection([
                                        ('exchange','Exchange Gain/Loss'),
                                        ('various','Various Gain/loss'),
                                        ], 'Reason'),
        'company_id': fields.many2one('res.company', 'Company'),
        'writeoff_type': fields.selection([
                                        ('income', 'Gain Account'),
                                        ('expense', 'Loss Account'),
                                        ],
                                        'Type', readonly=True),
    }
    _defaults = {
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid,
                                                    'account.move.line.reconcile.writeoff', context=c),
        'writeoff_type': _get_writeoff_type,
    }


    def writeoff_reason_change(self, cr, uid, ids, company_id, writeoff_reason, writeoff_type, context=None):
        result = {}
        if writeoff_reason and writeoff_type:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            if writeoff_reason == 'exchange':
                if writeoff_type == 'expense':
                    account_id = company.expense_currency_exchange_account_id.id
                elif writeoff_type == 'income':
                    account_id = company.income_currency_exchange_account_id.id
            elif writeoff_reason == 'various':
                if writeoff_type == 'expense':
                    account_id = company.expense_other_account_id.id
                elif writeoff_type == 'income':
                    account_id = company.income_other_account_id.id
            result['writeoff_acc_id'] = account_id
        return {'value': result}

