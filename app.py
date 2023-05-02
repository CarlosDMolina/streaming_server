from quadtree import *
from flask import Flask, request, render_template
from convert import *
from concurrent.futures import ProcessPoolExecutor

app = Flask(__name__)


def process_frame(args):
    quadtree, filename, folder_path, destination_path, res = args
    file_path = os.path.join(folder_path, filename)
    img = cv2.imread(file_path)
    quadtree.insert(img, res)
    processed_frame = quadtree.reconstruct_image()
    newfile = f'{destination_path}/{filename}'
    cv2.imwrite(newfile, processed_frame)


def process_frames(folder_path, destination_path, res):

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    if res == 0:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            img = cv2.imread(file_path)
            newfile = f'{destination_path}/{filename}'
            cv2.imwrite(newfile, img)
        return "success"
    else:
        quadtree = Qtree()
        with ProcessPoolExecutor() as executor:
            tasks = [(quadtree, filename, folder_path, destination_path, res)
                     for filename in os.listdir(folder_path)]
            executor.map(process_frame, tasks)
        return "success"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_video', methods=['GET'])
def process_video():

    frame_folder = 'static/frames'
    dest = 'static/processed_frames'
    res = 100 - int(request.args.get('bandwidth', 0))
    msg = process_frames(frame_folder, dest, res)

    return msg


if __name__ == '__main__':
    app.run(debug=True)
