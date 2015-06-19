# -*- coding: utf-8 -*-
# #############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
import logging
_logger = logging.getLogger(__name__)
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time


class doctor_professional(osv.osv):
    _name = "doctor.professional"
    _description = "Information about the healthcare professional"
    
    _inherits = {
        'res.users': 'user_id',
    }    
    
    _columns = {
        'user_id': fields.many2one('res.users', 'User', help='Related user name', required=True, ondelete='restrict'),
        'speciality_id': fields.many2one('doctor.speciality', 'Speciality', required=True),
        'professional_card': fields.char('Professional card', size=64, required=True),
        'authority': fields.char('Authority', size=64, required=True),
        'active': fields.boolean('Active'),
        'procedures_ids': fields.many2many('product.product', id1='professional_ids', id2='procedures_ids',
                                           string='My health procedures', required=False, ondelete='restrict'),
    }

    _defaults = {
        'active': True,
    }
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record['id'],record.user_id.name or ''))
        return res

class doctor_patient(osv.osv):
    _name = "doctor.patient"
    _description = "Information about the patient"
    #_rec_name = 'nombre'
    
    _inherits = {
        'res.partner': 'patient',
    }    

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        for patient in self.browse(cr, uid, ids, context=context):
            if 'birth_date' in vals:
                birth_date = vals['birth_date']
                current_date = time.strftime('%Y-%m-%d')
                if birth_date > current_date:
                    raise osv.except_osv(_('Warning !'), _("Birth Date Can not be a future date "))
        return super(doctor_patient, self).write(cr, uid, ids, vals, context=context)


    def create(self, cr, uid, vals, context=None):
        if 'birth_date' in vals:
            birth_date = vals['birth_date']
            current_date = time.strftime('%Y-%m-%d')
            if birth_date > current_date:
                raise osv.except_osv(_('Warning !'), _("Birth Date Can not be a future date "))
        
        return super(doctor_patient, self).create(cr, uid, vals, context=context)

    _columns = {
        'patient': fields.many2one('res.partner', 'Paciente', ondelete='cascade',
                                   domain=[('is_company', '=', False)]),
        'birth_date': fields.date('Date of Birth', required=True),
        'sex': fields.selection([('m', 'Male'), ('f', 'Female'), ], 'Sex', select=True, required=True),
        'blood_type': fields.selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'), ], 'Blood Type'),
        'rh': fields.selection([('+', '+'), ('-', '-'), ], 'Rh'),
        'insurer': fields.many2one('doctor.insurer', 'Insurer', required=False, help='Insurer'),
        'deceased': fields.boolean('Deceased', help="Mark if the patient has died"),
        'death_date': fields.date('Date of Death'),
        'death_cause': fields.many2one('doctor.diseases', 'Cause of Death'),
        'attentions_ids': fields.one2many('doctor.attentions', 'patient_id', 'Attentions'),
        'appointments_ids': fields.one2many('doctor.appointment', 'patient_id', 'Attentions'),
    }




doctor_patient()
