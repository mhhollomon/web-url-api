from flask import Flask, request, jsonify
from flask_cors import cross_origin
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Integer, create_engine, select, func, delete, update
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dotenv import load_dotenv
from typing import Any, Dict, List
import os

class Base(MappedAsDataclass, DeclarativeBase):
  pass

##----------------------------
## Configuration code
##----------------------------
load_dotenv()
CONFIG = {
    "SECRET_KEY": os.getenv("SECRET"),
    "DB_NAME": os.getenv("DB_NAME"),
}
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite://{CONFIG['DB_NAME']}"

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)

##----------------------------
## Tables
##----------------------------

class Bookmark(Base):
    __tablename__ = "bookmark"
    __table_args__ = {"sqlite_autoincrement": True}

    bid  : Mapped[int] = mapped_column(Integer, primary_key=True)
    url  : Mapped[str]
    title : Mapped[str]
    description : Mapped[str]
    tags : Mapped[List["Tag"]] = relationship(
        lazy=True, 
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Tag.name"
        )
    date_created : Mapped[datetime] = mapped_column(nullable=False, 
                                                    default=datetime.now(timezone.utc))

class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = {"sqlite_autoincrement": True}

    tid    : Mapped[int] = mapped_column(primary_key=True)
    name   : Mapped[str]
    bkm_id : Mapped[int] = mapped_column(ForeignKey("bookmark.bid"), 
                                         nullable=False, 
                                        )

##--------------------------------------
##--------------------------------------
## Routes
##--------------------------------------
##--------------------------------------

##--------------------------------------
## Get all Bookmarks (with tags)
##--------------------------------------
@app.route("/bookmarks", methods=["GET"])
@cross_origin()
def get_urls():
    tags = request.args.get("tags")
    logic = request.args.get("logic") or "AND"
    logic = logic.upper()
    stmt = select(Bookmark)
    if tags:
        stmt = stmt
        tags = tags.split(",")
        if logic == "OR":
            # It must have at least one of the tags
            stmt = stmt.join(Tag).where(Tag.name.in_(tags))
        else:
            # It must have all of the tags
            tag_select = select(Tag.bkm_id).where(Tag.name.in_(tags)).group_by(Tag.bkm_id).having(func.count(Tag.tid) == len(tags))
            stmt = stmt.where(Bookmark.bid.in_(tag_select))

    stmt = stmt.distinct(Bookmark.bid)
    with Session(engine) as session:
        urls = session.execute(stmt.order_by(Bookmark.date_created.desc()))
        urls = urls.scalars().all()
        return jsonify([{"id": u.bid, 
                         "url": u.url, 
                        "date_created": u.date_created.isoformat(),
                        "description": u.description,
                        "title": u.title,
                        "tags": [t.name for t in u.tags]
                        } for u in urls])

##--------------------------------------
## Get all Tags (with count)
##--------------------------------------
@app.route("/tags", methods=["GET"])
@cross_origin()
def get_tags():
    stmt = select(Tag.name, func.count(Tag.tid).label("count")).group_by(Tag.name).order_by(func.count(Tag.tid).desc())
    with Session(engine) as session:
        tags = session.execute(stmt)
        tags = tags.all()
        #print(f"---- tags ---\n{tags}\n----\n")
        fake_id : int = 1
        data = []
        for t in tags:
            # The fake_id is to help out React or whatever front end library
            # is going to display them. I guess I could just use the name itself
            # as the id. *shrug*.
            # At some point I may pull out tags as a "lexicon" or something.
            data.append({"count": t.count, "name": t.name, "id" : fake_id})
            fake_id += 1
        return jsonify(data)

##--------------------------------------
## Delete a bookmark using id.
##
## POST data = {
##   "id" : 1,
##   "secret" : "secret"
## }
##--------------------------------------

@app.route("/delete", methods=["POST"])
@cross_origin()
def delete_bookmark():
    data = request.json
    if not data:
        return jsonify({"error": "Missing required fields"}), 400
    
    secret = data.get("secret")
    if secret != CONFIG["SECRET_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401
    
    bookmark_id = data.get("id")
    stmt = select(Bookmark).where(Bookmark.bid==bookmark_id).limit(1)
    with Session(engine) as session:
        result = session.execute(stmt)
        url = result.scalars().one_or_none()
        if not url:
            return jsonify({"error": "Bookmark not found"}), 404
        stmt = delete(Tag).where(Tag.bkm_id==bookmark_id)
        session.execute(stmt)
        session.delete(url)
        session.commit()
        return jsonify({"message": "URL deleted"})
    
##--------------------------------------
## Create a bookmark.
##
## If a bookmark already exists with the URL, an error is returned.
##
## POST data = {
##   "id" : -2, -- actually ignored
##   "url" : "http:/example.com/test",
##   "title" : "Example",
##   "description" : "cool stuff here!",
##   "tags" : ["tag1", "tag2"],
##   "secret" : "secret"
## }
##--------------------------------------

@app.route("/create", methods=["POST"])
@cross_origin()
def create_bookmark():
    data = request.json
    if not data:
        return jsonify({"error": "Missing required fields"}), 400
    
    secret = data.get("secret")
    if secret != CONFIG["SECRET_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    url = data.get("url")
    title = data.get("title")
    description = data.get("description")
    tags = data.get("tags")
    if not url:
        return jsonify({"error": "Missing required fields"}), 400
    with Session(engine) as session:
        test_url = session.execute(select(Bookmark).where(Bookmark.url==url)).scalars().one_or_none()
        if test_url:
            return jsonify({"error": "URL already exists"}), 400
        new_url = Bookmark(bid=None, url=url, title=title, description=description, tags=[]) # type: ignore
        session.add(new_url)
        new_url : Bookmark = session.execute(select(Bookmark).where(Bookmark.url==url)).scalars().one()
        for tag in tags:
            new_tag = Tag(tid=None, name=tag, bkm_id=new_url.bid) # type: ignore
            session.add(new_tag)
        session.commit()

        return jsonify({"id": new_url.bid, 
                    "url": new_url.url,
                    "title": new_url.title,
                    "date_created": new_url.date_created.isoformat(), 
                    "description": new_url.description, 
                    "tags": tags}), 201

##--------------------------------------
## Update an existing a bookmark.
##
## If the URL is changed, the system checks to see if
## a bookmark exists with the new URL. If so, it will return an error.
##
## POST data = {
##   "id" : 3,
##   "url" : "http:/example.com/test",
##   "title" : "Example",
##   "description" : "cool stuff here!",
##   "tags" : ["tag1", "tag2"],
##   "secret" : "secret"
## }
##--------------------------------------

@app.route("/update", methods=["POST"])
@cross_origin()
def edit_bookmark():
    data = request.json
    if not data:
        return jsonify({"error": "Missing required fields"}), 400
    
    secret = data.get("secret")
    if secret != CONFIG["SECRET_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    bookmark_id : str = str(data.get("id") or "-2")
    print(f'bookmark_id: {bookmark_id}')
    url = data.get("url")
    title = data.get("title")
    description = data.get("description")
    tags = data.get("tags")
    if not url:
        return jsonify({"error": "Missing required fields"}), 400
    with Session(engine) as session:
        test_url = session.execute(select(Bookmark).where(Bookmark.url==url)).scalars().one_or_none()
        print(f'test_url: {test_url}')
        if test_url and test_url.bid != int(bookmark_id):
            return jsonify({"error": "URL already exists"}), 400
        stmt = update(Bookmark).where(Bookmark.bid==bookmark_id).values(url=url, title=title, description=description)
        session.execute(stmt)
        stmt = delete(Tag).where((Tag.bkm_id==bookmark_id) & (~ Tag.name.in_(tags))).execution_options(is_delete_using=True)
        session.execute(stmt)
        stmt = select(Tag.name).where(Tag.bkm_id==bookmark_id)
        old_tags = session.execute(stmt).scalars().all()
        for tag in tags:
            if tag in old_tags:
                continue
            new_tag = Tag(tid=None, name=tag, bkm_id=bookmark_id) # type: ignore
            session.add(new_tag)
        session.commit()
        new_url : Bookmark = session.execute(select(Bookmark).where(Bookmark.bid==bookmark_id)).scalars().one()

        return jsonify({"id": new_url.bid, 
                    "url": new_url.url,
                    "title": new_url.title,
                    "date_created": new_url.date_created.isoformat(), 
                    "description": new_url.description, 
                    "tags": tags}), 200



if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(engine)

    is_prod = os.getenv("FLASK_ENV") == "production"

    options : Dict[str, Any] = {}

    prefix : str | None = os.getenv("WAITRESS_PREFIX")

    if is_prod and prefix :
        options["url_prefix"] = prefix

    listen = os.getenv("WAITRESS_LISTEN")

    if listen:
        if is_prod:
            if listen.startswith("/"):
                options["unix_socket"] = listen
                options["unix_socket_perms"] = '660'
            else :
                options["listen"] = listen
        else :
            # app.run() doesn't support listen, so split
            # into host and port.
            (host, port) = listen.split(":")
            options["host"] = host
            options["port"] = port
    print(f"startup options = {options}")

    if is_prod:
        from waitress import serve
        serve(app, **options)
    else :
        app.run(debug=True, **options)
