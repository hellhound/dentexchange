$(document).ready(function() {
    make_active($("#id_employer_profile_praxis_profile_menu"));
});

$(document).ready(function() {
    $(".take-online-button,.take-offline-button").click(function(e) {
        var link = $(this);

        $.ajax(link.attr("href"), {
            success: function(data, textStatus, jqXHR) {
                posting = link.closest(".posting");
                if (link.hasClass("take-online-button")) {
                    posting.children(".take-offline-button").show();
                    posting.children(".glyphicon").removeClass(
                        "glyphicon-minus-sign").addClass("glyphicon-ok-sign");
                } else {
                    posting.children(".take-online-button").show();
                    posting.children(".glyphicon").removeClass(
                        "glyphicon-ok-sign").addClass("glyphicon-minus-sign");
                }
                link.hide();
            },
            error: ajax_error_handler
        });
        e.preventDefault();
    });
});

$(document).ready(function() {
    $("#id_postings_table tr").mouseenter(function(e) {
        $(this).find(".actions").show();
    })
    .mouseleave(function(e) {
        $(this).find(".actions").hide();
    });
});

$(document).ready(function() {
    $("#id_postings_table a.remove").click(function(e) {
        var link = $(this);
        var should_delete = confirm(
            "Do you really want to delete this job posting?");

        if (should_delete) {
            $.ajax(link.attr("href"), {
                success: function(data, textStatus, jqXHR) {
                    link.closest("tr").remove();
                },
                error: ajax_error_handler
            });
        }
        e.preventDefault();
    });
});
