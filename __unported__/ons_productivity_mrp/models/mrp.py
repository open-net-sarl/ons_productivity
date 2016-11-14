# -*- coding: utf-8 -*-
#
#  File: models/mrp.py
#  Module: ons_productivity_mrp
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2015-TODAY Open Net Sàrl. <http://www.open-net.ch>
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, _
from openerp.osv import fields

import logging
_logger = logging.getLogger(__name__)

class mrp_bom_workcenter_op_param(models.Model):
    _name = 'mrp.bom.wkc_op_param'
    _description = 'Rate for a workcenter operation, in the context of a BoM'

    # ---------- Fields management
    
    _columns = {
        'name': fields.many2one('mrp.routing.workcenter', 'Operation', ondelete='cascade', required=True),
        'workcenter_id': fields.related('name', 'workcenter_id', relation='mrp.workcenter', type='many2one', string='Work center'),
        'routing_id': fields.many2one('mrp.routing', 'Routing', ondelete='cascade', required=True),
        'bom_id': fields.many2one('mrp.bom', 'BoM', ondelete='cascade', required=True),
        'coeff': fields.float('Coefficient'),
        'sequence': fields.integer('Sequence'),
    }
    
    _defaults = {
        'sequence': lambda *a: 10,
    }

class mrp_bom(models.Model):
    _inherit = 'mrp.bom'

    # ---------- Fields management
    
    _columns = {
        'wkc_op_param_ids': fields.one2many('mrp.bom.wkc_op_param', 'bom_id', 'Workcenter operation parameters'),
    }

    # ---------- Instances management

    def create(self, cr, uid, vals, context={}):
        do_it = 'routing_id' in vals
        new_id = super(mrp_bom, self).create(cr, uid, vals, context=context)
        if new_id and do_it:
            self.synch_workcenter_params(cr, uid, [new_id], context=context)
        
        return new_id

    def write(self, cr, uid, ids, vals, context={}):
        do_it = 'routing_id' in vals
        ret = super(mrp_bom, self).write(cr, uid, ids, vals, context=context)
        if do_it:
            self.synch_workcenter_params(cr, uid, ids, context=context)
        
        return ret

    # ---------- Utilities

    def synch_workcenter_params(self, cr, uid, ids, context={}):
        if not ids:
            return False
        wkcp_obj = self.pool.get('mrp.bom.wkc_op_param')
        routings_obj = self.pool.get('mrp.routing.workcenter')
        if isinstance(ids, (int,long)): ids = [ids]
        for row in self.browse(cr, uid, ids, context=context):
            new_lst = []
            act_lst = [x.name.id for x in row.wkc_op_param_ids]
            ref_lst = []
            if row.routing_id:
                for wkl in row.routing_id.workcenter_lines:
                    if not wkl.workcenter_id:
                        continue
                    ref_lst.append(wkl.id)
                    if wkl.id in new_lst or wkl.id in act_lst:
                        continue
                    new_lst.append(wkl.id)
            
            # Add the missing items
            for routing_id in new_lst:
                routing = routings_obj.browse(cr, uid, routing_id, context=context)
                vals = {
                    'name': routing_id,
                    'bom_id': row.id,
                    'routing_id': row.routing_id.id,
                    'coeff': 1.0,
                    'sequence': routing and routing.sequence or 10,
                }
                wkcp_obj.create(cr, uid, vals, context=context)
            
            # Remove the useless items
            to_delete = [x for x in act_lst if x not in ref_lst]
            if to_delete:
                wkcp_ids = wkcp_obj.search(cr, uid, [('name', 'in', to_delete), ('bom_id', '=', row.id)], context=context)
                if wkcp_ids:
                    wkcp_obj.unlink(cr, uid, wkcp_ids, context=context)

        return True