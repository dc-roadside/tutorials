from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    
    # SQL constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 
         'The offer price must be strictly positive.')
    ]

    # Basic fields for property offers
    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    # Many2one fields for relationships
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    
    # Related field to property type
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", 
                                     related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                # Fallback for new records that haven't been saved yet
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            elif record.date_deadline:
                # Fallback for new records
                record.validity = (record.date_deadline - fields.Date.today()).days

    # Action methods for buttons
    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("Cannot accept an offer for a sold property.")
            
            # Refuse all other offers for this property
            other_offers = record.property_id.offer_ids.filtered(lambda o: o.id != record.id)
            other_offers.write({'status': 'refused'})
            
            # Accept this offer
            record.status = 'accepted'
            
            # Set property details
            record.property_id.write({
                'buyer_id': record.partner_id.id,
                'selling_price': record.price,
                'state': 'offer_accepted'
            })
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True