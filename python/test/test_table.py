# Copyright(C) 2023 InfiniFlow, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import infinity
from infinity.common import REMOTE_HOST


class TestTable:

    def test_version(self):
        print(infinity.__version__)

    def test_table(self):
        """
        target: test table apis
        method:
        1. create tables
            - 'my_table'        √
                - c1 int primary key
                - c2 float
            - 'my_table!@#'     ❌
                - c1 int primary key
                - c2 float
            - 'my-table-dash'   ❌
                - c1 float primary key
                - c2 int
            - '123_table'       ❌
                - c1 int primary key
                - c2 float
            - 'bad_column'      ❌
                - 123 int primary key
                - c2 float
            - ''                ❌
                - c1 int primary key
                - c2 float
        2. list tables
            - 'my_table'
        3. drop tables
            - 'my_table'
        4. list tables: empty
        expect: all operations successfully
        """
        infinity_obj = infinity.connect(REMOTE_HOST)
        db_obj = infinity_obj.get_database("default")
        db_obj.drop_table("my_table")

        # infinity
        tb = db_obj.create_table(
            "my_table", {"c1": "int, primary key", "c2": "float"}, None)
        assert tb is not None

        try:
            tb = db_obj.create_table(
                "my_table!@#", {"c1": "int, primary key", "c2": "float"}, None)
        except Exception as e:
            print(e)
        try:
            tb = db_obj.create_table(
                "my-table-dash", {"c1": "float, primary key", "c2": "int"}, None)
        except Exception as e:
            print(e)
        try:
            tb = db_obj.create_table(
                "123_table", {"c1": "int, primary key", "c1": "float"}, None)
        except Exception as e:
            print(e)
        try:
            tb = db_obj.create_table(
                "bad_column", {"123": "int, primary key", "c2": "float"}, None)
        except Exception as e:
            print(e)
        try:
            tb = db_obj.create_table(
                "", {"c1": "int, primary key", "c2": "float"}, None)
        except Exception as e:
            print(e)

        # FIXME: res = db_obj.describe_table("my_table")

        res = db_obj.list_tables()
        assert res.success

        res = db_obj.drop_table("my_table")
        assert res.success

        res = db_obj.list_tables()
        assert res.success

        # disconnect
        res = infinity_obj.disconnect()

        assert res.success

    # create/drop/describe/get valid table name with different column types
    # create/drop/describe/get table with 10000 columns with various column types.
    # create/drop table with different invalid options
    # create/drop/describe/get 1000 tables with 10000 columns with various column types.

    # after disconnection, create / drop / describe / list / get table
    # create/drop table with invalid options
    # create created table, drop dropped table.
    # describe created table, describe not-created table, describe dropped table

    # create/drop same table in different thread to test conflict
    # create/drop/list/get 1M table to reach the limit
    # create/drop/list/get table with name in chinese.
    # create/drop/list/get table with column name in chinese.
    # create table with invalid column name, invalid column option.
    # create empty column table