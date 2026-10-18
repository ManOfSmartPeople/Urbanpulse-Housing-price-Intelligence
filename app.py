"""UrbanPulse — Housing Price Intelligence."""
from __future__ import annotations
from flask import Flask, jsonify, render_template, request
from urbanpulse import land_registry

app = Flask(__name__)
app.json.sort_keys = False


def error_response(message, status=400):
    return jsonify({'ok': False, 'error': message}), status


@app.route('/')
def index():
    return render_template('index.html', registry_info=land_registry.dataset_info())


@app.route('/api/registry/info')
def registry_info():
    return jsonify({
        'ok': True,
        'info': land_registry.dataset_info(),
        'result': land_registry.STATE.get('result'),
        'progress': land_registry.get_progress(),
    })


@app.route('/api/registry/path', methods=['POST'])
def registry_path():
    data = request.get_json(silent=True) or {}
    path = (data.get('path') or '').strip()
    if not path:
        return error_response('Enter the local path to the HM Land Registry CSV or ZIP file.')
    try:
        land_registry.set_path(path)
        return jsonify({'ok': True, 'info': land_registry.dataset_info()})
    except Exception as e:
        return error_response(str(e))


@app.route('/api/registry/run', methods=['POST'])
def registry_run():
    data = request.get_json(silent=True) or {}
    try:
        chunk = max(25_000, min(int(data.get('chunk_size', 250_000)), 1_000_000))
        sample = max(10_000, min(int(data.get('sample_size', 100_000)), 250_000))
        job_id = land_registry.start_background_run(chunk_size=chunk, sample_size=sample)
        return jsonify({'ok': True, 'started': True, 'job_id': job_id, 'progress': land_registry.get_progress()})
    except RuntimeError as e:
        return error_response(str(e), 409)
    except Exception as e:
        return error_response(f'Unable to start the housing intelligence pipeline: {e}', 400)


@app.route('/api/registry/progress')
def registry_progress():
    return jsonify({'ok': True, 'progress': land_registry.get_progress()})


@app.route('/api/registry/result')
def registry_result():
    return jsonify({'ok': True, 'result': land_registry.STATE.get('result')})


if __name__ == '__main__':
    print('=' * 68)
    print('  UrbanPulse — Housing Price Intelligence')
    print('  http://127.0.0.1:5000')
    print('  Ctrl+Shift+D → technical / viva view')
    print('=' * 68)
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True, use_reloader=False)
