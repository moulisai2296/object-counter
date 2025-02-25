from typing import List
import psycopg2
from counter.domain.models import ObjectCount
from counter.domain.ports import ObjectCountRepo

class CountPostgresRepo(ObjectCountRepo):
    def __init__(self, host, port, database, user, password):
        """Initialize PostgreSQL connection parameters"""
        self.conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self._create_tables()

    def _create_tables(self):
        """Initialize the database schema"""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                # Create table matching the ObjectCount model
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS object_counts (
                        id SERIAL PRIMARY KEY,
                        object_class VARCHAR(100) UNIQUE,
                        count INTEGER NOT NULL DEFAULT 0,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            conn.commit()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        """
        Read object counts, optionally filtered by object classes
        Args:
            object_classes: Optional list of classes to filter by
        Returns:
            List of ObjectCount with object_class and count
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                if object_classes:
                    # Filter by specific classes
                    placeholders = ','.join(['%s'] * len(object_classes))
                    cur.execute(f"""
                        SELECT object_class, count 
                        FROM object_counts 
                        WHERE object_class IN ({placeholders})
                    """, object_classes)
                else:
                    # Get all classes
                    cur.execute("""
                        SELECT object_class, count 
                        FROM object_counts
                    """)
                
                results = cur.fetchall()
                return [ObjectCount(object_class=row[0], count=row[1]) 
                       for row in results]

    def update_values(self, new_values: List[ObjectCount]):
        """
        Update object counts with new values
        Args:
            new_values: List of ObjectCount with updated counts
        """
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                for value in new_values:
                    # Upsert - insert or update if exists
                    cur.execute("""
                        INSERT INTO object_counts (object_class, count)
                        VALUES (%s, %s)
                        ON CONFLICT (object_class) 
                        DO UPDATE SET count = object_counts.count + 1, updated_at = CURRENT_TIMESTAMP;
                    """, (value.object_class, value.count))
            conn.commit()