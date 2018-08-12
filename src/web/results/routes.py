from flask import render_template, jsonify
from flask_login import login_required, current_user

from web import app, db
from web.models import TaskResult


@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    return render_template(
        'results/result_list.html',
        results=current_user.results
    )


@app.route('/results/delete/<result_id>', methods=['POST'])
@login_required
def delete_results(result_id):
    if result_id is None:
        return jsonify({'Message': 'Id must be not null'}), 400

    result = TaskResult.query.get(result_id)
    if result is None:
        return jsonify(
            {'Message': 'There is not task result with the id.'}), 400

    db.session.delete(result)
    db.session.commit()

    return jsonify(
        {'Message': f'The result with id {result_id} has been removed'})
