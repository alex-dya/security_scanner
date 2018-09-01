$(document).ready(function () {
    var text_begin = 'Are you sure you want to delete result';
    get_translate(text_begin, function (data) {
        text_begin = data.translate;
    });

    function delete_result() {
        if (! confirm(`${text_begin}?`)){
            return;
        }
        var obj = this;
        $.post(('results/delete/' + this.id), function (data, status) {
            console.log('data:' + data.Message);
            $(obj).parents('tr').remove();
        }).fail(function (data, status) {
            alert(data.responseText);
            console.log('FAIL');
            console.log('data: ' + data.status);
            console.log('status: ' + status);
        });

    }

    $(".btn-delete").click(delete_result);
});
