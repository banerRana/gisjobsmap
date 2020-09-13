from api import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    valid = db.Column(db.Boolean, default=False)
    searches = db.Column(db.String(150))  # search terms

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'searches': self.searches
        }

    def __repr__(self):
        return '<Category {}>'.format(self.name)

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
