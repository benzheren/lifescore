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
        set_cache_regions_from_settings(_cache_settings())
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        import transaction
        transaction.abort()
        testing.tearDown()

    def _addSchools(self):
        from lifescore.models import NationalSchools, WorldSchools
        self.session.add(NationalSchools(1, 'Harvard University', 
            'Cambridge, MA', ''))
        self.session.add(NationalSchools(2, 'Princeton University', 
            'Princeton, NJ', ''))
        self.session.add(NationalSchools(3, 'Yale University', 'New Haven, CT',
            ''))
        self.session.add(NationalSchools(4, 'Columbia University', 
            'New York, NY', ''))
        self.session.add(NationalSchools(5, 'Stanford University',
            'Stanford, CA', ''))
        self.session.add(NationalSchools(6, 'University of Pennsylvania',
                                         'Philadelphia, PA', 'UPenn'))
        self.session.add(NationalSchools(7,"California Institute of Technology",
            "Pasadena, CA","Caltech"))
        self.session.add(NationalSchools(8, "Massachusetts Institute of \
                Technology", "Cambridge, MA", "MIT"))
        self.session.add(WorldSchools(1, "University of Cambridge", 
            "United Kingdom", ""))
        self.session.add(WorldSchools(2, "Harvard University", "United States",
            ""))
        self.session.add(WorldSchools(3, "Yale University", "United States", 
            ""))
        self.session.add(WorldSchools(4, "University College London", 
            "United Kingdom", ""))
        self.session.add(WorldSchools(5, "Massachusetts Institute of \
                Technology", "United States","MIT"))
        self.session.flush()

    def test_get_national_schools(self):
        from lifescore import views
        self._addSchools()
        schools = views.get_all_national_schools()
        self.assertEqual(len(schools['names']), 8)
        self.assertEqual(schools['names'][0], unicode('Harvard University'))
        self.assertEqual(schools['short_names'][5], unicode('UPenn'))

    def test_get_world_schools(self):
        from lifescore import views
        self._addSchools()
        schools = views.get_all_world_schools()
        self.assertEqual(len(schools['names']), 5)
        self.assertEqual(schools['names'][0], u'University of Cambridge')
        self.assertEqual(schools['short_names'][4], u'MIT')

    def test_get_school_rank(self):
        from lifescore import views
        self._addSchools()
        self.assertEqual(views.get_school_rank('Harvard University'), 500)
        self.assertEqual(views.get_school_rank('UPenn'), 495)
        self.assertEqual(views.get_school_rank('Columbia University'), 497)
        self.assertEqual(views.get_school_rank('MIT'), 496)
        self.assertEqual(views.get_school_rank('Random school name'), 0)
