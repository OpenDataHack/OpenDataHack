/*global require*/
require.config({
    paths: {
        ol: "http://openlayers.org/en/v3.17.1/build/ol",
        underscore: "../bower_components/underscore/underscore-min",
        moment: "../bower_components/moment/min/moment.min",
        json: "../bower_components/requirejs-plugins/src/json",
        text: "../bower_components/requirejs-plugins/lib/text",
        d3: "../bower_components/d3/d3.min",
        jquery: "../bower_components/jquery/dist/jquery.min",
        map: "modules/ol3-map"
    }
});

require([
    "ol",
    "underscore",
    "d3",
    "map",
    "jquery"
], function (
    ol,
    _,
    d3,
    map,
    $
) {
    "use strict";


    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(";");
        for (var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)===" ") {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    var csrftoken = getCookie("csrftoken");

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != "") {
                     var cookies = document.cookie.split(";");
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                         if (cookie.substring(0, name.length + 1) == (name + "=")) {
                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             break;
                         }
                     }
                 }
                 return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
             }
         }
    });
});
