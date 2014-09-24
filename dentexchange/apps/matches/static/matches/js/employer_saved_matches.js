$(document).ready(function() {
    make_active($("#id_employer_profile_saved_matches_menu"));

    $("#id_saved_matches_table tr").mouseenter(function(e) {
        $(this).find(".actions").show();
    })
    .mouseleave(function(e) {
        $(this).find(".actions").hide();
    });

    $("#id_saved_matches_table a.remove").click(function(e) {
        var link = $(this);

        $.ajax($("#id_saved_matches_table a.remove").attr("href"), {
            success: function(data, textStatus, jqXHR) {
                link.closest("tr").remove();
            },
            error: ajax_error_handler
        });
        e.preventDefault();
    });
});
