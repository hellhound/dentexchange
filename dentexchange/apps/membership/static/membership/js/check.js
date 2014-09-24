$(document).bind('ajaxSuccess', function(event, request, settings) {
    if (request.getResponseHeader('CURRENT') == null
            && settings.url != '/ajax_upload/') {
        window.location.href = '/membership/';
    }
});
