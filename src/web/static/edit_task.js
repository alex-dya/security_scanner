$(document).ready(function () {
    var counter = 1;
    $('.task-setting').each(function (index) {
        ++counter;
    });

    var delete_text = 'Delete';
    get_translate('Delete', function (data) {
        delete_text = data.translate;
    });

    var json = $('input[name="profiles"]').first().val();
    var profile_list = JSON.parse(json);

    $("#addrow").on("click", function () {
        var newRow = $("<tr class='task-setting'>");
        var cols = "";
        var rowName = 'settings-' + counter + '-';

        cols += '<th scope="row">' + counter + '</th>';
        cols += '<td><input type="text" name="' + rowName +
            'hostname" id="' + rowName + 'hostname" class="form-control"></td>';
        cols += '<td><select name="' + rowName + 'profile"' +
            ' id="' + rowName + 'profile" class="form-control">';

        profile_list.forEach(function (value) {
            cols += '<option value="' + value.id + '">' + value.name + '</option>'
        });
        cols += '</select></td>';
        cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="' + delete_text +'"></td>';

        newRow.append(cols);
        newRow.append("</tr>");
        $("#settings").append(newRow);
        counter++;
    });

    $('table[id="settings"]').on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();
        counter -= 1
    });

});
