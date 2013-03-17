
$(document).ready(function() {

    var slug = $("#new-report-video").attr("data-slug");
    $("#new-report-video").omplayer({
        slug: slug,
        width: 400, height: 255,
        style: 1
    });

    $("#search-ireport-button").click(function(e) {
        e.preventDefault();
        var search = $(".search-report-search").val();
        document.location.href ='listado-report-published?search-report=' + search;
        return false;
        });

    $('.disclaimer-btn').prepOverlay({
        subtype: 'iframe'
        });

    $('.add-report-button a').prepOverlay({
        subtype: 'ajax',
        filter: '#content>*',
        formselector: 'form',
        noform: 'close',
        closeselector: '#form-buttons-cancel',
        afterpost: function() {
            $.getScript(portal_url+"/++resource++openmultimedia.reporter/omupload.js", function(){
                // XXX: Eventually, we might have several widgets
                //      for now, we have only one.
                $.getScript(portal_url+"/@@render-upload-js.js?widget_id="+$(".upload-widget")[0].id);
            });
        },
        config: {onLoad: function() {
            $.getScript(portal_url+"/++resource++openmultimedia.reporter/omupload.js", function(){
                // XXX: Eventually, we might have several widgets
                //      for now, we have only one.
                $.getScript(portal_url+"/@@render-upload-js.js?widget_id="+$(".upload-widget")[0].id);
            });
        }}
        });

    $(".report-item").click(function(e) {
        //XXX: we're rendering a view first in a hidden iframe
        //and then the html generated i the iframe is pasted in the real dom
        //we do this because there's some javascript that needs to be executed
        //in order
        var url = $(this).attr("data-url");
        // var url = $(this).attr("data-url") + "/ajax-report";
        $(".main-report").children().css("display", "none");
        $("#loading").css("display", "block");
        // var iframe = document.createElement("iframe");
        // iframe.src = url;
        // $(".hidden-frame").remove();
        // $(iframe).attr("class","hidden-frame");
        // $(iframe).css("display","none");
        // document.body.appendChild(iframe);
        // $(".hidden-frame").load(function() {
        //     $(".main-report").html($(".hidden-frame").contents().find("html").html());
        //     $(".hidden-frame").remove();
        // });
        $.ajax({
            url: url + "/ajax-report",
            success:function(data) {
                $(".main-report").html(data);
                var slug = $("#new-report-video").attr("data-slug");
                $("#new-report-video").omplayer({
                    slug: slug,
                    width: 400, height: 255,
                    style: 1
                });

            }
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
            noform: 'close',
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