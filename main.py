from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class DBModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {name}, views = {views}, likes = {likes})"

#db.create_all() # used for onl once to create models in db

put_validate = reqparse.RequestParser()
put_validate.add_argument("name", type=str, help="Name of the video is required", required=True)
put_validate.add_argument("views", type=int, help="Views of the video", required=True)
put_validate.add_argument("likes", type=int, help="Likes on the video", required=True)

update_validate = reqparse.RequestParser()
update_validate.add_argument("name", type=str, help="Name of the video is required")
update_validate.add_argument("views", type=int, help="Views of the video")
update_validate.add_argument("likes", type=int, help="Likes on the video")

out_fields_serialize = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):
	@marshal_with(out_fields_serialize)
	def get(self, video_id):
		result = DBModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Could not find video with that id")
		return result

	@marshal_with(out_fields_serialize)
	def put(self, video_id):
		args = put_validate.parse_args()
		result = DBModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id taken...")

		video = DBModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		db.session.add(video)
		db.session.commit()
		return video, 201

	@marshal_with(out_fields_serialize)
	def patch(self, video_id):
		args = update_validate.parse_args()
		result = DBModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['views']:
			result.views = args['views']
		if args['likes']:
			result.likes = args['likes']

		db.session.commit()

		return result


	def delete(self, video_id):
		abort_if_video_id_doesnt_exist(video_id)
		del videos[video_id]
		return '', 204


api.add_resource(Video, "/asset/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)