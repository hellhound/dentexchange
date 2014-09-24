$(document).ready(function() {
    make_active($("#id_employee_profile_dashboard_menu"));

    $("#id_dashboard_matches_table a.remove").click(function(e) {
        var link = $(this);

        $.ajax(link.attr("href"), {
            success: function(data, textStatus, jqXHR) {
                link.closest("tr").remove();
                $("#id_total_saved_matches").html(data.total);
            },
            error: ajax_error_handler
        });
        e.preventDefault();
    });
});
