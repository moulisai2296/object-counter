from io import BytesIO
from flask import Flask, request, jsonify, Response
from counter import config


def create_app():
    app = Flask(__name__)
    count_action = config.get_count_action()
    print(count_action)
    @app.route('/object-count', methods=['POST'])
    def object_detection():
        """
        This endpoint accepts an image file and a threshold value via a POST request. 
        It processes the image to detect objects using a predefined detection model.
        It uses Mongo DB to store the metadata.
        Returns:
            JSON response containing the detected object count.
        """
        try:
            threshold = float(request.form.get('threshold', 0.5))
            uploaded_file = request.files['file']
            model_name = request.form.get('model_name', "rfcn")
            image = BytesIO()
            uploaded_file.save(image)
            print("******************** Mongo ***************************")
            count_response = count_action.execute(image, threshold)
            return jsonify(count_response)
        except Exception as e:
            return Response("Internal Server Error", status=500)

    @app.route('/object-count-pg', methods=['POST'])
    def object_detection_pg():
        """
        This endpoint accepts an image file and a threshold value via a POST request. 
        It processes the image to detect objects using a predefined detection model.
        It uses Postgres to store the metadata.
        Returns:
            JSON response containing the detected object count.
        """
        try:
            threshold = float(request.form.get('threshold', 0.5))
            uploaded_file = request.files['file']
            image = BytesIO()
            uploaded_file.save(image)
            print("********************* PG **************************")
            count_response = count_action.execute(image, threshold)
            list_predictions = jsonify(count_response)
            data = list_predictions.get_json()
            current_objects = {"predictions": data.get("current_objects", [])}
            return jsonify(current_objects)
        except Exception as e:
            return Response("Internal Server Error", status=500)
        
    @app.route('/get_object_count', methods=['GET'])
    def get_objects():
        """
        This end point gets all the objects
        """
        try:
            object_class = request.args.get('object_class')
            if not object_class:
                object_class = None
            count_response = count_action.get_objects(object_class)
            return jsonify(count_response)
        except Exception as e:
            return Response("Internal Server Error", status=500)

    @app.route('/')
    def home():
        """
        Dummy Home
        """
        return """
        <h1>Object Detection using tensorflow</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><code>POST /object-count</code> - Detect and count objects in images</li>
            <li><code>POST /object-count-pg</code> - Get raw predictions with bounding boxes</li>
        </ul>
        """
    return app

if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', debug=True)
