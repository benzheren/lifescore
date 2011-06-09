import json
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

    def _addUsersAndFriends(self):
        from lifescore.models import User, Friend
        user_1 = User(1, None, None, 'user_1', None, None, 850)
        user_2 = User(2, None, None, 'user_2', None, None, 840)
        friends_1 = [Friend(i, 'name_%d' % i) for i in range(2, 32)]
        friends_2 = [Friend(i, 'name_%d' % i) for i in range(32, 51)]
        user_1.friends = friends_1
        user_2.friends = friends_2
        self.session.add(user_1)
        self.session.add(user_2)
        self.session.flush()

    def test_get_relationship(self):
        from lifescore import views
        profile = json.loads('{"relationship_status": "Married"}')
        self.assertEqual(views._get_relationship_score(profile), 1.3)
        profile = json.loads('{}')
        self.assertEqual(views._get_relationship_score(profile), 1)


    def test_get_national_schools(self):
        from lifescore import views
        self._addSchools()
        schools = views._get_all_national_schools()
        self.assertEqual(len(schools['names']), 8)
        self.assertEqual(schools['names'][0], unicode('Harvard University'))
        self.assertEqual(schools['short_names'][5], unicode('UPenn'))

    def test_get_world_schools(self):
        from lifescore import views
        self._addSchools()
        schools = views._get_all_world_schools()
        self.assertEqual(len(schools['names']), 5)
        self.assertEqual(schools['names'][0], u'University of Cambridge')
        self.assertEqual(schools['short_names'][4], u'MIT')

    def test_get_school_rank(self):
        from lifescore import views
        self._addSchools()
        self.assertEqual(views._get_school_rank('Harvard University'), 500)
        self.assertEqual(views._get_school_rank('UPenn'), 495)
        self.assertEqual(views._get_school_rank('Columbia University'), 497)
        self.assertEqual(views._get_school_rank('MIT'), 496)
        self.assertEqual(views._get_school_rank('Random school name'), 0)

    def test_get_education_score(self):
        from lifescore import views
        self._addSchools()
        profile = json.loads('{"education":\
                             [{"school": {"name": "MIT"}, "type": "College"},\
                             {"school": {"name": "Harvard University"}, \
                             "type": "Graduate School"}]}')
        self.assertEqual(views._get_education_score(profile), 1246)
        profile = json.loads('{}')
        self.assertEqual(views._get_education_score(profile), 0)

    def test_world_rank_fetch(self):
        from lifescore import views
        self._addUsersAndFriends()
        request = testing.DummyRequest()
        world_rank = views.world_rank_fetch(request)
        json.dumps(world_rank)
        self.assertEquals(len(world_rank), 20)
        self.assertEquals(world_rank[0]['id'], 1)
        self.assertEquals(world_rank[0]['score'], 850)
        request = testing.DummyRequest(params={'start' : '40'})
        world_rank = views.world_rank_fetch(request)
        self.assertEqual(len(world_rank), 11)

    def test_friends_rank_fetch(self):
        from lifescore import views
        self._addUsersAndFriends()
        
        request = testing.DummyRequest(params={'fb_id' : 1})
        friends_rank = views.friends_rank_fetch(request)
        json.dumps(friends_rank)
        self.assertEqual(len(friends_rank), 20)
        
        request = testing.DummyRequest(params={'fb_id' : 1, 'start' : '20'})
        friends_rank = views.friends_rank_fetch(request)
        self.assertEqual(len(friends_rank), 10)
        
        request = testing.DummyRequest(params={'fb_id' : 1, 'start' : '40'})
        friends_rank = views.friends_rank_fetch(request)
        self.assertEqual(len(friends_rank), 0)

        request = testing.DummyRequest(params={'fb_id' : 2})
        friends_rank = views.friends_rank_fetch(request)
        self.assertEqual(len(friends_rank), 19)
        
 



