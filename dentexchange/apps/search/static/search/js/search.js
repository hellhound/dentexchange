function save(e, link) {
    $.ajax(link.attr("href"), {
        success: function(data, textStatus, jqXHR) {
            link.hide();
            link.closest("tr").addClass("success");
            link.closest("tr").find("div.remove").show();
        },
        error: ajax_error_handler
    });
    e.preventDefault();
}

function delete_row(e, link) {
    $.ajax(link.attr("href"), {
        success: function(data, textStatus, jqXHR) {
            link.closest("tr").removeClass("success");
            link.closest("tr").find(".actions-save").show();
            link.closest("div.remove").hide();
            $("#id_total_items").html(
                'Results (' + data.total + ')');
        },
        error: ajax_error_handler
    });
    e.preventDefault();
}

function search(data) {
    var total = 0;
    var object_list = data.object_list;

    $("#id_results_table tbody").empty();
    if (object_list != undefined) {
        var row_template = $.templates("#search_row_tmpl");
        var content_template = $.templates("#search_content_tmpl");
        var actions_template = $.templates("#actions_tmpl");

        for (i = 0; i < object_list.length; i++) {
            var row = object_list[i];

            row.save_match_url_caption = save_match_url_caption;
            row.view_details_url_caption = view_details_url_caption;
            row.save_match_url = save_match_url + '?pk=' + row.pk;
            row.view_details_url = view_details_url + '?pk=' + row.pk;
            row.delete_url = delete_url + '?pk=' + row.pk;
            row.content = content_template.render(row)
                + actions_template.render(row);
            $("#id_results_table tbody").append(
                row_template.render(row));
        }
        $(".actions-save").click(function(e) {
            save(e, $(this));
        });

        $("#id_results_table a.remove").click(function(e) {
            delete_row(e, $(this));
        });

        $("#id_results_table tr").mouseenter(function(e) {
            $(this).find(".actions").show();
        })
        .mouseleave(function(e) {
            $(this).find(".actions").hide();
        });
        total = object_list.length;
    }
    if (total == 0) {
        var empty_results_template = $.templates("#empty_results_tmpl");

        $("#id_results_table tbody").html(empty_results_template.render(
            {empty_results_message: empty_results_message}));
    }
    $("#id_total_items").html('Results (' + total + ')');
}

function search_with_spinner(e, spinner, should_prevent_default) {
    var timer = null;
    var anchor = $("#wrap");
    var container = $("#id_spinner_container");
    var form = $("form");
   
    spinner.spin();
    if (container.length == 0) {
        container = $("<div id=\"id_spinner_container\">")
            .css("width", 60).css("height", 60)
            .css("position", "absolute").css("left", window.innerWidth / 2)
            .css("top", window.innerHeight / 2);
        container.append(spinner.el);
    }
    anchor.append(container);
    $.ajax(form.attr("action"), {
        data: form.serialize(),
        success: function(data, textStatus, jqXHR) {
            timer = window.setInterval(function() {
                $.ajax(results_beacon_url, {
                    success: function(data, textStatus, jqHXR) {
                        if (data.done) {
                            spinner.stop();
                            container.remove();
                            window.clearInterval(timer);
                            search(data.results);
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
    if (should_prevent_default) e.preventDefault();
}

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
    var spinner = new Spinner(opts);

    make_active($("#id_profile_search_menu"));

    $("#id_keywords,#id_location").keyup(function(e) {
        search_with_spinner(e, spinner, false);
    });

    $("#id_search_button").click(function(e) {
        debugger;
        $("#id_search_hidden").val("1");
        search_with_spinner(e, spinner, true);
    });
});

$(document).ready(function() {
    var hidden = true;

    $("#id_show_filters").click(function(e) {
        $("#id_filters").animate({
            height: ["toggle", "swing"]
        }, 200, "linear", function() {
            if (hidden) {
                $("#id_filter_button").removeClass("glyphicon-chevron-down")
                .addClass("glyphicon-chevron-up");
            } else {
                $("#id_filter_button").removeClass("glyphicon-chevron-up")
                .addClass("glyphicon-chevron-down");
            }
            hidden = !hidden;
        });
    });
    
    $("#id_reset_filters").click(function(e) {
        $("#id_job_position").val($("#id_job_position option:first").val());
        $("#id_full_time").attr("checked", false);
        $("#id_part_time").attr("checked", false);
        $("#id_experience_years")
        .val($("#id_experience_years option:first").val());
        $("#id_visa").attr("checked", false);
        $("#id_distance").val($("#id_distance option:first").val());
        e.preventDefault();
    });
});
