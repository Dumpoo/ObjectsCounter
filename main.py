from flask import Flask, render_template, url_for, request, redirect, make_response, send_file
from counter import calculate
import os
import io


class Storage:
    def __init__(self):
        self.image_name = None
        self.path = None
        self.quantity = None
        self.file = None
        self.format = None


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')
app.template_folder = os.path.join(app.root_path, 'templates')

storage = Storage()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('page_1.html')


@app.route('/p3', methods=['POST', 'GET'])
def p3():
    return render_template('page_3.html', image=storage.image_name, quantity=storage.quantity)


@app.route('/<img_name>', methods=['POST', 'GET'])
def sended_image(img_name):
    return send_file(storage.file, mimetype=f'image/{storage.format}]')


@app.route('/p2', methods=['POST', 'GET'])
def p2():
    if request.method == 'POST':
        screen_size = (int(request.form.get('width')), int(request.form.get('height')))

        cropCoords = [
            int(request.form.get('x1')),
            int(request.form.get('y1')),
            screen_size[0] - int(request.form.get('x2')),
            screen_size[1] - int(request.form.get('y2'))
        ]

        if cropCoords[2] < 0 or cropCoords[3] < 0:
            cropCoords[2], cropCoords[0] = cropCoords[0], cropCoords[0] + cropCoords[2]
            cropCoords[3], cropCoords[1] = cropCoords[1], cropCoords[1] + cropCoords[3]

        objects_quantity = calculate(
            project_path=app.root_path,
            image_path=storage.path,
            crop_coords=tuple(cropCoords),
            screen_size=screen_size,
            debug=False
        )

        storage.quantity, image = objects_quantity

        if storage.image_name[storage.image_name.index('.')+1:] == 'jpg':
            storage.format = 'JPEG'
        else:
            storage.format = storage.image_name[storage.image_name.index('.')+1:].upper()

        byte_image = io.BytesIO()
        image.save(byte_image, format=storage.format)
        byte_image.seek(0)
        storage.file = byte_image

        return make_response(' ', 200)
    return render_template('page_2.html', image=storage.image_name)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files.get('image')
        filename = file.filename
        storage.image_name = filename
        storage.path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(storage.path)

    return redirect(url_for('p2'))


if __name__ == '__main__':
    app.run(debug=True)


