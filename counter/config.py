import os
from dotenv import load_dotenv
load_dotenv("prod.env")

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
from counter.adapters.count_repo_pg import CountPostgresRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects


def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:
    #fs_host = os.getenv('TFS_HOST', 'localhost')
    #fs_port = os.getenv('TFS_PORT', 8501)
    #mongo_host = os.getenv('MONGO_HOST', 'localhost')
    #mongo_port = os.getenv('MONGO_PORT', 27017)
    #mongo_db = os.getenv('MONGO_DB', 'prod_counter')
    tfs_host = os.getenv("TFS_HOST")
    tfs_port = os.getenv("TFS_PORT")
    data_store = os.getenv("DATA_STORE")
    if data_store == 'MONGO':
        #Get Mongo connection params when data store is Mongo DB
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = int(os.getenv("MONGO_PORT"))
        mongo_db = os.getenv("MONGO_DB")
        print(tfs_host,tfs_port,mongo_host,mongo_port,mongo_db)
        return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                    CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))
    elif data_store == 'PG':
        #Get PG connection params when data store is postgres DB
        pg_host = os.getenv("PG_HOST")
        pg_port = int(os.getenv("PG_PORT"))
        pg_db = os.getenv("PG_DB")
        pg_host=os.getenv('PG_HOST')
        pg_port=int(os.getenv('PG_PORT'))
        pg_db=os.getenv('PG_DB')
        pg_user=os.getenv('PG_USER')
        pg_password=os.getenv('PG_PASSWORD')
        return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                    CountPostgresRepo(host=pg_host, port=pg_port, database=pg_db, user=pg_user, password=pg_password))


def get_count_action() -> CountDetectedObjects:
    env = os.getenv("ENV")
    print(env)
    #env = os.getenv('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    print(count_action_fn)
    return globals()[count_action_fn]()
