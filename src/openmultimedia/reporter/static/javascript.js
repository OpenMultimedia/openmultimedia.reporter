
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

});