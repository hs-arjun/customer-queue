from odoo import fields, api, models, _
from odoo.exceptions import ValidationError

class CustomerService(models.TransientModel):
    _name = 'customer.service'

    user_name = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    date = fields.Datetime(default=fields.Datetime.now, string="Date")
    counter = fields.Many2one('counter.counter', string="Counter")
    customer_service_line_ids = fields.One2many('customer.service.line', 'customer_service_line_id', string="ids")

    def customer_service(self):
        token_data = self.env['token.token'].search([('service_done', '=', False)])
        print("data", token_data)
        token_list = []
        if token_data:
            for rec in token_data:
                self.customer_service_line_ids += self.env['customer.service.line'].new(
                    {
                        'customer': rec.name,
                        'customer_name': rec.customer_name,
                        'customer_mobile': rec.customer_mobile,
                    }
                )
        else:
            raise ValidationError(_("Not available token"))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'customer.service',
            'target': 'new',
            'res_id': self.id
        }


class CustomerServiceLine(models.TransientModel):
    _name = 'customer.service.line'

    customer = fields.Char(string="Customer Token")
    customer_name = fields.Char(string="Customer Name")
    customer_mobile = fields.Integer(string="Mobile")
    service_comment = fields.Text(string="Service comment")
    customer_service_line_id = fields.Many2one('customer.service', string="id")

    def service_given(self):
        print("okkkk")
        token_data = self.env['token.token'].search([('service_done', '=', False)])
        for rec in self:
            for token in token_data:
                if rec.customer == token.name:
                    token.service_done = True

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'customer.service',
            'target': 'new',
        }
