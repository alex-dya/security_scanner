$(document).ready(function () {
    function start_to_stop(obj) {
        obj.toggleClass('startbtn stopbtn');
        obj.toggleClass('btn-info btn-warning');
        obj.html('Stop');
        obj.unbind('click').click(stop_function);
    }

    function stop_to_start(obj) {
        obj.toggleClass('stopbtn startbtn');
        obj.toggleClass('btn-warning btn-info');
        obj.html('Run');
        obj.unbind('click').click(start_function);
    }

    function update_progressbar(id, progress) {
        var td_progress = $("#progressbar-" + id).first();
        var percents = Math.floor((progress.current / progress.total) * 100);
        var message = `<span>${progress.current} of ${progress.total}</span>`;
        td_progress.html(
            "<div class=\"progress\">\n" +
            "  <div class=\"progress-bar bg-info\" role=\"progressbar\" style=\"width: "
            + percents + "%\" aria-valuenow=\"" + progress.current
            + "\" aria-valuemin=\"0\" aria-valuemax=\"" + progress.total + "\">"
            + message + "</div>\n</div>"
        )
    }

    function delete_progessbar(id) {
        var td_progress = $("#progressbar-" + id).first();
        td_progress.html("")
    }

    var start_function = function () {
        var obj = $(this);
        $.ajax({
            type: "PUT",
            url: '/task_execute/' + this.id,
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify({"status": "Wait"})
        }).done(function (data) {
            start_to_stop(obj);
        }).fail(function (data) {
            alert('bad ' + data.responseText);
        });
    };

    var stop_function = function () {
        var obj = $(this);
        $.ajax({
            type: "PUT",
            url: '/task_execute/' + this.id,
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify({"status": "Idle"})
        }).done(function (data) {
            stop_to_start(obj);
        }).fail(function (data) {
            alert('bad ' + data.responseText);
        });

    };

    $(".startbtn").click(start_function);
    $(".stopbtn").click(stop_function);
    setInterval(function () {
        $('.stopbtn').each(function () {
            var obj = $(this);
            $.getJSON('/task_execute/' + this.id).done(
                function (data) {
                    console.log(data);
                    if (data.status === 'Idle') {
                        stop_to_start(obj);
                        delete_progessbar(data.task_id);
                    }
                    else if (data.status === 'Running') {
                        update_progressbar(data.task_id, data.progress);
                    }
                }
            );
        })
    }, 1000)
});
