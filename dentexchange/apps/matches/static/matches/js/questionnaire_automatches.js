function reset_id_praxis(praxes) {
    $("#id_praxes").empty().append($("<option></option>").attr(
        "value", "").html(all_praxes_caption));

    $.each(praxes, function(index, praxis) {
        var item = $("<option></option>").attr("value", praxis.pk).html(
            praxis.company_name);

        $("#id_praxes").append(item);
    });
}

function reset_id_job_posting(praxes, praxis_pk) {
    $("#id_job_postings").empty().append($("<option></option>").attr(
        "value", "").html(all_job_postings_caption));

    $.each(praxes, function(index, praxis) {
        $.each(praxis.job_postings, function(index, job_posting) {
            if (praxis_pk == undefined || praxis_pk == praxis.pk) {
                var item = $("<option></option>").attr(
                    "value", job_posting.pk).html(job_posting.position_name);

                $("#id_job_postings").append(item);
            }
        });
    });
}

function set_dropdown_values_from_querystring() {
    var praxis_pk = Number($.QueryString["praxis_pk"]);
    var job_posting_pk = Number($.QueryString["job_posting_pk"]);

    if (praxis_pk != NaN && praxis_pk > 0) {
        $("#id_praxes").val(String(praxis_pk));
    }
    if (job_posting_pk != NaN && job_posting_pk > 0) {
        $("#id_job_postings").val(String(job_posting_pk));
    }
}

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
    make_active($("#id_employer_profile_automatches_menu"));

    $("#id_automatches_table tr").mouseenter(function(e) {
        $(this).find(".actions").show();
    })
    .mouseleave(function(e) {
        $(this).find(".actions").hide();
    });

    reset_id_praxis(praxes);
    reset_id_job_posting(praxes);
    set_dropdown_values_from_querystring();
    $(".chosen-select").chosen({width: "300px"});

    $("#id_praxes").change(function(e) {
        praxis_pk = Number($(this).val());
        reset_id_job_posting(praxes, praxis_pk);
        $("#id_job_postings").trigger("chosen:updated").attr("value", ""
        );
    });

    $("#id_job_postings").change(function(e) {
        $("#id_filter").submit();
    });
});

$(document).ready(function() {
    $("#id_automatches_table a.actions-save").click(function(e) {
        save(e, $(this));
    });

    $("#id_automatches_table a.remove").click(function(e) {
        delete_row(e, $(this));
    });
});
