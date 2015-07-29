MyApp = new Backbone.Marionette.Application();

MyApp.addRegions({
  main: "#viewport"
});

MyApp.addInitializer(function(options){
  MyApp.main.show(new layoutView);
});

$(document).ready(function(){
  MyApp.start()
});