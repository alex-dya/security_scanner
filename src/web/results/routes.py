from flask import render_template, jsonify, abort
from flask_login import login_required, current_user

from web import app, db, get_locale
from web.models import TaskResult, Control
from web.results import exports
from web.results.forms import ExportForm

ACTIVE = 'results'


@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    return render_template(
        'results/result_list.html',
        results=current_user.results,
        active=ACTIVE,
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


@app.route('/results/show/<int:result_id>', methods=['GET'])
@login_required
def results_show(result_id):
    result = TaskResult.query.get(result_id)

    if not result:
        abort(404)

    if result.owner_id != current_user.id:
        abort(404)

    controls = {
        item.number: item
        for item in Control.query.filter_by(language=get_locale())
    }
    return render_template(
        'results/show.html',
        result=result,
        all_controls=controls,
        active=ACTIVE,
    )


@app.route('/result/export/<int:result_id>', methods=['GET', 'POST'])
@login_required
def result_export(result_id):
    result = TaskResult.query.get(result_id)

    if not result:
        abort(404)

    if result.owner_id != current_user.id:
        abort(404)

    form = ExportForm()

    if not form.validate_on_submit():
        return render_template(
            'results/export.html',
            form=form,
            active=ACTIVE,
        )

    generator = exports.generators[form.format.data]
    return generator(result)
