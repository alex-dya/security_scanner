function get_translate(data, callback) {
    $.getJSON('/translate', {'text': data}, callback);
}
