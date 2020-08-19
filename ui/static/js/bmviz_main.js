/* global $, _, crossfilter, d3  */
(function(bmviz) {
    'use strict';

    // Load the initial data required by the Nobel-viz
    var q = queue()
        .defer(d3.json, "static/data/world-110m.json")
        .defer(d3.json, "static/data/country_id_name_pair.json")
        .defer(d3.json, "static/data/country_info.json")
        .defer(d3.json, "static/data/babymetal_show_list.json");
    
    q.await(ready);

    function ready(error, worldMap, countryIdToNameTbl, countryInfo, shows) {
        // LOG ANY ERROR TO CONSOLE 
        if(error){
            return console.warn(error);
        }
        // STORE OUR COUNTRY-DATA DATASET
        bmviz.data.countryInfo = countryInfo;
        // MAKE OUR FILTER AND ITS DIMENSIONS
        bmviz.makeFilter(shows);
        bmviz.makeDimension();
        // INITIALIZE MENU AND MAP
        bmviz.initMenu();
        bmviz.initMap(worldMap, countryIdToNameTbl);
        // TRIGGER UPDATE WITH FULL WINNERS' DATASET
        bmviz.onDataChange();
    }
}(window.bmviz = window.bmviz || {}));
