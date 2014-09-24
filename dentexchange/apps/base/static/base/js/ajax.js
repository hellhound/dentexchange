function ajax_error_handler(jqXHR, textStatus, errorThrown) {
        $("<div>Something went wrong, please try again.</div>").dialog({
            modal: true,
            title: "Error"
        });
}
