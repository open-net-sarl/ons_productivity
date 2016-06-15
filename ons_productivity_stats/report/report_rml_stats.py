#-*- coding: utf-8 -*-
#
#  File: report/report_rml_stats.py
#  Module: ons_productivity_stats
#
#  Created by cyp@open-net.ch
#
#  Copyright (c) 2013 Open-Net Ltd. All rights reserved.
##############################################################################
#
# Copyright (c) 2011 OpenNet  (http://www.open-net.ch) 
# All Right Reserved
#
# Author : Yvon-Philippe Crittin (OpenNet)
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import time
from report import report_sxw
from osv import osv

import netsvc
logger = netsvc.Logger()

class report_rml_stats(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_rml_stats, self).__init__(cr, uid, name, context=context)
        logger.notifyChannel(' ***** Stats printing', netsvc.LOG_DEBUG, "Asked to print '%s' with the context: %s" % (name, str(context)) )
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
        })
        
report_sxw.report_sxw('report.rml.ons_stats',
                       'ons.stats', 
                       'addons/ons_productivity_stats/report/report_rml_stats.rml',
                       parser=report_rml_stats)
