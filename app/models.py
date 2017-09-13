from app import db
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.orm.exc import NoResultFound

vendors = db.Table('partner',
                   db.Column('business_id', db.Integer, db.ForeignKey('business.id')),
                   db.Column('vendor_id', db.Integer, db.ForeignKey('vendor.id')),
                   db.UniqueConstraint('business_id', 'vendor_id', name='part_1')
                   )


class Business(db.Model):
    """This class represents the Business table."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status', backref='Business')
    vendors = db.relationship('Vendor', secondary='partner', backref=db.backref('business', lazy='dynamic'))

    def __init__(self, name, status):
        """initialize with name."""
        self.name = name
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Business.query.all()

    def __repr__(self):
        return "<Vendor: {}>".format(self.name)


class Vendor(db.Model):
    """This class represents the Vendor table."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status', backref='Vendor')

    def __init__(self, name, status):
        """initialize with name."""
        self.name = name
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Vendor.query.all()

    def __repr__(self):
        return "<Vendor: {}>".format(self.name)


class Status(db.Model):
    """This class represents the Status table."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Status.query.all()

    def __repr__(self):
        return "<Status: {}>".format(self.name)


def get_or_create(db, model, defaults=None, **kwargs):
    try:
        return model.query.filter_by(**kwargs).one(), False
    except NoResultFound:
        pass
    params = {k: v for k, v in kwargs.iteritems()
              if not isinstance(v, ClauseElement)}
    params.update(defaults or {})
    instance = model(**params)
    db.make_transient(instance)
    db.session.add(instance)
    return instance, True
