window.setPaginationAjax = function () {
    $(".listingBar a").each(function() {
        var elem = $(this);
        var url = elem.attr("href");
        elem.attr("data-url", url);
        var tab = $(".reporter-tab-hidden").attr("id").split("-")[0];
        if(url.indexOf("wf_state") === -1) {
            elem.attr("href", url + "&wf_state=" + tab);
        }
    });

    $(".listingBar a").click(function(e) {
        e.preventDefault();
        $("#loading-small").css("display", "inline");
        var url = $(this).attr("href");
        var that = this;
        $.ajax({
            url: url,
            success:function(data) {
            var list = $(data).find(".reports-list");
            $(".reports-list").html(list.html());
            $("#loading-small").css("display", "none");
            setPaginationAjax();
        }
            });
        return false;
    });
};


window.intervalSetUpdate = function () {
    var tab = $(".reporter-filter-state.reporter-tab-hidden");
    //if theres no pagination or we are in the first page.... update
    if(!$(".listingBar .current").length || $(".listingBar .current").text() === "1") {
        var url = tab.attr("href");
        $.ajax({
            url: url,
            success:function(data) {
                var list = $(data).find(".reports-list");
                var tab2 = $(".reporter-filter-state.reporter-tab-hidden");
                //check if the tab was changed during the ajax call
                if(tab.attr("id") === tab2.attr("id") &&
                    (!$(".listingBar .current").length ||
                        $(".listingBar .current").text() === "1")) {
                    $(".reports-list").html(list.html());
                    setPaginationAjax();
                }
            }
        });
    }

};

$(document).ready(function() {

    setPaginationAjax();

    $(".reporter-filter-state").click(function(e) {
        e.preventDefault();
        var url = $(this).attr("href");
        var that = this;
        $("#loading-small").css("display", "inline");
        $.ajax({
            url: url,
            success:function(data) {
            var list = $(data).find(".reports-list");
            $(".reporter-tab-hidden").removeClass("reporter-tab-hidden");
            $(that).addClass("reporter-tab-hidden");
            $(".reports-list").html(list.html());
            $("#loading-small").css("display", "none");
            setPaginationAjax();
        }
            });
        return false;
    });
});