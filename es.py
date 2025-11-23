from ast import main
from elasticsearch import Elasticsearch

from utils.log import logger

superuser_name = 'elastic'
superuser_pwd = '7aNJbD0LTxsVLyuRcHSQ'
host = 'http://127.0.0.1:9200'


class ESConnection:
    def __init__(self):
        self.check_es_version()
        self.es = None

    def check_es_version(self):
        """检查elasticsearch版本，用于诊断"""
        try:
            import elasticsearch
            version = elasticsearch.__version__
            if version[0] >= 9:
                logger.warning(f"warning: detect elasticsearch version {version}, may be incompatible with ES 8.x")
                logger.warning("Try pip uninstall elasticsearch -y && pip install 'elasticsearch<9.0.0'")
                return False
            return True
        except Exception as e:
            logger.error(f"check es version failed: {e}")
            return True

    def create_connection(self):
        """连接Elasticsearch"""
        try:
            self.es = Elasticsearch(
                host,
                basic_auth=(superuser_name, superuser_pwd),
                request_timeout=10,
                max_retries=3,
                retry_on_timeout=False,
                http_compress=False,
            )
            return self
        except Exception as e:
            logger.error(f"connection es failed: {e}")
            return None

    def test_connection(self):
        """测试连接"""
        try:
            info = self.es.info()
            logger.info(f"connect Elasticsearch successfully, version: {info['version']['number']}, cluster_name: {info['cluster_name']}")
        except Exception as e:
            logger.error(f"connect Elasticsearch failed: {e}")
            return False
        return True
    
    def create_index(self, index_name):
        """创建索引"""
        try:
            resp = self.es.indices.create(index=index_name)
            logger.info(f"create index {index_name} successfully, response: {resp}")
        except Exception as e:
            logger.error(f"create index {index_name} failed: {e}")
            return False
        return True

    def insert_data(self, index_name, data):
        """插入数据"""
        try:
            resp = self.es.index(index=index_name, document=data)
            logger.info(f"insert data to {index_name} successfully, response: {resp}")
            return resp['_id']
        except Exception as e:
            logger.error(f"insert data to {index_name} failed: {e}")
            return None
    
    def delete_data(self, index_name, id):
        """删除数据"""
        try:
            resp = self.es.delete(index=index_name, id=id)
            logger.info(f"delete data from {index_name} successfully, response: {resp}")
            return resp['_id']
        except Exception as e:
            logger.error(f"delete data from {index_name} failed: {e}")
            return None
    
    def update_data(self, index_name, id, data):
        """更新数据"""
        try:
            resp = self.es.update(index=index_name, id=id, doc=data)
            logger.info(f"update data in {index_name} successfully, response: {resp}")
            return resp['_id']
        except Exception as e:
            logger.error(f"update data in {index_name} failed: {e}")
            return False
    
    def search_data(self, index_name, query):
        """搜索数据"""
        try:
            result = self.es.search(index=index_name, body=query)
            logger.info(f"search data in {index_name} successfully, response: {result}")
            return result['hits']['hits']
        except Exception as e:
            logger.error(f"search data in {index_name} failed: {e}")
            return None
    
    def delete_index(self, index_name):
        """删除索引"""
        try:
            resp = self.es.indices.delete(index=index_name)
            logger.info(f"delete index {index_name} successfully, response: {resp}")
            return True
        except Exception as e:
            logger.error(f"delete index {index_name} failed: {e}")
            return False

    def close_connection(self):
        """关闭连接"""
        try:
            self.es.close()
            logger.info("close connection successfully")
            return True
        except Exception as e:
            logger.error(f"close connection failed: {e}")
            return False
    
    def __del__(self):
        self.close_connection()


if __name__ == "__main__":
    es = ESConnection()
    es.create_connection()
    es.test_connection()
    es.create_index("test")
    _id = es.insert_data("test", {"name": "test"})
    es.update_data("test", _id, {"name": "test2"})
    es.search_data("test", {"query": {"match_all": {}}})
    es.delete_data("test", _id)
    es.delete_index("test")
    es.close_connection()