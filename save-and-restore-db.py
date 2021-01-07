#based on https://gist.github.com/joymax/5037443

import argparse
import json
import sys
import StringIO

import couchdb


USAGE = """
    # Dump views
    couchdb-views.py --database-url=http://couch.example.com:5984 \\
        --database-name=MYDB dump --dump-to=MYDB_views.json
    # Restore views, --force - optional argument to override views
    couchdb-views.py --database-url=http://127.0.0.1:5984 \\
        --database-name=MYDB load --load-from=MYDB_views.json
**Important!** Tool work ok with UNIX Pipes, so:
    couchdb-views.py --database-url=http://couch.example.com:5984 \\
        --database-name=MYDB dump | couchdb-views.py \\
        --database-url=http://127.0.0.1:5984 \\
        --database-name=MYDB load
"""


def create_connection(options):
    """
    Create connection to Couchdb Server
    """
    server = couchdb.Server("http://admin:admin@localhost:5984")
    # TODO: here we can add authentication if need so
    # if login and password:
    #     server.resource.credentials = (options.db_login, options.db_password)

    return server


def dump(options):
    """
    Dump design documents to file-like ``destination`` object
    or write it to output
    """
    server = create_connection(options)
    database = server[options.database_name]
    out = None

    if options.dump_to is None:
        out = StringIO.StringIO()
    else:
        out = open(options.dump_to, "w")

    for designdoc in database.view('_all_docs', include_docs=True)[
            '_design': '_design0']:
        doc = designdoc.doc.copy()
        del doc["_rev"]
        out.write(json.dumps(doc) + "\n")

    if options.dump_to is None:
        out.seek(0)
        print out.read()

    out.close()


def restore(options):
    server = create_connection(options)
    database = server[options.database_name]

    load_from = None

    if options.load_from is None:
        load_from = sys.stdin
    else:
        load_from = open(options.load_from, "r")

    docs = map(unicode.strip, map(unicode, load_from.readlines()))
    for doc_raw in docs:
        if not doc_raw:
            continue

        doc = json.loads(doc_raw)
        try:
            print "Creating view {}".format(doc["_id"])
            database.save(doc)
        except couchdb.http.ResourceConflict:
            if options.force:
                print " * Trying to override: {}".format(doc["_id"])
                old_doc = database.get(doc["_id"])
                database.delete(old_doc)
                database.save(doc)
            else:
                print " ! View already exist: {}".format(doc["_id"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dump or restore Design Documents of CouchDB.")

    parser.add_argument(
        "--database-url", required=True,
        default="http://127.0.0.1:5984",
        help="Specify url to Couchdb")

    parser.add_argument(
        "--database-name",
        default=None, required=True,
        help="Specify Database Name")

    subparsers = parser.add_subparsers(help="sub-command help")
    parser_dump = subparsers.add_parser("dump", help="Dump design document")
    parser_dump.add_argument("--dump-to", default=None)
    parser_dump.set_defaults(func=dump)

    parser_restore = subparsers.add_parser(
        "load", help="Restore design documents")
    parser_restore.add_argument("--load-from", default=None)
    parser_restore.add_argument(
        "--force", default=False, action="store_true",
        help="Override existing views")
    parser_restore.set_defaults(func=restore)
    try:
        options = parser.parse_args()
        options.func(options)
    except:
        print "Usage:"
        print USAGE