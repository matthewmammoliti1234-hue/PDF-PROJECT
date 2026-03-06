from flask import Flask, render_template, request, send_from_directory, abort, after_this_request
import os
import subprocess
import logging
import time
from werkzeug.utils import secure_filename

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf converter")
LOG_FOLDER = "logs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

DEFAULT_PASSWORD = "mypassword123"

# Max upload size
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

# ------------------------
# Rate Limiter
# ------------------------

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20 per minute"]
)

limiter.init_app(app)


# ------------------------
# Logging setup
# ------------------------

logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, "server.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ------------------------
# Allowed extensions
# ------------------------

ALLOWED_EXTENSIONS = {
    "pdf_to_word": ["pdf"],
    "word_to_pdf": ["docx", "doc"],
    "image_to_pdf": ["png", "jpg", "jpeg", "bmp", "tiff"],
    "pdf_to_image": ["pdf"],
    "pdf_to_text": ["pdf"],
    "compress": ["pdf"],
    "rotate": ["pdf"],
    "lock_pdf": ["pdf"],
    "unlock_pdf": ["pdf"]
}


def allowed_file(filename, action):
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in ALLOWED_EXTENSIONS.get(action, [])


def check_mime_type(filepath, action):
    ext = filepath.rsplit(".", 1)[-1].lower()
    return ext in ALLOWED_EXTENSIONS.get(action, [])


def cleanup_old_files(folder, max_age=3600):
    """
    Delete files older than max_age seconds
    Default: 1 hour
    """
    now = time.time()

    for filename in os.listdir(folder):

        path = os.path.join(folder, filename)

        if os.path.isfile(path):

            if now - os.path.getmtime(path) > max_age:

                try:
                    os.remove(path)
                    logging.info(f"Deleted old file: {filename}")

                except Exception as e:
                    logging.warning(f"Failed to delete {filename}: {e}")


@app.route("/")
def index():
    return render_template("index.html")


# Limit upload endpoint
@app.route("/process", methods=["POST"])
@limiter.limit("10 per minute")
def process():

    cleanup_old_files(OUTPUT_FOLDER)
    cleanup_old_files(UPLOAD_FOLDER)

    input_path = None

    try:

        file = request.files.get("file")
        action = request.form.get("action")
        password = request.form.get("password")
        rotate_degrees = request.form.get("degrees")

        if not file or not action:
            return "No file or action selected", 400

        filename = secure_filename(file.filename)

        if not filename:
            return "Invalid file name", 400

        if not allowed_file(filename, action):
            return f"File type not allowed for {action}", 400

        input_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(input_path)

        logging.info(f"Upload received: {filename} for action {action}")

        if not check_mime_type(input_path, action):
            os.remove(input_path)
            return "File MIME type does not match extension", 400

        base_name = os.path.splitext(filename)[0]
        output_file = None
        script_path = None
        args = []

        if action == "pdf_to_word":
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}.docx")
            script_path = os.path.join(SCRIPT_FOLDER, "pdf_to_word.py")
            args = [input_path, output_file]

        elif action == "word_to_pdf":
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}.pdf")
            script_path = os.path.join(SCRIPT_FOLDER, "word_to_pdf.py")
            args = [input_path, output_file]

        elif action == "image_to_pdf":
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}.pdf")
            script_path = os.path.join(SCRIPT_FOLDER, "image_to_pdf.py")
            args = [input_path, output_file]

        elif action == "pdf_to_image":
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_images.zip")
            script_path = os.path.join(SCRIPT_FOLDER, "pdf_to_image.py")
            args = [input_path, output_file]

        elif action == "pdf_to_text":
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}.txt")
            script_path = os.path.join(SCRIPT_FOLDER, "pdf_to_text.py")
            args = [input_path, output_file]

        elif action == "compress":
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_compressed.pdf")
            script_path = os.path.join(SCRIPT_FOLDER, "compress_pdf.py")
            args = [input_path, output_file]

        elif action == "rotate":

            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_rotated.pdf")

            script_path = os.path.join(SCRIPT_FOLDER, "rotate_pdf.py")

            degrees = rotate_degrees if rotate_degrees in ["90", "180", "270"] else "90"

            args = [input_path, degrees, output_file]

        elif action == "lock_pdf":

            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_locked.pdf")

            script_path = os.path.join(SCRIPT_FOLDER, "pdf_password.py")

            args = [input_path, output_file, "lock", password or DEFAULT_PASSWORD]

        elif action == "unlock_pdf":

            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_unlocked.pdf")

            script_path = os.path.join(SCRIPT_FOLDER, "pdf_password.py")

            args = [input_path, output_file, "unlock", password or DEFAULT_PASSWORD]

        else:

            os.remove(input_path)
            return "Action not implemented", 400

        if not os.path.exists(script_path):

            os.remove(input_path)
            logging.error(f"Script missing: {script_path}")
            return "Server configuration error", 500

        result = subprocess.run(
            ["python", script_path] + args,
            capture_output=True,
            text=True,
            timeout=30
        )

        os.remove(input_path)

        if result.returncode != 0:

            logging.error(
                f"Subprocess failed.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )

            return "Error processing file", 500

        if not os.path.exists(output_file):

            logging.error("Output file not created")
            return "Processing failed", 500

        logging.info(f"Processing completed: {output_file}")

        @after_this_request
        def remove_file(response):

            try:

                os.remove(output_file)
                logging.info(f"Deleted output file: {output_file}")

            except Exception as e:

                logging.warning(f"Cleanup failed: {e}")

            return response

        return send_from_directory(
            OUTPUT_FOLDER,
            os.path.basename(output_file),
            as_attachment=True
        )

    except subprocess.TimeoutExpired:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        logging.error("Processing timeout")

        return "Processing timed out", 500

    except Exception as e:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        logging.error(f"Server error: {str(e)}")

        return "Server error occurred", 500


# Rate limit handler
@app.errorhandler(429)
def ratelimit_handler(e):
    logging.warning("Rate limit exceeded")
    return "Too many requests. Please slow down.", 429


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
