from functools import lru_cache

import psycopg2
from typing import Dict, Any, Optional, List, Tuple

from scanner.types import BaseTransport


class PostgresTransport(BaseTransport):
    def __init__(self, config: Dict[str, Any], *args, timeout=10, **kwargs):
        super().__init__(*args, **kwargs)
        postgres_config = config.get('postgres', dict())
        self._login = postgres_config.get('username', '')
        self._password = postgres_config.get('password', '')
        self._address = config['hostname']
        self._db = postgres_config.get('dbname', 'postgres')
        self._port = int(postgres_config.get('port', '5432'))
        self._timeout = timeout
        self._client: Optional[psycopg2._psycopg.connection] = None

    def connect(self) -> None:
        if self._client:
            return

        self._client = psycopg2.connect(
            host=self._address,
            port=self._port,
            dbname=self._db,
            connect_timeout=self._timeout,
            user=self._login,
            password=self._password
        )

        self._client.set_session(readonly=True)

    @property
    def is_connect(self) -> bool:
        if self._client is None:
            return False

        return not self._client.closed

    def disconnect(self) -> None:
        if self._client is None:
            return

        self._client.close()

    @lru_cache(2048)
    def request(self, request: str) -> List[Tuple]:
        with self._client.cursor() as curr:
            curr.execute(request)
            return curr.fetchall()

    def __repr__(self) -> str:
        return f'PostgresTransport(hostname="{self._address}" port={self._port})'
