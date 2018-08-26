from flask import render_template
from flask_babel import get_locale
from flask_weasyprint import render_pdf, HTML

from web.models import Control

generators = dict()


def generator(text):
    def real_decorator(func):
        if text in generators:
            raise ValueError(f'{text} already exist in generators')

        generators[text] = func
        return func

    return real_decorator


@generator('PDF')
def generate_pdf(result):
    controls = {
        item.number: item
        for item in Control.query.filter_by(language=get_locale())
    }

    data = render_template(
        'results/document.html',
        all_controls=controls,
        results=result
    )

    return render_pdf(HTML(string=data))

