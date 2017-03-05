/* globals define require */
define([
    "ol",
    "underscore"
], function (
    ol,
    _
) {
    "use strict";
    var map,
        app;

    window.app = {};
    app = window.app;

    /**
     * @constructor
     * @extends {ol.control.Control}
     * @param {Object=} opt_options Control options.
     */

    app.CustomToolbarControl = function (opt_options) {
        var options,
            riskElement,
            element;

        options = opt_options || {};

        riskElement = document.createElement("h2");
        riskElement.setAttribute("id", "my-risk-value");
        riskElement.setAttribute("class", "results-label")
        riskElement.innerHTML ="Hover over map to get risk";

        element = document.createElement("div");
        element.setAttribute("id", "my-ol-control");
        element.className = "ol-unselectable ol-mycontrol";
        element.appendChild(riskElement);

        ol.control.Control.call(this, {
            element: element,
            target: options.target
        });

    };

    ol.inherits(app.CustomToolbarControl, ol.control.Control);

    map = new ol.Map({
        layers: [
            new ol.layer.Tile({
                source: new ol.source.Stamen({
                    layer: "toner-background"
                })
            }),
            // new ol.layer.Tile({
            //     preload: Infinity,
            //     visible: true,
            //     source: new ol.source.TileWMS({
            //         url: "http://apps.ecmwf.int/wms/",
            //         params: {
            //             "LAYERS": "composition_aod550",
            //             "token": "public"
            //         },
            //         serverType: "geoserver",
            //         crossOrigin: "anonymous",
            //         projection: "EPSG:4326"
            //     }),
            //     opacity: 0.5
            // })
        ],
        controls: ol.control.defaults({
            attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                collapsible: false
            })
        }).extend([
            new app.CustomToolbarControl()
        ]),
        renderer: "canvas",
        target: "map",
        view: new ol.View({
            center: [-279700, 7075000],
            zoom: 7
        }),

    });

    map.on("pointermove", function (evt) {
        var coordinate = evt.coordinate;
        var latlon = ol.proj.transform(coordinate, "EPSG:3857", "EPSG:4326");
        $.post(
            "query_computed_dataset",
            {latitude: latlon[1], longitude:latlon[0]},
            function (data) {
                document.getElementById("my-risk-value").innerText= data.risk;
            }
        );
    });

    return map;

});

