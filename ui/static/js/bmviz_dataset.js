/* global $, _, crossfilter, d3  */
(function(bmviz) {
    'use strict';

    bmviz.data = {};

    bmviz.TRANS_DURATION = 2000;
    bmviz.MAX_CENTROID_RADIUS = 30;
    bmviz.MIN_CENTROID_RADIUS = 2;

    bmviz.makeFilter = function(shows){
        bmviz.filter = crossfilter(shows);
    };

    bmviz.makeDimension = function(){
        bmviz.dimensionCountry = bmviz.filter.dimension(function(o){
            return o.country;
        });
        bmviz.dimensionYear = bmviz.filter.dimension(function(o){
            return o.year;
        });
    };

    bmviz.filterByCountries = function(countryNames) {
        if(countryNames.length === 0){
            bmviz.dimensionCountry.filter();
            bmviz.activeCountry = null;
        }
        else{
            bmviz.activeCountry = countryNames[0];
            bmviz.dimensionCountry.filter(function(name) {
                return countryNames.indexOf(name) > -1;
            });
        }        
    };

    bmviz.filterByYear = function(year) {        
        bmviz.activeYear = year;
        
        if(year == null){
            bmviz.activeYear = null;
            bmviz.dimensionYear.filter();
        }
        else{
            bmviz.activeYear = year;
            bmviz.dimensionYear.filter(year);
        }
    };

    bmviz.getCountryInfo = function() {
        var countryGroups = bmviz.dimensionCountry.group().all();

        // make main data-ball
        var data = countryGroups.map( function(c) {
            return { key: c.key, value: c.value };
        }).sort(function(a, b) {
            return b.value - a.value; // descending
        });

        return data;
    };

    bmviz.onDataChange = function() {
        var data = bmviz.getCountryInfo();
        bmviz.updateMap(data);
    };

}(window.bmviz = window.bmviz || {}));