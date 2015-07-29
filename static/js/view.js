'use strict'
// Views, all inherit BaseView

var layoutView = Backbone.Marionette.LayoutView.extend({
  template: "#layout-view-template",
  
  regions: {
    body: '#content',
  },  

  events: {

  },
  
  initialize: function(){
    this.onChildviewPlayAgain()
  },

  onChildviewVote: function(view, vote){
    this.body.show(new responseView({
      model: this.model, 
      response: vote
    }))
  },

  onChildviewPlayAgain: function(view, vote){
    this.model = new StartupOrFurniture();
    this.model.on("sync", this.onShow, this);
    this.model.fetch();
  },

  onShow: function() {
    this.body.show(new cardView(this.model));
  }
});

var cardView = Backbone.Marionette.ItemView.extend({
  template: "#card-view-template",

  events: {
    'mouseover .logo_wrapper': 'showFont',
    'mouseout .logo_wrapper': 'hideFont',
    'click .logo_wrapper': 'handleResponse' 
  },

  initialize: function(model){
    this.model = model
  },

  onShow: function() {
  },

  handleResponse: function(e){
    var vote = e.currentTarget.id
    this.model.addVote(vote)
    this.triggerMethod('vote', vote)
  },

  showFont: function(e) {
    $(".prompt").addClass('hide').removeClass('show');
    if(e.currentTarget.id == 'ycomb'){
      $(".ycomb_style").addClass('show').removeClass('hide');
    }else{
      $(".ikea_style").addClass('show').removeClass('hide');
    }
  },

  hideFont: function(a, b, c) {
    $(".prompt").addClass('hide').removeClass('show');
    $(".plain_style").addClass('show').removeClass('hide');
  }

});

var responseView = Backbone.Marionette.ItemView.extend({
  template: "#response-view-template",
  
  events: {
    'click .again': 'playAgain' 
  },

  initialize: function(data){
    this.model = data.model;
    this.model.set('response', data.response)
  },

  onShow: function() {
  },

  playAgain: function(e){
    this.triggerMethod('play:again',e)
  },

});