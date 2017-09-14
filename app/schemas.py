from marshmallow import validates, ValidationError, fields, pre_load, pre_dump

from app import ma


class StatusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', '_links')

    @validates('name')
    def validate_name(self, value):
        if value is None or not value:
            raise ValidationError('Status name can\'t be blank')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('status_route', id='<id>'),
        'collection': ma.URLFor('status_route')
    })


class VendorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status', '_links')

    status = fields.Nested(StatusSchema, only=('name',), required=False)

    @validates('name')
    def validate_name(self, value):
        if value is None or not value:
            raise ValidationError('Vendor name can\'t be blank')

    # @pre_load
    # def
    _links = ma.Hyperlinks({
        'self': ma.URLFor('vendor_route', id='<id>'),
        'collection': ma.URLFor('vendor_route')
    })


class BusinessSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'status', 'vendors', 'created_at', 'modified_at', '_links')
        ordered = True

    status = ma.Nested(StatusSchema, only=('name',))
    vendors = ma.Nested(VendorSchema, many=True, only=('id', 'name', 'status'))

    @validates('name')
    def validate_name(self, value):
        if value is None or not value:
            raise ValidationError('Business name can\'t be blank')

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('business_route', id='<id>'),
        'collection': ma.URLFor('business_route')
    })


class PartnerSchema(ma.Schema):
    class Meta:
        fields = ('name',)

    vendor = fields.Nested(VendorSchema, required=False, only=('name',))
    status = fields.Nested(StatusSchema, required=False, only=('name',))

    @validates('name')
    def validate_name(self, value):
        if value is None or not value:
            raise ValidationError('Business name can\'t be blank')


business_schema = BusinessSchema()
businesses_schema = BusinessSchema(many=True)
vendor_schema = VendorSchema()
vendors_schema = VendorSchema(many=True)
status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)
partner_schema = PartnerSchema()
