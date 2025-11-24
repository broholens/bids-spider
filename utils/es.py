from dataclasses import asdict, is_dataclass
from typing import Iterable, Mapping, Optional, Union
from elasticsearch import Elasticsearch, helpers

from utils.log import logger

superuser_name = 'elastic'
superuser_pwd = '7aNJbD0LTxsVLyuRcHSQ'
host = 'http://127.0.0.1:9200'

DEFAULT_TENDER_INDEX = "tenders"
TENDER_INDEX_BODY = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
    },
    "mappings": {
        "dynamic": "false",
        "properties": {
            "region": {"type": "keyword"},
            "href": {"type": "keyword"},
            "text": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "release_date": {"type": "keyword"},
            "crawl_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time||epoch_millis"},
            "html": {"type": "text", "index": False},
        },
    },
}


class ESConnection:
    def __init__(self, index_name: str = DEFAULT_TENDER_INDEX):
        self.check_es_version()
        self.es: Optional[Elasticsearch] = None
        self.default_index = index_name

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

    def _client(self) -> Optional[Elasticsearch]:
        if self.es is None:
            self.create_connection()
        return self.es

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
            return self.es
        except Exception as e:
            logger.error(f"connection es failed: {e}")
            self.es = None
            return None

    def test_connection(self):
        """测试连接"""
        client = self._client()
        if not client:
            return False
        try:
            info = client.info()
            logger.info(f"connect Elasticsearch successfully, version: {info['version']['number']}, cluster_name: {info['cluster_name']}")
        except Exception as e:
            logger.error(f"connect Elasticsearch failed: {e}")
            return False
        return True
    
    def ensure_index(self, index_name: Optional[str] = None, body: Optional[dict] = None) -> bool:
        """确保索引存在，若不存在则按照提供的mapping创建"""
        client = self._client()
        if not client:
            return False
        index = index_name or self.default_index
        try:
            if client.indices.exists(index=index):
                return True
            mapping_body = body or TENDER_INDEX_BODY
            client.indices.create(index=index, body=mapping_body)
            logger.info(f"create index {index} successfully with mapping.")
            return True
        except Exception as e:
            logger.error(f"create index {index} failed: {e}")
            return False

    def create_index(self, index_name, body: Optional[dict] = None):
        """创建索引"""
        return self.ensure_index(index_name, body)

    def insert_data(self, index_name, data, doc_id: Optional[str] = None):
        """插入数据"""
        client = self._client()
        if not client:
            return None
        try:
            resp = client.index(index=index_name, id=doc_id, document=data)
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
    
    # Tender specific helpers

    def _tender_to_doc(self, tender: Union[Mapping, object]) -> Mapping:
        """将Tender类型（dataclass或dict）转换为ES文档"""
        if tender is None:
            raise ValueError("tender is None")
        if is_dataclass(tender):
            doc = asdict(tender)
        elif isinstance(tender, Mapping):
            doc = dict(tender)
        else:
            raise TypeError(f"Unsupported tender type: {type(tender)}")
        doc.setdefault("region", "")
        doc.setdefault("href", "")
        doc.setdefault("text", "")
        doc.setdefault("release_date", "")
        doc.setdefault("crawl_date", "")
        doc.setdefault("html", "")
        return doc

    def save_tender(self, tender: Union[Mapping, object], index_name: Optional[str] = None) -> Optional[str]:
        """单条保存Tender，使用href作为文档ID"""
        if not self.ensure_index(index_name):
            return None
        doc = self._tender_to_doc(tender)
        doc_id = doc.get("href")
        if not doc_id:
            logger.error("tender href is empty, skip saving.")
            return None
        target_index = index_name or self.default_index
        return self.insert_data(target_index, doc, doc_id=doc_id)

    def save_tenders_bulk(
        self,
        tenders: Iterable[Union[Mapping, object]],
        index_name: Optional[str] = None,
        chunk_size: int = 500,
    ) -> Optional[dict]:
        """批量保存Tender，使用href作为文档ID"""
        if not self.ensure_index(index_name):
            return None
        client = self._client()
        if not client:
            return None
        target_index = index_name or self.default_index

        actions = []
        for tender in tenders:
            doc = self._tender_to_doc(tender)
            doc_id = doc.get("href")
            if not doc_id:
                logger.warning("Encountered tender without href, skip.")
                continue
            actions.append({
                "_index": target_index,
                "_id": doc_id,
                "_source": doc,
            })

        if not actions:
            logger.info("No valid tender data to save.")
            return None

        try:
            resp = helpers.bulk(client, actions, chunk_size=chunk_size, raise_on_error=False, stats_only=False)
            logger.info(f"save {len(actions)} tenders to {target_index} successfully.")
            return {"took": resp[1], "success_count": resp[0], "failed_count": len(actions) - resp[0]}
        except Exception as e:
            logger.error(f"bulk save tenders failed: {e}")
            return None

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