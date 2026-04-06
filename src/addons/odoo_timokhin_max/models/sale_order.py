import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
import string


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def _random_letters(self):
        return ''.join(random.choices(string.ascii_uppercase, k=10))

    responsible_employee = fields.Many2one(
        'hr.employee',
        string='Ответственный за выдачу',
        required=True)
    new_field_total = fields.Char(
        string='New Field',
        default=_random_letters,
        copy=False)

    @api.onchange('date_order', 'order_line')
    def _onchange_date_price_update(self):

        if self.date_order:
            now = datetime.datetime.now()
            # Костыль для предотвращения триггера onchange при создании ордера
            # и сохранения набора букв
            if self.date_order.strftime(
                    '%d.%m.%Y%H:%M:%S') != now.strftime('%d.%m.%Y%H:%M:%S'):
                date_str = self.date_order.strftime('%d.%m.%Y %H:%M:%S')
                amount = self.amount_total or 0.0
                self.new_field_total = f"{date_str} + {amount:.2f}"

    @api.onchange('new_field_total')
    def _onchange_field_len(self):
        if self.new_field_total and len(self.new_field_total) > 30:
            return {
                'warning': {
                    'title': "Превышена максимальная длина поля",
                    'message': f"Длина текста должна быть меньше 30 символов!",
                },
            }

    @api.constrains('new_field_total')
    def _constrains_new_field(self):
        if self.new_field_total and len(self.new_field_total) > 30:
            raise ValidationError(
                f"Длина текста должна быть меньше 30 символов!"
            )
