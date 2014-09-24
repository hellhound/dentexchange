$(document).ready(function() {
    var opts = {
        lines: 13, // The number of lines to draw
        length: 40, // The length of each line
        width: 10, // The line thickness
        radius: 25, // The radius of the inner circle
        trail: 60, // Afterglow percentage
        speed: .9,
        top: "auto", // Top position relative to parent in px
        left: "auto" // Left position relative to parent in px
    };
    var spinner = new Spinner(opts).spin();
    var timer = null;
    var anchor = $("#wrap");
    var button = $("#id_refresh_automatch");
    var container = $("<div id=\"id_spinner_container\">")
        .css("width", 60).css("height", 60)
        .css("position", "absolute").css("left", window.innerWidth / 2)
        .css("top", window.innerHeight / 2);

    container.append(spinner.el);
    button.click(function(e) {
        button.prop("disabled", true);
        anchor.append(container);
        $.ajax(button.closest("form").attr("action"), {
            success: function(data, textStatus, jqXHR) {
                timer = window.setInterval(function() {
                    $.ajax(refresh_automatches_beacon_url, {
                        success: function(data, textStatus, jqHXR) {
                            if (data.done) {
                                spinner.stop();
                                container.remove();
                                window.clearInterval(timer);
                                window.location.reload();
                            }
                        }
                    });
                }, 1000);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                button.prop("disabled", false);
                ajax_error_handler(jqXHR, textStatus, errorThrown);
            }
        });
    });
});
