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

    var start_function = function () {
        var obj = $(this);
        $.ajax({
            type: "PUT",
            url: '/task_execute/' + this.id,
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify({"status": "Running"})
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
        $('.startbtn').each(function () {
            var obj = $(this);
            $.getJSON('/task_execute/' + this.id).done(
                function (data) {
                    if (data.status !== 'Idle') {
                        start_to_stop(obj);
                    }
                }
            );
        });
        $('.stopbtn').each(function () {
            var obj = $(this);
            $.getJSON('/task_execute/' + this.id).done(
                function (data) {
                    if (data.status === 'Idle') {
                        stop_to_start(obj);
                    }
                }
            );
        })

    }, 5000)
});
