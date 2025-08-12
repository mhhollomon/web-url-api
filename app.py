from flask import Flask, request, jsonify
from flask_cors import cross_origin
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, create_engine, select, func
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

class Bookmark(Base):
    __tablename__ = "bookmark"

    bid  : Mapped[int] = mapped_column(primary_key=True)
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

    tid    : Mapped[int] = mapped_column(primary_key=True)
    name   : Mapped[str]
    bkm_id : Mapped[int] = mapped_column(ForeignKey("bookmark.bid"), 
                                         nullable=False, 
                                        )
##--------------------------------------
## Routes
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
            data.append({"count": t.count, "name": t.name, "id" : fake_id})
            fake_id += 1
        return jsonify(data)

# @app.route("/urls", methods=["POST"])
# def create_url():
#     if not request.is_json:
#         return jsonify({"error": "Invalid request"}), 400
#     data = request.get_json()
#     url = data.get("url")
#     tags = data.get("tags")
#     description = data.get("description")
#     if not url or not tags:
#         return jsonify({"error": "Missing required fields"}), 400
#     new_url = URL(url=url, desc=description) # type: ignore
#     for tag in tags:
#         new_tag = Tag(name=tag, url=new_url) # type: ignore
#         db.session.add(new_tag)
#     db.session.add(new_url)
#     db.session.commit()
#     return jsonify({"id": new_url.id, "url": new_url.url, 
#                     "date_created": new_url.date_created.isoformat(), 
#                     "description": new_url.desc, 
#                     "tags": tags}), 201

# @app.route("/urls/<int:url_id>", methods=["PUT"])
# def update_url(url_id):
#     url = URL.query.get(url_id)
#     if not url:
#         return jsonify({"error": "URL not found"}), 404
#     if not request.is_json:
#         return jsonify({"error": "Invalid request"}), 400
#     data = request.get_json()
#     new_url = data.get("url")
#     new_tags = data.get("tags")
#     new_desc = data.get("description")
#     if new_url:
#         url.url = new_url
#     if new_desc:
#         url.description = new_desc
#     if new_tags:
#         url.tags = []
#         for tag in new_tags:
#             new_tag = Tag(name=tag, url=url) # type: ignore
#             db.session.add(new_tag)
#     db.session.commit()
#     return jsonify({"id": url.id, "url": url.url, "date_created": url.date_created.isoformat(), 
#                     "description": new_url.description, 
#                     "tags": [t.name for t in url.tags]})

# @app.route("/urls/<int:url_id>", methods=["DELETE"])
# def delete_url(url_id):
#     url = URL.query.get(url_id)
#     if not url:
#         return jsonify({"error": "URL not found"}), 404
#     db.session.delete(url)
#     db.session.commit()
#     return jsonify({"message": "URL deleted"})


if __name__ == "__main__":
    with app.app_context():
        Base.metadata.create_all(engine)

    options : Dict[str, Any] = {}

    prefix : str | None = os.getenv("WAITRESS_PREFIX")

    if prefix:
        options["url_prefix"] = prefix

    listen = os.getenv("WAITRESS_LISTEN")

    if listen:
        if listen.startswith("/"):
            options["unix_socket"] = listen
            options["unix_socket_perms"] = 0o666
        else :
            options["listen"] = listen

    print(f"startup options = {options}")

    if os.getenv("FLASK_ENV") == "production":
        from waitress import serve
        serve(app, **options)
    else :
        app.run(debug=True)
