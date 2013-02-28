
$(document).ready(function() {
    // $('a.edit-report').prepOverlay({
    //          subtype: 'ajax',
    //          filter: '#content>*',
    //          formselector: 'form',
    //          noform: 'reload'
    //         });

//     $('a.view-report').prepOverlay({
//          subtype: 'ajax',
//          filter: '#content>*',
//          formselector: 'form',
//          noform: 'reload'
//         });

    $('.add-report-button a').prepOverlay({
        subtype: 'ajax',
        filter: '#content>*',
        formselector: 'form',
        config: {onLoad: function() {
            $.getScript(portal_url+"/++resource++openmultimedia.reporter/omupload.js", function(){
                // XXX: Eventually, we might have several widgets
                //      for now, we have only one.
                $.getScript(portal_url+"/@@render-upload-js.js?widget_id="+$(".upload-widget")[0].id);
            });
        }}
        });

    $(".report-item").click(function(e) {
        var url = $(this).attr("data-url");
        $(".main-report").children().css("display", "none");
        $("#loading").css("display", "block");
        $.ajax({
            url: url + "/ajax-report",
            success:function(data) {
                $(".main-report").html(data);            }
        });
    });

    var pairs = $(".report-pair");
    $("#reports-window").width(pairs.width()*pairs.length);

    $("#report-arrow-next-link").click(function(e) {
        e.preventDefault();
        var pairWidth = $(".report-pair").width();
        var scrollWidth = $("#report-reports").scrollLeft() + pairWidth;
        $("#report-reports").animate({scrollLeft: scrollWidth}, 500);
        return false;
    });

    $("#report-arrow-prev-link").click(function(e) {
        e.preventDefault();
        var pairWidth = $(".report-pair").width();
        var scrollWidth = $("#report-reports").scrollLeft() - pairWidth;
        $("#report-reports").animate({scrollLeft: scrollWidth}, 500);
        return false;
    });

    $("#add-report-name").keyup(function(){
        var href = $("#add-new-report").attr("data-href");
        value = href + "?form.widgets.name=" + encodeURI($(this).val());
        $("#add-new-report").attr("href", value);
        $('.add-report-button a').prepOverlay({
            subtype: 'ajax',
            filter: '#content>*',
            formselector: 'form',
            config: {onLoad: function() {
                $.getScript(portal_url+"/++resource++openmultimedia.reporter/omupload.js", function(){
                    // XXX: Eventually, we might have several widgets
                    //      for now, we have only one.
                    $.getScript(portal_url+"/@@render-upload-js.js?widget_id="+$(".upload-widget")[0].id);
            });
        }}
    });
});

});