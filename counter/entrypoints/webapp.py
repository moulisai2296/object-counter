from io import BytesIO
from flask import Flask, request, jsonify
from counter import config


def create_app():
    app = Flask(__name__)
    count_action = config.get_count_action()
    print(count_action)
    @app.route('/object-count', methods=['POST'])
    def object_detection():
        
        threshold = float(request.form.get('threshold', 0.5))
        uploaded_file = request.files['file']
        model_name = request.form.get('model_name', "rfcn")
        image = BytesIO()
        uploaded_file.save(image)
        print("******************** Mongo ***************************")
        count_response = count_action.execute(image, threshold)
        return jsonify(count_response)

    @app.route('/object-count-pg', methods=['POST'])
    def object_detection_pg():
        """
        This endpoint accepts an image file and a threshold value via a POST request. 
        It processes the image to detect objects using a predefined detection model.
        It uses Postgres to store the metadata.
        Returns:
            JSON response containing the detected object count.
        """
        threshold = float(request.form.get('threshold', 0.5))
        uploaded_file = request.files['file']
        image = BytesIO()
        uploaded_file.save(image)
        print("********************* PG **************************")
        count_response = count_action.execute(image, threshold)
        return jsonify(count_response)

    
    @app.route('/')
    def home():
        return """
        <h1>Object Detection API</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><code>POST /object-count</code> - Detect and count objects in images</li>
            <li><code>POST /predict</code> - Get raw predictions with bounding boxes</li>
        </ul>
        """
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', debug=True)
