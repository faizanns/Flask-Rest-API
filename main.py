from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)

# Configure SQLAlchemy with SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define the VideoModel class to represent videos in the database
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # __repr__ defines how to represent the VideoModel object when printed
    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

# Uncomment this line when running the code for the first time to create the database
#db.create_all()

# Argument parser for 'PUT' request (for adding new videos)
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video are required", required=True)

# Argument parser for 'PATCH' request (for updating existing videos)
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str)
video_update_args.add_argument("views", type=int)
video_update_args.add_argument("likes", type=int)

# Define how the output should be serialized (formatted) when returning video data
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Define the Video resource class, which handles HTTP requests
class Video(Resource):
    @marshal_with(resource_fields) # Automatically format the returned result
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")
        for key, value in args.items():
            if value:
                setattr(result, key, value)

        db.session.commit()
        return result, 200
    
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot delete")
        db.session.delete(result)
        db.session.commit()
        return {'message': 'Video deleted successfully'}, 204
    
# Add the Video resource to the API at the specified endpoint (/video/<int:video_id>)
api.add_resource(Video, "/video/<int:video_id>")

# Do not run the Flask app in debug mode when running the code in production
if __name__ == '__main__':
    app.run(debug=True)