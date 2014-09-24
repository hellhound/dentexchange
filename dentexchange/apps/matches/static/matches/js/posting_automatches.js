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
        },
    error: ajax_error_handler
    });
    e.preventDefault();
}

$(document).ready(function() {
    make_active($("#id_employee_profile_automatches_menu"));

    $("#id_automatches_table tr").mouseenter(function(e) {
        $(this).find(".actions").show();
    })
    .mouseleave(function(e) {
        $(this).find(".actions").hide();
    });

    $("#id_automatches_table a.actions-save").click(function(e) {
        save(e, $(this));
    });

    $("#id_automatches_table a.remove").click(function(e) {
        delete_row(e, $(this));
    });
});
