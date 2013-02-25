

var to_load = "http://localhost:8080/Plone/soy-reportero/++resource++openmultimedia.reporter/";

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
            $.getScript(to_load+"fileuploader.js", function(){
                $.getScript(to_load+"jquery.json.js", function(){
                    // XXX: Eventually, we might have several widgets
                    //      for now, we have only one.
                    $.getScript(to_load+"@@render-upload-js.js?widget_id="+$(".upload-widget")[0].id);
                });
            });
        }}
        });

});