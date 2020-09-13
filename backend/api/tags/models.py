from api import db


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    gis = db.Column(db.Boolean)
    valid = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'gis': self.gis
        }

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

    @classmethod
    def get_tag(cls, name):
        return db.session.query(cls).filter_by(name=name).first()

    @classmethod
    def get_or_create(cls, **kwargs):
        instance = db.session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
