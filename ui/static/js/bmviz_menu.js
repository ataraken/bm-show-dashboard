/* global $, _, crossfilter, d3  */
(function(bmviz) {
    'use strict';
    
    // Country selector
    
    bmviz.initMenu = function() {
        function initYearSelect() {
            var ALL_YEARS = 'All Years';
            var nats = bmviz.yearSelectGroups = bmviz.dimensionYear.group().all().sort()

            var selectData = [ALL_YEARS]
            nats.forEach(function(o) {
                selectData.push(o.key);
            });

            var yearSelect = d3.select('#year-select select');

            yearSelect.selectAll('option')
                .data(selectData).enter()
                .append('option')
                .attr('value', function(d) { return d; })
                .html(function(d){ return d; });
            
            yearSelect.on('change', function(d) {
                var year = d3.select(this).property('value');

                if(year === ALL_YEARS){
                    year = null;
                }

                bmviz.filterByYear(year);
                bmviz.onDataChange();
            });    
    
        }

        function initCountrySelect() {
            var ALL_COUNTRIES = 'All Countries';

            var nats = bmviz.countrySelectGroups = bmviz.dimensionCountry.group().all()
                .sort(function(a, b) {
                    return b.value - a.value; // descending
                });
                
            var selectData = [ALL_COUNTRIES];
            nats.forEach(function(o) {
                selectData.push(o.key);
            });

            var countrySelect = d3.select('#country-select select');

            countrySelect.selectAll('option')
                .data(selectData).enter()
                .append('option')
                .attr('value', function(d) { return d; })
                .html(function(d){ return d; });
                
            countrySelect.on('change', function(d) {
                var countries;
                var country = d3.select(this).property('value');
                     
                if(country === ALL_COUNTRIES){
                    countries = [];
                }
                else{
                    countries = [country];
                }
                bmviz.filterByCountries(countries);
                bmviz.onDataChange();
            });    
        }

        initYearSelect()
        initCountrySelect()
    };
    
}(window.bmviz = window.bmviz || {}));
