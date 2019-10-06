import pytest
import python_scripts.pymongo_db as pymongo_db
import mongomock
from bson.son import SON


@mongomock.patch(on_new='create')
class TestDBInit:
    db = mongomock.MongoClient().db
    collection = db.foobar
    expected_index = {'_id_': {'v': 2, 'key': [('_id', 1)], 'ns': 'db.foobar'},
                       'post_id_text': {'v': 2,
                                        'unique': True,
                                        'key': [('post_id', 'text')],
                                        'ns': 'db.foobar',
                                        }}

    def test_init_db(self):
        pymongo_db.init_db(self.collection)

        initialized_index = self.collection.index_information()
        print(initialized_index)

        assert initialized_index == self.expected_index



@mongomock.patch(on_new='create')
class TestInsertClass:
    db = mongomock.MongoClient().db
    collection = db['reddit']
    submission = None

    def test_insert_empty_submission(self):
        assert pymongo_db.insert_reddit_submission_dict(self.submission,
                                                        self.collection) == "Error, submission object is None"

    def test_insert_example_submission(self):
        submission = {'post_id': 'd2awru',
                      'title': '[USA-ME][H] 1080 ROG Strix, Ryzen 7 2700x w/cooler, 16gb Trident Z RGB ram, 16gb Adata XPG RGB ram, MSI B350 Tomahawk [W] Paypal/Local Cash',
                      'self_text': "Hey HWS! I rebuilt my PC about a month ago and I wasn't sure what I was going to do with my old parts. However I've now decided to sell most of them here as they aren't doing me any good just stored away. Everything here I have used and tested and are in great working condition. All Prices are **including shipping** and **negotiable**. If you buy more than one thing I'll cut deals! \n\n[Timestamps](https://imgur.com/a/TywG2pq?fbclid=IwAR1rZt833zXyCvBi17y6qlLuMgzhUPhZtGng8JHsoNgBD4TRFgPjuaZIWdU)\n\n&#x200B;\n\n* GTX 1080 ROG STRIX - $325\n\nUsed this for about 5 months with no overclock or mining done with it. Worked great. Just decided to go with a 2070 Super in the new build\n\n* Ryzen 7 2700x w/ stock prism cooler - $180\n\nUsed this for about 5 months as well with no overclock on it. Again, worked great, just ended up going with Ryzen gen 3 for the new PC. Combo with the MOBO for $240\n\n* MSI B350 Tomahawk MOBO - $75\n\nThis MOBO has it's BIOS updated and worked well with the 2700x. Comes with the IO shield. Combo with the CPU for $240\n\n* 16gb Trident Z RGB ram at 3200mhz - $80\n\nThis set ran and looks great in the PC for the 5 months I used it. Decided to go with a 32gb set of 3600mhz ram with the new PC. \n\n* 16gb Adata XPG RGB ram at 3000mhz - $75\n\nOriginally bought these to use with the old PC but ended up going with the Trident Z set so these have really only been used to test that they work\n\n* Also have an unopened CM Masterfan Pro 140 3 in 1 set - $30\n\nBought this thinking I would use it and never even opened the box. Will combo with other items if interested. \n\n&#x200B;\n\nAll in all these were all from a PC I built 5-6 months ago and my inpatient self saw ryzen 3000 and the super series and impulse bought a new PC. Everything runs great and Like I said prices are plenty negotiable as I don't need them here anymore.",
                      'created': 1568164879.0,
                      'author_info': {'author_id': 't2_r4oab6v',
                                      'author_name': 'daewonmtg',
                                      'author_trade_info': 'Trades: 1'}}

        pymongo_db.insert_reddit_submission_dict(submission, self.collection)
        assert self.collection.find_one({'post_id': 'd2awru'})['post_id'] == submission['post_id']
