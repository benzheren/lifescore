import unittest
from pyramid.config import Configurator
from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    from lifescore.models import DBSession, Base
    engine = create_engine('sqlite://')
    session = DBSession()
    session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return session

def _cache_settings():
    return {
        'cache.regions':'short_term, long_term',
        'cache.type':'memory',
        'cache.second.expire':'1',
        'cache.short_term.expire':'60',
        'cache.default_term.expire':'300',
        'cache.long_term.expire':'3600',
        }
    

class UnitTests(unittest.TestCase):
    def setUp(self):
        from pyramid_beaker import set_cache_regions_from_settings
        import beaker
        set_cache_regions_from_settings(_cache_settings())
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        import transaction
        transaction.abort()
        testing.tearDown()

    def _addSchools(self):
        from lifescore.models import NationalSchools
        self.session.add(NationalSchools(1, 'Harvard University', 'Cambridge, MA', ''))
        self.session.add(NationalSchools(2, 'Princeton University', 'Princeton,\
                                         NJ', ''))
        self.session.add(NationalSchools(3, 'Yale University', 'New Haven, CT', ''))
        self.session.add(NationalSchools(4, 'Columbia University', 'New York, NY', ''))
        self.session.add(NationalSchools(5, 'Stanford University', 'Stanford, CA', ''))
        self.session.add(NationalSchools(6, 'University of Pennsylvania',
                                         'Philadelphia, PA', 'UPenn'))
        self.session.flush()

    def test_get_national_schools(self):
        from lifescore import views
        self._addSchools()
        schools = views.get_all_national_schools()
        self.assertEqual(len(schools['names']), 6)
        self.assertEqual(schools['names'][0], unicode('Harvard University'))
        self.assertEqual(schools['short_names'][5], unicode('UPenn'))

    def test_get_school_rank(self):
        from lifescore import views
        self._addSchools()
        self.assertEqual(views.get_school_rank('Harvard University'), 500)
        self.assertEqual(views.get_school_rank('UPenn'), 495)
        self.assertEqual(views.get_school_rank('Columbia University'), 497)
