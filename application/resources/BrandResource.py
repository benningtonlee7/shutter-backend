from application import db, ma


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(64), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<Brand name:{} id:{}>'.format(self.id, self.brand_name)

class BrandSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Brand

    id = ma.auto_field()
    brand_name = ma.auto_field()
