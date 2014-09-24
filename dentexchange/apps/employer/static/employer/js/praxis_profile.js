$(document).ready(function() {
    make_active($("#id_employer_profile_praxis_profile_menu"));

    $("#id_praxes_table tr").mouseenter(function(e) {
        $(this).find(".actions").show();
    })
    .mouseleave(function(e) {
        $(this).find(".actions").hide();
    });

    $("#id_praxes_table a.remove").click(function(e) {
        var link = $(this);
        var should_delete = confirm(
            "Do you really want to delete this practice?");

        if (should_delete) {
            $.ajax(link.attr("href"), {
                success: function(data, textStatus, jqXHR) {
                    link.closest("tr").remove();
                },
                error: ajax_error_handler
            });
        }
        e.preventDefault();
        e.stopPropagation();
    });
});

$(document).ready(function() {
    $("#id_praxes_table tr").click(function(e) {
        window.location = $(this).find("a.job-posting-list").attr("href");
    });

    $("#id_praxes_table a.job-posting-list").click(function(e) {
        e.preventDefault();
    });
});
