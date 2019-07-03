from marshmallow import Schema, fields


class ValidateOrderLine(Schema):
    name = fields.String(required=True)
    price_unit = fields.Decimal(required=True)
    product_id = fields.Integer(required=True)
    product_uom = fields.Integer(required=True)
    product_uom_qty = fields.Decimal(required=True)
    tax_id = fields.Integer()
    discount = fields.Decimal()


class ValidateOrder(Schema):
    origin = fields.String()
    note = fields.String()
    partner_id = fields.Integer(required=True)
    warehouse_id = fields.Integer()
    pricelist_id = fields.Integer()
    partner_invoice_id = fields.Integer(required=True)
    partner_shipping_id = fields.Integer(required=True)
    order_line = fields.List(fields.Dict, required=True, default=[])



class ValidateInput(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
